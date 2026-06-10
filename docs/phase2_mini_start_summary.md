# Phase 2 mini-start summary

## Status

Phase 2 mini-start has been run as an additional check after Phase 1 current-scope closure.

This does not revise the Phase 1 closure decision and does not complete a full empirical phase.

## Scope

The run uses the existing limited artificial signed-graph model.

It does not address:

- human creativity in general,
- social value,
- aesthetic value,
- scientific value,
- human value judgment.

`utility_proxy` remains a structural proxy.

## Conditions

- node_count: `3, 4`
- candidate_limit: `10, 20, 50, 100, 200, 500`
- trials per condition: `30`
- methods:
  - `random_repair`
  - `random_search`
  - `local_repair`
  - `reinterpretation`

## Main observations

### candidate_limit sensitivity

- node_count=3: `reinterpretation_mean` stayed at `0.7231` from candidate_limit 10 through 500.
- node_count=4: `reinterpretation_mean` changed from `0.3956` at candidate_limit 10 to `0.5189` at candidate_limit 500.
- node_count=4: stronger baselines also improved with larger candidate_limit, and reinterpretation lost to the strongest baseline in all 30 trials at candidate_limit 100, 200, and 500.

This means that candidate_limit improves the structural proxy score for reinterpretation in node_count=4, but it does not by itself make reinterpretation outperform the stronger baselines under this setup.

### loss-case analysis

Focused condition:

- node_count: `4`
- candidate_limit: `50`
- trials: `30`

Result:

- loss_count: `26 / 30`
- best local-or-random method among losses:
  - random_search: `19`
  - local_repair: `7`

Representative high-margin losses are listed in `results/phase2_loss_cases.md`.

### breakdown analysis

Across all loss cases in the mini-start grid, reinterpretation has lower mean `novelty_distance` than the strongest baseline, while mean `preservation` is higher.

For the focused `node_count=4`, `candidate_limit=50` loss group, reinterpretation has higher mean `utility_proxy` and `density_score` than the strongest baseline, but lower mean `novelty_distance`.

This is a descriptive component difference under this experiment condition. It is not a causal explanation.

## Output files

- `results/phase2_candidate_limit_sensitivity.md`
- `results/phase2_candidate_limit_sensitivity.csv`
- `results/phase2_candidate_limit_sensitivity.json`
- `results/phase2_loss_cases.md`
- `results/phase2_loss_cases.csv`
- `results/phase2_loss_cases.json`
- `results/phase2_breakdown_analysis.md`
- `results/phase2_breakdown_analysis.csv`
- `results/phase2_breakdown_analysis.json`

## Position

Phase 2 mini-start is an additional check after Phase 1 current-scope closure.

It is not a full empirical phase, and it should not be described as proving reinterpretation search to be creativity.
