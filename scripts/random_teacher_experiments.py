"""ランダム教師モデルで探索手法を比較する最小実験。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random
from statistics import mean

try:
    from scripts import run_experiments as exp
except ModuleNotFoundError:
    import run_experiments as exp  # type: ignore[no-redef]


def build_random_teacher(nodes: tuple[str, ...], seed: int, edge_rate: float = 0.35