from __future__ import annotations

import json
from pathlib import Path

LINE_WIDTH = 32

# Overpunch trailing character: {ABCDEFGHI => +0..+9, }JKLMNOPQR => -0..-9
_OVERPUNCH = {}
for _digit, _char in enumerate("{ABCDEFGHI"):
    _OVERPUNCH[_char] = (_digit, 1)
for _digit, _char in enumerate("}JKLMNOPQR"):
    _OVERPUNCH[_char] = (_digit, -1)

_KINDS = {"1": "overtime", "2": "bonus"}


def decode_amount(field: str) -> int:
    digit, sign = _OVERPUNCH[field[-1]]
    high = field[:-1].strip()
    magnitude = (int(high) if high else 0) * 10 + digit
    return sign * magnitude


def run_ingest(args) -> int:
    inbox = Path(args.inbox)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    pays = []
    quarantined = []

    for path in sorted(inbox.glob("*.txt")):
        for line_no, line in enumerate(path.read_text().splitlines(), start=1):
            if len(line) < LINE_WIDTH:
                quarantined.append({"line": line_no, "reason": "short_line"})
                continue
            record_type = line[0:1]
            if record_type == "D":
                pays.append({
                    "emp": line[2:10].strip(),
                    "period": line[10:18],
                    "kind": _KINDS[line[1:2]],
                    "amount_cents": decode_amount(line[18:26]),
                })
            # H (file header) and T (file trailer) records are skipped.

    pays.sort(key=lambda row: (row["emp"], row["period"], row["kind"]))

    (out / "pays.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in pays)
    )
    (out / "quarantine.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in quarantined)
    )
    (out / "report.json").write_text(
        json.dumps(
            {"row_count": len(pays), "quarantine_count": len(quarantined)},
            ensure_ascii=False,
        )
        + "\n"
    )
    return 0
