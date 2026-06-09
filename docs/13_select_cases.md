# 代表ケース抽出の読み方

`scripts/select_cases.py` は、複数seedの中から、比較しやすい代表ケースを抽出します。

## 目的

平均スコアだけでは、どのようなケースで各探索方法が有利になるのか分かりません。

代表ケース抽出は、次を読むための補助です。

- 再解釈探索が比較的有利なケース
- 局所修復探索が比較的有利なケース
- ランダム探索が比較的有利なケース
- 各手法の差が小さいケース
- 同じケースを何度も読まないための重複回避

## 実行例

```bash
python scripts/select_cases.py \
  --nodes 3,4,5 \
  --trials 10 \
  --candidate-limit 200 \
  --output results/representative_cases.md \
  --json results/representative_cases.json \
  --logs-dir results/representative_cases
```

`--logs-dir` を指定すると、抽出された各代表ケースについて `explain_trial.py` 相当の説明ログも生成されます。

`--json` を指定すると、代表ケース一覧を機械処理しやすいJSON形式でも保存します。

## 重複排除

代表ケースは、可能な限り同じ `node_count / seed` を重複利用しないように選びます。

カテゴリは次の順序で選びます。

1. 再解釈探索が最も有利なケース
2. 局所修復探索が最も有利なケース
3. ランダム探索が最も有利なケース
4. 差が最も小さいケース

後続カテゴリでは、すでに選ばれた `node_count / seed` を避けます。

ただし、候補が足りない場合だけ重複を許容します。その場合は `duplicate_allowed` に `true` が入ります。

## Markdown出力内容

代表ケースサマリには、次が含まれます。

| 列 | 意味 |
|---|---|
| 種類 | どの観点で選ばれた代表ケースか |
| case_key | `node_count / seed` から作ったケース識別子 |
| ノード数 | そのケースのノード数 |
| seed | そのケースのseed |
| 単発ランダム | 単発ランダム修復のスコア |
| ランダム探索 | ランダム探索のスコア |
| 局所修復 | 局所修復探索のスコア |
| 再解釈 | 再解釈探索のスコア |
| margin | 対象手法のスコアから他手法の最大スコアを引いた値 |
| duplicate_allowed | 候補不足で重複利用を許容したか |

## JSON出力内容

JSON出力には、次が含まれます。

| フィールド | 意味 |
|---|---|
| metadata.node_counts | 対象ノード数 |
| metadata.trials | 各ノード数の試行数 |
| metadata.candidate_limit | 候補数予算 |
| metadata.dedupe_key | 重複排除に使うキー |
| metadata.note | この抽出の注意書き |
| representative_cases | 抽出された代表ケース一覧 |
| representative_cases[].label | 代表ケース種別 |
| representative_cases[].case_key | ケース識別子 |
| representative_cases[].node_count | ノード数 |
| representative_cases[].seed | seed |
| representative_cases[].scores | 各探索手法のスコア |
| representative_cases[].margin | 対象手法のmargin。差が最も小さいケースでは `null` |
| representative_cases[].score_spread | そのケース内の最大スコアと最小スコアの差 |
| representative_cases[].duplicate_allowed | 候補不足で重複利用を許容したか |

## margin の読み方

`margin` は、対象手法が他手法よりどの程度有利かを見るための値です。

```text
margin = score(target_method) - max(score(other_methods))
```

- 正の値: 対象手法が他手法より高い。
- 0付近: 差が小さい。
- 負の値: 対象手法として選ばれているが、他手法に負けている。

## 注意

代表ケース抽出は、説明補助です。

抽出されたケースは、平均的なケースではありません。むしろ、差が見えやすいケースや、比較上重要なケースを選んでいます。

したがって、代表ケースだけを見て全体傾向を結論してはいけません。

全体傾向は `scripts/run_experiments.py` のバッチ結果で確認し、代表ケースはその補助として読む必要があります。

## 実装済みの補助

現在は、次が利用できます。

- Markdown形式の代表ケースサマリ
- JSON形式の代表ケースサマリ
- 抽出ケースごとの説明ログ生成
- `node_count / seed` の重複回避

今後さらに必要なら、ノード数ごとの抽出、margin閾値による抽出、スコア構成要素での抽出を Phase 2 以降で検討します。
