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
