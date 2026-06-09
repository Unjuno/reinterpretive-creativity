from scripts.random_teacher_breakdowns import run_smoke_with_breakdowns
from scripts.reinterpretation_breakdown_gap import reinterpretation_breakdown_gap


def run_smoke_with_reinterpretation_gap(seed=0, limit=20):
    data = run_smoke_with_breakdowns(seed, limit)
    return {
        **data,
        "reinterpretation_breakdown_gap": reinterpretation_breakdown_gap(data),
    }
