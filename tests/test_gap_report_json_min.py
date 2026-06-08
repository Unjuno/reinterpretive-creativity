import json
import tempfile
import unittest
from pathlib import Path

from scripts.gap_report_json import write_json


class GapReportJsonTest(unittest.TestCase):
    def test_write_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'
            write_json(path, {'method': 'x', 'cases': []})
            self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['method'], 'x')


if __name__ == '__main__':
    unittest.main()
