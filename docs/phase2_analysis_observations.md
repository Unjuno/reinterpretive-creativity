# Phase 2 analysis observations

## Status

This note records cross-cutting observations from the Phase 2 checks that have already been run.

It is not a new experiment. It is an analysis note over existing Phase 2 result files and experiment-matrix entries.

It does not close the full empirical phase.

## Data inspected

The observations below rely on the following already-recorded Phase 2 outputs:

- `results/phase2_candidate_limit_sensitivity.md`
- `results/phase2_loss_cases.md`
- `results/phase2_breakdown_analysis.md`
- `results/phase2_teacher_bias_suite.md`
- `results/phase2_general_random_teacher_suite.md`
- `results/phase2_preservation_novelty_tradeoff.md`
- `results/phase2_utility_proxy_comparison.md`
- `results/phase2_noise_patterns.md`
- `docs/experiment_matrix.md`

## Stable observations

Several observations now recur across the Phase 2 material.

First, reinterpretation can produce a bounded structural-proxy signal, but the signal is condition-dependent. It is not uniformly dominant across stronger baselines.

Second, stronger baselines matter. Random search and local repair become hard competitors once candidate budgets increase. This is visible in the `node_count=4`, higher `candidate_limit` settings, where reinterpretation often loses to the strongest baseline.

Third, many apparent teacher-model differences must be read through raw-model size. The earlier single-positive-edge random-teacher smoke produced a much smaller raw model than the fixed-cycle teacher. The later `random_graph_p4` check reduced that raw-size mismatch and substantially shrank the observed reinterpretation mean drop.

Fourth, the preservation/novelty tradeoff appears central under the current score. Loss cases often preserve more than the baseline but lose enough novelty distance that the multiplicative total score falls behind.

Fifth, utility-proxy variant checks do not immediately reverse the broad win/loss pattern. This is only a group-mean recombination result, not a full per-trial robustness validation.

## Unstable observations

Several observations remain unstable or underdetermined.

Teacher-model effects are not yet fully isolated. The project now has both a single-positive-edge random teacher and a positive-edge-count-controlled random graph teacher, but not a full grid over random teacher families, graph sizes, and positive-edge counts.

Noise-pattern effects are suggestive but incomplete. The current noise-pattern minicheck varies `conflict_rate` and `extra_positive_rate` over a small fixed grid, using the fixed-cycle teacher only.

Utility-proxy robustness is not complete. The current comparison recombines group mean components. It does not recompute per-trial winners under each proxy variant.

Candidate-limit effects are strong enough that any claim based on a single candidate budget is fragile.

## Candidate-limit effects

The candidate-limit results suggest that reinterpretation is sensitive to search budget.

For small or moderate budgets, reinterpretation can tie or beat the strongest baseline in some conditions. As candidate limits increase, random search and local repair can improve enough to overtake reinterpretation.

In the general random graph teacher suite, `candidate_limit=100` gives `loss_count=30` for both `fixed_cycle` and `random_graph_p4`. This does not prove that reinterpretation is weak in all settings, but it shows that higher search budget can expose baseline strength.

Interpretation: candidate_limit should be treated as a first-class experimental dimension, not as an implementation detail.

## Teacher-model effects

The teacher-model checks now separate two issues that were previously mixed.

The single-positive-edge random-teacher suite showed a large drop in reinterpretation mean relative to fixed cycle. However, that teacher model also produced far fewer raw edges. This makes the result hard to interpret as teacher-model bias alone.

The general random graph teacher suite controls positive edge count at four positive edges for `node_count=4`. Under this condition, the random graph teacher has average raw-edge count close to the fixed-cycle teacher. The reinterpretation mean still drops slightly, but the drop is much smaller.

Observed `random_graph_p4 - fixed_cycle` reinterpretation mean deltas:

| candidate_limit | reinterpretation_mean_delta |
| ---: | ---: |
| 20 | -0.031371 |
| 50 | -0.019357 |
| 100 | -0.014019 |

