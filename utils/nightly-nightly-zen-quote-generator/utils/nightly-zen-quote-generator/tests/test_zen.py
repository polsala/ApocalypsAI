import datetime
import unittest
from src.zen import get_zen_quote

class TestZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        # Fixed date should always return the same quote.
        test_date = datetime.date(2023, 1, 1)
        quote1 = get_zen_quote(test_date)
        quote2 = get_zen_quote(test_date)
        self.assertEqual(quote1, quote2)
        # Verify against a known expected quote for this date.
        # Mock rationale: we pre‑computed the expected quote using the same algorithm.
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(quote1, expected)

    def test_today_is_valid(self):
        # Ensure the function works for today's date without error.
        today = datetime.date.today()
        quote = get_zen_quote(today)
        self.assertIsInstance(quote, str)
        self.assertTrue(len(quote) > 0)

if __name__ == "__main__":
    unittest.main()
