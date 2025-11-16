import datetime
import unittest
from utils.nightly_emoji_forecast.src.emoji_forecast import get_forecast, format_forecast, WEATHER_EMOJIS

class TestEmojiForecast(unittest.TestCase):
    def test_determinism(self):
        """Same date must always produce the same forecast."""
        date = datetime.date(2025, 11, 16)
        first = get_forecast(date, count=5)
        second = get_forecast(date, count=5)
        self.assertEqual(first, second)

    def test_variation_between_dates(self):
        """Different dates should yield different forecasts (high probability)."""
        date1 = datetime.date(2025, 11, 16)
        date2 = datetime.date(2025, 11, 17)
        forecast1 = get_forecast(date1, count=3)
        forecast2 = get_forecast(date2, count=3)
        self.assertNotEqual(forecast1, forecast2)

    def test_format_output(self):
        emojis = ["☀️", "☁️", "🌧️"]
        self.assertEqual(format_forecast(emojis), "☀️ ☁️ 🌧️")

    def test_emojis_are_valid(self):
        """All returned emojis must belong to the allowed set."""
        date = datetime.date(2025, 11, 16)
        forecast = get_forecast(date, count=10)
        for e in forecast:
            self.assertIn(e, WEATHER_EMOJIS)

if __name__ == "__main__":
    unittest.main()
