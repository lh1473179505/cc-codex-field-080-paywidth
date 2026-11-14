import argparse
def main(argv=None):
    p=argparse.ArgumentParser(prog="paywidth")
    sub=p.add_subparsers(dest="cmd", required=True)
    i=sub.add_parser("ingest"); i.add_argument("--inbox", required=True); i.add_argument("--out", required=True)
    v=sub.add_parser("verify"); v.add_argument("--out", required=True); v.add_argument("--expect", required=True)
    args=p.parse_args(argv)
    if args.cmd=="ingest":
        from paywidth.ingest import run_ingest
        return run_ingest(args)
    if args.cmd=="verify":
        from paywidth.verify import run_verify
        return run_verify(args)
    return 2
