from scripts.explanation_basis import explanation_basis


def attach_explanation_basis(report):
    return {
        **report,
        'explanation_basis': [
            explanation_basis(case) for case in report['cases']
        ],
    }
