import unittest
from unittest.mock import patch
import datetime

# Import the function under test.
from src.forecast import get_daily_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_determinism_for_fixed_date(self):
        """The same date must always yield the same emoji."""
        date = datetime.date(2023, 1, 1)
        first = get_daily_emoji_forecast(date)
        second = get_daily_emoji_forecast(date)
        self.assertEqual(first, second)
        self.assertIn(first, [
            "☀️", "🌤️", "⛅", "🌥️", "☁️",
            "🌧️", "⛈️", "❄️", "🌪️", "🌈"
        ])

    @patch('src.forecast.datetime')
    def test_mock_today(self, mock_datetime):
        """# Mock rationale: Ensure the function respects a mocked ``today`` without real system time.
        The mock returns a fixed date; the forecast should match the direct call with that date.
        """
        fixed_date = datetime.date(2022, 12, 25)
        # Mock ``datetime.date.today()``
        mock_datetime.date.today.return_value = fixed_date
        # Preserve the ``date`` constructor for other uses.
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        forecast_via_today = get_daily_emoji_forecast()
        forecast_direct = get_daily_emoji_forecast(fixed_date)
        self.assertEqual(forecast_via_today, forecast_direct)

    def test_forecast_is_one_of_the_choices(self):
        """Any returned emoji must belong to the predefined palette."""
        today = datetime.date.today()
        forecast = get_daily_emoji_forecast(today)
        self.assertIn(forecast, [
            "☀️", "🌤️", "⛅", "🌥️", "☁️",
            "🌧️", "⛈️", "❄️", "🌪️", "🌈"
        ])

if __name__ == "__main__":
    unittest.main()
