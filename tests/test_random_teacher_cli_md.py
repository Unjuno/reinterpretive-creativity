import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import random_teacher_cli


class TestCliMd(unittest.TestCase):
    def test_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.md"
            with patch.object(sys, "argv", ["prog", "--md", str(path)]):
                random_teacher_cli.main()
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
