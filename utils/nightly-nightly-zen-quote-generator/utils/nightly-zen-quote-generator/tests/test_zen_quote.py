import sys
import pathlib
import unittest
from unittest import mock

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from zen_quote import get_random_quote, Quote

class TestZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_with_seed(self):
        # Using a fixed seed should always return the same quote
        quote = get_random_quote(seed=42)
        self.assertIsInstance(quote, Quote)
        # Expected quote determined by Python's random with seed 42
        self.assertEqual(quote.text, "Let go or be dragged.")
        self.assertEqual(quote.author, "Zen Proverb")

    @mock.patch("zen_quote.random.choice")
    def test_random_choice_mock(self, mock_choice):
        # # Mock rationale: ensure get_random_quote uses random.choice internally.
        mock_choice.return_value = Quote(text="Mocked quote", author="Mock Author")
        quote = get_random_quote()
        mock_choice.assert_called_once()
        self.assertEqual(quote.text, "Mocked quote")
        self.assertEqual(quote.author, "Mock Author")

if __name__ == "__main__":
    unittest.main()
