import unittest
from scripts import random_teacher_smoke

class TestRandomTeacherSmoke(unittest.TestCase):
    def test_positive_edge(self):
        t = random_teacher_smoke.build_random_teacher(4, 0)
        self.assertTrue(any(v == 1 for v in t.values()))

if __name__ == "__main__":
    unittest.main()
