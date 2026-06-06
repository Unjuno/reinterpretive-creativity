import argparse
from pathlib import Path
from scripts import random_teacher_output as r

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--limit', type=int, default=10)
    p.add_argument('--json', type=Path, default=None)
    a = p.parse_args()
    data = r.build(seed=a.seed, limit=a.limit)
    print(data)
    if a.json is