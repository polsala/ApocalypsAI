import unittest
from unittest.mock import patch

# Import the module under test.
from daily_zen_quote_dispenser import get_zen_quote, QUOTES

class TestZenQuote(unittest.TestCase):
    def test_get_zen_quote_returns_string(self):
        # Ensure the function returns a string from the list.
        quote = get_zen_quote()
        self.assertIsInstance(quote, str)
        self.assertIn(quote, QUOTES)

    def test_get_zen_quote_deterministic_with_mock(self):
        # Mock rationale: we replace random.choice to return a known element,
        # guaranteeing deterministic output without any network or randomness.
        with patch('random.choice', return_value=QUOTES[2]):
            quote = get_zen_quote()
            self.assertEqual(quote, QUOTES[2])

if __name__ == "__main__":
    unittest.main()
