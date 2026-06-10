import unittest

from scripts import general_random_teacher as grt
from scripts import run_experiments as exp


class TestGeneralRandomTeacher(unittest.TestCase):
    def test_random_graph_teacher_positive_edge_count(self):
        teacher = grt.build_random_graph_teacher(
            node_count=4,
            positive_edge_count=4,
            seed=0,
        )
        self.assertEqual(grt.positive_edge_count(teacher), 4)
        self.assertEqual(len(teacher), len(exp.all_edges(exp.make_nodes(4))))

    def test_random_graph_teacher_is_deterministic(self):
        first = grt.build_random_graph_teacher(4, 4, seed=7)
        second = grt.build_random_graph_teacher(4, 4, seed=7)
        third = grt.build_random_graph_teacher(4, 4, seed=8)
        self.assertEqual(first, second)
        self.assertNotEqual(first, third)

    def test_random_graph_teacher_rejects_invalid_positive_count(self):
        with self.assertRaises(ValueError):
            grt.build_random_graph_teacher(4, 0, seed=0)
        with self.assertRaises(ValueError):
            grt.build_random_graph_teacher(4, 13, seed=0)

    def test_noisy_raw_from_random_teacher_has_conflict(self):
        for seed in range(10):
            teacher = grt.build_random_graph_teacher(4, 4, seed=seed)
            raw = grt.make_noisy_raw_from_teacher(teacher, seed=seed)
            self.assertTrue(exp.has_conflict(raw))
            self.assertGreaterEqual(grt.raw_edge_count(raw), grt.conflict_edge_count(raw))

    def test_run_methods_returns_standard_scores(self):
        teacher = grt.build_random_graph_teacher(4, 4, seed=0)
        raw = grt.make_noisy_raw_from_teacher(teacher, seed=0)
        scores = grt.run_methods(teacher, raw, seed=0, candidate_limit=5)
        self.assertEqual(
            set(scores),
            {"random_repair", "random_search", "local_repair", "reinterpretation"},
        )
        for score in scores.values():
            self.assertGreaterEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
