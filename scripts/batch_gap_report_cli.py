import argparse
from pathlib import Path

from scripts.batch_gap_report import build_report
from scripts.gap_report_json import write_json


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=Path, default=None)
    args = parser.parse_args(argv)
    report = build_report()
    print(report)
    if args.json is not None:
        write_json(args.json, report)


if __name__ == '__main__':
    main()
