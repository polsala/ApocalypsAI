import unittest
from unittest.mock import patch

# Mock rationale: we patch random.choice to return a predictable quote,
# ensuring the test is deterministic and offline.

from src.quote_generator import get_random_quote, _QUOTES

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_without_constraints(self):
        with patch("random.choice") as mock_choice:
            mock_choice.return_value = _QUOTES[0]
            quote = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(quote, _QUOTES[0])

    def test_random_quote_with_max_length(self):
        max_len = 30
        short_quotes = [q for q in _QUOTES if len(q) <= max_len]
        self.assertTrue(short_quotes)  # sanity check
        with patch("random.choice") as mock_choice:
            mock_choice.return_value = short_quotes[0]
            quote = get_random_quote(max_length=max_len)
            mock_choice.assert_called_once()
            self.assertIn(quote, short_quotes)

    def test_no_quote_fits_max_length(self):
        with self.assertRaises(ValueError):
            get_random_quote(max_length=5)

if __name__ == "__main__":
    unittest.main()
