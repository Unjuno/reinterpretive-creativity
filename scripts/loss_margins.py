def loss_margins(rows, method='reinterpretation'):
    out = []
    for row in rows:
        scores = row['scores']
        best = max(scores, key=scores.get)
        margin = scores[best] - scores[method]
        if margin > 0:
            out.append({'seed': row['seed'], 'best_method': best, 'margin': margin})
    return out
