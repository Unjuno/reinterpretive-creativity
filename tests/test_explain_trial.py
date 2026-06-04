from pathlib import Path
import tempfile
import unittest

from scripts import explain_trial


class TestExplainTrial(unittest.TestCase):
    def test_explain_case_contains_core_sections(self):
        text = explain_trial.explain_case(seed=0, node_count=4, candidate_limit=50)
        self.assertIn("# 1ケース説明ログ", text)
        self.assertIn("## 教師モデル", text)
        self.assertIn("## 初期モデル", text)
        self.assertIn("単発ランダム修復", text)
        self.assertIn("ランダム探索", text)
        self.assertIn("局所修復探索", text)
        self.assertIn("再解釈探索", text)
        self.assertIn("スコア内訳", text)
        self.assertIn("初期モデルからの変更", text)
        self.assertIn("教師モデルとの差分", text)

    def test_explain_case_contains_score_breakdown(self):
        text = explain_trial.explain_case(seed=0, node_count=4, candidate_limit=50)
        self.assertIn("novelty_distance", text)
        self.assertIn("preservation", text)
        self.assertIn("utility_proxy", text)
        self.assertIn("density_score", text)
        self.assertIn("node_coverage_score", text)
        self.assertIn("weak_connectivity_score", text)
        self.assertIn("in_out_coverage_score", text)
        self.assertIn("total_score", text)

    def test_explain_case_contains_local_repair_trace(self):
        text = explain_trial.explain_case(seed=0, node_count=4, candidate_limit=50)
        self.assertIn("局所修復探索の改善過程", text)
        self.assertIn("score_before", text)
        self.assertIn("score_after", text)
        self.assertIn("best_score", text)
        self.assertIn("改善", text)

    def test_explain_case_json_contains_core_fields(self):
        data = explain_trial.explain_case_json(seed=0, node_count=4, candidate_limit=50)
        self.assertIn("metadata", data)
        self.assertIn("teacher_model", data)
        self.assertIn("initial_model", data)
        self.assertIn("results", data)
        self.assertIn("random_repair", data["results"])
        self.assertIn("random_search", data["results"])
        self.assertIn("local_repair", data["results"])
        self.assertIn("reinterpretation", data["results"])
        local_repair = data["results"]["local_repair"]
        self.assertIn("score_breakdown", local_repair)
        self.assertIn("changes_from_initial", local_repair)
        self.assertIn("differences_from_teacher", local_repair)
        self.assertIn("local_repair_trace", local_repair)

    def test_explain_case_can_be_written_to_file(self):
        text = explain_trial.explain_case(seed=1, node_count=3, candidate_limit=20)
        data = explain_trial.explain_case_json(seed=1, node_count=3, candidate_limit=20)
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "explain.md"
            json_path = Path(tmp) / "explain.json"
            md_path.write_text(text, encoding="utf-8")
            explain_trial.write_json(json_path, data)
            self.assertTrue(md_path.exists())
            self.assertTrue(json_path.exists())
            self.assertIn("1ケース説明ログ", md_path.read_text(encoding="utf-8"))
            self.assertIn("local_repair_trace", json_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
