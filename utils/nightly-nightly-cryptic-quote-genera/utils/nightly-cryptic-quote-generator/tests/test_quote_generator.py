import unittest
from unittest.mock import patch

# Import the module under test
from utils.nightly-cryptic-quote-generator.src.quote_generator import get_random_quote, QUOTES

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_without_tag(self):
        # Mock random.choice to always return the first element
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # Mock rationale: deterministic selection
            quote = get_random_quote()
            self.assertEqual(quote, QUOTES[0]["text"])

    def test_random_quote_with_valid_tag(self):
        # Choose a tag that exists in multiple quotes, e.g., 'wisdom'
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # deterministic
            quote = get_random_quote(tag='wisdom')
            # The first quote in the filtered list should be the one with 'wisdom' tag
            filtered = [q for q in QUOTES if 'wisdom' in (t.lower() for t in q["tags"])]
            self.assertEqual(quote, filtered[0]["text"])

    def test_random_quote_with_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(tag='nonexistent')
        self.assertIn("No quotes found for tag 'nonexistent'", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
