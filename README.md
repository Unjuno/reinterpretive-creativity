# 再解釈型創造性モデル

このリポジトリは、**創造性の一部**を説明するための小さな形式モデル・シミュレーション実験です。

扱う対象は、創造性全体ではありません。ここでは、主体の内部ワールドモデルに生じた不整合が、別の整合的な構造へ再解釈されることで生まれる **再解釈型創造性** に限定します。

## 中心仮説

> 再解釈型創造性とは、主体の内部ワールドモデルに生じた不整合が、より整合的な代替モデルへ修復・変形され、その代替モデルが元のモデルと異なり、かつ何らかの価値を持つ場合に成立する創造性候補である。

このリポジトリでは、これを次の4条件で扱います。

1. 初期モデルに内部不整合がある。
2. 再解釈後モデルは内部的に整合している。
3. 再解釈後モデルは元のモデルと異なる。
4. 再解釈後モデルには、明示された評価基準上の価値がある。

## 扱わないこと

このリポジトリは、次を主張しません。

- 創造性全体を説明する。
- 人間の創造性を完全に証明する。
- シミュレーションだけで創造性を実証する。
- Lean や形式証明で創造性そのものを証明する。
- 対話・共通理解・行動リスク低減の一般理論を作る。

対話や共通理解は背景概念として重要ですが、このリポジトリの主対象は **創造性** です。

## 最小モデル

初期ワールドモデルを `W`、再解釈後モデルを `W'` とします。

再解釈型創造性候補 `RIC(W, W')` を、次のように定義します。

```text
RIC(W, W') :=
  Inc(W)       // W に内部不整合がある
  and Con(W')  // W' は内部的に整合している
  and Diff(W, W') // W と W' は異なる
  and Val(W')  // W' は評価基準上の価値を持つ
```

ここで重要なのは、**誤りそのものを創造性とは呼ばない**ことです。

誤り・不整合・曖昧さは、再解釈を発生させるきっかけになりえます。しかし、それが創造性候補になるには、少なくとも整合性・差分・価値が必要です。

## 現在の実装

現在は、次の範囲だけを実装しています。

- 符号付き有向グラフによる人工ワールドモデル
- 肯定関係と否定関係の衝突による内部不整合
- 単発ランダム修復、ランダム探索、局所修復探索、再解釈探索の比較
- 複数 seed / 複数ノード数による小規模バッチ実験
- 1ケースの変更辺・スコア内訳・局所修復探索の改善過程を読むための説明ログ
- 代表ケース抽出と代表ケース別の説明ログ生成
- JSON / CSV / Markdown 形式の結果出力
- 整合性、新規性、保存度、有用性 proxy による評価
- GitHub Actions による Python シミュレーションの最小検証

## 実行方法

```bash
python scripts/simulate.py
python scripts/run_experiments.py --nodes 3,4,5 --trials 10 --candidate-limit 200
python scripts/run_experiments.py --nodes 3,4,5 --trials 10 --candidate-limit 200 --json results/local_experiment.json --csv results/local_experiment.csv
python scripts/explain_trial.py --seed 0 --node-count 4 --candidate-limit 100 --output results/local_explain_trial.md
python scripts/select_cases.py --nodes 3,4,5 --trials 10 --candidate-limit 200 --output results/representative_cases.md --logs-dir results/representative_cases
python -m unittest discover -s tests
```

## 初期バッチ結果

固定設定の3〜5ノード比較では、次の結果になりました。

| ノード数 | 試行数 | 単発ランダム平均 | ランダム探索平均 | 局所修復平均 | 再解釈平均 | 改善量(単発) | 改善量(探索) | 改善量(局所) | 勝率(単発) | 勝率(探索) | 勝率(局所) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 0.2856 | 0.7439 | 0.7500 | 0.7500 | 0.4644 | 0.0061 | 0.0000 | 100.00% | 100.00% | 100.00% |
| 4 | 10 | 0.2303 | 0.5983 | 0.7514 | 0.4994 | 0.2691 | -0.0989 | -0.2520 | 100.00% | 10.00% | 0.00% |
| 5 | 10 | 0.2087 | 0.4498 | 0.4569 | 0.4141 | 0.2053 | -0.0358 | -0.0428 | 100.00% | 40.00% | 20.00% |

詳細は [`results/initial_batch_summary.md`](results/initial_batch_summary.md) を参照してください。

この結果は、創造性全体を証明するものではありません。局所修復探索はノード数4〜5で再解釈探索より高い代理スコアを出していますが、これは現行スコア関数と候補生成条件に依存します。

## 説明ログ

`explain_trial.py` は、1ケースについて次を Markdown で出力します。

- 教師モデル
- 初期モデル
- 単発ランダム修復の結果
- ランダム探索の結果
- 局所修復探索の結果
- 再解釈探索の結果
- スコア内訳
- 局所修復探索の改善過程
- 初期モデルからの変更辺
- 教師モデルとの差分

スコア内訳には、`novelty_distance`、`preservation`、`utility_proxy`、`density_score`、`node_coverage_score`、`weak_connectivity_score`、`in_out_coverage_score`、`total_score` が含まれます。

局所修復探索の改善過程には、変更した辺、変更前後の値、変更前後のスコア、その時点までの最良スコアが含まれます。

これは説明補助であり、創造性の証明ではありません。読み方は [`docs/12_explain_trial.md`](docs/12_explain_trial.md) を参照してください。

## 代表ケース抽出

`select_cases.py` は、複数seedの中から次の代表ケースを抽出します。

- 再解釈探索が最も有利なケース
- 局所修復探索が最も有利なケース
- ランダム探索が最も有利なケース
- 各手法の差が最も小さいケース

指定した `--logs-dir` には、抽出された各ケースの説明ログも保存されます。

この抽出は説明補助であり、創造性の証明ではありません。

## 文書

- [`docs/00_terms.md`](docs/00_terms.md): 用語定義
- [`docs/01_scope.md`](docs/01_scope.md): 射程
- [`docs/02_model.md`](docs/02_model.md): モデル定義
- [`docs/03_simulation_design.md`](docs/03_simulation_design.md): シミュレーション設計
- [`docs/04_limitations.md`](docs/04_limitations.md): 限界
- [`docs/05_related_work.md`](docs/05_related_work.md): 関連研究
- [`docs/06_hypothesis.md`](docs/06_hypothesis.md): 検証仮説
- [`docs/07_roadmap.md`](docs/07_roadmap.md): ロードマップ
- [`docs/08_ci_check.md`](docs/08_ci_check.md): CI確認用メモ
- [`docs/09_failure_analysis.md`](docs/09_failure_analysis.md): 失敗分析と集団分布
- [`docs/10_utility_proxy.md`](docs/10_utility_proxy.md): utility_proxy 設計メモ
- [`docs/11_search_strategy.md`](docs/11_search_strategy.md): 探索方針メモ
- [`docs/12_explain_trial.md`](docs/12_explain_trial.md): 1ケース説明ログの読み方
- [`docs/13_select_cases.md`](docs/13_select_cases.md): 代表ケース抽出の読み方

## CI

CI は `push` と `pull_request` だけで実行します。

手動起動用の `workflow_dispatch` は入れていません。

## 現時点の立場

このリポジトリは、完成した理論ではありません。

目的は、創造性の一類型である「再解釈型創造性」を、過剰主張を避けながら、形式化・シミュレーション・検証可能な仮説として整理することです。
