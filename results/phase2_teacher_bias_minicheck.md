# Phase 2 teacher-model bias minicheck

## Status

This is a minimal Phase 2 teacher-model comparison.

It is not a full empirical phase, and it does not complete teacher-model bias inspection.

The purpose is narrower: compare the fixed cycle teacher and the existing single-positive-edge random-teacher smoke under matched small conditions.

## Matched condition

| Dimension | Level |
| --- | --- |
| seed range | `0, 1, 2` |
| graph size | `node_count=4` |
| candidate_limit | `20` |
| teacher models | fixed cycle teacher; single-positive-edge random-teacher smoke |
| methods | random_repair, random_search, local_repair, reinterpretation |

## Scores by seed

| teacher_model | seed | random_repair | random_search | local_repair | reinterpretation |
| --- | ---: | ---: | ---: | ---: | ---: |
| fixed_cycle | 0 | 0.072917 | 0.447917 | 0.163542 | 0.240625 |
| fixed_cycle | 1 | 0.104167 | 0.713542 | 0.208333 | 0.481250 |
| fixed_cycle | 2 | 0.275000 | 0.403125 | 0.343750 | 0.401042 |
| random_single_positive_edge | 0 | 0.000000 | 0.604688 | 0.145833 | 0.121875 |
| random_single_positive_edge | 1 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| random_single_positive_edge | 2 | 0.000000 | 0.744792 | 0.145833 | 0.243750 |

## Mean scores

| teacher_model | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean |
| --- | ---: | ---: | ---: | ---: |
| fixed_cycle | 0.150694 | 0.521528 | 0.238542 | 0.374306 |
| random_single_positive_edge | 0.000000 | 0.449826 | 0.097222 | 0.121875 |

## Mean deltas: random_single_positive_edge minus fixed_cycle

| method | delta |
| --- | ---: |
| random_repair | -0.150694 |
| random_search | -0.071701 |
| local_repair | -0.141319 |
| reinterpretation | -0.252431 |

## Reading

Under this small matched condition, the single-positive-edge random-teacher smoke lowers the mean score of every method relative to the fixed cycle teacher.

The largest mean drop is for reinterpretation.

This suggests that teacher construction can materially affect the observed score pattern, so teacher-model bias remains a live issue.

However, this is only a minicheck:

- seed count is only 3,
- the random-teacher implementation is still a smoke generator, not a general random graph teacher,
- the result does not establish a stable teacher-model effect,
- the result does not close the full empirical phase.

## Interpretation constraints

- `utility_proxy` remains a structural proxy, not human value.
- The comparison is descriptive.
- The comparison does not prove or disprove creativity.
- The comparison does not complete teacher-model bias inspection.

## Next work

A stronger teacher-model bias inspection should use:

- a general random graph teacher generator,
- matched fixed/random teacher suites over a larger seed range,
- median and win/loss counts, not only means,
- score breakdown gap reporting,
- the same output schema used by the other Phase 2 result files.
