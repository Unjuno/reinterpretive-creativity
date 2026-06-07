from scripts.describe_gaps import describe_gaps


def gap_report(rows, method='reinterpretation', limit=3):
    return {
        'method': method,
        'limit': limit,
        'cases': describe_gaps(rows, method, limit),
    }
