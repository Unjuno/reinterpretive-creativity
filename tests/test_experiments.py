from pathlib import Path
import tempfile
import unittest

from scripts import run_experiments


class TestExperiments(unittest.TestCase):
    def test_noisy_case_always_has_conflict(self):
        for seed in range(10):
            _, raw = run_experiments.noisy_case(seed, node_count=3)
            self.assertTrue(any(values == {1, -1} for values in raw.values()))

    def test_utility_components_are_bounded(self):
        teacher, _ = run_experiments.noisy_case(seed=0, node_count=3)
        components = run_experiments.utility_components(teacher)
        for value in (
            components.density_score,
            components.node_coverage_score,
            components.weak_connectivity_score,
            components.in_out_coverage_score,
            components.utility,
        ):
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_empty_positive_structure_has_zero_utility(self):
        nodes = run_experiments.make_nodes(3)
        empty = {edge: 0 for edge in run_experiments.all_edges(nodes)}
        self.assertEqual(run_experiments.utility_proxy(empty), 0.0)

    def test_cycle_teacher_has_high_structural_utility(self):
        nodes = run_experiments.make_nodes(3)
        teacher = run_experiments.build_cycle_teacher(nodes)
        self.assertGreaterEqual(run_experiments.utility_proxy(teacher), 0.9)

    def test_trial_result_is_valid(self):
        result = run_experiments.run_trial(0, node_count=3)
        self.assertEqual(result.node_count, 3)
        self.assertGreaterEqual(result.random_repair_score, 0.0)
        self.assertGreaterEqual(result.random_search_score, 0.0)
        self.assertGreaterEqual(result.local_repair_score, 0.0)
        self.assertGreaterEqual(result.reinterpretation_score, 0.0)

    def test_summary_is_valid(self):
        results = [run_experiments.run_trial(seed, node_count=3) for seed in range(5)]
        summary = run_experiments.summarize(3, results)
        self.assertEqual(summary.node_count, 3)
        self.assertEqual(summary.trials, 5)
        self.assertGreaterEqual(summary.win_rate_vs_random_repair, 0.0)
        self.assertLessEqual(summary.win_rate_vs_random_repair, 1.0)
        self.assertGreaterEqual(summary.win_rate_vs_random_search, 0.0)
        self.assertLessEqual(summary.win_rate_vs_random_search, 1.0)
        self.assertGreaterEqual(summary.win_rate_vs_local_repair, 0.0)
        self.assertLessEqual(summary.win_rate_vs_local_repair, 1.0)

    def test_reinterpretation_not_worse_than_single_random_repair_on_small_batch(self):
        _, summaries = run_experiments.run_suite(node_counts=(3,), trials=10, candidate_limit=200)
        summary = summaries[0]
        self.assertGreaterEqual(summary.reinterpretation_mean, summary.random_repair_mean)

    def test_local_repair_search_is_measured(self):
        _, summaries = run_experiments.run_suite(node_counts=(4,), trials=5, candidate_limit=100)
        summary = summaries[0]
        self.assertGreaterEqual(summary.local_repair_mean, 0.0)
        self.assertIsInstance(summary.improvement_vs_local_repair_mean, float)

    def test_stronger_random_search_is_measured(self):
        _, summaries = run_experiments.run_suite(node_counts=(4,), trials=5, candidate_limit=100)
        summary = summaries[0]
        self.assertGreaterEqual(summary.random_search_mean, 0.0)
        self.assertIsInstance(summary.improvement_vs_random_search_mean, float)

    def test_multiple_node_counts(self):
        results, summaries = run_experiments.run_suite(node_counts=(3, 4, 5), trials=3, candidate_limit=50)
        self.assertEqual(len(summaries), 3)
        self.assertEqual({summary.node_count for summary in summaries}, {3, 4, 5})
        self.assertEqual(len(results), 9)

    def test_json_and_csv_outputs(self):
        results, summaries = run_experiments.run_suite(node_counts=(3,), trials=3, candidate_limit=50)
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "result.json"
            csv_path = Path(tmp) / "result.csv"
            run_experiments.write_json(json_path, results, summaries)
            run_experiments.write_csv(csv_path, results)
            self.assertTrue(json_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertIn("summaries", json_path.read_text(encoding="utf-8"))
            csv_text = csv_path.read_text(encoding="utf-8")
            self.assertIn("random_search_score", csv_text)
            self.assertIn("local_repair_score", csv_text)


if __name__ == "__main__":
    unittest.main()
