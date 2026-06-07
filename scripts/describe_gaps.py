from scripts.score_gap import score_gap
from scripts.top_losses import top_losses


def describe_gaps(rows, method='reinterpretation', limit=3):
    seeds = {loss['seed'] for loss in top_losses(rows, method, limit)}
    return [score_gap(row, method) for row in rows if row['seed'] in seeds]
