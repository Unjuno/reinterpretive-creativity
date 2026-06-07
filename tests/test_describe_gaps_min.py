import unittest

from scripts.describe_gaps import describe_gaps


class DescribeGapsTest(unittest.TestCase):
    def test_describes_top_loss(self):
        rows = [
            {'seed': 0, 'scores': {'reinterpretation': 1.0, 'other': 2.0}},
            {'seed': 1, 'scores': {'reinterpretation': 1.5, 'other': 1.6}},
        ]
        out = describe_gaps(rows, limit=1)
        self.assertEqual(out[0]['seed'], 0)
        self.assertEqual(out[0]['gap'], 1.0)


if __name__ == '__main__':
    unittest.main()
