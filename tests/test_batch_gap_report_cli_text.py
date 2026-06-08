import tempfile
import unittest
from pathlib import Path

from scripts import batch_gap_report_cli


class BatchGapReportCliTextTest(unittest.TestCase):
    def test_text_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.txt'
            batch_gap_report_cli.main(['--text', str(path)])
            self.assertIn('method:', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
