import unittest

from scripts.batch_reinterpretation_breakdown_gap_report import (
    build_reinterpretation_breakdown_gap_report,
)


class BatchReinterpretationBreakdownGapReportTest(unittest.TestCase):
    def test_builds_report_with_case_gap(self):
        report = build_reinterpretation_breakdown_gap_report(
            seeds=range(2),
            limit=3,
            case_limit=1,
        )
        case = report["cases"][0]
        self.assertIn("reinterpretation_breakdown_gap", case)
        self.assertIn("score_gap", case["reinterpretation_breakdown_gap"]["gap"])


if __name__ == "__main__":
    unittest.main()
