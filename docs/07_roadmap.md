# ロードマップ

このリポジトリは、主張を広げすぎず、段階的に進めます。

この文書は現在、履歴用ロードマップと今後の候補作業を分けて整理します。Phase 1 は current scope において closed です。

## Phase 0: 最小公開状態

目的: 見られても大きく破綻しない最小構成にする。

状態: 完了。

- [x] 日本語 README
- [x] 射程の明記
- [x] モデル定義
- [x] 限界の明記
- [x] 最小 Python シミュレーション
- [x] unittest
- [x] GitHub Actions CI

## Phase 1: current-scope closure

目的: 固定デモだけでなく、複数ケースで傾向を見て、限定モデル・前提・最小実験結果を整理する。

状態: current scope において closed。

- [x] 複数 seed で平均スコアを出す
- [x] `results/` に結果サマリを保存
- [x] 再解釈探索と単発ランダム修復の差を表にする
- [x] 強めのランダム探索ベースラインを追加
- [x] 局所修復探索を追加
- [x] JSON / CSV 出力を追加
- [x] モデル中核文書を追加
- [x] 形式的前提文書を追加
- [x] 完了条件文書を追加
- [x] 実験マトリクス文書を追加
- [x] 最小実験結果を整理
- [x] 第1フェーズ終了まとめを追加

Phase 1 の closure は、full empirical phase の完了を意味しません。full empirical phase は Phase 2 の候補作業です。

## Phase 2 候補: full empirical phase

目的: current-scope closure で得られた bounded signal を、より広い実験マトリクスで検査する。

状態: mini-start、random-teacher smoke 整理、teacher-model bias minicheck、teacher-model bias suite、保存度と新規性のトレードオフ整理、複数 utility_proxy minicheck、noise-pattern minicheck を実施済み。ただし full empirical phase は未完了。

候補作業:

- [x] candidate_limit 感度分析
- [x] ランダム生成された教師モデルの追加または再整理
- [x] ノイズ注入パターンの最小検査
- [ ] ノイズ注入パターンの本検査
- [x] 保存度と新規性のトレードオフ整理
- [x] 複数 utility_proxy の最小比較
- [ ] 複数 utility_proxy の本比較
- [x] teacher-model bias の最小検査
- [x] teacher-model bias suite
- [ ] teacher-model bias の本検査
- [x] loss-case analysis の拡張
- [x] breakdown analysis の拡張

mini-start 実施済み出力:

- `results/phase2_candidate_limit_sensitivity.md`
- `results/phase2_loss_cases.md`
- `results/phase2_breakdown_analysis.md`
- `docs/phase2_mini_start_summary.md`

random-teacher smoke 整理済み出力:

- `docs/15_random_teacher_model.md`
- `results/phase2_random_teacher_smoke.md`

teacher-model bias minicheck 出力:

- `results/phase2_teacher_bias_minicheck.md`

teacher-model bias suite 出力:

- `results/phase2_teacher_bias_suite.md`
- `results/phase2_teacher_bias_suite.csv`
- `results/phase2_teacher_bias_suite.json`

保存度と新規性のトレードオフ整理:

- `results/phase2_preservation_novelty_tradeoff.md`

utility_proxy minicheck 出力:

- `results/phase2_utility_proxy_comparison.md`
- `results/phase2_utility_proxy_comparison.csv`
- `results/phase2_utility_proxy_comparison.json`

noise-pattern minicheck 出力:

- `results/phase2_noise_patterns.md`
- `results/phase2_noise_patterns.csv`
- `results/phase2_noise_patterns.json`

teacher-model bias minicheck は本検査完了ではありません。現時点では fixed cycle teacher と single-positive-edge random-teacher smoke を小さい同一条件で比較し、teacher construction が score pattern に影響しうることを記録しただけです。

teacher-model bias suite は、fixed cycle teacher と既存 single-positive-edge random-teacher smoke を seed 0-29、candidate_limit 20/50 で比較した小規模拡張です。random teacher はまだ general random graph teacher ではなく、raw-edge count の差も大きいため、本検査完了ではありません。

保存度と新規性のトレードオフ整理は、既存 Phase 2 breakdown 結果の解釈整理です。新しい score function や追加実験ではありません。

utility_proxy minicheck は、既存 breakdown component 平均の proxy variant 再結合です。per-trial 再採点ではなく、utility_proxy の本比較完了でもありません。

noise-pattern minicheck は、既存 `noisy_case` の `conflict_rate` と `extra_positive_rate` を小さい grid で検査したものです。新しい noise generator の追加ではなく、ノイズ注入パターンの本検査完了でもありません。

これらは current Phase 1 の未完了作業ではありません。Phase 2 として扱います。

## Phase 3 候補: 説明可能なシミュレーションの拡張

目的: 平均スコアだけでなく、1ケースごとの変化をさらに読みやすくする。

既に完了しているもの:

- [x] 1ケース説明ログを追加
- [x] 教師モデル・初期モデル・各探索結果を Markdown 出力する
- [x] 初期モデルからの変更辺を出力する
- [x] 教師モデルとの差分を出力する
- [x] スコア構成要素の内訳を説明ログに追加する
- [x] 近傍探索の改善過程を保存する
- [x] 代表ケースを自動抽出する
- [x] 代表ケース抽出結果を JSON で保存できるようにする
- [x] 代表ケースの重複排除を追加する
- [x] 1ケース説明ログを JSON で保存できるようにする
- [x] CIで説明ログ生成を確認する

今後の候補:

- [ ] ケース比較の読みやすさを改善する
- [ ] score breakdown の可視化を検討する
- [ ] 代表ケース抽出基準の感度を確認する

## Phase 4 候補: 形式核の追加

目的: Lean などで、定義間の関係だけを形式化する。

候補作業:

- [ ] `Model` の最小定義
- [ ] `Consistent` / `Inconsistent` の定義
- [ ] `Differs` の定義
- [ ] `ReinterpretationCandidate` の定義
- [ ] 「創造性そのものの証明ではない」ことを文書に明記

## Phase 5 候補: 関連研究の補強

目的: 既存研究との接続を強める。

候補作業:

- [ ] Boden の創造性分類
- [ ] Wiggins の計算創造性形式化
- [ ] Amabile の新規性・評価基準の議論
- [ ] belief revision / model repair
- [ ] computational creativity の評価指標

## 将来課題: 集団分布とアンサンブル

生徒集団・生徒間交流・複数教師モデルは重要ですが、Phase 1 では実装しません。

理由は、現在の主目的が「再解釈型創造性の限定モデル」を整理することだからです。

扱うとしても、まずは [`09_failure_analysis.md`](09_failure_analysis.md) のような概念メモに留めます。

少なくとも current scope では、次は追加しません。

- 生徒集団シミュレーション
- 生徒間交流ネットワーク
- アンサンブル検証用CI
- 大規模な集団モデル

必要になった場合は、別フェーズまたは別リポジトリとして切り出します。

## やらないこと

少なくとも current scope では、次はやりません。

- 創造性全体の理論化
- 自然言語理解の完全モデル化
- 人間心理の実験的実証
- 社会的受容の実測
