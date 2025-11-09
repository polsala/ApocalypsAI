import unittest
from unittest.mock import patch

# Mock rationale: we patch ``random.choice`` to return the first element of the list,
# ensuring deterministic output without relying on actual randomness.

from utils.daily-zen-quote-dispenser.src.quote import get_random_quote, _QUOTES

class TestQuoteDispenser(unittest.TestCase):
    def test_random_quote_without_tag(self):
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote()
            self.assertEqual(quote, _QUOTES[0]["text"])

    def test_random_quote_with_valid_tag(self):
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            # Tag "silence" matches the fourth quote.
            quote = get_random_quote(tag="silence")
            self.assertEqual(quote, _QUOTES[3]["text"])

    def test_random_quote_with_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag 'nonexistent'", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
