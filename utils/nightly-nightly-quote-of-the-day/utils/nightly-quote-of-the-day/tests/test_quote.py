import unittest
from unittest.mock import patch

# Mock rationale: we patch ``random.choice`` to make the test deterministic without relying on actual randomness.

from src.quote import get_random_quote, _filter_by_tag

class TestQuoteUtility(unittest.TestCase):
    def test_filter_by_tag_returns_all_when_none(self):
        all_quotes = _filter_by_tag(None)
        self.assertEqual(len(all_quotes), 5)  # total quotes defined in the module

    def test_filter_by_tag_case_insensitive(self):
        humor_quotes = _filter_by_tag('HumOr')
        self.assertTrue(all('humor' in [t.lower() for t in q[2]] for q in humor_quotes))
        self.assertGreaterEqual(len(humor_quotes), 2)

    def test_get_random_quote_without_tag(self):
        # Force ``random.choice`` to return the first element for determinism.
        with patch('random.choice', lambda seq: seq[0]):
            quote, author = get_random_quote()
            self.assertEqual(quote, "The only way to do great work is to love what you do.")
            self.assertEqual(author, "Steve Jobs")

    def test_get_random_quote_with_tag(self):
        with patch('random.choice', lambda seq: seq[0]):
            quote, author = get_random_quote('programming')
            # The only programming‑tagged quote in the list is the Linus Torvalds one.
            self.assertEqual(quote, "Talk is cheap. Show me the code.")
            self.assertEqual(author, "Linus Torvalds")

    def test_get_random_quote_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote('nonexistent')
        self.assertIn('No quotes found for tag', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
