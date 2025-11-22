import unittest
import datetime
from nightly_emoji_forecast.src.forecast import get_emoji_forecast, EMOJI_PALETTE

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # January 1st -> first emoji in the palette
        self.assertEqual(get_emoji_forecast(datetime.date(2025, 1, 1)), EMOJI_PALETTE[0])
        # February 28th (non‑leap year) -> day 59
        self.assertEqual(get_emoji_forecast(datetime.date(2025, 2, 28)), EMOJI_PALETTE[(59 - 1) % len(EMOJI_PALETTE)])
        # Leap day (2024-02-29) -> day 60
        self.assertEqual(get_emoji_forecast(datetime.date(2024, 2, 29)), EMOJI_PALETTE[(60 - 1) % len(EMOJI_PALETTE)])
        # December 31st -> day 365 (or 366 in leap year)
        self.assertEqual(get_emoji_forecast(datetime.date(2025, 12, 31)), EMOJI_PALETTE[(365 - 1) % len(EMOJI_PALETTE)])

    def test_consistency(self):
        # Same date always yields same emoji
        d = datetime.date(2025, 11, 22)
        first = get_emoji_forecast(d)
        for _ in range(5):
            self.assertEqual(get_emoji_forecast(d), first)

    def test_future_date_mock(self):
        # Mock rationale: ensure function works for dates far in the future without external calls.
        future = datetime.date(2100, 7, 4)
        # No network needed; deterministic calculation only.
        result = get_emoji_forecast(future)
        self.assertIsInstance(result, str)
        self.assertIn(result, EMOJI_PALETTE)

if __name__ == "__main__":
    unittest.main()
