# Phase 2 mini-start: breakdown analysis

## Scope

勝ちケースと負けケースで、`reinterpretation` と strongest baseline の score components 平均を比較する。

ここでの strongest baseline は、各 trial で `random_repair`, `random_search`, `local_repair` のうち最も高い score の method である。

この分析は原因を断定しない。成分差が見える条件を記録するだけである。

## Group counts

| group | case_count |
|---|---:|
| reinterpretation_tied_win_all | 213 |
| reinterpretation_strict_win_all | 75 |
| reinterpretation_loss_all | 147 |
| n4_limit50_reinterpretation_tied_win_all | 4 |
| n4_limit50_reinterpretation_loss_all | 26 |

## Mean component comparison

| group | component | reinterpretation_mean | best_baseline_mean | delta |
|---|---|---:|---:|---:|
| reinterpretation_tied_win_all | novelty_distance | 0.7390 | 0.7218 | 0.0172 |
| reinterpretation_tied_win_all | preservation | 0.9615 | 0.9409 | 0.0206 |
| reinterpretation_tied_win_all | utility_proxy | 0.9588 | 0.9395 | 0.0193 |
| reinterpretation_tied_win_all | density_score | 0.9507 | 0.9061 | 0.0446 |
| reinterpretation_tied_win_all | node_coverage_score | 0.9977 | 0.9930 | 0.0047 |
| reinterpretation_tied_win_all | weak_connectivity_score | 0.9977 | 0.9930 | 0.0047 |
| reinterpretation_tied_win_all | in_out_coverage_score | 0.8480 | 0.8392 | 0.0088 |
| reinterpretation_tied_win_all | total_score | 0.6817 | 0.6356 | 0.0461 |
| reinterpretation_strict_win_all | novelty_distance | 0.6900 | 0.6411 | 0.0489 |
| reinterpretation_strict_win_all | preservation | 0.9419 | 0.8836 | 0.0584 |
| reinterpretation_strict_win_all | utility_proxy | 0.9297 | 0.8750 | 0.0547 |
| reinterpretation_strict_win_all | density_score | 0.8767 | 0.7500 | 0.1267 |
| reinterpretation_strict_win_all | node_coverage_score | 0.9933 | 0.9800 | 0.0133 |
| reinterpretation_strict_win_all | weak_connectivity_score | 0.9933 | 0.9800 | 0.0133 |
| reinterpretation_strict_win_all | in_out_coverage_score | 0.8417 | 0.8167 | 0.0250 |
| reinterpretation_strict_win_all | total_score | 0.6063 | 0.4753 | 0.1310 |
| reinterpretation_loss_all | novelty_distance | 0.5618 | 0.7721 | -0.2103 |
| reinterpretation_loss_all | preservation | 0.9477 | 0.9069 | 0.0408 |
| reinterpretation_loss_all | utility_proxy | 0.8854 | 0.9011 | -0.0157 |
| reinterpretation_loss_all | density_score | 0.7466 | 0.7772 | -0.0306 |
| reinterpretation_loss_all | node_coverage_score | 0.9949 | 0.9983 | -0.0034 |
| reinterpretation_loss_all | weak_connectivity_score | 0.9949 | 0.9983 | -0.0034 |
| reinterpretation_loss_all | in_out_coverage_score | 0.8444 | 0.8665 | -0.0221 |
| reinterpretation_loss_all | total_score | 0.4631 | 0.6319 | -0.1688 |
| n4_limit50_reinterpretation_tied_win_all | novelty_distance | 0.6667 | 0.5833 | 0.0833 |
| n4_limit50_reinterpretation_tied_win_all | preservation | 0.8810 | 0.9583 | -0.0774 |
| n4_limit50_reinterpretation_tied_win_all | utility_proxy | 0.7844 | 0.7969 | -0.0125 |
| n4_limit50_reinterpretation_tied_win_all | density_score | 0.4375 | 0.5000 | -0.0625 |
| n4_limit50_reinterpretation_tied_win_all | node_coverage_score | 1.0000 | 1.0000 | 0.0000 |
| n4_limit50_reinterpretation_tied_win_all | weak_connectivity_score | 1.0000 | 1.0000 | 0.0000 |
| n4_limit50_reinterpretation_tied_win_all | in_out_coverage_score | 0.8750 | 0.8125 | 0.0625 |
| n4_limit50_reinterpretation_tied_win_all | total_score | 0.4576 | 0.4404 | 0.0172 |
| n4_limit50_reinterpretation_loss_all | novelty_distance | 0.5385 | 0.7436 | -0.2051 |
| n4_limit50_reinterpretation_loss_all | preservation | 0.9557 | 0.8762 | 0.0795 |
| n4_limit50_reinterpretation_loss_all | utility_proxy | 0.8947 | 0.8560 | 0.0387 |
| n4_limit50_reinterpretation_loss_all | density_score | 0.7788 | 0.6442 | 0.1346 |
| n4_limit50_reinterpretation_loss_all | node_coverage_score | 0.9904 | 1.0000 | -0.0096 |
| n4_limit50_reinterpretation_loss_all | weak_connectivity_score | 0.9904 | 1.0000 | -0.0096 |
| n4_limit50_reinterpretation_loss_all | in_out_coverage_score | 0.8462 | 0.8702 | -0.0240 |
| n4_limit50_reinterpretation_loss_all | total_score | 0.4548 | 0.5507 | -0.0959 |

## Reading

- Across all tied-win cases, `reinterpretation` has slightly higher mean `novelty_distance`, `preservation`, and `utility_proxy` than the strongest baseline.
- Across all loss cases, `reinterpretation` has much lower mean `novelty_distance` than the strongest baseline, while mean `preservation` is higher. In this setup, stronger preservation does not by itself prevent score losses.
- For the focused `node_count=4`, `candidate_limit=50` loss group, `reinterpretation` has higher mean `utility_proxy` and `density_score` than the strongest baseline, but lower mean `novelty_distance`. This shows the multiplicative score can be dominated by distance gaps in that condition.
- These are condition-specific structural proxy differences, not claims about human creativity or causal mechanisms.

## Files

- `results/phase2_breakdown_analysis.csv`
- `results/phase2_breakdown_analysis.json`
