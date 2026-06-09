from scripts.random_teacher_reinterpretation_gap import run_smoke_with_reinterpretation_gap


def attach_reinterpretation_breakdown_gap(report, trial_limit=20):
    return {
        **report,
        "cases": [
            {
                **case,
                "reinterpretation_breakdown_gap": run_smoke_with_reinterpretation_gap(
                    seed=case["seed"],
                    limit=trial_limit,
                )["reinterpretation_breakdown_gap"],
            }
            for case in report["cases"]
        ],
    }
