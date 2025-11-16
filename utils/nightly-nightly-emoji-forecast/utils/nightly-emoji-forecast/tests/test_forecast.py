import unittest
from datetime import date
# Mock rationale: No external calls; the function is pure and deterministic, so no mocks are required.

from utils.nightly_emoji_forecast.src.forecast import get_forecast, _WEATHER_EMOJIS

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # 2025-01-01 => seed = 2025+1+1 = 2027
        # idx1 = 2027 % 12 = 11 -> 🌫️
        # idx2 = (2027*7) % 12 = 5 -> 🌦️
        # idx3 = (2027*13) % 12 = 11 -> 🌫️
        d = date(2025, 1, 1)
        self.assertEqual(get_forecast(d), "🌫️🌦️🌫️")

    def test_repeatability(self):
        d = date(2023, 12, 31)
        first = get_forecast(d)
        second = get_forecast(d)
        self.assertEqual(first, second)

    def test_emoji_coverage(self):
        # Generate forecasts for a range of dates and ensure at least half of the emoji set appears.
        seen = set()
        for year in range(2020, 2026):
            for month in range(1, 13):
                d = date(year, month, 15)
                seen.update(get_forecast(d))
        self.assertGreaterEqual(len(seen), len(_WEATHER_EMOJIS) // 2)

if __name__ == "__main__":
    unittest.main()
