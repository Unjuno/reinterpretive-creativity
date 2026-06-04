from pathlib import Path
import tempfile
import unittest

from scripts import select_cases


class TestSelectCases(unittest.TestCase):
    def test_collect_and_select_representative_cases(self):
        cases = select_cases.collect_cases(node_counts=(3,), trials=3, candidate_limit=20)
        self.assertEqual(len(cases), 3)
        selected = select_cases.select_representative_cases(cases)
        self.assertIn("再解釈探索が最も有利なケース", selected)
        self.assertIn("局所修復探索が最も有利なケース", selected)
        self.assertIn("ランダム探索が最も有利なケース", selected)
        self.assertIn("差が最も小さいケース", selected)
        for value in selected.values():
            self.assertEqual(len(value), 3)

    def test_representative_cases_avoid_duplicate_keys_when_possible(self):
        cases = select_cases.collect_cases(node_counts=(3, 4), trials=3, candidate_limit=20)
        selected = select_cases.select_representative_cases(cases)
        keys = [case.key for case, _, _ in selected.values()]
        self.assertEqual(len(keys), len(set(keys)))

    def test_summary_markdown_contains_core_table(self):
        cases = select_cases.collect_cases(node_counts=(3,), trials=3, candidate_limit=20)
        selected = select_cases.select_representative_cases(cases)
        text = select_cases.summary_markdown(
            selected=selected,
            node_counts=(3,),
            trials=3,
            candidate_limit=20,
        )
        self.assertIn("# 代表ケース抽出サマリ", text)
        self.assertIn("再解釈探索が最も有利なケース", text)
        self.assertIn("case_key", text)
        self.assertIn("duplicate_allowed", text)

    def test_representative_cases_json_contains_core_fields(self):
        cases = select_cases.collect_cases(node_counts=(3,), trials=3, candidate_limit=20)
        selected = select_cases.select_representative_cases(cases)
        data = select_cases.representative_cases_json(
            selected=selected,
            node_counts=(3,),
            trials=3,
            candidate_limit=20,
        )
        self.assertIn("metadata", data)
        self.assertIn("representative_cases", data)
        self.assertEqual(data["metadata"]["node_counts"], [3])
        self.assertEqual(data["metadata"]["dedupe_key"], "node_count/seed")
        first_case = data["representative_cases"][0]
        self.assertIn("label", first_case)
        self.assertIn("case_key", first_case)
        self.assertIn("scores", first_case)
        self.assertIn("duplicate_allowed", first_case)

    def test_write_outputs_with_logs_and_json(self):
        cases = select_cases.collect_cases(node_counts=(3,), trials=3, candidate_limit=20)
        selected = select_cases.select_representative_cases(cases)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "summary.md"
            json_output = Path(tmp) / "summary.json"
            logs_dir = Path(tmp) / "logs"
            select_cases.write_outputs(
                selected=selected,
                output=output,
                logs_dir=logs_dir,
                node_counts=(3,),
                trials=3,
                candidate_limit=20,
                json_output=json_output,
            )
            self.assertTrue(output.exists())
            self.assertTrue(json_output.exists())
            self.assertIn("代表ケース", output.read_text(encoding="utf-8"))
            self.assertIn("representative_cases", json_output.read_text(encoding="utf-8"))
            self.assertTrue(any(logs_dir.glob("*.md")))


if __name__ == "__main__":
    unittest.main()
