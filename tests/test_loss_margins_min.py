import unittest

from scripts.loss_margins import loss_margins


class LossMarginsTest(unittest.TestCase):
    def test_returns_positive_loss_margin(self):
        rows = [{'seed': 1, 'scores': {'reinterpretation': 1.0, 'other': 1.5}}]
        self.assertEqual(loss_margins(rows), [{'seed': 1, 'best_method': 'other', 'margin': 0.5}])


if __name__ == '__main__':
    unittest.main()
