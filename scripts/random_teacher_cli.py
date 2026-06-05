import argparse
import json

from scripts import random_teacher_output


def main():
    parser = argparse.ArgumentParser(description="ランダム教師実験の最小CLI")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", default=None)
    parser.add_argument("--md", default=None)
    args = parser.parse_args()
    data = random_teacher_output.build(seed=args.seed, limit=args.limit