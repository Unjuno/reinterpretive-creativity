"""ランダム生成された教師モデルで探索手法を比較する。

固定サイクル教師モデルだけに依存しない検査を行うための独立スクリプト。
これは説明補助であり、人間の創造性の証明ではない。
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from random import Random
from statistics import mean

try:
    from scripts import run_experiments
except ModuleNotFoundError:  # `python scripts/random_teacher_experiments.py` 用