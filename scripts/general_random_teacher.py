"""General random graph teacher utilities for Phase 2 checks.

This module is intentionally small.  It adds a random teacher generator that can
control the number of positive directed edges, so that teacher-model checks do
not have to rely only on the single-positive-edge smoke generator.

The generated teachers are still synthetic structural teachers.  They are not
claims about human teachers, human creativity, or human value judgments.
"""

from __future__ import annotations

from random import Random
from typing import Iterable

from scripts import run_experiments as exp


def build_random_graph_teacher(
    node_count: int = 4,
    positive_edge_count: int | None = None,
    seed: int = 0,
) -> exp.Model:
    """Build a random directed graph teacher with a fixed positive-edge count.

    Args:
        node_count: Number of nodes in the synthetic graph.
        positive_edge_count: Number of directed edges marked positive.  When
            omitted, this defaults to ``node_count`` so the random teacher has
            the same positive-edge count as the fixed cycle teacher.
        seed: Random seed for deterministic generation.

    Returns:
        A full edge dictionary whose values are ``1`` for selected positive
        edges and ``0`` otherwise.
    """

    nodes = exp.make_nodes(node_count)
    edges = exp.all_edges(nodes)
    if positive_edge_count is None:
        positive_edge_count = node_count
    if positive_edge_count < 1:
        raise ValueError("positive_edge_count must be at least 1")
    if positive_edge_count > len(edges):
        raise ValueError("positive_edge_count cannot exceed available edges")

    rng = Random(seed)
    positives = set(rng.sample(edges, positive_edge_count))
    return {edge: 1 if edge in positives else 0 for edge in edges}


def make_noisy_raw_from_teacher(
    teacher: exp.Model,
    seed: int = 0,
    conflict_rate: float = 0.35,
    extra_positive_rate: float = 0.25,
) -> exp.RawModel:
    """Create a noisy raw model from an arbitrary teacher.

    The rule mirrors ``run_experiments.noisy_case`` but accepts an explicit
    teacher model instead of always constructing the fixed cycle teacher.
    """

    rng = Random(seed)
    raw: exp.RawModel = {}

    for edge, value in teacher.items():
        if value == 1:
            raw[edge] = {1}
            if rng.random() < conflict_rate:
                raw[edge].add(-1)
        elif rng.random() < extra_positive_rate:
            raw[edge] = {1}

    if not exp.has_conflict(raw):
        teacher_positive_edges = [edge for edge, value in teacher.items() if value == 1]
        edge = rng.choice(teacher_positive_edges)
        raw.setdefault(edge, {1}).add(-1)

    return raw


def run_methods(
    teacher: exp.Model,
    raw: exp.RawModel,
    seed: int,
    candidate_limit: int,
) -> dict[str, float]:
    """Run the standard method set and return only structural proxy scores."""

    return {
        "random_repair": exp.random_repair(teacher, raw, seed)[0],
        "random_search": exp.random_search_baseline(teacher, raw, seed, candidate_limit)[0],
        "local_repair": exp.local_repair_search(teacher, raw, seed, candidate_limit)[0],
        "reinterpretation": exp.reinterpretation_search(teacher, raw, seed, candidate_limit)[0],
    }


def positive_edge_count(teacher: exp.Model) -> int:
    """Return the number of positive teacher edges."""

    return len(exp.positive_edges(teacher))


def raw_edge_count(raw: exp.RawModel) -> int:
    """Return the number of explicit raw edges."""

    return len(raw)


def conflict_edge_count(raw: exp.RawModel) -> int:
    """Return the number of raw edges containing both positive and negative evidence."""

    return sum(1 for values in raw.values() if values == {1, -1})


def singleton_positive_edge_count(raw: exp.RawModel) -> int:
    """Return the number of raw edges containing only positive evidence."""

    return sum(1 for values in raw.values() if values == {1})


def strongest_baseline_score(scores: dict[str, float]) -> float:
    """Return the strongest non-reinterpretation baseline score."""

    return max(scores["random_repair"], scores["random_search"], scores["local_repair"])


def count_reinterpretation_losses(score_rows: Iterable[dict[str, float]]) -> int:
    """Count rows where reinterpretation loses to the strongest baseline."""

    return sum(
        1
        for scores in score_rows
        if scores["reinterpretation"] < strongest_baseline_score(scores)
    )
