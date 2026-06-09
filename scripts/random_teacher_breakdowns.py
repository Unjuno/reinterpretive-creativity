from scripts.random_teacher_models import run_smoke_with_models
from scripts.score_breakdown import score_breakdown


def run_smoke_with_breakdowns(seed=0, limit=20):
    data = run_smoke_with_models(seed, limit)
    teacher = data['teacher']
    raw = data['raw']
    for result in data['results'].values():
        result['breakdown'] = score_breakdown(result['model'], teacher, raw)
    return data
