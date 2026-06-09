# Closure Criteria

This document defines what counts as sufficient closure for the current phase of the reinterpretive creativity model.

Closure does not mean proving creativity in general. It means reaching a stable, limited research model with explicit definitions, assumptions, tests, and remaining uncertainties.

## Current definitions

The current model defines:

- a world model as a signed directed graph,
- inconsistency as structural conflict inside that graph,
- repair as inconsistency reduction that stays close to the starting model,
- reinterpretation as search for a coherent, different alternative model evaluated by structural proxy measures,
- score components as diagnostic measurements,
- success, failure, and neutral outcomes relative to baselines and metrics.

These definitions are sufficient for the current artificial graph experiments.

## What remains unknown

The current model does not yet settle:

- which graph conditions make reinterpretation outperform local repair,
- which score components dominate reinterpretation wins or losses,
- how sensitive results are to seed, candidate limit, and teacher-model construction,
- whether the utility proxy is too strong, too weak, or misaligned,
- whether some apparent reinterpretation wins are artifacts of the scoring rule,
- how far the graph model can be generalized beyond the current simulation setting.

These unknowns are part of the research target, not defects to hide.

## Minimum closure for this phase

This phase can be considered closed when the project has:

1. A stable model core document.
2. A stable formal assumptions document.
3. A defined experiment matrix for seeds, node counts, candidate limits, and teacher-model variants.
4. A baseline comparison table covering reinterpretation, local repair, random search, and simple repair.
5. A loss-case analysis showing where reinterpretation fails.
6. A breakdown analysis showing which score components explain observed gaps as measurement material.
7. A written statement of non-claims and remaining uncertainties.

## Not required for closure

The following are not required for this phase:

- proving creativity itself,
- modeling human value judgment,
- generating natural-language causal explanations,
- showing that reinterpretation always wins,
- building a polished CLI or user-facing interface,
- generalizing beyond the artificial graph setting.

## Next required document

The next central document should be an experiment matrix.

It should specify which parameters are varied, which metrics are observed, and what outcomes count as support, failure, or uncertainty.

Until that matrix exists, the model is defined but not yet empirically closed.
