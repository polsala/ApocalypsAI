import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.date.today() to a fixed date so the test is deterministic and offline.

from src.quote_generator import get_daily_zen

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date_returns_expected_quote(self):
        fixed_date = datetime.date(2023, 1, 15)  # 15th day of the year
        expected_index = fixed_date.timetuple().tm_yday % 10  # len(_QUOTES) == 10
        # Import the internal quote list via a protected attribute for test clarity
        from src.quote_generator import _QUOTES
        expected_quote = _QUOTES[expected_index]

        with patch.object(datetime.date, "today", return_value=fixed_date):
            result = get_daily_zen()
        self.assertEqual(result, expected_quote)

    def test_none_date_uses_today(self):
        # Ensure the function falls back to datetime.date.today() when no argument is given.
        today = datetime.date(2024, 12, 31)
        with patch.object(datetime.date, "today", return_value=today):
            result = get_daily_zen()
        # Compute expected quote manually
        from src.quote_generator import _QUOTES
        expected = _QUOTES[today.timetuple().tm_yday % len(_QUOTES)]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
