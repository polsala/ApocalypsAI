import unittest
from unittest.mock import patch

# Mock rationale: we import the module directly; no network or file I/O occurs.
from utils.random_compliment_generator.src.compliment import get_compliment, _flatten, COMPLIMENTS

class TestComplimentUtility(unittest.TestCase):
    def test_flatten_all(self):
        all_compliments = _flatten()
        expected = [c for cat in COMPLIMENTS.values() for c in cat]
        self.assertCountEqual(all_compliments, expected)

    def test_flatten_specific(self):
        work_compliments = _flatten(["work"])
        self.assertCountEqual(work_compliments, COMPLIMENTS["work"])

    def test_flatten_invalid_category(self):
        with self.assertRaises(ValueError):
            _flatten(["nonexistent"])

    @patch('random.choice', return_value='Mocked compliment')
    def test_get_compliment_no_category(self, mock_choice):
        # Ensure deterministic output via mock
        result = get_compliment()
        mock_choice.assert_called_once()
        self.assertEqual(result, 'Mocked compliment')

    @patch('random.choice', return_value='Mocked coding compliment')
    def test_get_compliment_with_category(self, mock_choice):
        result = get_compliment('coding')
        mock_choice.assert_called_once()
        self.assertEqual(result, 'Mocked coding compliment')

    def test_get_compliment_invalid_category(self):
        with self.assertRaises(ValueError):
            get_compliment('invalid')

if __name__ == '__main__':
    unittest.main()
