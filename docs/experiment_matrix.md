# Experiment Matrix

This document defines the experiment matrix for the empirical phase of the reinterpretive creativity model.

An experiment matrix specifies what varies, what is measured, and how outcomes are interpreted. It is not a user interface or a CLI feature.

## Purpose

The purpose is to test when reinterpretation search helps, when it fails, and which measured score components account for the observed gaps.

The experiment does not aim to prove creativity in general.

## Core questions

Q1. Under which graph conditions does reinterpretation outperform local repair?

Q2. Under which conditions does local repair, random search, or simple repair outperform reinterpretation?

Q3. Are wins and losses mainly explained by distance, preservation, utility proxy, or aggregate score?

Q4. How sensitive are results to seed, trial limit, candidate limit, and teacher-model construction?

Q5. Are apparent wins stable, or are they artifacts of the scoring rule or experimental setup?

## Methods to compare

The minimum comparison set is:

- simple repair or random repair,
- random search,
- local repair,
- reinterpretation search.

No method is assumed to be the true winner in advance.

## Matrix dimensions

The full empirical matrix should vary the following dimensions.

| Dimension | Minimal levels | Purpose |
| --- | --- | --- |
| seed range | 0-29 | Check random-seed sensitivity. |
| trial limit | 20, 50 | Check whether results change with more trials. |
| graph size | current default, larger variant | Check whether structure size changes outcomes. |
| candidate limit | current default, lower, higher | Check whether reinterpretation depends on search budget. |
| teacher model | fixed teacher, random teacher | Check whether results depend on the reference model. |

If a dimension is not yet exposed by code, it should be marked as a required implementation hook rather than silently ignored.

## Metrics

Each condition should record:

- win count by method,
- mean and median score by method,
- loss cases for reinterpretation,
- score gap between reinterpretation and the winning method,
- breakdown gaps for distance, preservation, utility proxy, and aggregate score.

Breakdown gaps are measurement material. They are not causal explanations.

## Outcome interpretation

A condition supports the model when reinterpretation outperforms baselines and the result is stable across seeds and reasonable parameter changes.

A condition weakens the model when reinterpretation repeatedly loses in settings where it was expected to help.

A condition is uncertain when differences are small, unstable, or dominated by artifacts such as score design, candidate-limit effects, or teacher-model bias.

## Minimum executable phase

The first executable phase should not cover every combination.

It should run:

1. A small smoke matrix using a few seeds and the current default graph settings.
2. A baseline matrix comparing all methods over a larger seed range.
3. A loss-case extraction for reinterpretation failures.
4. A breakdown-gap report for selected cases when available.

This is enough to decide whether the model has bounded empirical traction before expanding the matrix.

## Phase 2 mini-start execution

A small Phase 2 mini-start has now been run as an additional post-Phase-1 check, not as full empirical phase closure.

Executed conditions:

| Dimension | Executed levels |
| --- | --- |
| seed range | 0-29 |
| trial count | 30 per condition |
| graph size | node_count 3, 4 |
| candidate_limit | 10, 20, 50, 100, 200, 500 |
| methods | random_repair, random_search, local_repair, reinterpretation |

Recorded outputs:

- `results/phase2_candidate_limit_sensitivity.md`
- `results/phase2_candidate_limit_sensitivity.csv`
- `results/phase2_candidate_limit_sensitivity.json`
- `results/phase2_loss_cases.md`
- `results/phase2_loss_cases.csv`
- `results/phase2_loss_cases.json`
- `results/phase2_breakdown_analysis.md`
- `results/phase2_breakdown_analysis.csv`
- `results/phase2_breakdown_analysis.json`
- `docs/phase2_mini_start_summary.md`

Interpretation constraints:

- This mini-start does not show that reinterpretation search is creativity.
- It only records how structural proxy scores change under the listed conditions.
- Breakdown differences are descriptive measurement results, not causal explanations.
- Phase 1 remains closed for the current scope.

