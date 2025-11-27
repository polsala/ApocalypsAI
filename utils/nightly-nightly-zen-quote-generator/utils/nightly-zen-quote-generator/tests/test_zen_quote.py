import unittest
from unittest.mock import patch

# Mock rationale: we patch ``random.choice`` to return a deterministic element,
# ensuring the test runs offline and produces the same result every time.

from zen_quote import get_random_quote, QUOTES

class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_without_tag(self):
        # Force ``random.choice`` to return the first quote in the list.
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote()
            self.assertEqual(quote, QUOTES[0])

    def test_get_random_quote_with_valid_tag(self):
        # Choose a tag that appears in multiple quotes; we still force the first match.
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote(tag='humor')
            # The first quote with the 'humor' tag in the data set is at index 2.
            expected = next(q for q in QUOTES if 'humor' in [t.lower() for t in q.get('tags', [])])
            self.assertEqual(quote, expected)

    def test_get_random_quote_with_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(tag='nonexistent')
        self.assertIn("No quotes found for tag 'nonexistent'", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
