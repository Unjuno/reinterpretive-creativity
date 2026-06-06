import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestRandomTeacherCli(unittest.TestCase):
    def test_cli_accepts_seed_and_limit(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/random_teacher_cli.py",
                "--seed",
                "1",
                "--