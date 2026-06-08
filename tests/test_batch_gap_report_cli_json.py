import json
import tempfile
import unittest
from pathlib import Path

from scripts import batch_gap_report_cli


class BatchGapReportCliJsonTest(unittest.TestCase):
    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'
            batch_gap_report_cli.main(['--json', str(path)])
            data = json.loads(path.read_text(encoding='utf-8'))
            self.assertIn('cases', data)


if __name__ == '__main__':
    unittest.main()
