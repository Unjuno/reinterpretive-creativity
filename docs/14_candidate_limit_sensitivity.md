# candidate_limit 感度分析

`scripts/sensitivity_candidate_limit.py` は、探索予算を変えたときの平均スコアを比較する補助スクリプトです。

## 目的

`candidate_limit` を固定したまま結論すると、探索手法の比較を誤る可能性があります。この文書では、複数の探索予算で傾向を見る理由だけを記録します。

## 実行

`python scripts/sensitivity_candidate_limit.py --nodes 4,5 --trials 10 --candidate-limits 50,100,200,500`

## 注意

これは説明補助であり、創造性の証明ではありません。
