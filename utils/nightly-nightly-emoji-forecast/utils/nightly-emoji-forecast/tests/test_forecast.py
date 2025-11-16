import unittest
import datetime
from src.forecast import generate_forecast, EMOJI_MAP


class TestEmojiForecast(unittest.TestCase):
    def test_repeatability(self):
        """The same date must always yield the same forecast."""
        test_date = datetime.date(2023, 5, 17)
        first = generate_forecast(test_date)
        second = generate_forecast(test_date)
        self.assertEqual(first, second)
        for emoji in first:
            self.assertIn(emoji, EMOJI_MAP)

    def test_variation(self):
        """Different dates should (very likely) produce different forecasts."""
        date_a = datetime.date(2023, 5, 17)
        date_b = datetime.date(2023, 5, 18)
        forecast_a = generate_forecast(date_a)
        forecast_b = generate_forecast(date_b)
        self.assertNotEqual(forecast_a, forecast_b)


if __name__ == "__main__":
    unittest.main()
