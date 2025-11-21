import unittest
from unittest.mock import patch

# Import the module under test
from src.quote_dispenser import get_random_quote, QUOTES

class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_returns_string(self):
        # Ensure the function returns a string from the list.
        quote = get_random_quote()
        self.assertIsInstance(quote, str)
        self.assertIn(quote, QUOTES)

    def test_random_choice_mocked(self):
        # Mock rationale: we replace random.choice to make the test deterministic.
        with patch('random.choice', return_value=QUOTES[2]):
            quote = get_random_quote()
            self.assertEqual(quote, QUOTES[2])

if __name__ == '__main__':
    unittest.main()
