import unittest

from scripts.breakdown_gap import breakdown_gap


class BreakdownGapTest(unittest.TestCase):
    def test_reports_component_gaps(self):
        target = {'breakdown': {'distance': 0.2, 'preservation': 0.5, 'utility_proxy': 0.4, 'score': 0.04}}
        winner = {'breakdown': {'distance': 0.3, 'preservation': 0.7, 'utility_proxy': 0.6, 'score': 0.12}}
        out = breakdown_gap(target, winner)
        self.assertAlmostEqual(out['score_gap'], 0.08)
        self.assertAlmostEqual(out['preservation_gap'], 0.2)


if __name__ == '__main__':
    unittest.main()
