from scripts.gap_report import gap_report
from scripts.random_teacher_batch_smoke import run_batch


def build_report(seeds=range(3), limit=20, method='reinterpretation', case_limit=3):
    rows = run_batch(seeds, limit)
    return gap_report(rows, method, case_limit)
