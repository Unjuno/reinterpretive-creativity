import unittest

from scripts.score_gap import score_gap


class ScoreGapTest(unittest.TestCase):
    def test_reports_score_gap(self):
        row = {'seed': 2, 'scores': {'reinterpretation': 1.0, 'other': 1.5}}
        self.assertEqual(score_gap(row)['gap'], 0.5)
        self.assertEqual(score_gap(row)['best_method'], 'other')


if __name__ == '__main__':
    unittest.main()
