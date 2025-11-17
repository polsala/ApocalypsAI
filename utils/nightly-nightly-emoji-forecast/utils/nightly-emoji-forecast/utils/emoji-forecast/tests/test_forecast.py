import datetime
import unittest
from emoji_forecast.src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # January 1st falls in the first 73‑day bucket → SUNNY_EMOJIS
        date = datetime.date(2023, 1, 1)
        forecast = get_emoji_forecast(date)
        self.assertIn(forecast.split()[0], ["☀️", "🌤️", "🌞", "🌈"])
        self.assertIn(forecast.split()[1], ["☀️", "🌤️", "🌞", "🌈"])

        # April 15th (day 105) falls in the second bucket → CLOUDY_EMOJIS
        date = datetime.date(2023, 4, 15)
        forecast = get_emoji_forecast(date)
        self.assertIn(forecast.split()[0], ["☁️", "🌥️", "🌫️", "🌁"])
        self.assertIn(forecast.split()[1], ["☁️", "🌥️", "🌫️", "🌁"])

        # October 31st (day 304) falls in the fifth bucket → SNOWY_EMOJIS
        date = datetime.date(2023, 10, 31)
        forecast = get_emoji_forecast(date)
        self.assertIn(forecast.split()[0], ["❄️", "☃️", "⛄", "🌨️"])
        self.assertIn(forecast.split()[1], ["❄️", "☃️", "⛄", "🌨️"])

    def test_determinism(self):
        date = datetime.date(2024, 2, 29)  # Leap year date
        first = get_emoji_forecast(date)
        second = get_emoji_forecast(date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
