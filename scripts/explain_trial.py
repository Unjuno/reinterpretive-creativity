"""1つの実験ケースについて、各探索結果の変更内容を説明する。

目的:
- 平均スコアだけでなく、1ケースで何が変わったかを見る。
- 教師モデル、初期モデル、各探索結果、変更辺、スコア内訳をMarkdownで出力する。
- 局所修復探索について、改善・摂動の過程をMarkdownで出力する。
- 同じ内容を機械処理しやすいJSONでも出力できるようにする。

注意:
- これは説明補助であり、創造性の証明ではない。
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from random import Random

try:
    from scripts import run_experiments
except ModuleNotFoundError:  # `python scripts/explain_trial.py` 用
    import run_experiments  # type: ignore[no-redef]

Model = run_experiments.Model
RawModel = run_experiments.RawModel
Edge = run_experiments.Edge


@dataclass(frozen=True)
class LocalRepairTraceStep:
    """局所修復探索の1ステップ。"""

    step: int
    action: str
    edge: Edge
    old_value: int
    new_value: int
    previous_score: float
    new_score: float
    best_score: float
    evaluated: int


def edge_label(edge: Edge) -> str:
    return f"{edge[0]}->{edge[1]}"


def value_label(value: int) -> str:
    if value == 1:
        return "肯定"
    if value == -1:
        return "否定"
    return "不明"


def action_label(action: str) -> str:
    if action == "improve":
        return "改善"
    if action == "perturb":
        return "摂動"
    if action == "initial_perturb":
        return "初期摂動"
    return action


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


def first_changed_edge(before: Model, after: Model) -> tuple[Edge, int, int]:
    changes = changed_edges(before, after)
    if not changes:
        raise ValueError("変更された辺がありません")
    return changes[0]


def change_rows(before: Model, after: Model) -> list[str]:
    changes = changed_edges(before, after)
    if not changes:
        return ["| _なし_ | _なし_ | _なし_ |"]
    return [
        f"| `{edge_label(edge)}` | {value_label(old)} | {value_label(new)} |"
        for edge, old, new in changes
    ]


def score_breakdown(candidate: Model, teacher: Model, raw: RawModel) -> dict[str, float]:
    """候補モデルの総合スコアを構成要素に分解する。"""

    novelty_distance = run_experiments.distance(candidate, teacher)
    preservation = run_experiments.preservation(raw, candidate)
    utility_components = run_experiments.utility_components(candidate)
    utility_proxy = utility_components.utility
    total_score = run_experiments.score(candidate, teacher, raw)

    return {
        "novelty_distance": novelty_distance,
        "preservation": preservation,
        "utility_proxy": utility_proxy,
        "density_score": utility_components.density_score,
        "node_coverage_score": utility_components.node_coverage_score,
        "weak_connectivity_score": utility_components.weak_connectivity_score,
        "in_out_coverage_score": utility_components.in_out_coverage_score,
        "total_score": total_score,
    }


def score_breakdown_rows(candidate: Model, teacher: Model, raw: RawModel) -> list[str]:
    values = score_breakdown(candidate, teacher, raw)
    return [
        f"| novelty_distance | {values['novelty_distance']:.4f} | 教師モデルとの差分。大きいほど教師モデルと異なる |",
        f"| preservation | {values['preservation']:.4f} | 初期モデルの非矛盾情報をどれだけ保存したか |",
        f"| utility_proxy | {values['utility_proxy']:.4f} | 構造的な有用性らしさの暫定 proxy |",
        f"| density_score | {values['density_score']:.4f} | 空構造と過密構造を下げる密度指標 |",
        f"| node_coverage_score | {values['node_coverage_score']:.4f} | 肯定辺が覆うノードの割合 |",
        f"| weak_connectivity_score | {values['weak_connectivity_score']:.4f} | 肯定辺の最大弱連結成分比率 |",
        f"| in_out_coverage_score | {values['in_out_coverage_score']:.4f} | 入辺・出辺を持つノードの広がり |",
        f"| total_score | {values['total_score']:.4f} | novelty_distance * preservation * utility_proxy |",
    ]


def local_repair_search_with_trace(
    teacher: Model,
    raw: RawModel,
    seed: int,
    candidate_limit: int,
) -> tuple[float, Model, list[LocalRepairTraceStep]]:
    """局所修復探索を説明用に再実行し、改善・摂動の過程を返す。"""

    rng = Random(seed + 300_000)
    edges = tuple(teacher.keys())
    current = run_experiments.to_model(raw, edges)
    trace: list[LocalRepairTraceStep] = []
    step = 0

    if not run_experiments.differs(current, teacher):
        edge = rng.choice(edges)
        old_value = current[edge]
        current[edge] = 0 if current[edge] != 0 else 1
        current_score = (
            run_experiments.score(current, teacher, raw)
            if run_experiments.differs(current, teacher)
            else -1.0
        )
        step += 1
        trace.append(
            LocalRepairTraceStep(
                step=step,
                action="initial_perturb",
                edge=edge,
                old_value=old_value,
                new_value=current[edge],
                previous_score=-1.0,
                new_score=current_score,
                best_score=current_score,
                evaluated=0,
            )
        )
    else:
        current_score = run_experiments.score(current, teacher, raw)

    best_model = dict(current)
    best_score = current_score
    evaluated = 0

    while evaluated < candidate_limit:
        moved = False
        best_neighbor: Model | None = None
        best_neighbor_score = current_score
        for candidate in run_experiments.neighbor_candidates(current, edges, rng):
            if evaluated >= candidate_limit:
                break
            evaluated += 1
            if not run_experiments.differs(candidate, teacher):
                continue
            candidate_score = run_experiments.score(candidate, teacher, raw)
            if candidate_score > best_neighbor_score:
                best_neighbor = candidate
                best_neighbor_score = candidate_score
            if candidate_score > best_score:
                best_model = candidate
                best_score = candidate_score

        if best_neighbor is not None:
            previous = current
            previous_score = current_score
            edge, old_value, new_value = first_changed_edge(previous, best_neighbor)
            current = best_neighbor
            current_score = best_neighbor_score
            moved = True
            step += 1
            trace.append(
                LocalRepairTraceStep(
                    step=step,
                    action="improve",
                    edge=edge,
                    old_value=old_value,
                    new_value=new_value,
                    previous_score=previous_score,
                    new_score=current_score,
                    best_score=best_score,
                    evaluated=evaluated,
                )
            )

        if not moved:
            previous_score = current_score
            current = dict(current)
            edge = rng.choice(edges)
            old_value = current[edge]
            values = [-1, 0, 1]
            values.remove(current[edge])
            current[edge] = rng.choice(values)
            current_score = (
                run_experiments.score(current, teacher, raw)
                if run_experiments.differs(current, teacher)
                else -1.0
            )
            step += 1
            trace.append(
                LocalRepairTraceStep(
                    step=step,
                    action="perturb",
                    edge=edge,
                    old_value=old_value,
                    new_value=current[edge],
                    previous_score=previous_score,
                    new_score=current_score,
                    best_score=best_score,
                    evaluated=evaluated,
                )
            )

    return best_score, best_model, trace


def trace_rows(trace: list[LocalRepairTraceStep]) -> list[str]:
    if not trace:
        return ["| _なし_ | _なし_ | _なし_ | _なし_ | _なし_ | _なし_ | _なし_ | _なし_ |"]
    return [
        "| "
        f"{step.step} | "
        f"{action_label(step.action)} | "
        f"{step.evaluated} | "
        f"`{edge_label(step.edge)}` | "
        f"{value_label(step.old_value)} | "
        f"{value_label(step.new_value)} | "
        f"{step.previous_score:.4f} | "
        f"{step.new_score:.4f} | "
        f"{step.best_score:.4f} |"
        for step in trace
    ]


def local_repair_trace_block(trace: list[LocalRepairTraceStep]) -> str:
    lines = [
        "#### 局所修復探索の改善過程",
        "",
        "| step | action | evaluated | 辺 | 変更前 | 変更後 | score_before | score_after | best_score |",
        "|---:|---|---:|---|---|---|---:|---:|---:|",
        *trace_rows(trace),
    ]
    return "\n".join(lines)


def result_block(
    title: str,
    score: float,
    initial: Model,
    teacher: Model,
    raw: RawModel,
    result: Model,
    extra_sections: list[str] | None = None,
) -> str:
    lines = [
        f"### {title}",
        "",
        f"score: `{score:.4f}`",
        "",
        "#### スコア内訳",
        "",
        "| 指標 | 値 | 意味 |",
        "|---|---:|---|",
        *score_breakdown_rows(result, teacher, raw),
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
    if extra_sections:
        lines.extend(["", *extra_sections])
    return "\n".join(lines)


def edge_record(edge: Edge, value: int) -> dict[str, object]:
    return {
        "edge": edge_label(edge),
        "src": edge[0],
        "dst": edge[1],
        "value": value,
        "label": value_label(value),
    }


def model_records(model: Model) -> list[dict[str, object]]:
    return [edge_record(edge, value) for edge, value in sorted(model.items()) if value != 0]


def raw_records(raw: RawModel, edges: tuple[Edge, ...]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for edge in sorted(edges):
        values = raw.get(edge)
        label = raw_value_label(values)
        if label == "不明":
            continue
        records.append(
            {
                "edge": edge_label(edge),
                "src": edge[0],
                "dst": edge[1],
                "values": sorted(values or []),
                "label": label,
            }
        )
    return records


def change_records(before: Model, after: Model) -> list[dict[str, object]]:
    return [
        {
            "edge": edge_label(edge),
            "src": edge[0],
            "dst": edge[1],
            "before": old_value,
            "after": new_value,
            "before_label": value_label(old_value),
            "after_label": value_label(new_value),
        }
        for edge, old_value, new_value in changed_edges(before, after)
    ]


def trace_records(trace: list[LocalRepairTraceStep]) -> list[dict[str, object]]:
    return [
        {
            "step": step.step,
            "action": step.action,
            "action_label": action_label(step.action),
            "evaluated": step.evaluated,
            "edge": edge_label(step.edge),
            "src": step.edge[0],
            "dst": step.edge[1],
            "old_value": step.old_value,
            "new_value": step.new_value,
            "old_label": value_label(step.old_value),
            "new_label": value_label(step.new_value),
            "score_before": step.previous_score,
            "score_after": step.new_score,
            "best_score": step.best_score,
        }
        for step in trace
    ]


def result_record(
    score: float,
    initial: Model,
    teacher: Model,
    raw: RawModel,
    result: Model,
    trace: list[LocalRepairTraceStep] | None = None,
) -> dict[str, object]:
    record: dict[str, object] = {
        "score": score,
        "score_breakdown": score_breakdown(result, teacher, raw),
        "model": model_records(result),
        "changes_from_initial": change_records(initial, result),
        "differences_from_teacher": change_records(teacher, result),
    }
    if trace is not None:
        record["local_repair_trace"] = trace_records(trace)
    return record


def build_case(
    seed: int,
    node_count: int,
    candidate_limit: int,
) -> tuple[Model, RawModel, Model, dict[str, tuple[float, Model]], list[LocalRepairTraceStep]]:
    teacher, raw = run_experiments.noisy_case(seed=seed, node_count=node_count)
    initial = run_experiments.to_model(raw, teacher.keys())

    random_repair_score, random_repair_model = run_experiments.random_repair(
        teacher, raw, seed=seed
    )
    random_search_score, random_search_model = run_experiments.random_search_baseline(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )
    local_repair_score, local_repair_model, local_repair_trace = local_repair_search_with_trace(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )
    reinterpretation_score, reinterpretation_model = run_experiments.reinterpretation_search(
        teacher, raw, seed=seed, candidate_limit=candidate_limit
    )

    results = {
        "random_repair": (random_repair_score, random_repair_model),
        "random_search": (random_search_score, random_search_model),
        "local_repair": (local_repair_score, local_repair_model),
        "reinterpretation": (reinterpretation_score, reinterpretation_model),
    }
    return teacher, raw, initial, results, local_repair_trace


def explain_case(seed: int, node_count: int, candidate_limit: int) -> str:
    teacher, raw, initial, results, local_repair_trace = build_case(
        seed=seed,
        node_count=node_count,
        candidate_limit=candidate_limit,
    )

    random_repair_score, random_repair_model = results["random_repair"]
    random_search_score, random_search_model = results["random_search"]
    local_repair_score, local_repair_model = results["local_repair"]
    reinterpretation_score, reinterpretation_model = results["reinterpretation"]

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
        result_block("単発ランダム修復", random_repair_score, initial, teacher, raw, random_repair_model),
        "",
        result_block("ランダム探索", random_search_score, initial, teacher, raw, random_search_model),
        "",
        result_block(
            "局所修復探索",
            local_repair_score,
            initial,
            teacher,
            raw,
            local_repair_model,
            extra_sections=[local_repair_trace_block(local_repair_trace)],
        ),
        "",
        result_block("再解釈探索", reinterpretation_score, initial, teacher, raw, reinterpretation_model),
        "",
        "## 注意",
        "",
        "このログは、候補モデルの変更内容、スコア構成要素、局所修復探索の改善過程を読むための説明補助です。",
        "創造性そのものを証明するものではありません。",
    ]
    return "\n".join(lines) + "\n"


def explain_case_json(seed: int, node_count: int, candidate_limit: int) -> dict[str, object]:
    teacher, raw, initial, results, local_repair_trace = build_case(
        seed=seed,
        node_count=node_count,
        candidate_limit=candidate_limit,
    )

    return {
        "metadata": {
            "seed": seed,
            "node_count": node_count,
            "candidate_limit": candidate_limit,
            "note": "1ケース説明ログは説明補助であり、創造性の証明ではない。",
        },
        "teacher_model": model_records(teacher),
        "initial_model": raw_records(raw, tuple(teacher.keys())),
        "results": {
            "random_repair": result_record(
                results["random_repair"][0],
                initial,
                teacher,
                raw,
                results["random_repair"][1],
            ),
            "random_search": result_record(
                results["random_search"][0],
                initial,
                teacher,
                raw,
                results["random_search"][1],
            ),
            "local_repair": result_record(
                results["local_repair"][0],
                initial,
                teacher,
                raw,
                results["local_repair"][1],
                trace=local_repair_trace,
            ),
            "reinterpretation": result_record(
                results["reinterpretation"][0],
                initial,
                teacher,
                raw,
                results["reinterpretation"][1],
            ),
        },
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="1ケース説明ログを生成する")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--node-count", type=int, default=4)
    parser.add_argument("--candidate-limit", type=int, default=100)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--json", type=Path, default=None)
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

    if args.json is not None:
        write_json(
            args.json,
            explain_case_json(
                seed=args.seed,
                node_count=args.node_count,
                candidate_limit=args.candidate_limit,
            ),
        )


if __name__ == "__main__":
    main()
