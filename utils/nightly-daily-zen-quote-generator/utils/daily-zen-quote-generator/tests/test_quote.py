import unittest
from unittest.mock import patch
import datetime

# Import the function under test.
from src.quote import get_daily_zen_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_fixed_date_mapping(self):
        """Ensure a known date maps to the expected quote.

        # Mock rationale: we patch ``datetime.date.today`` to return a deterministic
        # date so the function behaves predictably without any network or external I/O.
        """
        fixed_date = datetime.date(2023, 1, 1)  # Day 1 of the year
        expected_quote = (
            "The journey of a thousand miles begins with one step."
        )
        # Mock ``datetime.date.today`` to return ``fixed_date``.
        with patch.object(datetime.date, "today", return_value=fixed_date):
            self.assertEqual(get_daily_zen_quote(), expected_quote)

    def test_wrap_around(self):
        """Check that the modulo logic wraps after the list length.

        # Mock rationale: using a date far enough into the year to exceed the quote list.
        """
        # 2023 is not a leap year; day 365 maps to the last quote.
        last_day = datetime.date(2023, 12, 31)
        expected_last = (
            "Do not seek the truth; simply stop thinking about it."
        )
        with patch.object(datetime.date, "today", return_value=last_day):
            self.assertEqual(get_daily_zen_quote(), expected_last)

        # Day 366 (hypothetical) should wrap to the first quote.
        wrap_day = datetime.date(2024, 12, 31)  # 2024 is a leap year, day 366
        expected_first = (
            "The journey of a thousand miles begins with one step."
        )
        with patch.object(datetime.date, "today", return_value=wrap_day):
            self.assertEqual(get_daily_zen_quote(), expected_first)

if __name__ == "__main__":
    unittest.main()
