import builtins
import unittest
from unittest import mock

# Mock rationale: deterministic test by mocking random.choice to return a fixed compliment.

from utils.random_compliment_generator.src.compliment import get_compliment, _COMPLIMENTS


class TestComplimentGenerator(unittest.TestCase):
    def test_get_compliment_returns_string(self):
        # Ensure the function returns a string from the list.
        result = get_compliment()
        self.assertIsInstance(result, str)
        self.assertIn(result, _COMPLIMENTS)

    @mock.patch('random.choice')
    def test_get_compliment_deterministic(self, mock_choice):
        # Force random.choice to return the first element.
        mock_choice.return_value = _COMPLIMENTS[0]
        result = get_compliment()
        self.assertEqual(result, _COMPLIMENTS[0])
        mock_choice.assert_called_once_with(_COMPLIMENTS)

    @mock.patch('builtins.print')
    @mock.patch('utils.random_compliment_generator.src.compliment.get_compliment')
    def test_cli_prints_compliment(self, mock_get, mock_print):
        mock_get.return_value = "Test compliment"
        # Import the module and invoke main directly.
        from utils.random_compliment_generator.src.compliment import main
        main()
        mock_print.assert_called_once_with("Test compliment")


if __name__ == "__main__":
    unittest.main()
