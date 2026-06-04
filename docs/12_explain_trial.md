# 1ケース説明ログの読み方

`scripts/explain_trial.py` は、1つの実験ケースについて、教師モデル・初期モデル・各探索結果を Markdown / JSON で出力します。

## 目的

平均スコアだけでは、モデルが何を変えたのか分かりません。

説明ログは、次を見るための補助です。

- 初期モデルにどの不整合があるか
- 各探索方法がどの辺を変えたか
- 教師モデルとどの辺で異なるか
- 高スコア候補がどの指標で高くなったか
- 局所修復探索がどのステップで何を変えたか
- 高スコア候補が本当に解釈しやすい構造か
- 後続ツールで変更辺やスコア内訳を再利用できるか

## 実行例

```bash
python scripts/explain_trial.py \
  --seed 0 \
  --node-count 4 \
  --candidate-limit 100 \
  --output results/local_explain_trial.md \
  --json results/local_explain_trial.json
```

標準出力にMarkdownを出したい場合は、`--output` を省略します。

```bash
python scripts/explain_trial.py --seed 0 --node-count 4 --candidate-limit 100
```

## Markdown出力内容

Markdown出力には、次が含まれます。

| セクション | 内容 |
|---|---|
| 条件 | seed、ノード数、候補数予算 |
| 教師モデル | 参照モデルの肯定・否定関係 |
| 初期モデル | 生徒側の初期理解。矛盾を含みうる |
| 単発ランダム修復 | 矛盾を1回だけランダム解消した結果 |
| ランダム探索 | 同じ候補数予算で広く探索した結果 |
| 局所修復探索 | 初期モデル近傍を1辺ずつ改善した結果 |
| 再解釈探索 | 現在の再解釈候補生成方式による結果 |
| スコア内訳 | novelty、保存度、utility_proxy、utility構成要素 |
| 局所修復探索の改善過程 | どの辺をどう変え、スコアがどう変わったか |
| 初期モデルからの変更 | 初期理解からどの辺が変わったか |
| 教師モデルとの差分 | 教師モデルとどの辺が異なるか |

## JSON出力内容

JSON出力には、次が含まれます。

| フィールド | 意味 |
|---|---|
| metadata.seed | seed |
| metadata.node_count | ノード数 |
| metadata.candidate_limit | 候補数予算 |
| teacher_model | 教師モデルの辺リスト |
| initial_model | 初期モデルの辺リスト。矛盾も含む |
| results.random_repair | 単発ランダム修復の結果 |
| results.random_search | ランダム探索の結果 |
| results.local_repair | 局所修復探索の結果 |
| results.reinterpretation | 再解釈探索の結果 |
| results.*.score | 総合スコア |
| results.*.score_breakdown | スコア構成要素 |
| results.*.model | 結果モデルの辺リスト |
| results.*.changes_from_initial | 初期モデルからの変更辺 |
| results.*.differences_from_teacher | 教師モデルとの差分 |
| results.local_repair.local_repair_trace | 局所修復探索の改善過程 |

## スコア内訳

各探索結果には、次の指標が出力されます。

| 指標 | 意味 |
|---|---|
| novelty_distance | 教師モデルとの差分。大きいほど教師モデルと異なる |
| preservation | 初期モデルの非矛盾情報をどれだけ保存したか |
| utility_proxy | 構造的な有用性らしさの暫定 proxy |
| density_score | 空構造と過密構造を下げる密度指標 |
| node_coverage_score | 肯定辺が覆うノードの割合 |
| weak_connectivity_score | 肯定辺の最大弱連結成分比率 |
| in_out_coverage_score | 入辺・出辺を持つノードの広がり |
| total_score | `novelty_distance * preservation * utility_proxy` |

この内訳により、候補が高得点になった理由を分解できます。

例えば、高スコアでも `preservation` が低ければ、初期理解をかなり捨てている可能性があります。逆に `preservation` が高くても `utility_proxy` が低ければ、誤った理解を保存しすぎている可能性があります。

## 局所修復探索の改善過程

局所修復探索には、次の表またはJSON配列が追加されます。

| 列 | 意味 |
|---|---|
| step | 記録された探索ステップ |
| action | 改善、摂動、初期摂動の区別 |
| evaluated | その時点までに評価した候補数 |
| edge | 変更した辺 |
| old_value | 変更前の値 |
| new_value | 変更後の値 |
| score_before | 変更前のスコア |
| score_after | 変更後のスコア |
| best_score | その時点までの最良スコア |

これにより、局所修復探索が高得点を出した場合に、どの変更が効いたのかを追えます。

ただし、これは局所修復探索の説明補助です。探索過程が読めることは、創造性の証明ではありません。

## 注意

このログは、説明補助です。

高スコア候補が出ても、それは創造性の証明ではありません。

このログで確認できるのは、あくまで次です。

> ある人工ケースで、候補モデルがどの関係を保存し、どの関係を変え、どのproxy指標によって高く評価され、局所修復探索がどの変更過程をたどったか。

## 今後の改善案

今後、必要なら次を追加できます。

- 変更辺の数
- 変更種別の集計
- 複数ケースの代表例抽出
- JSON出力を使った可視化

ただし、初期MVPでは、説明ログは1ケースを読むための最小機能に留めます。
