import unittest

from scripts import simulate


class TestSimulation(unittest.TestCase):
    def test_initial_model_has_conflict(self):
        raw = simulate.build_initial_conflicts()
        self.assertTrue(simulate.has_conflict(raw))

    def test_teacher_and_initial_are_defined(self):
        teacher = simulate.build_teacher()
        raw = simulate.build_initial_conflicts()
        initial = simulate.to_model(raw)
        self.assertEqual(len(teacher), len(simulate.EDGES))
        self.assertEqual(len(initial), len(simulate.EDGES))

    def test_best_reinterpretation_differs_from_teacher(self):
        teacher = simulate.build_teacher()
        raw = simulate.build_initial_conflicts()
        best_score, best_model = simulate.best_reinterpretation(teacher, raw)
        self.assertGreaterEqual(best_score, 0.0)
        self.assertTrue(simulate.differs(best_model, teacher))

    def test_reinterpretation_not_worse_than_seeded_random_demo(self):
        teacher = simulate.build_teacher()
        raw = simulate.build_initial_conflicts()
        random_score, _ = simulate.random_repair(teacher, raw, seed=42)
        best_score, _ = simulate.best_reinterpretation(teacher, raw)
        self.assertGreaterEqual(best_score, random_score)


if __name__ == "__main__":
    unittest.main()
