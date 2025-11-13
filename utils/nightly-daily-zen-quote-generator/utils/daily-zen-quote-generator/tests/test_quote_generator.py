import unittest
from datetime import date

# Mock rationale: import the function directly; no external resources needed.
from daily_zen_quote_generator import get_zen_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_january_first(self):
        # 2023-01-01 is day 1 → first quote
        self.assertEqual(get_zen_quote(date(2023, 1, 1)), "Be present.")

    def test_december_31(self):
        # 2023-12-31 is day 365 → (365-1) % 5 = 4 → fifth quote
        self.assertEqual(get_zen_quote(date(2023, 12, 31)), "Know yourself.")

    def test_leap_year_feb_29(self):
        # 2024 is a leap year; Feb 29 is day 60 → (60-1) % 5 = 4 → fifth quote
        self.assertEqual(get_zen_quote(date(2024, 2, 29)), "Know yourself.")

    def test_cli_parsing_valid(self):
        # Ensure the internal parser works for a valid date string.
        from daily_zen_quote_generator import _parse_cli_arg
        self.assertEqual(_parse_cli_arg("2022-07-04"), date(2022, 7, 4))

    def test_cli_parsing_invalid(self):
        from daily_zen_quote_generator import _parse_cli_arg
        with self.assertRaises(ValueError):
            _parse_cli_arg("07-04-2022")

if __name__ == "__main__":
    unittest.main()
