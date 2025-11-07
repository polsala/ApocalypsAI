import unittest
from datetime import datetime
from src import emoji_calendar
from unittest.mock import patch

class TestEmojiCalendar(unittest.TestCase):
    def test_emoji_for_weekday_and_weekend(self):
        # March 2025: 1st is Saturday, 2nd Sunday, 3rd Monday
        self.assertEqual(emoji_calendar._emoji_for_day(2025, 3, 1), "🌙")  # Saturday
        self.assertEqual(emoji_calendar._emoji_for_day(2025, 3, 2), "🌙")  # Sunday
        self.assertEqual(emoji_calendar._emoji_for_day(2025, 3, 3), "🌞")  # Monday

    @patch('src.emoji_calendar._mock_holiday_emoji')
    def test_holiday_override(self, mock_holiday):
        # Mock a holiday on 2025-03-17
        mock_holiday.return_value = "☘️"
        self.assertEqual(emoji_calendar._emoji_for_day(2025, 3, 17), "☘️")
        mock_holiday.assert_called_once_with("2025-03-17")

    def test_generate_month_calendar_structure(self):
        # Use a fixed month to verify layout (March 2025)
        cal_str = emoji_calendar.generate_month_calendar(2025, 3)
        lines = cal_str.split('\n')
        # Header line should contain month name and year
        self.assertIn("March 2025", lines[0])
        # Weekday header should be present
        self.assertEqual(lines[1], "Mo Tu We Th Fr Sa Su")
        # Verify first week contains two spaces for Monday/Tuesday (since month starts on Saturday)
        first_week = lines[2]
        self.assertTrue(first_week.startswith("  "))
        # Verify that a known holiday (mocked in code) appears correctly
        # 2025-12-25 is Christmas, but not in March, so ensure no unexpected holiday emoji
        self.assertNotIn("🎄", cal_str)

if __name__ == '__main__':
    unittest.main()
