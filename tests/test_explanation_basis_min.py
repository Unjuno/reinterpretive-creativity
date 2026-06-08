import unittest

from scripts.explanation_basis import explanation_basis


class ExplanationBasisTest(unittest.TestCase):
    def test_builds_basis_without_causal_reason(self):
        basis = explanation_basis({'seed': 1, 'method': 'reinterpretation', 'gap': 0.5})
        self.assertEqual(basis['claim'], 'target_method_lost')
        self.assertEqual(basis['basis'], 'score_gap')
        self.assertIn('not a causal reason', basis['note'])


if __name__ == '__main__':
    unittest.main()
