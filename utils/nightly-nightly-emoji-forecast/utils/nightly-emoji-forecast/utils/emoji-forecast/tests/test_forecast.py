import unittest
from datetime import date
# Mock rationale: we use fixed dates to ensure deterministic behavior without external calls.
from src.forecast import generate_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_sunny(self):
        # Jan 4, 2023 -> day 4, 4 % 4 == 0 -> ☀️
        d = date(2023, 1, 4)
        self.assertEqual(generate_forecast(d), "☀️")

    def test_cloudy(self):
        # Jan 5, 2023 -> day 5, 5 % 4 == 1 -> ☁️
        d = date(2023, 1, 5)
        self.assertEqual(generate_forecast(d), "☁️")

    def test_rainy(self):
        # Jan 6, 2023 -> day 6, 6 % 4 == 2 -> 🌧️
        d = date(2023, 1, 6)
        self.assertEqual(generate_forecast(d), "🌧️")

    def test_snowy(self):
        # Jan 7, 2023 -> day 7, 7 % 4 == 3 -> ❄️
        d = date(2023, 1, 7)
        self.assertEqual(generate_forecast(d), "❄️")

if __name__ == "__main__":
    unittest.main()
