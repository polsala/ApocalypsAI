import unittest
import datetime
from src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Mock rationale: using fixed dates to verify deterministic output
        cases = [
            (datetime.date(2023, 1, 1), "🌤️☁️❄️"),
            (datetime.date(2023, 12, 31), "🌧️❄️☀️"),
            (datetime.date(2024, 2, 29), "⛅🌥️🌩️"),  # 2024 is a leap year
        ]
        for date_obj, expected in cases:
            with self.subTest(date=date_obj):
                self.assertEqual(get_forecast(date_obj), expected)

if __name__ == "__main__":
    unittest.main()
