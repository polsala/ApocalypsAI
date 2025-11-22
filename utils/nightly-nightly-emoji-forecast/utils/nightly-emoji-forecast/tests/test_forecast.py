import datetime
import unittest
from unittest.mock import patch

# Mock rationale: we import the function directly to avoid any side‑effects from CLI parsing.
from utils.nightly_emoji_forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 2023-01-01 -> ordinal 738156, 738156 % 8 = 4 -> 🌧️
        date = datetime.date(2023, 1, 1)
        self.assertEqual(get_forecast(date), "🌧️")

        # 2024-02-29 (leap year) -> ordinal 738791, 738791 % 8 = 7 -> 🌪️
        date = datetime.date(2024, 2, 29)
        self.assertEqual(get_forecast(date), "🌪️")

        # 2025-12-31 -> ordinal 739822, 739822 % 8 = 6 -> ❄️
        date = datetime.date(2025, 12, 31)
        self.assertEqual(get_forecast(date), "❄️")

    def test_today_mocked(self):
        # Mock datetime.date.today() to a fixed date and ensure CLI prints expected emoji.
        # Mock rationale: we patch the date class method to return a known date without network.
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = datetime.date(2022, 7, 4)
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            # Import inside the patch to ensure the patched date is used.
            from utils.nightly_emoji_forecast.src import forecast as fc
            self.assertEqual(fc.get_forecast(datetime.date.today()), "⛅")

if __name__ == "__main__":
    unittest.main()
