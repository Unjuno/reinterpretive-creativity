import json
import tempfile
import unittest
from pathlib import Path

from scripts import batch_gap_report_cli


class BatchGapReportCliBasisTest(unittest.TestCase):
    def test_basis_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'
            batch_gap_report_cli.main(['--basis', '--json', str(path)])
            data = json.loads(path.read_text(encoding='utf-8'))
            self.assertIn('explanation_basis', data)


if __name__ == '__main__':
    unittest.main()
