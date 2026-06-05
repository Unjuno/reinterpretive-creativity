import unittest

from scripts import random_teacher_experiments


class TestRandomTeacherExperiments(unittest.TestCase):
    def test_run_smoke_returns_four_scores(self):
        result = random_teacher_experiments.run_smoke(seed=0, limit=10)
        self.assertEqual(
            set(result),
            {"random_repair", "random_search", "local_repair", "reinterpretation"},
        )
        for value in result.values():
            self.assertGreaterEqual(value, 0.0)

