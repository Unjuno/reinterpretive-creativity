from scripts.loss_margins import loss_margins


def top_losses(rows, method='reinterpretation', limit=3):
    losses = loss_margins(rows, method)
    return sorted(losses, key=lambda x: x['margin'], reverse=True)[:limit]
