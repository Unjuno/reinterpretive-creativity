import unittest

from scripts.score_gap import score_gap


class ScoreGapTest(unittest.TestCase):
    def test_reports_best_score_and_gap(self):
        row = {'seed': 2, 'scores': {'reinterpretation': 1.0, 'other': 1.5}}
        self.assertEqual(
            score_gap(row),
            {
                'seed': 2,
                'method': 'reinterpretation',
                'method_score': 1.0,
                'best_method': 'other',
                'best_score': 1.5,
                'gap': 0.5,
            },
        )


if __name__ == '__main__':
    unittest.main()
