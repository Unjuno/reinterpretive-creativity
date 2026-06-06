import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestRandomTeacherCli(unittest.TestCase):
    def test_cli_accepts_seed_and_limit(self):
        result = subprocess.run([sys.executable, "scripts/random_teacher_cli.py", "--seed", "1", "--limit", "5"], check=True, capture_output=True, text=True)
        self.assertIn("random_repair", result.stdout)
        self.assertIn("reinterpretation", result.stdout)

    def test_cli_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.json"
            subprocess.run([sys.executable, "