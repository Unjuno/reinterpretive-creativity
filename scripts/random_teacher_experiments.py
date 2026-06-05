"""ランダム教師モデルを既存探索へ接続する最小実験。

手順:
1. make_noisy_raw_from_teacher で教師モデルから初期rawモデルを作る。
2. ランダム教師から初期モデルを生成する。
3. 既存の random_repair / random_search / local_repair / reinterpretation に渡す。
4. 小さいスモーク比較結果をJSONとして出す。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random

try:
    from scripts import run_experiments as exp
    from scripts.random_teacher_smoke import build_random_teacher
except Module