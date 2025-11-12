import unittest
import datetime
from unittest.mock import patch

# Mock rationale: we replace datetime.date.today() with a fixed date so the
# forecast is deterministic and the test does not depend on the actual current day.

from utils.emoji_forecast.src.forecast import generate_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_fixed_date_forecast(self):
        fixed_date = datetime.date(2023, 10, 31)  # Halloween – arbitrary choice
        expected = generate_forecast(fixed_date)  # compute once for reference
        # Patch datetime.date.today to return the fixed date
        with patch.object(datetime.date, "today", return_value=fixed_date):
            result = generate_forecast()
        self.assertEqual(result, expected)
        # Ensure the forecast consists of 1‑3 emojis separated by spaces
        parts = result.split()
        self.assertTrue(1 <= len(parts) <= 3)
        for emoji in parts:
            self.assertTrue(len(emoji) > 0)  # basic sanity check

    def test_consistency_across_calls(self):
        # Same date should always give the same forecast, even across multiple calls
        date = datetime.date(2024, 1, 1)
        first = generate_forecast(date)
        second = generate_forecast(date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
