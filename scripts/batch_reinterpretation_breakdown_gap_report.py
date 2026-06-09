from scripts.batch_gap_report import build_report
from scripts.report_reinterpretation_breakdown_gap import attach_reinterpretation_breakdown_gap


def build_reinterpretation_breakdown_gap_report(
    seeds=range(3),
    limit=20,
    method="reinterpretation",
    case_limit=3,
):
    report = build_report(seeds, limit, method, case_limit)
    return attach_reinterpretation_breakdown_gap(report, trial_limit=limit)
