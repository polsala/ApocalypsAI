import unittest
from datetime import date

# Import the function from the sibling src package
from ..src.forecast import get_forecast


class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Jan 1 -> day 1 % 4 = 1 -> "⛅"
        self.assertEqual(get_forecast(date(2023, 1, 1)), "⛅")
        # Jan 2 -> day 2 % 4 = 2 -> "🌧️"
        self.assertEqual(get_forecast(date(2023, 1, 2)), "🌧️")
        # Jan 3 -> day 3 % 4 = 3 -> "❄️"
        self.assertEqual(get_forecast(date(2023, 1, 3)), "❄️")
        # Jan 4 -> day 4 % 4 = 0 -> "☀️"
        self.assertEqual(get_forecast(date(2023, 1, 4)), "☀️")

    def test_mocked_today(self):
        # Mock rationale: directly passing a date object avoids any external calls.
        # Dec 31, 2022 -> day 365 % 4 = 1 -> "⛅"
        self.assertEqual(get_forecast(date(2022, 12, 31)), "⛅")


if __name__ == "__main__":
    unittest.main()
