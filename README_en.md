# Reinterpretive Creativity Model

This repository contains a small formal model and simulation suite for studying a limited form of **reinterpretive creativity**.

The project does not attempt to explain creativity in general. It studies a narrow structural case: an internally inconsistent artificial world model is transformed into a coherent and different alternative model, and that alternative is evaluated by explicit structural proxy measures.

## Core idea

A reinterpretive-creativity candidate is treated as a case where:

1. the initial model has internal inconsistency,
2. the reinterpreted model is internally coherent,
3. the reinterpreted model differs from the initial model,
4. the reinterpreted model is evaluated by explicit structural proxies.

In the current implementation, world models are represented as signed directed graphs.

## What this repository does not claim

This repository does not claim that:

- it proves human creativity,
- it explains creativity in general,
- simulation alone establishes creativity,
- `utility_proxy` measures human value,
- the model captures social, aesthetic, or scientific value,
- reinterpretation is always superior to random or local repair baselines,
- the full empirical phase is complete.

The project is intentionally limited. Its value is in making a small set of structural assumptions explicit and testable.

## Current status

Phase 1 is closed for the current scope.

Phase 2 has reached an interim analysis point. The repository now records:

- candidate-limit sensitivity,
- loss-case analysis,
- breakdown analysis,
- teacher-model bias checks,
- a general random graph teacher suite,
- preservation / novelty tradeoff notes,
- utility-proxy comparison minicheck,
- noise-pattern minicheck,
- cross-cutting analysis observations,
- an interpretive note separated from the empirical claims,
- an interim Phase 2 summary.

The full empirical phase remains deferred.

## Main empirical reading

The current results support only a bounded structural signal.

Reinterpretation search can produce competitive structural-proxy scores under some conditions, but it is sensitive to:

- candidate limit,
- graph size,
- teacher-model construction,
- raw-model size and density,
- noise pattern,
- preservation / novelty tradeoffs,
- baseline search strength.

A recurring pattern is that reinterpretation can preserve acquired structure well, while still losing total score when novelty distance is insufficient under the current score function.

## Interpretive reading

The repository also contains a separate speculative note on authority, diversity, and reinterpretation.

That note is not an empirical conclusion. It is a philosophical reading inspired by the results. It treats fixed teacher structure as locally useful for preserving acquired structure, while diversity and randomness can broaden the search space beyond a local threshold.

This interpretive reading should not be used as evidence for claims about human communities or human creativity.

## Running the code

The project uses Python standard-library tooling.

```bash
python scripts/simulate.py
python scripts/run_experiments.py --nodes 3,4,5 --trials 10 --candidate-limit 200
python scripts/explain_trial.py --seed 0 --node-count 4 --candidate-limit 100 --output results/local_explain_trial.md --json results/local_explain_trial.json
python scripts/select_cases.py --nodes 3,4,5 --trials 10 --candidate-limit 200 --output results/representative_cases.md --json results/representative_cases.json --logs-dir results/representative_cases
python -m unittest discover -s tests
```

## Key documents

- [`README.md`](README.md): Japanese overview.
- [`docs/model_core.md`](docs/model_core.md): current model core.
- [`docs/formal_assumptions.md`](docs/formal_assumptions.md): formal assumptions.
- [`docs/experiment_matrix.md`](docs/experiment_matrix.md): experiment matrix and recorded checks.
- [`docs/phase1_closure_summary_en.md`](docs/phase1_closure_summary_en.md): Phase 1 closure summary in English.
- [`docs/phase2_analysis_observations.md`](docs/phase2_analysis_observations.md): cross-cutting Phase 2 analysis observations.
- [`docs/phase2_interpretive_note.md`](docs/phase2_interpretive_note.md): speculative interpretive note.
- [`docs/phase2_interim_summary.md`](docs/phase2_interim_summary.md): Phase 2 interim summary.

## License

MIT License.
