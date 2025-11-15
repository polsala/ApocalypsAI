import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.date.today() with a fixed date so the test is deterministic and offline.
from utils.nightly_emoji_forecast.src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_today_forecast_mocked(self):
        # Simulate that today is 2023-01-02 (Monday)
        mock_date = datetime.date(2023, 1, 2)
        with patch.object(datetime.date, "today", return_value=mock_date):
            self.assertEqual(get_emoji_forecast(), "🌞")

    def test_specific_dates(self):
        cases = [
            (datetime.date(2023, 1, 2), "🌞"),  # Monday
            (datetime.date(2023, 1, 3), "🌤️"),  # Tuesday
            (datetime.date(2023, 1, 4), "🌧️"),  # Wednesday
            (datetime.date(2023, 1, 5), "⛈️"),  # Thursday
            (datetime.date(2023, 1, 6), "🌈"),  # Friday
            (datetime.date(2023, 1, 7), "❄️"),  # Saturday
            (datetime.date(2023, 1, 8), "🌙"),  # Sunday
        ]
        for dt, expected in cases:
            with self.subTest(date=dt):
                self.assertEqual(get_emoji_forecast(dt), expected)

if __name__ == "__main__":
    unittest.main()
