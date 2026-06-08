import argparse
from pathlib import Path

from scripts.batch_gap_report import build_report
from scripts.gap_report_json import write_json
from scripts.gap_report_text import write_text
from scripts.report_explanation_basis import attach_explanation_basis


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=Path, default=None)
    parser.add_argument('--text', type=Path, default=None)
    parser.add_argument('--basis', action='store_true')
    args = parser.parse_args(argv)
    report = build_report()
    if args.basis:
        report = attach_explanation_basis(report)
    print(report)
    if args.json is not None:
        write_json(args.json, report)
    if args.text is not None:
        write_text(args.text, report)


if __name__ == '__main__':
    main()
