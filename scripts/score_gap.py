def score_gap(row, method='reinterpretation'):
    scores = row['scores']
    best = max(scores, key=scores.get)
    method_score = scores[method]
    best_score = scores[best]
    return {
        'seed': row['seed'],
        'method': method,
        'method_score': method_score,
        'best_method': best,
        'best_score': best_score,
        'gap': best_score - method_score,
    }
