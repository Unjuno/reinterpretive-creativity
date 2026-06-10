# Phase 2 preservation/novelty tradeoff note

## Status

This note organizes the preservation/novelty tradeoff visible in the existing Phase 2 mini-start breakdown results.

It does not introduce a new experiment, a new score function, or a new claim about creativity.

## Score relation

The current structural proxy score is multiplicative:

```text
score = novelty_distance * preservation * utility_proxy
```

This means a higher preservation value cannot by itself guarantee a higher total score. A large novelty-distance gap can dominate the product even when preservation is higher.

## Source material

This note relies on the existing Phase 2 breakdown analysis:

- `results/phase2_breakdown_analysis.md`
- `results/phase2_breakdown_analysis.csv`
- `results/phase2_breakdown_analysis.json`

No new script was added.

## Key observed groups

| group | novelty_delta | preservation_delta | utility_proxy_delta | total_score_delta | reading |
| --- | ---: | ---: | ---: | ---: | --- |
| reinterpretation_tied_win_all | 0.0172 | 0.0206 | 0.0193 | 0.0461 | Reinterpretation has slightly higher novelty, preservation, and utility proxy. |
| reinterpretation_strict_win_all | 0.0489 | 0.0584 | 0.0547 | 0.1310 | Strict wins show positive deltas across all three score factors. |
| reinterpretation_loss_all | -0.2103 | 0.0408 | -0.0157 | -0.1688 | Higher preservation does not offset the novelty-distance deficit. |
| n4_limit50_reinterpretation_loss_all | -0.2051 | 0.0795 | 0.0387 | -0.0959 | Even higher preservation and utility proxy do not offset the novelty-distance deficit. |

Deltas are `reinterpretation_mean - best_baseline_mean`.

## Main interpretation

The existing Phase 2 results show two different regimes.

### Win regime

In the tied-win and strict-win aggregates, reinterpretation has positive deltas for:

- novelty_distance,
- preservation,
- utility_proxy,
- total_score.

This is the cleanest regime for the current score design: reinterpretation does not need to trade preservation against novelty because all three score factors move in the same direction.

### Loss regime

In the aggregate loss group, reinterpretation has:

- lower novelty_distance,
- higher preservation,
- slightly lower utility_proxy,
- lower total_score.

In the focused `node_count=4`, `candidate_limit=50` loss group, reinterpretation has:

- lower novelty_distance,
- higher preservation,
- higher utility_proxy,
- lower total_score.

This focused group is the clearest preservation/novelty tradeoff signal in the current result set. Reinterpretation preserves more of the initial raw structure and scores better on utility_proxy, but still loses because the novelty-distance deficit is large under the multiplicative score.

## Consequence for interpretation

These results should not be read as showing that preservation is bad or that novelty is always better.

They show a narrower structural fact: under the current multiplicative proxy, preservation helps only when novelty_distance and utility_proxy remain sufficiently high. Preservation cannot compensate indefinitely for low novelty_distance.

## What this does not show

This note does not show:

- that reinterpretation search is creativity,
- that novelty is more important than preservation in human judgment,
- that the current score weights are correct,
- that the tradeoff is stable across teacher models,
- that the full empirical phase is closed.

## Follow-up work

The next useful step is not to change the score immediately. The next useful step is to compare alternative utility_proxy or score-composition variants while keeping the same cases fixed.

That would separate two questions:

1. whether the observed loss pattern is robust across scoring variants,
2. whether the current multiplicative composition over-penalizes lower novelty_distance in preservation-heavy candidates.
