# Phase 2 random-teacher smoke

## Status

This is a small Phase 2 mini-check using the existing random-teacher smoke scripts.

It is not a full empirical phase, and it is not a completed teacher-model bias inspection.

## Existing implementation used

The existing implementation is a **single-positive-edge random-teacher smoke**:

- `node_count`: `4`
- teacher construction: choose one directed edge by seed and set it to `1`; all other directed edges are `0`
- raw model construction: for each positive teacher edge, keep `{1}` or create `{1, -1}` by seed
- comparison methods:
  - `random_repair`
  - `random_search`
  - `local_repair`
  - `reinterpretation`
- candidate limit: `20`
- seeds: `0, 1, 2`

This uses the existing random-teacher smoke path rather than adding a new script.

## Scores

| seed | random_repair | random_search | local_repair | reinterpretation |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.000000 | 0.604688 | 0.145833 | 0.121875 |
| 1 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 2 | 0.000000 | 0.744792 | 0.145833 | 0.243750 |

## Mean scores

| method | mean_score |
| --- | ---: |
| random_repair | 0.000000 |
| random_search | 0.449826 |
| local_repair | 0.097222 |
| reinterpretation | 0.121875 |

## Reading

Under this very small smoke condition, random_search has the highest mean structural proxy score.

reinterpretation scores above local_repair on mean, but below random_search.

This is only a smoke result. It should not be read as evidence that reinterpretation generally wins or loses under random teacher models.

## Interpretation constraints

- `utility_proxy` remains a structural proxy, not human value.
- This result does not prove creativity.
- This result does not close the full empirical phase.
- This result does not complete teacher-model bias inspection.
- The current teacher generator is not yet a general random graph teacher generator.

## Next required work

To inspect teacher-model bias, the next step should compare fixed teacher and random teacher under matched conditions:

- same seed range,
- same node_count,
- same candidate_limit,
- same method set,
- same output schema,
- breakdown gap recording for wins and losses.
