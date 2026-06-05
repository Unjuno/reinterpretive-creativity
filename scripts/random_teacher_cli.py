import argparse
import json
from pathlib import Path

from scripts import random_teacher_output


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--json", default=None)
    p.add_argument("--md", default=None)
    a = p.parse_args()
    data = random