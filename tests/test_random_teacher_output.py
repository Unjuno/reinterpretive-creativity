import unittest

from scripts import random_teacher_output as r


class TestRandomTeacherOutput(unittest.TestCase):
    def test_build_has_four_scores(self):
        data = r.build(seed=0, limit=10)
        keys = {"random_repair", "random_search", "local_repair", "reinterpretation"}
        self.assertEqual(set(data["scores"]), keys)


if __name__ == "__main__":
    unittest.main()
