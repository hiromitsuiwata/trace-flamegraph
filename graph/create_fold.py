import argparse
import datetime
import os

def main():
    args = get_args()

    events = filter_lines(args)

    group_by_thread_id = group_by_thread(events)

    for id, evs in group_by_thread_id.items():
        print(id)

    group_by_thread_id_and_timestamp = separate_according_to_thread_reuse(group_by_thread_id)

    for id, evs in group_by_thread_id_and_timestamp.items():
        fold_list = transform_to_fold(evs)
        write_fold_file(fold_list, args, id)
        print(id)

def group_by_thread(events):
    """TraceAdviceのログをスレッドごとにグループ化する"""
    thread_dict = {}
    for event in events:
        parts = event.split(' ')
        thread_id = parts[1]
        if thread_id in thread_dict:
            thread_dict[thread_id].append(event)
        else:
            thread_dict[thread_id] = [event]
    return thread_dict

def separate_according_to_thread_reuse(thread_dict):

    """スレッドごとにfold形式のリストを作成する"""
    fold_dict = {}
    for thread_id, events in thread_dict.items():
        depth = 0
        sub_group = []
        key = None
        for e in events:
            event_dict = parse_line(e)
            if depth == 0:
                parts = e.split(' ')
                key = f'{event_dict['threadId']}_{parts[0]}'
                sub_group = []
                fold_dict[key] = sub_group
            if event_dict['kind'] == 'onEnter':
                depth = depth + 1
            elif event_dict['kind'] == 'onExit':
                depth = depth - 1
            sub_group.append(e)
            
    return fold_dict

def transform_to_fold(events):
    """TraceAdviceのログからfold形式のリストを作成する"""
    call_stack = []
    fold_list = []
    for index, event in enumerate(events):
        if index < len(events) - 1:
            this_dict = parse_line(event)
            next_dict = parse_line(events[index + 1])
            time_delta = next_dict['timestamp'] - this_dict['timestamp']
            if this_dict['kind'] == 'onEnter':
                call_stack.append(this_dict['method'])
                fold_list.append(stack_to_fold(call_stack, time_delta))
            elif this_dict['kind'] == 'onExit':
                call_stack.pop()
                fold_list.append(stack_to_fold(call_stack, time_delta))
    return fold_list

def write_fold_file(fold_list: list, args, id: str):
    """fold形式のファイルを書き出す"""
    file_id = id.replace(':', '-')
    with open(os.path.join(args.output_dir, 'fold_'+file_id+'.txt'), mode='w', encoding='utf-8') as file:
        for fold in fold_list:
            file.write(f'{fold}\n')

def stack_to_fold(stack: list, time_delta: datetime.timedelta):
    """スタックをfold形式に変換する"""
    stack_str = ';'.join(stack)
    time = int(timedelta_to_microsecond(time_delta))
    return f'{stack_str} {time}'

def timedelta_to_microsecond(timedelta: datetime.timedelta):
    """timedeltaをマイクロ秒に変換する"""
    return timedelta / datetime.timedelta(microseconds=1)

def parse_line(line: str):   
    """TraceAdviceの行をパースして辞書にして返す"""
    parts = line.split(' ')
    dict = {
        'timestamp': str_to_datetime(parts[0]),
        'threadId': parts[1],
        'kind': parts[3],
        'method': parts[4]
    }
    return dict

def str_to_datetime(str: str):
    """文字列を日時に変換する"""
    return datetime.datetime.fromisoformat(str)

def filter_lines(args):
    """ログファイルからTraceAdviceの行だけを取り出す"""
    events = []
    with open(args.input, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if ' TraceAdvice ' in line:
                events.append(line.strip())
    return events

def get_args():
    """引数の定義とパースを行う"""
    parser = argparse.ArgumentParser(description='ログからFlameGraphのfold形式のファイルを作るスクリプト')
    parser.add_argument('-i', '--input', required=True, type=str, help='入力するログファイルのパス')
    parser.add_argument('-d', '--output_dir', required=True, type=str, help='出力するfoldファイルのディレクトリパス')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()