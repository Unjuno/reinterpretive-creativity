import unittest

from scripts import run_experiments


class TestExperiments(unittest.TestCase):
    def test_noisy_case_always_has_conflict(self):
        for seed in range(10):
            _, raw = run_experiments.noisy_case(seed)
            self.assertTrue(any(values == {1, -1} for values in raw.values()))

    def test_trial_result_is_valid(self):
        result = run_experiments.run_trial(0)
        self.assertGreaterEqual(result.random_score, 0.0)
        self.assertGreaterEqual(result.reinterpretation_score, 0.0)

    def test_summary_is_valid(self):
        results = [run_experiments.run_trial(seed) for seed in range(5)]
        summary = run_experiments.summarize(results)
        self.assertEqual(summary.trials, 5)
        self.assertGreaterEqual(summary.win_rate, 0.0)
        self.assertLessEqual(summary.win_rate, 1.0)

    def test_reinterpretation_not_worse_on_small_batch(self):
        results = [run_experiments.run_trial(seed) for seed in range(10)]
        summary = run_experiments.summarize(results)
        self.assertGreaterEqual(summary.reinterpretation_mean, summary.random_mean)


if __name__ == "__main__":
    unittest.main()
