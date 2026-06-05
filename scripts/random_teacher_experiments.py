from random import Random
try:
    from scripts import run_experiments as e
    from scripts.random_teacher_smoke import build_random_teacher as b
except ModuleNotFoundError:
    import run_experiments as e
    from random_teacher_smoke import build_random_teacher as b


def make_noisy_raw_from_teacher(t, seed=0):
    r = Random(seed)
    raw = {}
    for k, v in t.items():
       