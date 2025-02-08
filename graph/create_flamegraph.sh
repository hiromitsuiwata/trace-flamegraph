#!/usr/bin/bash

# ab -n 12 -c 3 http://localhost:9080/myapp/api/helloworld1

SCRIPT_DIR=$(cd $(dirname $0); pwd)
OUTPUT_DIR="${SCRIPT_DIR}/../data/output"
echo ${OUTPUT_DIR}
python3 ${SCRIPT_DIR}/create_fold.py -i $1 -d ${OUTPUT_DIR}

while read -r FILE; do

  # ファイル一つ毎の処理
  echo "file: ${FILE}"
  BASENAME=$(basename ${FILE} ".txt")
  echo ${BASENAME}
  perl "${SCRIPT_DIR}/flamegraph.pl" --flamechart ${FILE} > "${OUTPUT_DIR}/${BASENAME}.svg"

done < <(find ${OUTPUT_DIR} -mindepth 1 -maxdepth 1)