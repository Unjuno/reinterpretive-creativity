"""ランダム生成された教師モデルで探索手法を比較する。

目的:
- 固定サイクル教師モデルだけに依存しない検査を行う。
- 既存の run_experiments.py を壊さず、別スクリプトとして実験する。

注意:
- これは説明補助であり、人間の創造性の証明ではない。
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
    import run_experiments  # type: ignore[no-redef]

Model = run_experiments.Model
RawModel = run_experiments.Raw