Interpretation: the earlier single-edge random-teacher drop was partly a raw-size artifact. After reducing that artifact, teacher construction still matters, but the effect looks smaller under the tested condition.

This is not a full teacher-model bias inspection.

## Noise-pattern effects

The noise-pattern minicheck suggests that noise construction affects the observed structural-proxy score.

`extra_positive_heavy` produced a higher tied-win rate than the current baseline noise pattern, while `extra_positive_light` produced a high loss count. `combined_high_noise` had a high reinterpretation mean but still many losses, which implies that a high absolute reinterpretation score does not necessarily mean superiority over the strongest baseline.

Interpretation: noise effects should be read jointly with baseline strength, not only by reinterpretation mean.

This is not a noise-pattern robustness validation.

## Utility-proxy effects

The utility-proxy comparison indicates that the broad group-level pattern is not immediately overturned by the tested proxy variants.

Tied-win and strict-win groups keep positive recombined-total deltas across the tested variants. Aggregate loss cases keep negative recombined-total deltas. In the focused `node_count=4`, `candidate_limit=50` loss group, reinterpretation keeps a positive utility-proxy delta but still has a negative recombined-total delta.

Interpretation: utility_proxy is not the only source of losses under the current measurements. Novelty distance and preservation interact with it through the total score.

This remains a structural proxy analysis only. It is not a claim about human value.

## Loss-case structure

The clearest loss-case pattern is the preservation/novelty tension.

The recorded preservation/novelty tradeoff note shows that reinterpretation loss groups can have positive preservation delta while still losing total score because novelty delta is negative.

This matters because it prevents a simple reading such as "reinterpretation loses because it fails to preserve the raw model." In the focused `node_count=4`, `candidate_limit=50` loss group, preservation and utility_proxy can be positive while total score is negative.

Interpretation: under the current multiplicative score, distance from the teacher can dominate the final result even when preservation remains high.

This is a measurement observation, not a psychological or aesthetic claim.

## Artifact-like findings

The following findings should be treated as artifact-sensitive:

- large drops from the single-positive-edge random-teacher smoke,
- any conclusion drawn from one candidate limit,
- high reinterpretation mean without comparing strongest-baseline loss count,
- utility_proxy conclusions based only on group-mean recombination,
- noise-pattern conclusions from the small fixed grid alone.

These observations are still useful, but they should not be converted into broad claims.

## Credible bounded signal

The current data still supports a bounded signal:

- reinterpretation can produce competitive structural-proxy scores in selected conditions,
- wins and losses can be decomposed into measurable score components,
- candidate-limit sensitivity, teacher construction, noise pattern, and proxy weighting are now visible as separate uncertainty sources,
- the project can state where the current signal is fragile.

This is enough for a useful interim analysis. It is not enough for full empirical phase closure.

## What cannot be claimed

The project should not claim:

- that the model proves human creativity,
- that `utility_proxy` measures human value,
- that the current score captures social, aesthetic, or scientific value,
- that teacher-model bias has been fully inspected,
- that noise-pattern robustness has been established,
- that utility_proxy robustness has been established,
- that full empirical phase closure has been reached.

## What should be summarized next

The next document should be an interim summary, not another expansion of the result matrix.

That summary should state:

- Phase 1 is closed for current scope.
- Phase 2 has enough observations for an interim stop point.
- The strongest remaining uncertainties are candidate-limit sensitivity, teacher-model construction, noise-pattern construction, and proxy robustness.
- The general random graph teacher check reduced one major confound but did not complete the teacher-model bias inspection.
- Full empirical phase work is deferred.

## Suggested stop line

A reasonable stop line for this repository is:

1. Keep Phase 1 closed.
2. Treat the current Phase 2 analysis as an interim empirical analysis.
3. Add a concise `phase2_interim_summary.md`.
4. Do not continue adding large experimental grids in this repository unless a new explicit full empirical phase is started.
