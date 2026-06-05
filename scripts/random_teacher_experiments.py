"""Random teacher smoke experiment."""

from __future__ import annotations

import argparse
import json
from random import Random

try:
    from scripts import run_experiments as exp
except ModuleNotFoundError:
    import run_experiments as exp  # type: ignore[no-redef]


def build_random_teacher(nodes: tuple[str, ...], seed: int, edge_rate: float = 0.35) -> exp.Model:
    rng = Random(seed)