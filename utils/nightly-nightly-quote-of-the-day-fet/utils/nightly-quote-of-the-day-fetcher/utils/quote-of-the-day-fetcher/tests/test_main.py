import unittest
from unittest.mock import patch

from quote_of_the_day_fetcher.src.main import get_quote


class TestQuoteFetcher(unittest.TestCase):
    def test_get_quote_no_tag(self):
        # Mock random.choice to always return the first element for deterministic output
        with patch('quote_of_the_day_fetcher.src.main.random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # Mock rationale: deterministic first element
            quote = get_quote()
            self.assertEqual(quote["author"], "Franklin D. Roosevelt")
            self.assertIn("limit to our realization", quote["quote"])

    def test_get_quote_with_tag(self):
        with patch('quote_of_the_day_fetcher.src.main.random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]
            quote = get_quote(tag="humor")
            self.assertEqual(quote["author"], "Oscar Wilde")
            self.assertIn("Be yourself", quote["quote"])

    def test_get_quote_invalid_tag(self):
        with self.assertRaises(ValueError):
            get_quote(tag="nonexistent")


if __name__ == "__main__":
    unittest.main()
