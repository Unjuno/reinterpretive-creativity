import unittest

from scripts.score_breakdown import score_breakdown


class ScoreBreakdownTest(unittest.TestCase):
    def test_score_is_product(self):
        teacher = {('A', 'B'): 1, ('B', 'A'): 0}
        candidate = {('A', 'B'): 0, ('B', 'A'): 1}
        raw = {('B', 'A'): {1}}
        out = score_breakdown(candidate, teacher, raw)
        self.assertEqual(out['score'], out['distance'] * out['preservation'] * out['utility_proxy'])


if __name__ == '__main__':
    unittest.main()
