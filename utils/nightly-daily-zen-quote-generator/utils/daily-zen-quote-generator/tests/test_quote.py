import unittest
from unittest import mock
import datetime

# Import the module under test.
from src.quote import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_output_for_known_date(self):
        # Mock rationale: we fix the date to a known value to make the test deterministic.
        test_date = datetime.date(2023, 1, 15)  # 15th day of the year
        expected_quote = "Let go or be dragged."  # 15 % 10 = 5 -> index 4 (0‑based)
        self.assertEqual(get_quote(test_date), expected_quote)

    def test_today_uses_datetime_today(self):
        # Mock rationale: replace datetime.date.today() with a fixed date.
        with mock.patch('datetime.date') as mock_date:
            mock_date.today.return_value = datetime.date(2024, 12, 31)
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            # 2024 is a leap year, Dec 31 is day 366
            expected_quote = "When you realize nothing is lacking, the whole world belongs to you."
            self.assertEqual(get_quote(), expected_quote)

    def test_wrap_around(self):
        # Mock rationale: ensure that day numbers larger than the quote list wrap correctly.
        test_date = datetime.date(2022, 12, 31)  # Non‑leap year, day 365
        # 365 % 10 = 5 -> index 4
        expected_quote = "Let go or be dragged."
        self.assertEqual(get_quote(test_date), expected_quote)

if __name__ == "__main__":
    unittest.main()
