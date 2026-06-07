import unittest

from scripts.random_teacher_batch_smoke import run_batch


class RandomTeacherBatchSmokeTest(unittest.TestCase):
    def test_run_batch_returns_one_result_per_seed(self):
        rows = run_batch(seeds=range(2), limit=3)
        self.assertEqual([row['seed'] for row in rows], [0, 1])
        self.assertIn('reinterpretation', rows[0]['scores'])


if __name__ == '__main__':
    unittest.main()
