import unittest
from unittest import mock

# Mock rationale: we replace `random.choice` to return a deterministic value
# so the test does not depend on actual randomness and remains offline.

from utils.nightly_random_quote_generator.utils.random_quote_generator.src.quote import get_random_quote, _QUOTES

class TestRandomQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_returns_string(self):
        # Ensure the function returns a string from the list.
        quote = get_random_quote()
        self.assertIsInstance(quote, str)
        self.assertIn(quote, _QUOTES)

    @mock.patch('random.choice')
    def test_get_random_quote_deterministic(self, mock_choice):
        # Force `random.choice` to return the first quote.
        mock_choice.return_value = _QUOTES[0]
        quote = get_random_quote()
        self.assertEqual(quote, _QUOTES[0])
        mock_choice.assert_called_once_with(_QUOTES)

if __name__ == '__main__':
    unittest.main()
