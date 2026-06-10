# Phase 2 noise-pattern minicheck

## Status

This is a small Phase 2 minicheck over the existing noise parameters in `noisy_case`.

It does not add a new noise generator, does not change the score function, and does not close the full empirical phase.

## Existing implementation used

The existing `noisy_case` function exposes two noise parameters:

- `conflict_rate`: probability of adding `-1` to a teacher-positive edge already containing `{1}`.
- `extra_positive_rate`: probability of adding `{1}` to a teacher-nonpositive edge.

The implementation also ensures that at least one conflict exists in the raw model.

## Matched condition

| Dimension | Level |
| --- | --- |
| seed range | `0-29` |
| trial count | `30` per pattern |
| graph size | `node_count=4` |
| candidate_limit | `50` |
| teacher model | fixed cycle teacher |
| methods | random_repair, random_search, local_repair, reinterpretation |

## Noise patterns

| noise_pattern | conflict_rate | extra_positive_rate | reading |
| --- | ---: | ---: | --- |
| baseline_current | 0.35 | 0.25 | current default setting |
| conflict_light | 0.10 | 0.25 | fewer teacher-positive conflicts |
| conflict_heavy | 0.70 | 0.25 | more teacher-positive conflicts |
| extra_positive_light | 0.35 | 0.05 | fewer extra positives on non-teacher edges |
| extra_positive_heavy | 0.35 | 0.60 | more extra positives on non-teacher edges |
| combined_high_noise | 0.70 | 0.60 | high conflict and high extra-positive noise |

## Summary results

| noise_pattern | avg_raw_edges | avg_conflict_edges | avg_singleton_positive_edges | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean | tied_win_rate | strict_win_rate | loss_count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_current | 5.966667 | 1.800000 | 4.166667 | 0.216319 | 0.512251 | 0.458421 | 0.455181 | 0.133333 | 0.133333 | 26 |
| conflict_light | 5.966667 | 1.033333 | 4.933333 | 0.182031 | 0.460562 | 0.390259 | 0.400409 | 0.166667 | 0.133333 | 25 |
| conflict_heavy | 5.966667 | 3.166667 | 2.800000 | 0.267622 | 0.591386 | 0.546642 | 0.531181 | 0.166667 | 0.100000 | 25 |
| extra_positive_light | 4.300000 | 1.800000 | 2.500000 | 0.103600 | 0.537578 | 0.366073 | 0.405981 | 0.066667 | 0.033333 | 28 |
| extra_positive_heavy | 8.700000 | 1.800000 | 6.900000 | 0.339549 | 0.441920 | 0.529257 | 0.509525 | 0.333333 | 0.166667 | 20 |
| combined_high_noise | 8.700000 | 3.166667 | 5.533333 | 0.434236 | 0.527893 | 0.685429 | 0.611583 | 0.100000 | 0.033333 | 27 |

## Reading

Under this small matched condition, changing the existing noise parameters materially changes the observed score pattern.

The highest reinterpretation mean appears in the `combined_high_noise` pattern, but local_repair is stronger there and reinterpretation still loses in 27 of 30 trials.

The highest tied-win rate appears in the `extra_positive_heavy` pattern, where reinterpretation ties or beats the strongest baseline in 10 of 30 trials.

The `extra_positive_light` pattern is the weakest for reinterpretation by win rate: reinterpretation loses in 28 of 30 trials.

## Interpretation constraints

These are structural proxy outcomes under a small fixed setting.

They do not show that any noise pattern is more realistic.

They do not show human creativity, human value, social value, aesthetic value, or scientific value.

They do not close the full empirical phase.

## Next work

A fuller noise-pattern check should:

- include more graph sizes,
- include more candidate_limit values,
- record medians and win/loss counts,
- include teacher-model variants,
- include breakdown gaps for loss cases,
- keep `utility_proxy` explicitly structural.
