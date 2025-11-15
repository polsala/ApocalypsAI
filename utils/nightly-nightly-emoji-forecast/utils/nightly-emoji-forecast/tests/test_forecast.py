import datetime
import unittest
from src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 should map to the 4th emoji (index 3) → "🌦️"
        test_date = datetime.date(2023, 1, 1)
        expected = "🌦️"
        result = get_emoji_forecast(test_date)
        self.assertEqual(result, expected)

    def test_today_consistency(self):
        today = datetime.date.today()
        first = get_emoji_forecast(today)
        second = get_emoji_forecast(today)
        self.assertEqual(first, second)

    def test_invalid_type_raises(self):
        # The function expects a datetime.date; passing a string should raise AttributeError
        with self.assertRaises(AttributeError):
            # Mock rationale: deliberately misuse the API to ensure type safety
            get_emoji_forecast("not-a-date")

if __name__ == "__main__":
    unittest.main()
