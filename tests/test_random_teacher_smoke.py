import unittest

from scripts import random_teacher_smoke
from scripts import run_experiments


class TestRandomTeacherSmoke(unittest.TestCase):
    def test_random_teacher_has_positive_edge(self):
        teacher = random_teacher_smoke.build_random_teacher(node_count=4, seed=0)
        self.assertTrue(any(value == 1 for value in teacher.values()))
        self.assertGreaterEqual(run_experiments.utility