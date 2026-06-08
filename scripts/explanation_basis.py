def explanation_basis(gap):
    return {
        'seed': gap['seed'],
        'method': gap['method'],
        'claim': 'target_method_lost' if gap['gap'] > 0 else 'target_method_not_lost',
        'basis': 'score_gap',
        'value': gap['gap'],
        'note': 'This is an explanation basis, not a causal reason.',
    }
