"""再解釈型創造性モデルの最小シミュレーション。

人工的な符号付き有向グラフで、内部不整合を持つモデルから
整合的な代替モデルを探す。これは人間の創造性の証明ではない。
"""

from __future__ import annotations

from itertools import product
from random import Random
from typing import Dict, Iterable, Tuple

Node = str
Edge = Tuple[Node, Node]
Model = Dict[Edge, int]  # -1: 否定, 0: 不明, 1: 肯定

NODES: tuple[Node, ...] = ("A", "B", "C")
EDGES: tuple[Edge, ...] = tuple((a, b) for a in NODES for b in NODES if a != b)


def build_teacher() -> Model:
    model = {edge: 0 for edge in EDGES}
    model[("A", "B")] = 1
    model[("B", "C")] = 1
    model[("C", "A")] = 1
    return model


def build_initial_conflicts() -> dict[Edge, set[int]]:
    return {
        ("A", "B"): {1},
        ("B", "C"): {1, -1},
        ("C", "A"): {1},
        ("A", "C"): {1},
    }


def has_conflict(raw: dict[Edge, set[int]]) -> bool:
    return any(1 in values and -1 in values for values in raw.values())


def to_model(raw: dict[Edge, set[int]]) -> Model:
    model = {edge: 0 for edge in EDGES}
    for edge, values in raw.items():
        if values == {1}:
            model[edge] = 1
        elif values == {-1}:
            model[edge] = -1
        else:
            model[edge] = 0
    return model


def differs(a: Model, b: Model) -> bool:
    return any(a[edge] != b[edge] for edge in EDGES)


def distance(a: Model, b: Model) -> float:
    return sum(1 for edge in EDGES if a[edge] != b[edge]) / len(EDGES)


def preservation(raw: dict[Edge, set[int]], candidate: Model) -> float:
    total = 0
    kept = 0
    for edge, values in raw.items():
        if values in ({1}, {-1}):
            total += 1
            kept += int(candidate[edge] in values)
    return kept / total if total else 0.0


def utility_proxy(candidate: Model) -> float:
    positives = sum(1 for value in candidate.values() if value == 1)
    if positives == 0:
        return 0.0
    if positives <= 3:
        return positives / 3
    return max(0.0, 1.0 - (positives - 3) / 3)


def score(candidate: Model, teacher: Model, raw: dict[Edge, set[int]]) -> float:
    return distance(candidate, teacher) * preservation(raw, candidate) * utility_proxy(candidate)


def candidates() -> Iterable[Model]:
    for values in product((-1, 0, 1), repeat=len(EDGES)):
        yield dict(zip(EDGES, values))


def best_reinterpretation(teacher: Model, raw: dict[Edge, set[int]]) -> tuple[float, Model]:
    best_score = -1.0
    best_model: Model | None = None
    for candidate in candidates():
        if not differs(candidate, teacher):
            continue
        current = score(candidate, teacher, raw)
        if current > best_score:
            best_score = current
            best_model = candidate
    assert best_model is not None
    return best_score, best_model


def random_repair(teacher: Model, raw: dict[Edge, set[int]], seed: int = 42) -> tuple[float, Model]:
    rng = Random(seed)
    model = to_model(raw)
    for edge, values in raw.items():
        if values == {1, -1}:
            model[edge] = rng.choice((-1, 0, 1))
    if not differs(model, teacher):
        edge = rng.choice(EDGES)
        model[edge] = 0 if model[edge] != 0 else 1
    return score(model, teacher, raw), model


def compact(model: Model) -> str:
    parts = []
    for edge, value in sorted(model.items()):
        if value == 1:
            parts.append(f"{edge[0]}->{edge[1]}")
        elif value == -1:
            parts.append(f"not {edge[0]}->{edge[1]}")
    return ", ".join(parts) or "empty"


def main() -> None:
    teacher = build_teacher()
    raw = build_initial_conflicts()
    random_score, random_model = random_repair(teacher, raw)
    best_score, best_model = best_reinterpretation(teacher, raw)

    print("内部不整合あり:", has_conflict(raw))
    print("教師モデル:", compact(teacher))
    print("ランダム修復:", round(random_score, 4), compact(random_model))
    print("再解釈探索:", round(best_score, 4), compact(best_model))


if __name__ == "__main__":
    main()
