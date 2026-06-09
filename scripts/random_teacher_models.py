from scripts import run_experiments as e
from scripts.random_teacher_experiments import make_noisy_raw_from_teacher
from scripts.random_teacher_smoke import build_random_teacher


def _pack(result):
    score, model = result
    return {'score': score, 'model': model}


def run_smoke_with_models(seed=0, limit=20):
    teacher = build_random_teacher(4, seed)
    raw = make_noisy_raw_from_teacher(teacher, seed)
    return {
        'teacher': teacher,
        'raw': raw,
        'results': {
            'random_repair': _pack(e.random_repair(teacher, raw, seed)),
            'random_search': _pack(e.random_search_baseline(teacher, raw, seed, limit)),
            'local_repair': _pack(e.local_repair_search(teacher, raw, seed, limit)),
            'reinterpretation': _pack(e.reinterpretation_search(teacher, raw, seed, limit)),
        },
    }
