"""複数ケースから代表ケースを抽出する。

目的:
- 平均値だけでは見えない、典型的な勝ち/負けケースを選ぶ。
- 再解釈探索、局所修復探索、ランダム探索がそれぞれ有利なケースを探す。
- 選ばれたケースについて、説明ログをMarkdownで生成できるようにする。
- 代表ケース一覧をJSONで保存できるようにする。
- 代表ケースの node_count / seed 重複を可能な範囲で避ける。

注意:
- 代表ケース抽出は説明補助であり、創造性の証明ではない。
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts import explain_trial, run_experiments
except ModuleNotFoundError:  # `python scripts/select_cases.py` 用
    import explain_trial  # type: ignore[no-redef]
    import run_experiments  # type: ignore[no-redef]


@dataclass(frozen=True)
class CaseScores:
    node_count: int
    seed: int
    random_repair_score: float
    random_search_score: float
    local_repair_score: float
    reinterpretation_score: float

    @property
    def best_score(self) -> float:
        return max(
            self.random_repair_score,
            self.random_search_score,
            self.local_repair_score,
            self.reinterpretation_score,
        )

    @property
    def score_spread(self) -> float:
        return self.best_score - min(
            self.random_repair_score,
            self.random_search_score,
            self.local_repair_score,
            self.reinterpretation_score,
        )

    @property
    def key(self) -> tuple[int, int]:
        return (self.node_count, self.seed)

    @property
    def key_label(self) -> str:
        return f"n{self.node_count}_seed{self.seed}"


def score_case(seed: int, node_count: int, candidate_limit: int) -> CaseScores:
    result = run_experiments.run_trial(
        seed=seed,
        node_count=node_count,
        candidate_limit=candidate_limit,
    )
    return CaseScores(
        node_count=node_count,
        seed=seed,
        random_repair_score=result.random_repair_score,
        random_search_score=result.random_search_score,
        local_repair_score=result.local_repair_score,
        reinterpretation_score=result.reinterpretation_score,
    )


def collect_cases(
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limit: int,
) -> list[CaseScores]:
    cases: list[CaseScores] = []
    for node_count in node_counts:
        for seed in range(trials):
            cases.append(score_case(seed, node_count, candidate_limit))
    return cases


def margin_for(case: CaseScores, method: str) -> float:
    scores = {
        "random_repair": case.random_repair_score,
        "random_search": case.random_search_score,
        "local_repair": case.local_repair_score,
        "reinterpretation": case.reinterpretation_score,
    }
    target = scores[method]
    others = [value for key, value in scores.items() if key != method]
    return target - max(others)


def available_cases(cases: list[CaseScores], used_keys: set[tuple[int, int]]) -> list[CaseScores]:
    """未使用ケースを返す。足りない場合は呼び出し側で重複許容に戻す。"""

    return [case for case in cases if case.key not in used_keys]


def select_best_margin_case(
    cases: list[CaseScores],
    method: str,
    used_keys: set[tuple[int, int]] | None = None,
) -> tuple[CaseScores, float, bool]:
    """指定手法のmarginが最大のケースを選ぶ。

    used_keys が渡された場合、可能な限り既出の node_count / seed を避ける。
    候補が尽きた場合だけ重複を許容し、duplicate_allowed=True を返す。
    """

    if not cases:
        raise ValueError("cases が空です")

    used_keys = used_keys or set()
    candidates = available_cases(cases, used_keys)
    duplicate_allowed = False
    if not candidates:
        candidates = cases
        duplicate_allowed = True

    selected = max(candidates, key=lambda case: margin_for(case, method))
    return selected, margin_for(selected, method), duplicate_allowed


def select_closest_case(
    cases: list[CaseScores],
    used_keys: set[tuple[int, int]] | None = None,
) -> tuple[CaseScores, bool]:
    """全手法のスコア差が最小のケースを選ぶ。

    used_keys が渡された場合、可能な限り既出の node_count / seed を避ける。
    候補が尽きた場合だけ重複を許容し、duplicate_allowed=True を返す。
    """

    if not cases:
        raise ValueError("cases が空です")

    used_keys = used_keys or set()
    candidates = available_cases(cases, used_keys)
    duplicate_allowed = False
    if not candidates:
        candidates = cases
        duplicate_allowed = True

    return min(candidates, key=lambda case: case.score_spread), duplicate_allowed


def format_score(value: float) -> str:
    return f"{value:.4f}"


def case_row(label: str, case: CaseScores, margin: float | None, duplicate_allowed: bool) -> str:
    margin_text = "-" if margin is None else format_score(margin)
    duplicate_text = "yes" if duplicate_allowed else "no"
    return (
        "| "
        f"{label} | "
        f"`{case.key_label}` | "
        f"{case.node_count} | "
        f"{case.seed} | "
        f"{format_score(case.random_repair_score)} | "
        f"{format_score(case.random_search_score)} | "
        f"{format_score(case.local_repair_score)} | "
        f"{format_score(case.reinterpretation_score)} | "
        f"{margin_text} | "
        f"{duplicate_text} |"
    )


def select_representative_cases(cases: list[CaseScores]) -> dict[str, tuple[CaseScores, float | None, bool]]:
    used_keys: set[tuple[int, int]] = set()

    reinterpretation_case, reinterpretation_margin, reinterpretation_duplicate = select_best_margin_case(
        cases,
        "reinterpretation",
        used_keys=used_keys,
    )
    used_keys.add(reinterpretation_case.key)

    local_repair_case, local_repair_margin, local_repair_duplicate = select_best_margin_case(
        cases,
        "local_repair",
        used_keys=used_keys,
    )
    used_keys.add(local_repair_case.key)

    random_search_case, random_search_margin, random_search_duplicate = select_best_margin_case(
        cases,
        "random_search",
        used_keys=used_keys,
    )
    used_keys.add(random_search_case.key)

    closest_case, closest_duplicate = select_closest_case(cases, used_keys=used_keys)
    used_keys.add(closest_case.key)

    return {
        "再解釈探索が最も有利なケース": (
            reinterpretation_case,
            reinterpretation_margin,
            reinterpretation_duplicate,
        ),
        "局所修復探索が最も有利なケース": (
            local_repair_case,
            local_repair_margin,
            local_repair_duplicate,
        ),
        "ランダム探索が最も有利なケース": (
            random_search_case,
            random_search_margin,
            random_search_duplicate,
        ),
        "差が最も小さいケース": (closest_case, None, closest_duplicate),
    }


def summary_markdown(
    selected: dict[str, tuple[CaseScores, float | None, bool]],
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limit: int,
) -> str:
    lines = [
        "# 代表ケース抽出サマリ",
        "",
        "## 条件",
        "",
        f"- node_counts: `{','.join(str(item) for item in node_counts)}`",
        f"- trials: `{trials}`",
        f"- candidate_limit: `{candidate_limit}`",
        "",
        "## 代表ケース",
        "",
        "| 種類 | case_key | ノード数 | seed | 単発ランダム | ランダム探索 | 局所修復 | 再解釈 | margin | duplicate_allowed |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for label, (case, margin, duplicate_allowed) in selected.items():
        lines.append(case_row(label, case, margin, duplicate_allowed))
    lines.extend(
        [
            "",
            "## 読み方",
            "",
            "`margin` は、対象手法のスコアから、他の手法の最大スコアを引いた値です。",
            "",
            "- 正の値: その手法が他手法より高い。",
            "- 負の値: その手法は代表として選ばれているが、他手法に負けている。",
            "- `差が最も小さいケース`: 全手法のスコア幅が最小のケース。",
            "- `duplicate_allowed`: 候補不足により既出の `node_count / seed` を再利用したかどうか。",
            "",
            "この抽出は説明補助であり、創造性の証明ではありません。",
        ]
    )
    return "\n".join(lines) + "\n"


def selected_case_record(
    label: str,
    case: CaseScores,
    margin: float | None,
    duplicate_allowed: bool,
) -> dict[str, object]:
    return {
        "label": label,
        "case_key": case.key_label,
        "node_count": case.node_count,
        "seed": case.seed,
        "scores": {
            "random_repair": case.random_repair_score,
            "random_search": case.random_search_score,
            "local_repair": case.local_repair_score,
            "reinterpretation": case.reinterpretation_score,
        },
        "margin": margin,
        "score_spread": case.score_spread,
        "duplicate_allowed": duplicate_allowed,
    }


def representative_cases_json(
    selected: dict[str, tuple[CaseScores, float | None, bool]],
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limit: int,
) -> dict[str, object]:
    return {
        "metadata": {
            "node_counts": list(node_counts),
            "trials": trials,
            "candidate_limit": candidate_limit,
            "dedupe_key": "node_count/seed",
            "note": "代表ケース抽出は説明補助であり、創造性の証明ではない。",
        },
        "representative_cases": [
            selected_case_record(label, case, margin, duplicate_allowed)
            for label, (case, margin, duplicate_allowed) in selected.items()
        ],
    }


def write_json(
    path: Path,
    selected: dict[str, tuple[CaseScores, float | None, bool]],
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limit: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = representative_cases_json(selected, node_counts, trials, candidate_limit)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_outputs(
    selected: dict[str, tuple[CaseScores, float | None, bool]],
    output: Path,
    logs_dir: Path | None,
    node_counts: tuple[int, ...],
    trials: int,
    candidate_limit: int,
    json_output: Path | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        summary_markdown(selected, node_counts, trials, candidate_limit),
        encoding="utf-8",
    )

    if json_output is not None:
        write_json(
            path=json_output,
            selected=selected,
            node_counts=node_counts,
            trials=trials,
            candidate_limit=candidate_limit,
        )

    if logs_dir is None:
        return

    logs_dir.mkdir(parents=True, exist_ok=True)
    for index, (label, (case, _, _)) in enumerate(selected.items(), start=1):
        slug = f"{index:02d}_{case.key_label}"
        text = explain_trial.explain_case(
            seed=case.seed,
            node_count=case.node_count,
            candidate_limit=candidate_limit,
        )
        path = logs_dir / f"{slug}.md"
        path.write_text(f"<!-- {label} -->\n\n" + text, encoding="utf-8")


def parse_node_counts(value: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="代表ケースを抽出する")
    parser.add_argument("--nodes", default="3,4,5", help="例: 3 または 3,4,5")
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--candidate-limit", type=int, default=200)
    parser.add_argument("--output", type=Path, default=Path("results/representative_cases.md"))
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--logs-dir", type=Path, default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    node_counts = parse_node_counts(args.nodes)
    cases = collect_cases(
        node_counts=node_counts,
        trials=args.trials,
        candidate_limit=args.candidate_limit,
    )
    selected = select_representative_cases(cases)
    write_outputs(
        selected=selected,
        output=args.output,
        logs_dir=args.logs_dir,
        node_counts=node_counts,
        trials=args.trials,
        candidate_limit=args.candidate_limit,
        json_output=args.json,
    )
    print(summary_markdown(selected, node_counts, args.trials, args.candidate_limit), end="")


if __name__ == "__main__":
    main()
