import unittest
from unittest import mock
import datetime
from src.emoji_calendar import generate_calendar, _parse_holidays

class TestEmojiCalendar(unittest.TestCase):
    def test_parse_holidays_valid(self):
        # Mock rationale: ensure parsing works for a simple list
        input_str = "2025-12-25,2025-01-01"
        result = _parse_holidays(input_str)
        expected = [datetime.date(2025, 12, 25), datetime.date(2025, 1, 1)]
        self.assertEqual(result, expected)

    def test_parse_holidays_empty(self):
        self.assertEqual(_parse_holidays(""), [])

    def test_generate_calendar_fixed_month(self):
        # Mock today's date to a known month (February 2025, non‑leap year)
        year, month = 2025, 2
        holidays = [datetime.date(2025, 2, 14)]  # Valentine's Day
        cal_str = generate_calendar(year, month, holidays)
        # Verify header contains correct month and year
        self.assertIn("📅 February 2025", cal_str)
        # Verify a Saturday has 🌞 and a Sunday 🌜
        # 1 Feb 2025 is Saturday
        self.assertIn("🌞  1", cal_str)
        # 2 Feb 2025 is Sunday
        self.assertIn("🌜  2", cal_str)
        # Verify holiday is marked with 🎉
        self.assertIn("🎉14", cal_str)
        # Ensure no unexpected emojis appear
        self.assertNotIn("❌", cal_str)

    @mock.patch('datetime.date')
    def test_generate_calendar_with_mocked_today(self, mock_date):
        # Mock rationale: freeze today to March 2025 to test default path
        mock_date.today.return_value = datetime.date(2025, 3, 15)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        cal_str = generate_calendar(mock_date.today().year, mock_date.today().month)
        self.assertIn("📅 March 2025", cal_str)
        # March 1 2025 is Saturday
        self.assertIn("🌞  1", cal_str)
        # March 2 2025 is Sunday
        self.assertIn("🌜  2", cal_str)

if __name__ == "__main__":
    unittest.main()
