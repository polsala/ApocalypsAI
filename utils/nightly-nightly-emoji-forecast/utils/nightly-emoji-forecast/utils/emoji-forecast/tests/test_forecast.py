import unittest
import datetime
from unittest import mock

# Mock rationale: Ensure deterministic behavior without relying on actual current date.
from emoji_forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_consistency_for_fixed_date(self):
        test_date = datetime.date(2023, 1, 1)
        forecast_one = get_forecast(test_date)
        forecast_two = get_forecast(test_date)
        self.assertEqual(forecast_one, forecast_two, "Forecast should be deterministic for a given date")
        # Verify structure: two weather emojis followed by a space and one event emoji
        parts = forecast_one.split(" ")
        self.assertEqual(len(parts), 2)
        weather, event = parts
        self.assertEqual(len(weather), 2)  # two emojis (may be surrogate pairs)
        self.assertIn(event, ["🚀", "🎉", "🛠️", "📚", "🍕", "🧩", "💡", "🐛", "⚡", "🧪"])

    @mock.patch("emoji_forecast.src.forecast.datetime.date")
    def test_today_mock(self, mock_date):
        # Mock rationale: Simulate today as 2022-12-25 without touching system clock.
        mock_date.today.return_value = datetime.date(2022, 12, 25)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        forecast = get_forecast(mock_date.today())
        # Consistency check – calling twice yields same result.
        self.assertEqual(forecast, get_forecast(mock_date.today()))

if __name__ == "__main__":
    unittest.main()
