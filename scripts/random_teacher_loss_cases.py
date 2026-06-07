def loss_cases(rows, method='reinterpretation'):
    return [
        row for row in rows
        if row['scores'][method] < max(row['scores'].values())
    ]
