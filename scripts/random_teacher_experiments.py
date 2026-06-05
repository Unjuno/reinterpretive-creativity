from __future__ import annotations

import json
from pathlib import Path
from random import Random

try:
    from scripts import run_experiments as exp
    from scripts.random_teacher_smoke import build_random_teacher
except ModuleNotFoundError:
    import run_experiments as exp
    from random_teacher_smoke import build_random_teacher


def make_noisy_raw_from_teacher(teacher, seed=0, conflict_rate=0.35, extra_positive_rate=0.25):
    rng