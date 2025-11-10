import unittest
from unittest.mock import patch

# Mock rationale: We patch `random.choice` to make the selection deterministic, ensuring the test runs offline and always yields the same result.

from src.quote import get_zen_quote, QUOTES

class TestZenQuote(unittest.TestCase):
    def test_random_quote_deterministic(self):
        # Force `random.choice` to always return the first element.
        with patch('random.choice', lambda seq: seq[0]):
            quote = get_zen_quote()
            self.assertEqual(quote, QUOTES[0])

    def test_max_length_filter(self):
        # Choose a max length that only includes a subset of quotes.
        max_len = 30
        # Expected quotes are those with length <= 30.
        expected = [q for q in QUOTES if len(q) <= max_len]
        self.assertTrue(expected)  # Ensure at least one quote qualifies.
        with patch('random.choice', lambda seq: seq[0]):
            quote = get_zen_quote(max_length=max_len)
            self.assertIn(quote, expected)

    def test_no_quotes_meet_length(self):
        # Set a max length that is too small for any quote.
        with self.assertRaises(ValueError) as cm:
            get_zen_quote(max_length=5)
        self.assertIn('No quotes found', str(cm.exception))

if __name__ == '__main__':
    unittest.main()
