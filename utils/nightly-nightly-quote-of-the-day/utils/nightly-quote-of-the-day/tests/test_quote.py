import unittest
from unittest.mock import patch

# Import the module using its package path
from utils.nightly-quote-of-the-day.src import quote

class TestQuoteUtility(unittest.TestCase):
    def test_random_quote_without_tag(self):
        # Mock random.choice to always return the first quote
        with patch('random.choice', return_value=quote.QUOTES[0]):
            result = quote.get_random_quote()
            self.assertEqual(result, quote.QUOTES[0]["text"])

    def test_random_quote_with_tag(self):
        # Mock random.choice to return a known quote that matches the tag 'wisdom'
        with patch('random.choice', return_value=quote.QUOTES[2]):  # third quote has 'wisdom'
            result = quote.get_random_quote(tag='wisdom')
            self.assertEqual(result, quote.QUOTES[2]["text"])

    def test_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as cm:
            quote.get_random_quote(tag='nonexistent')
        self.assertIn("No quotes found for tag", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
