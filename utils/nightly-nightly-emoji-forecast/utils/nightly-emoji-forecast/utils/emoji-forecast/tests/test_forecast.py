import unittest
from datetime import datetime
from src.forecast import forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Deterministic expectations derived from the hashing algorithm.
        cases = {
            "2025-01-01": "🌤️",
            "2025-12-01": "🌥️",
            "2024-02-29": "❄️",  # leap day
            "2023-07-04": "🌞",
        }
        for date_str, expected in cases.items():
            with self.subTest(date=date_str):
                self.assertEqual(forecast(date_str), expected)

    def test_datetime_input(self):
        dt = datetime(2025, 1, 1, 12, 0, 0)
        self.assertEqual(forecast(dt), "🌤️")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            forecast("01-01-2025")

if __name__ == "__main__":
    unittest.main()
