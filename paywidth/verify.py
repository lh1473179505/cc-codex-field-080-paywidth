from __future__ import annotations
import json
from pathlib import Path
def rows(path):
    p=Path(path)
    if not p.is_file(): return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
def run_verify(args) -> int:
    exp=json.loads(Path(args.expect).read_text())
    got=rows(Path(args.out)/"pays.jsonl")
    quar=rows(Path(args.out)/"quarantine.jsonl")
    errors=[]
    key=lambda r:(r.get("emp"),r.get("period"),r.get("kind"))
    if [key(r) for r in got]!=sorted(key(r) for r in got):
        errors.append("pays.jsonl must be sorted by emp,period,kind")
    by={key(r):r for r in got}
    exp_by={key(r):r for r in exp["rows"]}
    if set(by)!=set(exp_by):
        errors.append(f"keys extra={sorted(set(by)-set(exp_by))} missing={sorted(set(exp_by)-set(by))}")
    for k,e in exp_by.items():
        g=by.get(k)
        if not g: continue
        if g.get("amount_cents")!=e["amount_cents"]:
            errors.append(f"{k} amount {g.get('amount_cents')} != {e['amount_cents']}")
    if not any(q.get("reason")=="short_line" for q in quar):
        errors.append(f"short_line not quarantined {quar}")
    if errors:
        print("verify failed:")
        for e in errors: print(" -", e)
        return 1
    print("verify ok"); return 0
