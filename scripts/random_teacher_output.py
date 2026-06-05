import json
from pathlib import Path
from scripts.random_teacher_experiments import run_smoke


def build(seed=0, limit=20):
    return {"seed": seed, "limit": limit, "scores": run_smoke(seed, limit)}


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path, data):
    Path(path).write_text(str(data) + "\n", encoding="utf-8")
