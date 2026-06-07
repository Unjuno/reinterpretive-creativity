import unittest

from scripts.random_teacher_win_counts import win_counts


class RandomTeacherWinCountsTest(unittest.TestCase):
    def test_counts_best_method_per_row(self):
        rows = [
            {'seed': 0, 'scores': {'a': 1.0, 'b': 2.0}},
            {'seed': 1, 'scores': {'a': 3.0, 'b': 2.0}},
        ]
        self.assertEqual(win_counts(rows), {'a': 1, 'b': 1})


if __name__ == '__main__':
    unittest.main()
