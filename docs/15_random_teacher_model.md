# ランダム教師モデル設計メモ

## 目的

固定サイクル教師だけに依存しない検査を追加する。

この文書でいう教師モデルは、人工 signed-graph 実験の参照構造である。人間の教師、社会的評価、審美的評価、科学的評価、または人間の価値判断を表すものではない。

## 現在の位置づけ

ランダム教師モデル系のスクリプトは、すでに最小 smoke として存在する。

既存の主な構成は次の通り。

| File | Role |
| --- | --- |
| `scripts/random_teacher_smoke.py` | ランダム教師モデルの最小生成。現在はノード4の有向辺集合から1本の肯定辺を選ぶ smoke 実装。 |
| `scripts/random_teacher_experiments.py` | ランダム教師から noisy raw model を作り、既存探索メソッドを比較する。 |
| `scripts/random_teacher_batch_smoke.py` | 複数 seed の smoke 実行と平均スコア集計。 |
| `scripts/random_teacher_models.py` | 教師モデル、raw model、各探索結果モデルを含む詳細出力。 |
| `scripts/random_teacher_breakdowns.py` | 各探索結果に score breakdown を付与する。 |
| `scripts/random_teacher_reinterpretation_gap.py` | 再解釈探索と比較対象の breakdown gap を出す。 |
| `scripts/random_teacher_cli.py` / `scripts/random_teacher_output.py` | smoke 結果を標準出力またはファイルに出力する補助。 |

## 現在の smoke 実装

現時点の `build_random_teacher` は、有向辺ごとに一定確率で肯定辺を置く一般ランダムグラフ生成器ではない。

現在の挙動は次の通り。

1. `node_count` 個のノードを作る。
2. 全有向辺を作る。
3. すべての辺を `0` に初期化する。
4. seed で決定される1本の有向辺だけを `1` にする。

したがって、これは full random teacher model ではなく、**single-positive-edge random-teacher smoke** として扱う。

## 使い方

この smoke は、固定サイクル教師で見えた傾向が、少なくとも別の参照構造でも同じように観察されるかを粗く見るための入口である。

結果の読み方には次の制約を置く。

- smoke 結果は teacher-model bias の検証完了を意味しない。
- smoke 結果は full empirical phase closure を意味しない。
- `utility_proxy` は structural proxy であり、人間の価値判断ではない。
- breakdown gap は記述的な測定結果であり、因果説明ではない。

## Phase 2 mini-check 状態

`results/phase2_random_teacher_smoke.md` に、既存 smoke 実装を使った最小結果を記録した。

この記録により、未完了項目「ランダム生成された教師モデルの追加または再整理」は、少なくとも次の状態まで整理済みとする。

- 既存スクリプトの役割を明示した。
- 現在の実装が full random teacher model ではなく single-positive-edge smoke であることを明示した。
- smoke 結果を Phase 2 の追加記録として保存した。

ただし、次は未完了のまま残す。

- 有向辺ごとに一定確率で肯定辺を置く一般 random teacher generator。
- fixed teacher と random teacher の十分な seed 範囲での比較。
- teacher-model bias の検査完了。

## 次の実装単位

次に実装する場合の最小単位は次の通り。

1. `build_random_teacher` に `positive_edge_probability` を追加する。
2. 最低1本の肯定辺を保証する。
3. fixed teacher と random teacher を同じ出力形式で比較できる batch script を追加する。
4. teacher-model bias 検査として、score pattern と breakdown gap の差分を記録する。
