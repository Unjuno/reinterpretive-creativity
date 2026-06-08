import unittest

from scripts.report_explanation_basis import attach_explanation_basis


class ReportExplanationBasisTest(unittest.TestCase):
    def test_attach_explanation_basis(self):
        report = {'cases': [{'seed': 0, 'method': 'm', 'gap': 1.0}]}
        out = attach_explanation_basis(report)
        self.assertEqual(out['explanation_basis'][0]['basis'], 'score_gap')


if __name__ == '__main__':
    unittest.main()
