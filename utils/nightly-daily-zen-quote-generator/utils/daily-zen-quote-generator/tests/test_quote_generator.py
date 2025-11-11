import os
import sys
import unittest
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from quote_generator import QUOTES, get_random_quote


class TestQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # A deterministic subset of quotes for testing purposes
        self.sample_quotes = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "When the mind is still, the universe surrenders.",
        ]

    @patch("quote_generator.random.choice")
    def test_random_choice_is_mocked(self, mock_choice):
        """# Mock rationale: guarantee deterministic output by mocking random.choice"""
        mock_choice.return_value = self.sample_quotes[1]
        with patch("quote_generator.QUOTES", self.sample_quotes):
            result = get_random_quote()
            self.assertEqual(result, self.sample_quotes[1])
            mock_choice.assert_called_once()

    def test_max_length_filter_returns_expected(self):
        """# Mock rationale: filter leaves a single candidate, making random.choice deterministic"""
        # Only the first quote is <= 50 characters
        with patch("quote_generator.QUOTES", self.sample_quotes):
            result = get_random_quote(max_length=50)
            self.assertEqual(result, self.sample_quotes[0])

    def test_no_match_raises_value_error(self):
        """# Mock rationale: verify proper error handling when filter excludes all quotes"""
        with self.assertRaises(ValueError):
            get_random_quote(max_length=10)


if __name__ == "__main__":
    unittest.main()
