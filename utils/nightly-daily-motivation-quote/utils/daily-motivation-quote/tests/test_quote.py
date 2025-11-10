import unittest
import sys
import os
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Mock rationale: we replace random.choice to return a deterministic element,
# ensuring the test does not depend on actual randomness.
from quote import get_random_quote, format_quote, QUOTES


class TestDailyMotivationQuote(unittest.TestCase):
    def test_get_random_quote_no_category(self):
        with patch("random.choice", return_value=QUOTES[0]) as mock_choice:
            quote = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(quote, QUOTES[0])

    def test_get_random_quote_with_category(self):
        humor_quotes = [q for q in QUOTES if q["category"] == "humor"]
        with patch("random.choice", return_value=humor_quotes[0]) as mock_choice:
            quote = get_random_quote(category="humor")
            mock_choice.assert_called_once()
            self.assertEqual(quote["category"], "humor")

    def test_get_random_quote_invalid_category(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(category="nonexistent")
        self.assertIn("No quotes found for category", str(ctx.exception))

    def test_format_quote(self):
        quote = {
            "text": "Test quote",
            "author": "Tester",
            "category": "wisdom",
        }
        formatted = format_quote(quote)
        self.assertTrue(formatted.startswith("🧠"))
        self.assertIn('"Test quote" – Tester', formatted)


if __name__ == "__main__":
    unittest.main()
