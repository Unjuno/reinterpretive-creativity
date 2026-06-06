import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestRandomTeacherCli(unittest.TestCase):
    def test_cli_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.json"
            subprocess.run([sys.executable, "scripts/random_teacher_cli.py", "--seed", "1", "--limit", "5", "--json",