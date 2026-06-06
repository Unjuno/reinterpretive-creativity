import argparse

from scripts import random_teacher_output as r


def main() -> None:
    parser = argparse.ArgumentParser(description="ランダム教師実験を標準出力に表示する")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    print(r.build(seed=args.seed, limit=args.limit))


if __name__ == "__main__":
    main()
