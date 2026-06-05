# candidate_limit 感度分析

`scripts/sensitivity_candidate_limit.py` は、探索予算 `candidate_limit` を変えたとき、各探索手法の平均スコアがどう変わるかを見るための補助スクリプトです。

## 目的

固定された探索予算だけで、再解釈探索・ランダム探索・局所修復探索の優劣を判断すると危険です。

この分析では、複数の `candidate_limit` を指定し、探索予算に対するスコア変化を確認します。

## 実行例

`python scripts/sensitivity_candidate_limit.py --nodes 4,5 --trials 10 --candidate-limits 50,100,200,500 --output results/candidate_limit_sensitivity.md --json results/candidate_limit_sensitivity.json --csv results/candidate_limit_sensitivity