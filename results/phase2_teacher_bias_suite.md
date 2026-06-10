# Phase 2 teacher-model bias suite

## Status

This is a small Phase 2 teacher-model bias suite.

It extends the earlier teacher-model minicheck, but it still does not complete teacher-model bias inspection.

The random teacher is still the existing single-positive-edge smoke generator, not a general random graph teacher generator.

## Existing implementation used

The fixed teacher is the existing fixed cycle teacher.

The random teacher uses the existing `build_random_teacher(node_count=4, seed=seed)` implementation, which sets exactly one randomly chosen directed edge to `1` and all other directed edges to `0`.

The random-teacher raw model uses the existing `make_noisy_raw_from_teacher`, which creates `{1}` or `{1, -1}` for teacher-positive edges.

## Matched condition

| Dimension | Level |
| --- | --- |
| seed range | `0-29` |
| trial count | `30` per condition |
| graph size | `node_count=4` |
| candidate_limit | `20`, `50` |
| teacher models | fixed_cycle; random_single_positive_edge |
| methods | random_repair, random_search, local_repair, reinterpretation |

## Summary results

| teacher_model | candidate_limit | avg_raw_edges | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean | tied_win_rate | strict_win_rate | loss_count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_cycle | 20 | 5.966667 | 0.216319 | 0.436625 | 0.341649 | 0.436822 | 0.500000 | 0.466667 | 15 |
| random_single_positive_edge | 20 | 1.000000 | 0.000000 | 0.332830 | 0.071319 | 0.148194 | 0.500000 | 0.000000 | 15 |
| fixed_cycle | 50 | 5.966667 | 0.216319 | 0.512251 | 0.458421 | 0.455181 | 0.133333 | 0.133333 | 26 |
| random_single_positive_edge | 50 | 1.000000 | 0.000000 | 0.356597 | 0.152257 | 0.181997 | 0.500000 | 0.000000 | 15 |

## Mean deltas: random_single_positive_edge minus fixed_cycle

| candidate_limit | random_repair_delta | random_search_delta | local_repair_delta | reinterpretation_delta |
| ---: | ---: | ---: | ---: | ---: |
| 20 | -0.216319 | -0.103795 | -0.270330 | -0.288627 |
| 50 | -0.216319 | -0.155654 | -0.306164 | -0.273185 |

## Reading

Under this small suite, the existing random single-positive-edge teacher lowers the mean score of every method relative to the fixed cycle teacher.

The mean drop for reinterpretation is large under both tested candidate limits:

- `-0.288627` at `candidate_limit=20`
- `-0.273185` at `candidate_limit=50`

However, the comparison has a structural confound: the random single-positive-edge teacher produces much smaller raw models. Its average raw-edge count is `1.000000`, while the fixed-cycle condition has average raw-edge count `5.966667`.

Therefore, this suite supports the claim that teacher construction materially affects observed structural-proxy scores, but it does not isolate teacher-model bias cleanly.

## Interpretation constraints

This suite does not show that the fixed teacher is better or worse as a model of any real teacher.

It does not show that the random teacher is more realistic.

It does not prove or disprove creativity.

It does not include human value, social value, aesthetic value, or scientific value.

It does not close the full empirical phase.

## Next work

A fuller teacher-model bias inspection should use:

- a general random graph teacher generator,
- fixed and random teacher suites with comparable raw-edge counts,
- multiple graph sizes,
- multiple candidate_limit values,
- per-condition median and win/loss counts,
- breakdown-gap reporting for selected wins and losses.
