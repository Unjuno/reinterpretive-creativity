import unittest

from scripts.top_losses import top_losses


class TopLossesTest(unittest.TestCase):
    def test_returns_largest_losses_first(self):
        rows = [
            {'seed': 0, 'scores': {'reinterpretation': 1.0, 'other': 1.2}},
            {'seed': 1, 'scores': {'reinterpretation': 1.0, 'other': 2.0}},
        ]
        self.assertEqual(top_losses(rows, limit=1), [{'seed': 1, 'best_method': 'other', 'margin': 1.0}])


if __name__ == '__main__':
    unittest.main()
