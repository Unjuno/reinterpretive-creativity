from pathlib import Path
import tempfile
import unittest

from scripts import random_teacher_output


class TestRandomTeacherOutput(unittest.TestCase):
    def test_build_has_scores(self):
        data = random_teacher_output.build(seed=0, limit=10)
        self.assertIn("scores", data)
        self.assertEqual(set(data["scores"]), {"random_repair", "random_search", "local_repair", "reinterpretation