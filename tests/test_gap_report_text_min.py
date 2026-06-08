import tempfile
import unittest
from pathlib import Path

from scripts.gap_report_text import write_text


class GapReportTextTest(unittest.TestCase):
    def test_write_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.txt'
            write_text(path, {'method': 'x'})
            self.assertIn('method: x', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
