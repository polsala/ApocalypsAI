import unittest
from unittest.mock import patch
import datetime

# Mock rationale: import the module under test.
from src.quote import get_today_quote, QUOTES

class TestDailyZenQuote(unittest.TestCase):
    def test_quote_is_deterministic_for_fixed_date(self):
        fixed_date = datetime.date(2023, 1, 1)
        with patch('src.quote.datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            # First call
            quote1 = get_today_quote()
            # Second call – should be identical because the algorithm is deterministic.
            quote2 = get_today_quote()
        self.assertEqual(quote1, quote2, "Quote should be deterministic for the same date")
        self.assertIn(quote1, QUOTES, "Quote must be one of the predefined quotes")

    def test_quote_is_string(self):
        # Ensure the function returns a string even without mocking (uses real today).
        quote = get_today_quote()
        self.assertIsInstance(quote, str)
        self.assertTrue(len(quote) > 0, "Quote should not be empty")

if __name__ == "__main__":
    unittest.main()
