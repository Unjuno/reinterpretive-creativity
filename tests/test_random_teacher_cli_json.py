import tempfile
import unittest
from pathlib import Path
from scripts import random_teacher_output as r


class TestRandomTeacherCliJson(unittest.TestCase):
    def test_write_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'out.json'
            r.write_json(path, r.build(1, 5))
            self.assertTrue(path.exists())
            self.assert