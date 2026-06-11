# Phase 2 interim summary

## Status

This document is an interim summary of the Phase 2 work completed after Phase 1 current-scope closure.

It does not close the full empirical phase.

It records what has been inspected, what appears stable, what remains unresolved, and where a reasonable stop line can be drawn for the current repository.

## Phase 1 status

Phase 1 remains closed for the current scope.

The Phase 2 work below does not reopen Phase 1. It extends the project beyond the Phase 1 closure boundary by checking how the bounded signal behaves under additional experimental and interpretive pressure.

## Phase 2 work completed so far

The following Phase 2 items have been recorded:

- candidate_limit sensitivity,
- loss-case analysis,
- breakdown analysis,
- random-teacher smoke positioning,
- teacher-model bias minicheck,
- teacher-model bias suite,
- general random graph teacher suite,
- preservation / novelty tradeoff note,
- utility_proxy comparison minicheck,
- noise-pattern minicheck,
- cross-cutting analysis observations,
- interpretive note on authority, diversity, and reinterpretation.

## Main empirical observations

### 1. Reinterpretation has a bounded structural signal

The Phase 2 data does not show that reinterpretation is universally stronger than the baselines.

It does show that reinterpretation can produce competitive structural-proxy scores under some conditions, and that its wins and losses can be decomposed into measurable components.

This is the main bounded signal that remains credible.

### 2. Candidate limit is a first-class condition

Candidate-limit sensitivity is not an implementation detail.

As candidate limits increase, stronger baselines such as random search and local repair can find competitive or better candidates. In high-budget conditions, reinterpretation often loses to the strongest baseline.

This means future claims must specify candidate_limit rather than treating it as incidental.

### 3. Teacher construction matters, but the single-edge random teacher had a raw-size confound

The single-positive-edge random-teacher smoke produced a much smaller raw model than the fixed-cycle teacher. The large drop observed there should therefore not be read as clean teacher-model bias alone.

The later general random graph teacher suite added a positive-edge-count-controlled random graph teacher. This reduced the raw-size mismatch. Under that condition, the teacher-model difference became smaller.

This suggests that part of the earlier effect came from raw-model size and density rather than from randomness alone.

Teacher-model bias remains unresolved beyond this controlled small check.

### 4. Loss cases often involve preservation without enough novelty

The preservation / novelty tradeoff note suggests that reinterpretation can preserve more of the raw model while still losing total score.

In loss groups, preservation can be positive but novelty distance can be negative enough to pull down the multiplicative total score.

This means reinterpretation is not simply failing to preserve. Under the current score, it can be preservation-heavy and novelty-poor.

### 5. Utility_proxy variants do not immediately reverse the broad pattern

The utility_proxy comparison minicheck recombines existing group-level breakdown means under several proxy variants.

The broad win/loss structure is not immediately overturned by those tested variants.

However, this is not per-trial rescoring. It is not a full utility_proxy robustness validation.

### 6. Noise pattern changes both opportunity and risk

The noise-pattern minicheck shows that changing conflict and extra-positive rates affects reinterpretation scores and loss counts.

Noise can increase the room for reinterpretation, but it can also increase the room for baselines to find good alternatives. Higher absolute reinterpretation score is therefore not the same as stronger relative performance.

Noise-pattern robustness remains unresolved beyond the small fixed grid.

## Interpretive reading

A separate interpretive note records a speculative reading of the Phase 2 results.

That reading treats authority or fixed teacher structure as locally useful for preserving acquired structure. It then treats diversity or randomness as a possible source of broader search and reinterpretation beyond a local threshold.

This reading is philosophical and poetic. It is not an empirical conclusion of the model.

The empirical documents remain the source for what was measured.

## What can be claimed now

The project can currently claim the following, within the model:

- Phase 1 is closed for the current scope.
- Phase 2 has produced a useful interim analysis.
- Reinterpretation has a bounded structural-proxy signal.
- The signal is sensitive to candidate_limit, teacher construction, noise pattern, and score-component interactions.
- The project can decompose wins and losses into distance, preservation, utility_proxy, and aggregate score components.
- The previous single-positive-edge random-teacher result contained a raw-size confound.
- A positive-edge-count-controlled random graph teacher reduces that confound but does not close teacher-model bias inspection.

## What cannot be claimed

The project should not claim:

- that it proves human creativity,
- that `utility_proxy` measures human value,
- that the current model captures social, aesthetic, or scientific value,
- that reinterpretation is generally superior to all baselines,
- that teacher-model bias has been fully inspected,
- that noise-pattern robustness has been established,
- that utility_proxy robustness has been established,
- that the full empirical phase is complete.

## Remaining unresolved work

The following remain future work:

- full teacher-model bias inspection across graph sizes, positive-edge counts, and teacher families,
- full noise-pattern robustness inspection,
- per-trial utility_proxy rescoring under multiple variants,
- broader candidate-limit and graph-size matrix execution,
- stronger summary of representative win and loss cases,
- possible formal separation between preservation-heavy and novelty-heavy reinterpretation modes.

## Recommended stop line

A reasonable stop line for the current repository is now available:

1. Keep Phase 1 closed.
2. Treat the current Phase 2 material as an interim empirical analysis.
3. Do not claim full empirical phase closure.
4. Do not keep adding experimental grids unless a new full empirical phase is explicitly started.
5. Use the analysis observations and interpretive note as material for later writing, not as proof of external claims.

## Next phase, if opened

If a later phase is opened, it should be framed as a full empirical phase rather than another informal extension of Phase 2.

That phase should predefine:

- graph-size levels,
- teacher-model families,
- positive-edge-count levels,
- noise-pattern grid,
- candidate-limit grid,
- utility_proxy variants,
- primary outcome metrics,
- stop conditions.

Without that predefined matrix, further additions risk becoming exploratory sprawl.
