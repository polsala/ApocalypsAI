import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.date.today to control output without network.
from src.zen_quote import get_today_quote, QUOTES

class TestZenQuote(unittest.TestCase):
    def test_deterministic_output(self):
        # Choose a known date and compute expected index manually
        test_date = datetime.date(2023, 4, 15)  # year+month+day = 2023+4+15 = 2042
        expected_idx = (2023 + 4 + 15) % len(QUOTES)
        expected_quote = QUOTES[expected_idx]

        with patch.object(datetime.date, "today", return_value=test_date):
            self.assertEqual(get_today_quote(), expected_quote)

    def test_wrap_around(self):
        # Date that forces wrap-around (e.g., very large sum)
        test_date = datetime.date(9999, 12, 31)  # sum = 9999+12+31 = 10042
        expected_idx = (9999 + 12 + 31) % len(QUOTES)
        expected_quote = QUOTES[expected_idx]
        with patch.object(datetime.date, "today", return_value=test_date):
            self.assertEqual(get_today_quote(), expected_quote)

if __name__ == "__main__":
    unittest.main()
