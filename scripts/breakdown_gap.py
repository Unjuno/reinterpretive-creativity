def breakdown_gap(target, winner):
    target_breakdown = target['breakdown']
    winner_breakdown = winner['breakdown']
    return {
        'distance_gap': winner_breakdown['distance'] - target_breakdown['distance'],
        'preservation_gap': winner_breakdown['preservation'] - target_breakdown['preservation'],
        'utility_proxy_gap': winner_breakdown['utility_proxy'] - target_breakdown['utility_proxy'],
        'score_gap': winner_breakdown['score'] - target_breakdown['score'],
    }
