import unittest

from scripts.random_teacher_loss_cases import loss_cases


class RandomTeacherLossCasesTest(unittest.TestCase):
    def test_returns_rows_where_method_is_not_best(self):
        rows = [
            {'seed': 0, 'scores': {'reinterpretation': 1.0, 'other': 2.0}},
            {'seed': 1, 'scores': {'reinterpretation': 3.0, 'other': 2.0}},
        ]
        self.assertEqual(loss_cases(rows), [rows[0]])


if __name__ == '__main__':
    unittest.main()
