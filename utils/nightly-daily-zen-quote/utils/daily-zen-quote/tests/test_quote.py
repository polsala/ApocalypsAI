import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.date.today to a fixed date so the test is deterministic and offline.
from daily_zen_quote.src.quote import get_daily_quote, _QUOTES

class TestDailyZenQuote(unittest.TestCase):
    def test_known_date(self):
        # Choose a date where we can manually compute the expected index.
        fixed_date = datetime.date(2023, 1, 15)  # 15th day of the year
        expected_index = (fixed_date.timetuple().tm_yday - 1) % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_daily_quote(fixed_date), expected_quote)

    def test_today_mocked(self):
        fixed_today = datetime.date(2024, 12, 31)  # last day of a leap year (366)
        with patch.object(datetime.date, "today", return_value=fixed_today):
            # Mock rationale: patching today ensures the function uses our fixed date.
            expected_index = (fixed_today.timetuple().tm_yday - 1) % len(_QUOTES)
            expected_quote = _QUOTES[expected_index]
            self.assertEqual(get_daily_quote(), expected_quote)

    def test_cycle_wraparound(self):
        # Verify that after the list length, it wraps correctly.
        # Use a date far beyond the list length.
        day_number = len(_QUOTES) * 3 + 5  # arbitrary large day number
        # Compute a date with that day_of_year (ignoring year overflow for simplicity)
        # We'll construct a date in a non‑leap year where day 1 = Jan 1.
        year = 2025
        date = datetime.date(year, 1, 1) + datetime.timedelta(days=day_number - 1)
        expected_index = (day_number - 1) % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_daily_quote(date), expected_quote)

if __name__ == "__main__":
    unittest.main()
