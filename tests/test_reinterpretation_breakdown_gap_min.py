import unittest

from scripts.reinterpretation_breakdown_gap import reinterpretation_breakdown_gap


class ReinterpretationBreakdownGapTest(unittest.TestCase):
    def test_reports_winner_gap(self):
        data = {
            "results": {
                "reinterpretation": {
                    "score": 0.1,
                    "breakdown": {
                        "distance": 0.2,
                        "preservation": 0.5,
                        "utility_proxy": 0.4,
                        "score": 0.1,
                    },
                },
                "other": {
                    "score": 0.2,
                    "breakdown": {
                        "distance": 0.3,
                        "preservation": 0.6,
                        "utility_proxy": 0.5,
                        "score": 0.2,
                    },
                },
            }
        }
        out = reinterpretation_breakdown_gap(data)
        self.assertEqual(out["target_method"], "reinterpretation")
        self.assertEqual(out["winner_method"], "other")
        self.assertIn("utility_proxy_gap", out["gap"])


if __name__ == "__main__":
    unittest.main()
