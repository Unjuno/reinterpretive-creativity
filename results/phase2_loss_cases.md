# Phase 2 mini-start: loss-case analysis

## Scope

対象は `reinterpretation` が `random_search` または `local_repair` より低い structural proxy score を出したケースである。

ここでは Phase 1 closure の最小実験で重要だった `node_count=4`, `candidate_limit=50`, `trials=30` を中心に読む。

## Loss extraction

- condition: `node_count=4`, `candidate_limit=50`, `trials=30`
- loss definition: `reinterpretation_score < max(random_search_score, local_repair_score)`
- loss_count: `26` / `30`
- best local-or-random method among losses: `random_search=19`, `local_repair=7`

## Representative loss cases

| seed | best_local_or_random | random_repair | random_search | local_repair | reinterpretation | loss_margin |
|---:|---|---:|---:|---:|---:|---:|
| 1 | random_search | 0.1042 | 0.7448 | 0.3646 | 0.4812 | 0.2635 |
| 20 | random_search | 0.0760 | 0.6703 | 0.3271 | 0.4089 | 0.2615 |
| 14 | random_search | 0.0729 | 0.6719 | 0.4812 | 0.4266 | 0.2453 |
| 18 | random_search | 0.2094 | 0.8021 | 0.5724 | 0.5615 | 0.2406 |
| 19 | random_search | 0.1604 | 0.5990 | 0.4812 | 0.4010 | 0.1979 |
| 25 | random_search | 0.2792 | 0.6047 | 0.4469 | 0.4469 | 0.1578 |

## Structural-proxy reading of representative cases

### seed 1

- best local-or-random method: `random_search`
- score gap over reinterpretation: `0.2635`

| component | reinterpretation | random_search | local_repair |
|---|---:|---:|---:|
| novelty_distance | 0.5000 | 0.8333 | 0.4167 |
| preservation | 1.0000 | 1.0000 | 1.0000 |
| utility_proxy | 0.9625 | 0.8937 | 0.8750 |
| density_score | 1.0000 | 0.7500 | 0.7500 |
| node_coverage_score | 1.0000 | 1.0000 | 1.0000 |
| weak_connectivity_score | 1.0000 | 1.0000 | 1.0000 |
| in_out_coverage_score | 0.7500 | 0.8750 | 0.7500 |

Reading: in this case, `random_search` is higher on `novelty_distance` by `0.3333`. This is an observed component difference, not a causal claim.

### seed 20

- best local-or-random method: `random_search`
- score gap over reinterpretation: `0.2615`

| component | reinterpretation | random_search | local_repair |
|---|---:|---:|---:|
| novelty_distance | 0.4167 | 0.7500 | 0.3333 |
| preservation | 1.0000 | 1.0000 | 1.0000 |
| utility_proxy | 0.9812 | 0.8937 | 0.9812 |
| density_score | 1.0000 | 0.7500 | 1.0000 |
| node_coverage_score | 1.0000 | 1.0000 | 1.0000 |
| weak_connectivity_score | 1.0000 | 1.0000 | 1.0000 |
| in_out_coverage_score | 0.8750 | 0.8750 | 0.8750 |

Reading: in this case, `random_search` is higher on `novelty_distance` by `0.3333`. This is an observed component difference, not a causal claim.

### seed 14

- best local-or-random method: `random_search`
- score gap over reinterpretation: `0.2453`

| component | reinterpretation | random_search | local_repair |
|---|---:|---:|---:|
| novelty_distance | 0.5833 | 0.8333 | 0.5000 |
| preservation | 1.0000 | 1.0000 | 1.0000 |
| utility_proxy | 0.7312 | 0.8063 | 0.9625 |
| density_score | 0.7500 | 0.5000 | 1.0000 |
| node_coverage_score | 0.7500 | 1.0000 | 1.0000 |
| weak_connectivity_score | 0.7500 | 1.0000 | 1.0000 |
| in_out_coverage_score | 0.6250 | 0.8750 | 0.7500 |

Reading: in this case, `random_search` is higher on `novelty_distance` by `0.2500`. This is an observed component difference, not a causal claim.

### seed 18

- best local-or-random method: `random_search`
- score gap over reinterpretation: `0.2406`

| component | reinterpretation | random_search | local_repair |
|---|---:|---:|---:|
| novelty_distance | 0.5833 | 0.8333 | 0.5833 |
| preservation | 1.0000 | 1.0000 | 1.0000 |
| utility_proxy | 0.9625 | 0.9625 | 0.9812 |
| density_score | 1.0000 | 1.0000 | 1.0000 |
| node_coverage_score | 1.0000 | 1.0000 | 1.0000 |
| weak_connectivity_score | 1.0000 | 1.0000 | 1.0000 |
| in_out_coverage_score | 0.7500 | 0.7500 | 0.8750 |

Reading: in this case, `random_search` is higher on `novelty_distance` by `0.2500`. This is an observed component difference, not a causal claim.

## Notes

- `novelty_distance`, `preservation`, and `utility_proxy` multiply into `total_score`; a lower value in one component can offset higher values elsewhere.
- In the selected loss cases, `random_search` often reaches larger `novelty_distance` while maintaining enough `utility_proxy` to score higher.
- These are structural proxy observations under this setup only.

## Files

- `results/phase2_loss_cases.csv`
- `results/phase2_loss_cases.json`
