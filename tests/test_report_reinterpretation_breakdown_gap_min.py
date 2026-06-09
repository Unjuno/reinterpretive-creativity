import unittest

from scripts.gap_report import gap_report
from scripts.report_reinterpretation_breakdown_gap import attach_reinterpretation_breakdown_gap


class ReportReinterpretationBreakdownGapTest(unittest.TestCase):
    def test_attaches_gap_to_cases(self):
        rows = [
            {"seed": 0, "scores": {"reinterpretation": 1.0, "other": 2.0}},
        ]
        report = gap_report(rows, limit=1)
        out = attach_reinterpretation_breakdown_gap(report, trial_limit=3)
        gap = out["cases"][0]["reinterpretation_breakdown_gap"]
        self.assertEqual(gap["target_method"], "reinterpretation")
        self.assertIn("score_gap", gap["gap"])


if __name__ == "__main__":
    unittest.main()
