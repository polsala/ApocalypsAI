import unittest
from datetime import date

# Mock rationale: Import the module directly from the relative path to keep the test self‑contained.
# The repository layout ensures that ``utils/nightly-emoji-forecast`` is on the PYTHONPATH when tests run.
from src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 2023-01-01 => (2023+1+1) % 10 = 5 => "🌪️"
        self.assertEqual(get_forecast(date(2023, 1, 1)), "🌪️")
        # 2023-07-04 => (2023+7+4) % 10 = 4 => "❄️"
        self.assertEqual(get_forecast(date(2023, 7, 4)), "❄️")
        # 2025-12-31 => (2025+12+31) % 10 = 8 => "🌙"
        self.assertEqual(get_forecast(date(2025, 12, 31)), "🌙")

    def test_today_consistency(self):
        today = date.today()
        # Ensure the function returns a string of length 1 or 2 (emoji may be multi‑codepoint).
        result = get_forecast(today)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) >= 1)

if __name__ == "__main__":
    unittest.main()
