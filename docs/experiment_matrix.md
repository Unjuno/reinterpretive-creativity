# Experiment Matrix

This document defines the minimum experiment matrix for the next phase of the reinterpretive creativity model.

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

- simple repair,
- random search,
- local repair,
- reinterpretation search.

No method is assumed to be the true winner in advance.

## Matrix dimensions

The minimum matrix should vary the following dimensions.

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
4. A breakdown-gap report for selected cases.

This is enough to decide whether the model has empirical traction before expanding the matrix.

## Closure condition for the experiment phase

The experiment phase can close when the project can state:

- where reinterpretation tends to win,
- where it tends to lose,
- which measured components dominate wins and losses,
- which results are unstable or likely artifacts,
- which assumptions need revision.

If these statements cannot be made after running the matrix, the model remains defined but empirically unresolved.
