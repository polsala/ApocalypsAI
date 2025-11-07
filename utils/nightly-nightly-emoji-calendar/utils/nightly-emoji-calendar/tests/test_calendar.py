import datetime
import unittest
from unittest.mock import patch

# Import the function under test
from src.calendar import get_emoji_date

class TestEmojiCalendar(unittest.TestCase):
    def test_known_date(self):
        """Deterministic test for a known date.
        Date: 2023-10-31 (Tuesday, October)
        Expected emojis: 📅 for weekday, 🌰 for October.
        """
        test_date = datetime.date(2023, 10, 31)
        result = get_emoji_date(test_date)
        expected = "📅 Tue 🌰 Oct 31, 2023"
        self.assertEqual(result, expected)

    @patch('src.calendar.datetime')
    def test_today_mocked(self, mock_datetime):
        """Mock datetime.date.today() to ensure CLI uses the mocked date.
        # Mock rationale: we replace today() with a fixed date to keep the test deterministic.
        """
        fixed_date = datetime.date(2022, 2, 14)  # Monday, February
        mock_datetime.date.today.return_value = fixed_date
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Import inside the patched context to ensure the patched datetime is used
        from src import calendar as calendar_mod
        result = calendar_mod.get_emoji_date(calendar_mod.datetime.date.today())
        expected = "📅 Mon 🌹 Feb 14, 2022"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
