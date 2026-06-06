import argparse
from pathlib import Path

from scripts import random_teacher_output as r


def main() -> None:
    parser = argparse.ArgumentParser(description="ランダム教師実験を標準出力に表示する")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()
    data = r.build(seed=args.seed, limit=args.limit)
    if