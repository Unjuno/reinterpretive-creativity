import argparse
import json
from pathlib import Path

from scripts.random_teacher_experiments import run_smoke


def markdown(data):
    lines = ["# ランダム教師実験", "", "| method | score |", "|---|---:|"]
    for key, value in data["scores"].items():
        lines.append(f"| {key} | {value:.4f} |")
    lines.append("")
    lines.append("これは説明補助であり、創造性の証明ではない。")
    return "\n".join(lines) + "\n