# Phase 2 general random teacher suite

## Status

This is a Phase 2 teacher-model check using a generated random graph teacher.

It adds a general random directed graph teacher with a controlled positive-edge count.  The goal is to reduce the raw-size confound of the previous single-positive-edge random-teacher smoke path.

This is still not full empirical phase closure.

## Teacher models

| teacher_model | definition |
| --- | --- |
| fixed_cycle | existing fixed cycle teacher over `node_count=4` |
| random_graph_p4 | random directed graph teacher over `node_count=4` with `positive_edge_count=4` |

The fixed cycle teacher has four positive directed edges when `node_count=4`.  `random_graph_p4` therefore matches the fixed teacher's positive-edge count while randomizing which directed edges are positive.

## Matched condition

| Dimension | Level |
| --- | --- |
| seed range | `0-29` |
| trial count | `30` per condition |
| graph size | `node_count=4` |
| positive_edge_count | `4` for `random_graph_p4` |
| candidate_limit | `20`, `50`, `100` |
| teacher models | `fixed_cycle`, `random_graph_p4` |
| methods | random_repair, random_search, local_repair, reinterpretation |

## Summary results

| teacher_model | candidate_limit | avg_raw_edges | avg_conflict_edges | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean | tied_win_rate | strict_win_rate | loss_count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_cycle | 20 | 5.966667 | 1.800000 | 0.216319 | 0.436625 | 0.341649 | 0.436822 | 0.500000 | 0.466667 | 15 |
| random_graph_p4 | 20 | 6.133333 | 1.800000 | 0.227729 | 0.467412 | 0.342350 | 0.405450 | 0.300000 | 0.266667 | 21 |
| fixed_cycle | 50 | 5.966667 | 1.800000 | 0.216319 | 0.512251 | 0.458421 | 0.455181 | 0.133333 | 0.133333 | 26 |
| random_graph_p4 | 50 | 6.133333 | 1.800000 | 0.227729 | 0.498258 | 0.458051 | 0.435825 | 0.100000 | 0.100000 | 27 |
| fixed_cycle | 100 | 5.966667 | 1.800000 | 0.216319 | 0.609664 | 0.564679 | 0.473648 | 0.000000 | 0.000000 | 30 |
| random_graph_p4 | 100 | 6.133333 | 1.800000 | 0.227729 | 0.568497 | 0.557542 | 0.459629 | 0.000000 | 0.000000 | 30 |

## Reinterpretation mean deltas

`random_graph_p4 - fixed_cycle`:

| candidate_limit | reinterpretation_mean_delta |
| ---: | ---: |
| 20 | -0.031371 |
| 50 | -0.019357 |
| 100 | -0.014019 |

## Reading

The previous single-positive-edge random-teacher suite had a strong raw-size confound: the random teacher produced far fewer explicit raw edges than the fixed cycle teacher.

In this suite, `random_graph_p4` has an average raw-edge count of `6.133333`, close to the fixed cycle teacher's `5.966667`.  The large reinterpretation mean drop observed in the single-positive-edge smoke setting shrinks substantially under this more size-comparable random graph teacher.

This suggests that part of the earlier random-teacher drop came from the single-edge construction rather than from random teacher construction alone.

At the same time, reinterpretation still loses frequently against stronger baselines, especially at higher candidate limits.  At `candidate_limit=100`, reinterpretation has `loss_count=30` in both teacher conditions.

## Interpretation constraints

This suite does not show that the random graph teacher is realistic.

It does not show that the fixed cycle teacher is realistic.

It does not claim human creativity, human value, social value, aesthetic value, or scientific value.

It does not close the full empirical phase.

## Next work

A fuller teacher-model bias inspection would need:

- multiple positive-edge counts,
- multiple graph sizes,
- repeated random graph teacher families,
- candidate_limit and noise-pattern cross checks,
- breakdown-gap reporting for selected loss cases.
