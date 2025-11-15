import datetime
import unittest
from unittest.mock import patch

# Import the module under test
from utils.nightly_emoji_calendar.src.emoji_calendar import get_emoji_for_date, month_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_get_emoji_special_date(self):
        # Christmas should return the special emoji 🎄
        date_obj = datetime.date(2025, 12, 25)
        self.assertEqual(get_emoji_for_date(date_obj), "🎄")

    def test_get_emoji_weekday(self):
        # 2025-01-06 is a Monday → 🌞
        date_obj = datetime.date(2025, 1, 6)
        self.assertEqual(get_emoji_for_date(date_obj), "🌞")

    def test_month_calendar_structure(self):
        # Use a fixed month where we know the layout: February 2025 (non‑leap year)
        weeks = month_calendar(2025, 2)
        # February 2025 starts on Saturday (weekday 5) and has 28 days
        # Verify number of weeks (should be 4 or 5 depending on layout)
        self.assertTrue(len(weeks) in (4, 5))
        # Verify first week padding and first day mapping
        first_week = weeks[0]
        # Expect days: Mon(0), Tue(0), Wed(0), Thu(0), Fri(0), Sat(1), Sun(2)
        expected = [(0, ""), (0, ""), (0, ""), (0, ""), (0, ""), (1, "🏖️"), (2, "🛌")]
        self.assertEqual(first_week, expected)

    @patch('datetime.date')
    def test_get_emoji_today_mock(self, mock_date):
        # Mock datetime.date.today() to return a known Friday
        mock_date.today.return_value = datetime.date(2025, 1, 10)  # Friday
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Import inside the patched context to ensure the function uses the mock
        from utils.nightly_emoji_calendar.src.emoji_calendar import get_emoji_for_date
        today = datetime.date.today()
        self.assertEqual(today.weekday(), 4)  # sanity check: Friday
        self.assertEqual(get_emoji_for_date(today), "🎉")

if __name__ == "__main__":
    unittest.main()
