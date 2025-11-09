import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a known value so the test is deterministic and offline.

from utils.random-compliment-generator.src.compliment import get_random_compliment, _COMPLIMENTS

class TestRandomCompliment(unittest.TestCase):
    def test_return_type(self):
        """Ensure the function returns a string from the list without mocking."""
        result = get_random_compliment()
        self.assertIsInstance(result, str)
        self.assertIn(result, _COMPLIMENTS)

    @patch('random.choice')
    def test_deterministic_output(self, mock_choice):
        """When `random.choice` is mocked, the function should return the mocked value.

        This guarantees test repeatability.
        """
        mock_choice.return_value = _COMPLIMENTS[0]
        result = get_random_compliment()
        mock_choice.assert_called_once_with(_COMPLIMENTS)
        self.assertEqual(result, _COMPLIMENTS[0])

if __name__ == '__main__':
    unittest.main()
