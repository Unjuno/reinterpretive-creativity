from scripts import run_experiments as e


def score_breakdown(candidate, teacher, raw):
    distance = e.distance(candidate, teacher)
    preservation = e.preservation(raw, candidate)
    utility = e.utility_proxy(candidate)
    return {
        'distance': distance,
        'preservation': preservation,
        'utility_proxy': utility,
        'score': distance * preservation * utility,
    }
