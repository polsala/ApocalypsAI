import unittest
from unittest.mock import patch

# Mock rationale: we patch random.choice to return the first element of the list,
# ensuring deterministic output without relying on actual randomness.

from src.quote import get_random_quote, _filter_quotes

class TestQuoteUtility(unittest.TestCase):
    def test_filter_no_tag_returns_all(self):
        all_quotes = _filter_quotes(None)
        self.assertGreaterEqual(len(all_quotes), 1)

    def test_filter_specific_tag(self):
        wisdom = _filter_quotes("wisdom")
        self.assertTrue(all(q["tag"] == "wisdom" for q in wisdom))
        self.assertGreaterEqual(len(wisdom), 1)

    def test_filter_unknown_tag_raises(self):
        with self.assertRaises(ValueError):
            get_random_quote("nonexistent")

    @patch('random.choice', lambda seq: seq[0])
    def test_random_quote_deterministic(self):
        # With the mock, the first quote in the filtered list is always returned.
        quote = get_random_quote("humor")
        expected = "I have not failed. I've just found 10,000 ways that won't work."
        self.assertEqual(quote, expected)

    @patch('random.choice', lambda seq: seq[0])
    def test_random_quote_no_tag(self):
        quote = get_random_quote()
        # First element of the full list
        expected = "The only limit to our realization of tomorrow is our doubts of today."
        self.assertEqual(quote, expected)

if __name__ == "__main__":
    unittest.main()
