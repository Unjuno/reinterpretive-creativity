# candidate_limit 感度分析

`scripts/sensitivity_candidate_limit.py` は、探索予算 `candidate_limit` を変えたとき、各探索手法の平均スコアがどう変わるかを見るための補助スクリプトです。

## 目的

現在の実験では、再解釈探索・ランダム探索・局所修復探索を比較しています。

ただし、探索手法の強さは `candidate_limit` に依存します。

そのため、固定値だけで結論するのではなく、複数の `candidate_limit` で傾向を確認します。

## 実行例

```bash
python scripts/sensitivity_candidate_limit.py \
  --nodes 4,5 \
  --trials 10 \
  --candidate-limits 50,100,200,500 \
  --output results/candidate_limit_sensitivity.md \
  --json results/candidate_limit_sensitivity.json \
  --csv results/candidate_limit_sensitivity.csv
```

## 出力

| 出力 | 内容 |
|---|---|
| Markdown | 人間が読むための表 |
| JSON | 後続ツールで扱うための構造化デ