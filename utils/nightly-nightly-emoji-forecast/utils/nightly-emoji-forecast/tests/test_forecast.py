import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch `datetime.date.today` to return a fixed date so the test is deterministic and offline.
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # January 1st should map to the first emoji in the list.
        date = datetime.date(2025, 1, 1)
        self.assertEqual(get_emoji_forecast(date), "☀️")

    def test_wrap_around(self):
        # Use a date far enough to wrap around the emoji list.
        # There are 20 emojis; day 21 should map to the first emoji again.
        date = datetime.date(2025, 1, 21)
        self.assertEqual(get_emoji_forecast(date), "☀️")

    @patch('utils.nightly-emoji-forecast.src.forecast.datetime.date')
    def test_today_mocked(self, mock_date_class):
        # Mock `today()` to return March 15, 2025 (day 74).
        mock_date_instance = datetime.date(2025, 3, 15)
        mock_date_class.today.return_value = mock_date_instance
        mock_date_class.fromisoformat.side_effect = datetime.date.fromisoformat
        # Directly call the function with the mocked today date.
        self.assertEqual(get_emoji_forecast(mock_date_class.today()), "🌦️")

if __name__ == "__main__":
    unittest.main()
