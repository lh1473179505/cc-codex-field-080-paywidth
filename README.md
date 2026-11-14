# paywidth

薪酬导出还是定长文本。记录类型决定同一组列怎么读，金额用尾部过账符号，行宽不够的进隔离区。

```
python -m paywidth ingest --inbox fixtures/inbox --out <out>
python -m paywidth verify --out <out> --expect fixtures/expected/pays.json
```
