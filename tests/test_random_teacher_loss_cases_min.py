import unittest
from scripts.random_teacher_loss_cases import loss_cases

class T(unittest.TestCase):
    def test_loss_cases(self):
        rows = [
            {'scores': {'reinterpretation': 1.0, 'other': 2.0}},
            {'scores': {'reinterpretation': 3.0, 'other': 2.0}},
        ]
        self.assertEqual(loss_cases(rows), [rows[0]])

if __name__ == '__main__':
    unittest.main()
