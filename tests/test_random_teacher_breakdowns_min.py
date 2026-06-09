import unittest

from scripts.random_teacher_breakdowns import run_smoke_with_breakdowns


class RandomTeacherBreakdownsTest(unittest.TestCase):
    def test_adds_breakdowns(self):
        out = run_smoke_with_breakdowns(seed=0, limit=3)
        item = out['results']['reinterpretation']
        self.assertIn('breakdown', item)
        self.assertIn('utility_proxy', item['breakdown'])


if __name__ == '__main__':
    unittest.main()
