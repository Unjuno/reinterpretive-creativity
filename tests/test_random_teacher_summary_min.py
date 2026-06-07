import unittest

from scripts.random_teacher_batch_smoke import summarize


class RandomTeacherSummaryTest(unittest.TestCase):
    def test_summarize_returns_means(self):
        rows = [
            {'seed': 0, 'scores': {'x': 1.0}},
            {'seed': 1, 'scores': {'x': 3.0}},
        ]
        self.assertEqual(summarize(rows), {'x': 2.0})


if __name__ == '__main__':
    unittest.main()
