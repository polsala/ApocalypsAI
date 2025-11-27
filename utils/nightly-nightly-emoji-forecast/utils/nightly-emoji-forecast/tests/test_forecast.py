import datetime
import unittest
from unittest import mock

# Mock rationale: we want deterministic behavior without relying on the actual system date.
# By patching ``datetime.date.today`` we can simulate any day we like.

from nightly_emoji_forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 2023-01-01 is day 1 of the year → index 0 → ☀️
        self.assertEqual(
            get_forecast(datetime.date(2023, 1, 1)),
            "☀️",
        )
        # 2023-01-02 is day 2 → index 1 → 🌤️
        self.assertEqual(
            get_forecast(datetime.date(2023, 1, 2)),
            "🌤️",
        )
        # 2023-12-31 is day 365 (non‑leap year) → (365-1) % 12 = 4 → ☁️
        self.assertEqual(
            get_forecast(datetime.date(2023, 12, 31)),
            "☁️",
        )
        # 2024-02-29 is day 60 (leap year) → (60-1) % 12 = 11 → 🌈
        self.assertEqual(
            get_forecast(datetime.date(2024, 2, 29)),
            "🌈",
        )

    def test_today_via_cli(self):
        # Simulate running the module as a script with no arguments.
        with mock.patch("datetime.date") as mock_date:
            mock_date.today.return_value = datetime.date(2025, 3, 15)
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            from nightly_emoji_forecast.src import forecast as mod
            self.assertEqual(mod.get_forecast(mock_date.today()), mod.get_forecast(datetime.date(2025, 3, 15)))

if __name__ == "__main__":
    unittest.main()