## Phase 2 random-teacher smoke

A separate random-teacher smoke has been recorded in `results/phase2_random_teacher_smoke.md`.

Executed smoke condition:

| Dimension | Executed levels |
| --- | --- |
| seed range | 0-2 |
| trial count | 3 smoke seeds |
| graph size | node_count 4 |
| candidate_limit | 20 |
| teacher model | single-positive-edge random-teacher smoke |
| methods | random_repair, random_search, local_repair, reinterpretation |

Mean scores:

| method | mean_score |
| --- | ---: |
| random_repair | 0.000000 |
| random_search | 0.449826 |
| local_repair | 0.097222 |
| reinterpretation | 0.121875 |

Interpretation constraints:

- This smoke does not complete teacher-model bias inspection.
- The current random-teacher implementation is not yet a general random graph teacher generator.
- The result only positions the existing smoke path and records a minimal output.
- `utility_proxy` remains a structural proxy.

## Phase 2 teacher-model bias minicheck

A minimal teacher-model comparison has been recorded in `results/phase2_teacher_bias_minicheck.md`.

Executed minicheck condition:

| Dimension | Executed levels |
| --- | --- |
| seed range | 0-2 |
| trial count | 3 seeds per teacher model |
| graph size | node_count 4 |
| candidate_limit | 20 |
| teacher models | fixed cycle teacher; single-positive-edge random-teacher smoke |
| methods | random_repair, random_search, local_repair, reinterpretation |

Mean scores:

| teacher_model | random_repair_mean | random_search_mean | local_repair_mean | reinterpretation_mean |
| --- | ---: | ---: | ---: | ---: |
| fixed_cycle | 0.150694 | 0.521528 | 0.238542 | 0.374306 |
| random_single_positive_edge | 0.000000 | 0.449826 | 0.097222 | 0.121875 |

Interpretation constraints:

- This minicheck suggests teacher construction can materially affect the observed score pattern.
- It does not complete teacher-model bias inspection.
- It does not replace a larger fixed/random teacher suite.
- It does not close the full empirical phase.
- `utility_proxy` remains a structural proxy.

## Phase 2 preservation/novelty tradeoff note

A preservation/novelty tradeoff note has been recorded in `results/phase2_preservation_novelty_tradeoff.md`.

This note uses the existing Phase 2 breakdown analysis and does not add a new experiment or score function.

Key observed deltas:

| group | novelty_delta | preservation_delta | utility_proxy_delta | total_score_delta |
| --- | ---: | ---: | ---: | ---: |
| reinterpretation_tied_win_all | 0.0172 | 0.0206 | 0.0193 | 0.0461 |
| reinterpretation_strict_win_all | 0.0489 | 0.0584 | 0.0547 | 0.1310 |
| reinterpretation_loss_all | -0.2103 | 0.0408 | -0.0157 | -0.1688 |
| n4_limit50_reinterpretation_loss_all | -0.2051 | 0.0795 | 0.0387 | -0.0959 |

Interpretation constraints:

- This is a descriptive interpretation of existing breakdown measurements.
- It does not show that novelty is more important than preservation in human judgment.
- It does not change `utility_proxy` or the score function.
- It does not close the full empirical phase.

## Current-scope closure

A current-scope closure can be reached after a minimal experimental run, if the project can state:

- where reinterpretation scores well,
- where it loses or becomes unstable,
- which results remain unresolved,
- which assumptions or metrics need later revision.

This current-scope closure is weaker than a full empirical phase closure.

## Full empirical phase closure

The full empirical phase can close when the project can state, after broader matrix execution:

- where reinterpretation tends to win,
- where it tends to lose,
- which measured components dominate wins and losses,
- which results are unstable or likely artifacts,
- which assumptions need revision.

If these statements cannot be made after running the full matrix, the model remains empirically unresolved beyond the current scope.
