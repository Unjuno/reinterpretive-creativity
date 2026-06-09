import unittest

from scripts.random_teacher_reinterpretation_gap import run_smoke_with_reinterpretation_gap


class RandomTeacherReinterpretationGapTest(unittest.TestCase):
    def test_adds_reinterpretation_gap(self):
        out = run_smoke_with_reinterpretation_gap(seed=0, limit=3)
        gap = out["reinterpretation_breakdown_gap"]
        self.assertEqual(gap["target_method"], "reinterpretation")
        self.assertIn("winner_method", gap)
        self.assertIn("score_gap", gap["gap"])


if __name__ == "__main__":
    unittest.main()
