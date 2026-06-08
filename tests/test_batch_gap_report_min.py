import unittest

from scripts.batch_gap_report import build_report


class BatchGapReportTest(unittest.TestCase):
    def test_build_report_has_cases(self):
        report = build_report(seeds=range(2), limit=3, case_limit=1)
        self.assertEqual(report['method'], 'reinterpretation')
        self.assertEqual(report['limit'], 1)
        self.assertIn('cases', report)


if __name__ == '__main__':
    unittest.main()
