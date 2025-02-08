# trace-flamegraph

## agentの準備

agentをビルドする。

```bash
mvn -f agent/pom.xml clean package
```

Libertyのjvm.optionsにagent-1.0.jarを指定する。

```txt
-javaagent:/path/to/agent-1.0.jar
```

## アプリケーションの打鍵とログを取得

アプリケーションを打鍵して標準出力を任意のディレクトリに保管する。

## 可視化

[flamegraph.pl](https://github.com/brendangregg/FlameGraph/blob/master/flamegraph.pl)を`graph`ディレクトリに配置する。

スクリプトを実行する。

```bash
./graph/create_flamegraph.sh /path/to/sample.log
```
