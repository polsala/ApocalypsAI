import unittest
from unittest.mock import patch

# Mock rationale: We patch ``random.choice`` to return a deterministic value
# so the test does not depend on actual randomness.

from src.compliment import get_compliment

class TestComplimentGenerator(unittest.TestCase):
    def test_unfiltered_compliment(self):
        with patch('random.choice', return_value='Mocked compliment') as mock_choice:
            result = get_compliment()
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Mocked compliment')

    def test_known_category(self):
        with patch('random.choice', return_value='Creative mock') as mock_choice:
            result = get_compliment('creative')
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Creative mock')

    def test_unknown_category_falls_back(self):
        with patch('random.choice', return_value='Fallback mock') as mock_choice:
            result = get_compliment('nonexistent')
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Fallback mock')

    def test_category_case_insensitivity(self):
        with patch('random.choice', return_value='Case mock') as mock_choice:
            result = get_compliment('TeChNiCaL')
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Case mock')

if __name__ == '__main__':
    unittest.main()
