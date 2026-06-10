# Phase 2 utility_proxy comparison minicheck

## Status

This is a minimal utility_proxy comparison based on existing Phase 2 breakdown results.

It does not add a new experiment, does not change the main score function, and does not complete full utility_proxy validation.

## Method

Source data:

- `results/phase2_breakdown_analysis.csv`
- `results/phase2_breakdown_analysis.json`

The comparison recombines existing mean utility components under several utility_proxy variants.

This is not per-trial rescoring. It is a group-level minicheck using existing component means.

The recombined total is:

```text
recombined_total = novelty_distance_mean * preservation_mean * recombined_utility_proxy_mean
```

## Proxy variants

| proxy_variant | density_score | node_coverage_score | weak_connectivity_score | in_out_coverage_score |
| --- | ---: | ---: | ---: | ---: |
| current_weighted | 0.35 | 0.25 | 0.25 | 0.15 |
| uniform_components | 0.25 | 0.25 | 0.25 | 0.25 |
| density_heavy | 0.50 | 0.20 | 0.20 | 0.10 |
| coverage_heavy | 0.20 | 0.30 | 0.30 | 0.20 |
| in_out_heavy | 0.25 | 0.20 | 0.20 | 0.35 |

## Summary by group

### reinterpretation_tied_win_all

Across all variants, reinterpretation keeps a positive recombined-total delta.

| proxy_variant | delta_utility_proxy | delta_recombined_total |
| --- | ---: | ---: |
| current_weighted | 0.019278 | 0.043189 |
| uniform_components | 0.015698 | 0.040435 |
| density_heavy | 0.025059 | 0.047129 |
| coverage_heavy | 0.013498 | 0.039249 |
| in_out_heavy | 0.016109 | 0.040245 |

### reinterpretation_strict_win_all

Across all variants, reinterpretation keeps a positive recombined-total delta.

| proxy_variant | delta_utility_proxy | delta_recombined_total |
| --- | ---: | ---: |
| current_weighted | 0.054750 | 0.108628 |
| uniform_components | 0.044583 | 0.102577 |
| density_heavy | 0.071167 | 0.117100 |
| coverage_heavy | 0.038333 | 0.100157 |
| in_out_heavy | 0.045750 | 0.101972 |

### reinterpretation_loss_all

Across all variants, reinterpretation keeps a negative recombined-total delta.

| proxy_variant | delta_utility_proxy | delta_recombined_total |
| --- | ---: | ---: |
| current_weighted | -0.015731 | -0.159589 |
| uniform_components | -0.014881 | -0.160635 |
| density_heavy | -0.018878 | -0.156806 |
| coverage_heavy | -0.012585 | -0.162373 |
| in_out_heavy | -0.016752 | -0.159419 |

### n4_limit50_reinterpretation_loss_all

In the focused loss group, reinterpretation has a positive utility_proxy delta under every tested variant, but the recombined total remains negative under every tested variant.

| proxy_variant | delta_utility_proxy | delta_recombined_total |
| --- | ---: | ---: |
| current_weighted | 0.038702 | -0.097298 |
| uniform_components | 0.022837 | -0.108556 |
| density_heavy | 0.061058 | -0.079375 |
| coverage_heavy | 0.016346 | -0.115221 |
| in_out_heavy | 0.021394 | -0.107521 |

### n4_limit50_reinterpretation_tied_win_all

This small tied-win group has only four cases. Reinterpretation keeps a positive recombined-total delta across all variants, but the margin is small and should not be overread.

| proxy_variant | delta_utility_proxy | delta_recombined_total |
| --- | ---: | ---: |
| current_weighted | -0.012500 | 0.015189 |
| uniform_components | 0.000000 | 0.023414 |
| density_heavy | -0.025000 | 0.005993 |
| coverage_heavy | 0.000000 | 0.024386 |
| in_out_heavy | 0.006250 | 0.026555 |

## Reading

This minicheck suggests that the existing Phase 2 win/loss pattern is not highly sensitive to these simple utility_proxy recombinations at the group-mean level.

The focused `node_count=4`, `candidate_limit=50` loss group is especially useful: reinterpretation has higher recombined utility_proxy under every tested variant, but still has lower recombined total because the novelty-distance deficit remains large.

This supports the earlier preservation/novelty tradeoff note: changing utility_proxy weights alone does not remove the observed loss pattern in that focused group.

## Limits

This note does not show that the current utility_proxy is correct.

It does not test all plausible utility_proxy variants.

It does not perform per-trial rescoring, so it cannot replace a full robustness check.

It does not show anything about human value, social value, aesthetic value, or scientific value.

## Next work

A fuller utility_proxy robustness check should:

- rescore each trial under each proxy variant,
- record win/loss counts under each variant,
- compare median as well as mean scores,
- include teacher-model variants,
- preserve the distinction between structural proxy and human value.
