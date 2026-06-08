import tempfile
import unittest
from pathlib import Path

from scripts.gap_report_markdown import write_markdown


class GapReportMarkdownTest(unittest.TestCase):
    def test_write_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.md'
            write_markdown(path, {'method': 'x', 'limit': 1, 'cases': []})
            self.assertIn('method: x', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
