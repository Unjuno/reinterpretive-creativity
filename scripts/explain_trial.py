"""1つの実験ケースについて、各探索結果の変更内容を説明する。

目的:
- 平均スコアだけでなく、1ケースで何が変わったかを見る。
- 教師モデル、初期モデル、各探索結果、変更辺をMarkdownで出力する。

注意:
- これは説明補助であり、創造性の証明ではない。
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts import run_experiments
except ModuleNotFoundError:  # `python scripts/explain_trial.py` 用
    import run_experiments  # type: ignore[no-redef]

Model = run_experiments.Model
RawModel = run_experiments.RawModel
Edge = run_experiments.Edge


def edge_label(edge: Edge) -> str:
    return f"{edge[0]}->{edge[1]}"


def value_label(value: int) -> str:
    if value == 1:
        return "肯定"
    if value == -1:
        return "否定"
    return "不明"


def raw_value_label(values: set[int] | None) -> str:
    if values is None:
        return "不明"
    if values == {1}:
        return "肯定"
    if values == {-1}:
        return "否定"
    if values == {1, -1}:
        return "矛盾"
    return "不明"


def model_rows(model: Model) -> list[str]:
    rows = []
    for edge, value in sorted(model.items()):
        if value != 0:
            rows.append(f"| `{edge_label(edge)}` | {value_label(value)} |")
    return rows or ["| _なし_ | _なし_ |"]


def raw_rows(raw: RawModel, edges: tuple[Edge, ...]) -> list[str]:
    rows = []
    for edge in sorted(edges):
        values = raw.get(edge)
        label = raw_value_label(values)
        if label != "不明":
            rows.append(f"| `{edge_label(edge)}` | {label} |")
    return rows or ["| _なし_ | _なし_ |"]


def changed_edges(before: Model, after: Model) -> list[tuple[Edge, int, int]]:
    return [
        (edge, before[edge], after[edge])
        for edge in sorted(before)
        if before[edge] != after[edge]
    ]


def change_rows(before: Model, after: Model) -> list[str]:
    changes = changed_edges(before, after)
    if not changes:
        return ["| _なし_ | _なし_ | _なし_ |"]
    return [
        f"| `{edge_label(edge)}` | {value_label(old)} | {value_label(new)} |"
        for edge, old, new in changes
    ]


def result_block(
    title: str,
    score: float,
    initial: Model,
    teacher: Model,
    result: Model,
) -> str:
    lines = [
        f"### {title}",
        "",
        f"score: `{score:.4f}`",
        "",
        "#### 結果モデル",
        "",
        "| 辺 | 値 |",
        "|---|---|",
        *model_rows(result),
        "",
        "#### 初期モデルからの変更",
        "",
        "| 辺 | 初期 | 結果 |",
        "|---|---|---|",
        *change_rows(initial, result),
        "",
        "#### 教師モデルとの差分",
        "",
        "| 辺 | 教師 | 結果 |",
        "|---|---|---|",
        *change_rows(teacher, result),
    ]
    return "\n".join(lines)


def explain_case(seed: int, node_count: int, candidate_limit: int) -> str:
    teacher, raw = run_experiments.noisy_case(seed=seed, node_count=node_count)
    initial = run_experiments.to_model(raw, teacher.keys())

    random_repair_score, random_repair_model = run_experiments.random_repair(
        teacher, raw, seed=seed
    )
    random_search_score, random_search_model = run_experiments.random_search_baseline(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )
    local_repair_score, local_repair_model = run_experiments.local_repair_search(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )
    reinterpretation_score, reinterpretation_model = run_experiments.reinterpretation_search(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )

    lines = [
        "# 1ケース説明ログ",
        "",
        "## 条件",
        "",
        f"- seed: `{seed}`",
        f"- node_count: `{node_count}`",
        f"- candidate_limit: `{candidate_limit}`",
        "",
        "## 教師モデル",
        "",
        "| 辺 | 値 |",
        "|---|---|",
        *model_rows(teacher),
        "",
        "## 初期モデル",
        "",
        "| 辺 | 値 |",
        "|---|---|",
        *raw_rows(raw, tuple(teacher.keys())),
        "",
        "## 探索結果",
        "",
        result_block("単発ランダム修復", random_repair_score, initial, teacher, random_repair_model),
        "",
        result_block("ランダム探索", random_search_score, initial, teacher, random_search_model),
        "",
        result_block("局所修復探索", local_repair_score, initial, teacher, local_repair_model),
        "",
        result_block("再解釈探索", reinterpretation_score, initial, teacher, reinterpretation_model),
        "",
        "## 注意",
        "",
        "このログは、候補モデルの変更内容を読むための説明補助です。",
        "創造性そのものを証明するものではありません。",
    ]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="1ケース説明ログを生成する")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--node-count", type=int, default=4)
    parser.add_argument("--candidate-limit", type=int, default=100)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    text = explain_case(
        seed=args.seed,
        node_count=args.node_count,
        candidate_limit=args.candidate_limit,
    )
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
