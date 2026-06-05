from pathlib import Path
import tempfile
import unittest

from scripts import sensitivity_candidate_limit


class TestCandidateLimitSensitivity(unittest.TestCase):
    def test_run_sensitivity_returns_summaries(self):
        summaries = sensitivity_candidate_limit.run_sensitivity(
            node_counts=(4,),
            trials=2,
            candidate_limits=(10, 20),
        )
        self.assertEqual(len(summaries), 2)
        self.assertEqual({summary.candidate_limit for summary in summaries}, {10, 20})
        self.assertTrue(all(summary.node_count == 4 for summary in summaries))

    def test_format_summary_contains_core_columns(self):
        summaries = sensitivity_candidate_limit.run_sensitivity(
            node_counts=(4,),
            trials=2,
            candidate_limits=(10,),
        )
        text = sensitivity_candidate_limit.format_summary(summaries)
        self.assertIn("# candidate_limit 感度分析", text)
        self.assertIn("candidate_limit", text)
        self.assertIn("ランダム探索平均", text)
        self.assertIn("局所修復平均", text)
        self.assertIn("再解釈平均", text)

    def test_write_outputs(self):
        summaries = sensitivity_candidate_limit.run_sensitivity(
            node_counts=(4,),
            trials=2,
            candidate_limits=(10,),
        )
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "sensitivity.md"
            json_path = Path(tmp) / "sensitivity.json"
            csv_path = Path(tmp) / "sensitivity.csv"
            sensitivity_candidate_limit.write_markdown(md_path, summaries)
            sensitivity_candidate_limit.write_json(
                json_path,
                summaries,
                node_counts=(4,),
                trials=2,
                candidate_limits=(10,),
            )
            sensitivity_candidate_limit.write_csv(csv_path, summaries)
            self.assertTrue(md_path.exists())
            self.assertTrue(json_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertIn("candidate_limit", md_path.read_text(encoding="utf-8"))
            self.assertIn("summaries", json_path.read_text(encoding="utf-8"))
            self.assertIn("candidate_limit", csv_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
