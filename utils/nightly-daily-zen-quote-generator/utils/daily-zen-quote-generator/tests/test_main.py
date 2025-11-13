import unittest
from unittest.mock import patch

# Mock rationale: ensure deterministic output by mocking random.choice to return the first eligible quote.

from src.main import get_random_quote, _filter_by_theme

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_filter_by_theme_existing(self):
        quotes = [
            {"text": "A", "tags": ["mindfulness"]},
            {"text": "B", "tags": ["nature"]},
        ]
        filtered = _filter_by_theme(quotes, "nature")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["text"], "B")

    def test_filter_by_theme_none(self):
        quotes = [{"text": "A", "tags": ["mindfulness"]}]
        self.assertEqual(_filter_by_theme(quotes, None), quotes)

    def test_filter_by_theme_no_match(self):
        quotes = [{"text": "A", "tags": ["mindfulness"]}]
        filtered = _filter_by_theme(quotes, "nonexistent")
        self.assertEqual(filtered, [])

    @patch('random.choice')
    def test_get_random_quote_no_theme(self, mock_choice):
        # Force deterministic selection of the first quote
        mock_choice.side_effect = lambda seq: seq[0]
        quote = get_random_quote()
        self.assertIsInstance(quote, str)
        # The first quote in the built‑in list is known
        self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    @patch('random.choice')
    def test_get_random_quote_with_theme(self, mock_choice):
        mock_choice.side_effect = lambda seq: seq[0]
        quote = get_random_quote(theme="nature")
        # First nature‑tagged quote in the list
        self.assertEqual(quote, "A flower does not think of competing with the flower next to it. It just blooms.")

    def test_get_random_quote_invalid_theme(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(theme="unknown")
        self.assertIn("No quotes found for theme", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
