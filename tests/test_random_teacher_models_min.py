import unittest

from scripts.random_teacher_models import run_smoke_with_models


class RandomTeacherModelsTest(unittest.TestCase):
    def test_returns_scores_and_models(self):
        out = run_smoke_with_models(seed=0, limit=3)
        self.assertIn('teacher', out)
        self.assertIn('raw', out)
        self.assertIn('reinterpretation', out['results'])
        self.assertIn('score', out['results']['reinterpretation'])
        self.assertIn('model', out['results']['reinterpretation'])


if __name__ == '__main__':
    unittest.main()
