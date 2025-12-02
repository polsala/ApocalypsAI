import datetime
import unittest
from src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # Using the earliest representable date (year 1) gives a predictable result.
        date = datetime.date(1, 1, 1)
        forecast = get_emoji_forecast(date)
        # Expected emojis calculated manually from the algorithm above.
        expected = "🌤️☀️☀️"  # Mock rationale: ordinal=1 → idx1=1, idx2=0, idx3=0
        self.assertEqual(forecast, expected)

    def test_consistency(self):
        # Repeated calls with the same date must return the same forecast.
        date = datetime.date(2025, 12, 2)
        first = get_emoji_forecast(date)
        second = get_emoji_forecast(date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
