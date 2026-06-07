import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import random_teacher_cli


class TestRandomTeacherCli(unittest.TestCase):
    def test_cli_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.json"
            argv = ["prog", "--seed", "1", "--limit", "5", "--json", str(path)]
            with patch.object(sys, "argv", argv):
                random_teacher_cli.main()
            self.assertTrue(path.exists())
            self.assertIn("random_repair", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
