"""candidate_limit 感度分析を実行する。

目的:
- 探索予算 candidate_limit を変えたとき、各探索手法の平均スコアがどう変わるかを見る。
- 再解釈探索、ランダム探索、局所修復探索の関係が探索予算に依存するかを確認する。

注意:
- これは説明補助であり、創造性の証明ではない。
- ノード数3では再解釈探索が全候補探索になりやすく、candidate_limit の影響が見えにくい。
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from scripts import run_experiments
except ModuleNotFoundError:  # `python scripts/sensitivity_candidate_limit.py` 用
    import run_experiments  # type: ignore[no-redef]


@dataclass(frozen=True)
class SensitivitySummary:
    candidate_limit: int
    node_count: int
    trials: int
    random_repair_mean: float
    random_search_mean: float
    local_repair_mean: float
    reinterpretation_mean: float
    improvement_vs_random_repair_mean: float
    improvement_vs_random_search_mean: float
    improvement_vs_local_repair_mean: float
    win_rate_vs_random_repair: float
    win_rate_vs_random_search: float
    win_rate_vs_local_repair: float


def parse_int_list(value: str) -> tuple[int, ...]:
    items = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not items:
        raise ValueError("空の整数リストは指定できません")
    return items


def run_sensitivity(
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limits: tuple[int, ...],
) -> list[SensitivitySummary]:
    summaries: list[SensitivitySummary] = []
    for candidate_limit in candidate_limits:
        _, experiment_summaries = run_experiments.run_suite(
            node_counts=node_counts,
            trials=trials,
            candidate_limit=candidate_limit,
        )
        for summary in experiment_summaries:
            summaries.append(
                SensitivitySummary(
                    candidate_limit=candidate_limit,
                    node_count=summary.node_count,
                    trials=summary.trials,
                    random_repair_mean=summary.random_repair_mean,
                    random_search_mean=summary.random_search_mean,
                    local_repair_mean=summary.local_repair_mean,
                    reinterpretation_mean=summary.reinterpretation_mean,
                    improvement_vs_random_repair_mean=summary.improvement_vs_random_repair_mean,
                    improvement_vs_random_search_mean=summary.improvement_vs_random_search_mean,
                    improvement_vs_local_repair_mean=summary.improvement_vs_local_repair_mean,
                    win_rate_vs_random_repair=summary.win_rate_vs_random_repair,
                    win_rate_vs_random_search=summary.win_rate_vs_random_search,
                    win_rate_vs_local_repair=summary.win_rate_vs_local_repair,
                )
            )
    return summaries


def format_summary(summaries: list[SensitivitySummary]) -> str:
    lines = [
        "# candidate_limit 感度分析",
        "",
        "| candidate_limit | ノード数 | 試行数 | 単発ランダム平均 | ランダム探索平均 | 局所修復平均 | 再解釈平均 | 改善量(単発) | 改善量(探索) | 改善量(局所) | 勝率(単発) | 勝率(探索) | 勝率(局所) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| "
            f"{summary.candidate_limit} | "
            f"{summary.node_count} | "
            f"{summary.trials} | "
            f"{summary.random_repair_mean:.4f} | "
            f"{summary.random_search_mean:.4f} | "
            f"{summary.local_repair_mean:.4f} | "
            f"{summary.reinterpretation_mean:.4f} | "
            f"{summary.improvement_vs_random_repair_mean:.4f} | "
            f"{summary.improvement_vs_random_search_mean:.4f} | "
            f"{summary.improvement_vs_local_repair_mean:.4f} | "
            f"{summary.win_rate_vs_random_repair:.2%} | "
            f"{summary.win_rate_vs_random_search:.2%} | "
            f"{summary.win_rate_vs_local_repair:.2%} |"
        )
    lines.extend(
        [
            "",
            "## 注意",
            "",
            "この表は、探索予算 candidate_limit に対するスコアの変化を見るための補助です。",
            "人間の創造性を証明するものではありません。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_markdown(path: Path, summaries: list[SensitivitySummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_summary(summaries), encoding="utf-8")


def write_json(
    path: Path,
    summaries: list[SensitivitySummary],
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limits: tuple[int, ...],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "metadata": {
            "node_counts": list(node_counts),
            "trials": trials,
            "candidate_limits": list(candidate_limits),
            "note": "candidate_limit 感度分析は説明補助であり、創造性の証明ではない。",
        },
        "summaries": [asdict(summary) for summary in summaries],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, summaries: list[SensitivitySummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(asdict(summaries[0]).keys()) if summaries else [],
        )
        writer.writeheader()
        for summary in summaries:
            writer.writerow(asdict(summary))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="candidate_limit 感度分析を実行する")
    parser.add_argument("--nodes", default="4,5", help="例: 4 または 4,5")
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--candidate-limits", default="50,100,200,500")
    parser.add_argument("--output", type=Path, default=Path("results/candidate_limit_sensitivity.md"))
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--csv", type=Path, default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    node_counts = parse_int_list(args.nodes)
    candidate_limits = parse_int_list(args.candidate_limits)
    summaries = run_sensitivity(
        node_counts=node_counts,
        trials=args.trials,
        candidate_limits=candidate_limits,
    )
    write_markdown(args.output, summaries)
    if args.json is not None:
        write_json(args.json, summaries, node_counts, args.trials, candidate_limits)
    if args.csv is not None:
        write_csv(args.csv, summaries)
    print(format_summary(summaries), end="")


if __name__ == "__main__":
    main()
