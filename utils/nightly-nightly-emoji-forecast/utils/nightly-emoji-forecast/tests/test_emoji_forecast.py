import unittest
from utils.nightly-emoji-forecast.src.emoji_forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Deterministic expectations based on the current hashing algorithm
        cases = {
            "2025-01-01": "🌞",
            "2025-02-14": "🌦️",
            "2025-03-17": "🌧️",
            "2025-12-25": "❄️",
            "2025-12-31": "🌪️",
        }
        for date_str, expected in cases.items():
            with self.subTest(date=date_str):
                self.assertEqual(get_forecast(date_str), expected)

    def test_invalid_date_raises(self):
        with self.assertRaises(ValueError):
            get_forecast("not-a-date")

if __name__ == "__main__":
    unittest.main()
