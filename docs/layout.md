# 定长薪酬文件

`--inbox` 下每个 `.txt` 一行一条记录，行宽应为 32 个字符（不含换行）。短于 32 的行进入 `--out/quarantine.jsonl`（`line,reason=short_line`，line 为 1-based 含该文件内行号），不要猜想缺的列。不要访问外网，不要用 Docker。

列约定（0-based，左闭右开）：

- `[0:1]` 记录类型：`H` 文件头（跳过）、`D` 明细、`T` 文件尾（跳过）。
- `[1:2]` 明细子类：`1` 加班，`2` 奖金。只对 `D` 有效。
- `[2:10]` 工号，去空白。
- `[10:18]` 期间 `YYYYMMDD`。
- `[18:26]` 金额，8 个字符，右对齐，末位是过账符号（overpunch），不是普通数字或小数点。

过账符号（末位）含义：`{ABCDEFGHI` 分别是 +0 到 +9，`}JKLMNOPQR` 分别是 -0 到 -9。前面的字符是整数的高位（可空格填充）。例如 `0000120{` 是 +1200 分，`0000001J` 是 -11 分。最终 `amount_cents` 为带符号整数。

同一组金额列在子类 `1` 时表示加班费 `kind=overtime`，子类 `2` 时表示奖金 `kind=bonus`。不要把两种明细混成一个字段。

输出 `--out/pays.jsonl`：`emp,period,kind,amount_cents`，按 (emp,period,kind) 排序。`--out/report.json` 含 `row_count`、`quarantine_count`。
