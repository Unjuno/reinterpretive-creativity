from pathlib import Path
import tempfile
import unittest

from scripts import random_teacher_output as r


class TestRandomTeacherOutput(unittest.TestCase):
    def test_output_files(self):
        data = r.build(seed=0, limit=10)
        self.assertEqual(set(data["scores"]), {"random_repair", "random_search", "local_repair", "reinterpretation"})
        with tempfile