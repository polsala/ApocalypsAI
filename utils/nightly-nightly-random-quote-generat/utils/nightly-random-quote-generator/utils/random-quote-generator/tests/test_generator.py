import unittest
from unittest import mock

# Mock rationale: We replace ``random.choice`` with a deterministic function so the test outcome does not depend on actual randomness.
# This ensures the test suite is fully offline and repeatable.

from random_quote_generator.src.generator import get_random_quote

class TestRandomQuoteGenerator(unittest.TestCase):
    def test_random_quote_without_keyword(self):
        with mock.patch('random.choice', return_value='MOCKED QUOTE'):
            quote = get_random_quote()
            self.assertEqual(quote, 'MOCKED QUOTE')

    def test_random_quote_with_keyword_match(self):
        # Choose a keyword that appears in at least one quote.
        keyword = 'future'
        # The filtered list will contain exactly one quote in our data set.
        expected = "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt"
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote(keyword)
            self.assertEqual(quote, expected)

    def test_random_quote_with_keyword_no_match(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote('nonexistentkeyword')
        self.assertIn('No quotes found containing keyword', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
