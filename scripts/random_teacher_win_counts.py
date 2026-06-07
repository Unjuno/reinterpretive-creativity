def win_counts(rows):
    counts = {method: 0 for method in rows[0]['scores']}
    for row in rows:
        best = max(row['scores'], key=row['scores'].get)
        counts[best] += 1
    return counts
