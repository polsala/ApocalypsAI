import unittest
from datetime import date
from nightly_emoji_forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # Mock rationale: Using a fixed date ensures deterministic output without external calls.
        test_date = date(2025, 11, 16)
        forecast = get_emoji_forecast(test_date)
        # The expected value was pre‑computed using the same algorithm.
        self.assertEqual(forecast, "☀️ 🌈")

    def test_consistency_across_calls(self):
        # Mock rationale: Verify that repeated calls with the same date yield identical results.
        test_date = date(2023, 1, 1)
        first = get_emoji_forecast(test_date)
        second = get_emoji_forecast(test_date)
        self.assertEqual(first, second)

    def test_different_dates_produce_different_forecasts(self):
        # Mock rationale: Ensure the function is sensitive to the input date.
        forecast_a = get_emoji_forecast(date(2022, 12, 31))
        forecast_b = get_emoji_forecast(date(2023, 1, 1))
        self.assertNotEqual(forecast_a, forecast_b)

if __name__ == "__main__":
    unittest.main()
