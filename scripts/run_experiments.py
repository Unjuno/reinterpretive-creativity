"""複数ケースで再解釈探索を検査する実験スクリプト。

目的:
- 固定デモだけでなく、複数 seed の人工モデルで傾向を見る。
- 再解釈探索とランダム修復の平均スコアを比較する。

注意:
- これは人間の創造性の証明ではない。
- 価値は utility_proxy による簡易指標である。
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from statistics import mean

try:
    from scripts import simulate
except ModuleNotFoundError:  # `python scripts/run_experiments.py` 用
    import simulate  # type: ignore[no-redef]


@dataclass(frozen=True)
class TrialResult:
    seed: int
    random_score: float
    reinterpretation_score: float
    improvement: float


@dataclass(frozen=True)
class ExperimentSummary:
    trials: int
    random_mean: float
    reinterpretation_mean: float
    improvement_mean: float
    win_rate: float


def noisy_case(seed: int, conflict_rate: float = 0.35, extra_positive_rate: float = 0.25):
    """教師モデルから、矛盾を含む初期モデルを生成する。"""

    rng = Random(seed)
    teacher = simulate.build_teacher()
    raw: dict[simulate.Edge, set[int]] = {}

    for edge, value in teacher.items():
        if value == 1:
            raw[edge] = {1}
            if rng.random() < conflict_rate:
                raw[edge].add(-1)
        elif rng.random() < extra_positive_rate:
            raw[edge] = {1}

    # 最低1つは内部不整合を入れる。そうでないと再解釈型創造性の検査にならない。
    if not simulate.has_conflict(raw):
        edge = rng.choice([edge for edge, value in teacher.items() if value == 1])
        raw.setdefault(edge, {1}).add(-1)

    return teacher, raw


def run_trial(seed: int) -> TrialResult:
    teacher, raw = noisy_case(seed)
    random_score, _ = simulate.random_repair(teacher, raw, seed=seed)
    reinterpretation_score, _ = simulate.best_reinterpretation(teacher, raw)
    return TrialResult(
        seed=seed,
        random_score=random_score,
        reinterpretation_score=reinterpretation_score,
        improvement=reinterpretation_score - random_score,
    )


def summarize(results: list[TrialResult]) -> ExperimentSummary:
    if not results:
        raise ValueError("結果が空です")
    wins = sum(1 for result in results if result.reinterpretation_score >= result.random_score)
    return ExperimentSummary(
        trials=len(results),
        random_mean=mean(result.random_score for result in results),
        reinterpretation_mean=mean(result.reinterpretation_score for result in results),
        improvement_mean=mean(result.improvement for result in results),
        win_rate=wins / len(results),
    )


def format_summary(summary: ExperimentSummary) -> str:
    return "\n".join(
        [
            f"試行数: {summary.trials}",
            f"ランダム修復 平均スコア: {summary.random_mean:.4f}",
            f"再解釈探索 平均スコア: {summary.reinterpretation_mean:.4f}",
            f"平均改善量: {summary.improvement_mean:.4f}",
            f"勝率: {summary.win_rate:.2%}",
        ]
    )


def main() -> None:
    results = [run_trial(seed) for seed in range(30)]
    print(format_summary(summarize(results)))


if __name__ == "__main__":
    main()
