# Phase 2 mini-start: candidate_limit sensitivity

## Scope

This is a small post-Phase-1 additional check. It does not reopen Phase 1 and does not complete a full empirical phase.

The experiment measures score changes on a limited artificial signed-graph model. `utility_proxy` is a structural proxy, not a human value judgment.

## Conditions

- node_count: `3, 4`
- candidate_limit: `10, 20, 50, 100, 200, 500`
- trials per condition: `30`
- methods: `random_repair`, `random_search`, `local_repair`, `reinterpretation`

## Summary

| candidate_limit | node_count | trials | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean | tied_win_rate | strict_win_rate | loss_count | Δ vs random_search | Δ vs local_repair |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 3 | 30 | 0.2255 | 0.4736 | 0.4530 | 0.7231 | 100.00% | 90.00% | 0 | 0.2495 | 0.2702 |
| 10 | 4 | 30 | 0.2163 | 0.3706 | 0.3392 | 0.3956 | 46.67% | 36.67% | 16 | 0.0251 | 0.0564 |
| 20 | 3 | 30 | 0.2255 | 0.5478 | 0.5972 | 0.7231 | 100.00% | 63.33% | 0 | 0.1754 | 0.1259 |
| 20 | 4 | 30 | 0.2163 | 0.4366 | 0.3416 | 0.4368 | 50.00% | 46.67% | 15 | 0.0002 | 0.0952 |
| 50 | 3 | 30 | 0.2255 | 0.6323 | 0.7231 | 0.7231 | 100.00% | 0.00% | 0 | 0.0908 | 0.0000 |
| 50 | 4 | 30 | 0.2163 | 0.5123 | 0.4584 | 0.4552 | 13.33% | 13.33% | 26 | -0.0571 | -0.0032 |
| 100 | 3 | 30 | 0.2255 | 0.6828 | 0.7231 | 0.7231 | 100.00% | 0.00% | 0 | 0.0403 | 0.0000 |
| 100 | 4 | 30 | 0.2163 | 0.5519 | 0.6151 | 0.4736 | 0.00% | 0.00% | 30 | -0.0782 | -0.1414 |
| 200 | 3 | 30 | 0.2255 | 0.7165 | 0.7231 | 0.7231 | 100.00% | 0.00% | 0 | 0.0066 | 0.0000 |
| 200 | 4 | 30 | 0.2163 | 0.5853 | 0.7519 | 0.4903 | 0.00% | 0.00% | 30 | -0.0950 | -0.2616 |
| 500 | 3 | 30 | 0.2255 | 0.7231 | 0.7231 | 0.7231 | 100.00% | 0.00% | 0 | 0.0000 | 0.0000 |
| 500 | 4 | 30 | 0.2163 | 0.6157 | 0.7519 | 0.5189 | 0.00% | 0.00% | 30 | -0.0967 | -0.2329 |

## Reading

- node_count=3: reinterpretation_mean stayed at `0.7231` from candidate_limit 10 through 500. This happens because the current implementation uses exhaustive candidates when edge count is small enough, so candidate_limit does not bind this condition.
- node_count=4: reinterpretation_mean rose from `0.3956` at candidate_limit 10 to `0.5189` at candidate_limit 500; the change is `0.1233`.
- node_count=4 also shows stronger baseline pressure as candidate_limit increases. At candidate_limit 50 and above, reinterpretation loses frequently against random_search and/or local_repair under this structural proxy.
- This should be read as a condition-specific score pattern, not as evidence that reinterpretation search is or is not creativity.

## Files

- `results/phase2_candidate_limit_sensitivity.csv`
- `results/phase2_candidate_limit_sensitivity.json`
