import unittest

from scripts.gap_report import gap_report


class GapReportTest(unittest.TestCase):
    def test_wraps_described_cases(self):
        rows = [
            {'seed': 0, 'scores': {'reinterpretation': 1.0, 'other': 2.0}},
        ]
        report = gap_report(rows, limit=1)
        self.assertEqual(report['method'], 'reinterpretation')
        self.assertEqual(report['limit'], 1)
        self.assertEqual(report['cases'][0]['gap'], 1.0)


if __name__ == '__main__':
    unittest.main()
