"""複数ケースで再解釈探索を検査する実験スクリプト。

目的:
- 固定デモだけでなく、複数 seed / 複数ノード数の人工モデルで傾向を見る。
- 再解釈探索を、単発ランダム修復・強めのランダム探索・局所修復探索と比較する。
- 結果を JSON / CSV に保存できるようにする。

注意:
- これは人間の創造性の証明ではない。
- 価値は utility_proxy による簡易指標である。
- ノード数が増えると全候補探索は爆発するため、候補サンプリング上限を使う。
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path
from random import Random
from statistics import mean
from typing import Iterable

Node = str
Edge = tuple[Node, Node]
Model = dict[Edge, int]
RawModel = dict[Edge, set[int]]


@dataclass(frozen=True)
class UtilityComponents:
    """有用性 proxy の内訳。

    すべて 0.0〜1.0 の無次元スコアとして扱う。
    """

    density_score: float
    node_coverage_score: float
    weak_connectivity_score: float
    in_out_coverage_score: float

    @property
    def utility(self) -> float:
        """重み付き平均による合成 utility proxy。"""

        return (
            0.35 * self.density_score
            + 0.25 * self.node_coverage_score
            + 0.25 * self.weak_connectivity_score
            + 0.15 * self.in_out_coverage_score
        )


@dataclass(frozen=True)
class TrialResult:
    node_count: int
    seed: int
    random_repair_score: float
    random_search_score: float
    local_repair_score: float
    reinterpretation_score: float
    improvement_vs_random_repair: float
    improvement_vs_random_search: float
    improvement_vs_local_repair: float


@dataclass(frozen=True)
class ExperimentSummary:
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


def make_nodes(node_count: int) -> tuple[Node, ...]:
    if node_count < 2:
        raise ValueError("node_count は2以上である必要があります")
    if node_count > 26:
        raise ValueError("現時点では node_count は26以下にしてください")
    return tuple(chr(ord("A") + index) for index in range(node_count))


def all_edges(nodes: tuple[Node, ...]) -> tuple[Edge, ...]:
    return tuple((src, dst) for src in nodes for dst in nodes if src != dst)


def nodes_in_model(model: Model) -> set[Node]:
    return {node for edge in model for node in edge}


def positive_edges(model: Model) -> list[Edge]:
    return [edge for edge, value in model.items() if value == 1]


def build_cycle_teacher(nodes: tuple[Node, ...]) -> Model:
    teacher = {edge: 0 for edge in all_edges(nodes)}
    for index, src in enumerate(nodes):
        dst = nodes[(index + 1) % len(nodes)]
        teacher[(src, dst)] = 1
    return teacher


def has_conflict(raw: RawModel) -> bool:
    return any(1 in values and -1 in values for values in raw.values())


def noisy_case(
    seed: int,
    node_count: int = 3,
    conflict_rate: float = 0.35,
    extra_positive_rate: float = 0.25,
) -> tuple[Model, RawModel]:
    """教師モデルから、矛盾を含む初期モデルを生成する。"""

    rng = Random(seed)
    nodes = make_nodes(node_count)
    teacher = build_cycle_teacher(nodes)
    raw: RawModel = {}

    for edge, value in teacher.items():
        if value == 1:
            raw[edge] = {1}
            if rng.random() < conflict_rate:
                raw[edge].add(-1)
        elif rng.random() < extra_positive_rate:
            raw[edge] = {1}

    if not has_conflict(raw):
        edge = rng.choice([edge for edge, value in teacher.items() if value == 1])
        raw.setdefault(edge, {1}).add(-1)

    return teacher, raw


def to_model(raw: RawModel, edges: Iterable[Edge]) -> Model:
    model = {edge: 0 for edge in edges}
    for edge, values in raw.items():
        if values == {1}:
            model[edge] = 1
        elif values == {-1}:
            model[edge] = -1
        else:
            model[edge] = 0
    return model


def differs(a: Model, b: Model) -> bool:
    return any(a[edge] != b[edge] for edge in a)


def distance(a: Model, b: Model) -> float:
    return sum(1 for edge in a if a[edge] != b[edge]) / len(a)


def preservation(raw: RawModel, candidate: Model) -> float:
    total = 0
    kept = 0
    for edge, values in raw.items():
        if values in ({1}, {-1}):
            total += 1
            kept += int(candidate[edge] in values)
    return kept / total if total else 0.0


def density_score(candidate: Model) -> float:
    positives = len(positive_edges(candidate))
    node_count = len(nodes_in_model(candidate))
    target = max(1, node_count)
    if positives == 0:
        return 0.0
    return max(0.0, 1.0 - abs(positives - target) / target)


def node_coverage_score(candidate: Model) -> float:
    nodes = nodes_in_model(candidate)
    if not nodes:
        return 0.0
    covered = {node for edge in positive_edges(candidate) for node in edge}
    return len(covered) / len(nodes)


def weak_connectivity_score(candidate: Model) -> float:
    nodes = nodes_in_model(candidate)
    positives = positive_edges(candidate)
    if not nodes or not positives:
        return 0.0

    adjacency = {node: set() for node in nodes}
    for src, dst in positives:
        adjacency[src].add(dst)
        adjacency[dst].add(src)

    seen: set[Node] = set()
    largest = 0
    for start in nodes:
        if start in seen:
            continue
        stack = [start]
        size = 0
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            size += 1
            stack.extend(adjacency[node] - seen)
        largest = max(largest, size)

    return largest / len(nodes)


def in_out_coverage_score(candidate: Model) -> float:
    nodes = nodes_in_model(candidate)
    positives = positive_edges(candidate)
    if not nodes or not positives:
        return 0.0

    out_nodes = {src for src, _ in positives}
    in_nodes = {dst for _, dst in positives}
    return (len(out_nodes) + len(in_nodes)) / (2 * len(nodes))


def utility_components(candidate: Model) -> UtilityComponents:
    return UtilityComponents(
        density_score=density_score(candidate),
        node_coverage_score=node_coverage_score(candidate),
        weak_connectivity_score=weak_connectivity_score(candidate),
        in_out_coverage_score=in_out_coverage_score(candidate),
    )


def utility_proxy(candidate: Model) -> float:
    return utility_components(candidate).utility


def score(candidate: Model, teacher: Model, raw: RawModel) -> float:
    return distance(candidate, teacher) * preservation(raw, candidate) * utility_proxy(candidate)


def exhaustive_candidates(edges: tuple[Edge, ...]) -> Iterable[Model]:
    for values in product((-1, 0, 1), repeat=len(edges)):
        yield dict(zip(edges, values))


def sampled_candidates(
    edges: tuple[Edge, ...],
    raw: RawModel,
    seed: int,
    candidate_limit: int,
) -> Iterable[Model]:
    """初期モデルをある程度保存する候補を決定的にサンプリングする。"""

    rng = Random(seed)
    base = to_model(raw, edges)
    yield base

    for _ in range(candidate_limit):
        candidate = dict(base)
        for edge in edges:
            if rng.random() < 0.25:
                candidate[edge] = rng.choice((-1, 0, 1))
        for edge, values in raw.items():
            if values == {1, -1}:
                candidate[edge] = rng.choice((-1, 0, 1))
        yield candidate


def random_candidates(
    edges: tuple[Edge, ...],
    seed: int,
    candidate_limit: int,
) -> Iterable[Model]:
    rng = Random(seed)
    for _ in range(candidate_limit):
        yield {edge: rng.choice((-1, 0, 1)) for edge in edges}


def neighbor_candidates(model: Model, edges: tuple[Edge, ...], rng: Random) -> Iterable[Model]:
    """1辺だけ変更した近傍候補をランダム順で返す。"""

    edge_order = list(edges)
    rng.shuffle(edge_order)
    for edge in edge_order:
        values = [-1, 0, 1]
        values.remove(model[edge])
        rng.shuffle(values)
        for value in values:
            candidate = dict(model)
            candidate[edge] = value
            yield candidate


def best_from_stream(stream: Iterable[Model], teacher: Model, raw: RawModel) -> tuple[float, Model]:
    best_score = -1.0
    best_model: Model | None = None
    for candidate in stream:
        if not differs(candidate, teacher):
            continue
        current = score(candidate, teacher, raw)
        if current > best_score:
            best_score = current
            best_model = candidate

    if best_model is None:
        raise RuntimeError("候補モデルが見つかりません")
    return best_score, best_model


def reinterpretation_search(
    teacher: Model,
    raw: RawModel,
    seed: int,
    candidate_limit: int,
) -> tuple[float, Model]:
    edges = tuple(teacher.keys())
    if len(edges) <= 8:
        stream = exhaustive_candidates(edges)
    else:
        stream = sampled_candidates(
            edges,
            raw,
            seed=seed + 100_000,
            candidate_limit=candidate_limit,
        )
    return best_from_stream(stream, teacher, raw)


def random_search_baseline(
    teacher: Model,
    raw: RawModel,
    seed: int,
    candidate_limit: int,
) -> tuple[float, Model]:
    edges = tuple(teacher.keys())
    stream = random_candidates(
        edges,
        seed=seed + 200_000,
        candidate_limit=candidate_limit,
    )
    return best_from_stream(stream, teacher, raw)


def local_repair_search(
    teacher: Model,
    raw: RawModel,
    seed: int,
    candidate_limit: int,
) -> tuple[float, Model]:
    """初期モデルから1辺変更の近傍をたどる局所修復探索。

    改善する近傍があれば移動し、改善がない場合は1辺だけ摂動して停滞から抜ける。
    候補評価回数は candidate_limit で制限する。
    """

    rng = Random(seed + 300_000)
    edges = tuple(teacher.keys())
    current = to_model(raw, edges)
    if not differs(current, teacher):
        edge = rng.choice(edges)
        current[edge] = 0 if current[edge] != 0 else 1

    current_score = score(current, teacher, raw) if differs(current, teacher) else -1.0
    best_model = dict(current)
    best_score = current_score
    evaluated = 0

    while evaluated < candidate_limit:
        moved = False
        best_neighbor: Model | None = None
        best_neighbor_score = current_score
        for candidate in neighbor_candidates(current, edges, rng):
            if evaluated >= candidate_limit:
                break
            evaluated += 1
            if not differs(candidate, teacher):
                continue
            candidate_score = score(candidate, teacher, raw)
            if candidate_score > best_neighbor_score:
                best_neighbor = candidate
                best_neighbor_score = candidate_score
            if candidate_score > best_score:
                best_model = candidate
                best_score = candidate_score

        if best_neighbor is not None:
            current = best_neighbor
            current_score = best_neighbor_score
            moved = True

        if not moved:
            current = dict(current)
            edge = rng.choice(edges)
            values = [-1, 0, 1]
            values.remove(current[edge])
            current[edge] = rng.choice(values)
            current_score = score(current, teacher, raw) if differs(current, teacher) else -1.0

    return best_score, best_model


def random_repair(teacher: Model, raw: RawModel, seed: int) -> tuple[float, Model]:
    rng = Random(seed)
    model = to_model(raw, teacher.keys())
    for edge, values in raw.items():
        if values == {1, -1}:
            model[edge] = rng.choice((-1, 0, 1))
    if not differs(model, teacher):
        edge = rng.choice(tuple(model.keys()))
        model[edge] = 0 if model[edge] != 0 else 1
    return score(model, teacher, raw), model


def run_trial(seed: int, node_count: int = 3, candidate_limit: int = 500) -> TrialResult:
    teacher, raw = noisy_case(seed=seed, node_count=node_count)
    random_repair_score, _ = random_repair(teacher, raw, seed=seed)
    random_search_score, _ = random_search_baseline(
        teacher,
        raw,
        seed=seed,
        candidate_limit=candidate_limit,
    )
    local_repair_score, _ = local_repair_search(
        teacher,
        raw,
        seed=seed,
        candidate_limit=candidate_limit,
    )
    reinterpretation_score, _ = reinterpretation_search(
        teacher,
        raw,
        seed=seed,
        candidate_limit=candidate_limit,
    )
    return TrialResult(
        node_count=node_count,
        seed=seed,
        random_repair_score=random_repair_score,
        random_search_score=random_search_score,
        local_repair_score=local_repair_score,
        reinterpretation_score=reinterpretation_score,
        improvement_vs_random_repair=reinterpretation_score - random_repair_score,
        improvement_vs_random_search=reinterpretation_score - random_search_score,
        improvement_vs_local_repair=reinterpretation_score - local_repair_score,
    )


def summarize(node_count: int, results: list[TrialResult]) -> ExperimentSummary:
    if not results:
        raise ValueError("結果が空です")
    wins_vs_random_repair = sum(
        1 for result in results if result.reinterpretation_score >= result.random_repair_score
    )
    wins_vs_random_search = sum(
        1 for result in results if result.reinterpretation_score >= result.random_search_score
    )
    wins_vs_local_repair = sum(
        1 for result in results if result.reinterpretation_score >= result.local_repair_score
    )
    return ExperimentSummary(
        node_count=node_count,
        trials=len(results),
        random_repair_mean=mean(result.random_repair_score for result in results),
        random_search_mean=mean(result.random_search_score for result in results),
        local_repair_mean=mean(result.local_repair_score for result in results),
        reinterpretation_mean=mean(result.reinterpretation_score for result in results),
        improvement_vs_random_repair_mean=mean(
            result.improvement_vs_random_repair for result in results
        ),
        improvement_vs_random_search_mean=mean(
            result.improvement_vs_random_search for result in results
        ),
        improvement_vs_local_repair_mean=mean(
            result.improvement_vs_local_repair for result in results
        ),
        win_rate_vs_random_repair=wins_vs_random_repair / len(results),
        win_rate_vs_random_search=wins_vs_random_search / len(results),
        win_rate_vs_local_repair=wins_vs_local_repair / len(results),
    )


def run_suite(
    node_counts: tuple[int, ...] = (3,),
    trials: int = 30,
    candidate_limit: int = 500,
) -> tuple[list[TrialResult], list[ExperimentSummary]]:
    all_results: list[TrialResult] = []
    summaries: list[ExperimentSummary] = []

    for node_count in node_counts:
        results = [
            run_trial(seed=seed, node_count=node_count, candidate_limit=candidate_limit)
            for seed in range(trials)
        ]
        all_results.extend(results)
        summaries.append(summarize(node_count, results))

    return all_results, summaries


def format_summary(summaries: list[ExperimentSummary]) -> str:
    lines = [
        "| ノード数 | 試行数 | 単発ランダム平均 | ランダム探索平均 | 局所修復平均 | 再解釈平均 | 改善量(単発) | 改善量(探索) | 改善量(局所) | 勝率(単発) | 勝率(探索) | 勝率(局所) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| "
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
    return "\n".join(lines)


def write_json(path: Path, results: list[TrialResult], summaries: list[ExperimentSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "summaries": [asdict(summary) for summary in summaries],
        "trials": [asdict(result) for result in results],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, results: list[TrialResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "node_count",
                "seed",
                "random_repair_score",
                "random_search_score",
                "local_repair_score",
                "reinterpretation_score",
                "improvement_vs_random_repair",
                "improvement_vs_random_search",
                "improvement_vs_local_repair",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))


def parse_node_counts(value: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="再解釈型創造性モデルの複数ケース実験")
    parser.add_argument("--nodes", default="3", help="例: 3 または 3,4,5")
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--candidate-limit", type=int, default=500)
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--csv", type=Path, default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    results, summaries = run_suite(
        node_counts=parse_node_counts(args.nodes),
        trials=args.trials,
        candidate_limit=args.candidate_limit,
    )
    print(format_summary(summaries))

    if args.json is not None:
        write_json(args.json, results, summaries)
    if args.csv is not None:
        write_csv(args.csv, results)


if __name__ == "__main__":
    main()
