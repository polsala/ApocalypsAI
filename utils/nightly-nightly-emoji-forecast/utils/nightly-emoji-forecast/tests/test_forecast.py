import datetime
import unittest
from forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Deterministic expectations derived from the algorithm.
        cases = {
            datetime.date(2023, 1, 1): "☀️ 🌥️ 🌨️",
            datetime.date(2023, 12, 25): "⛈️ 🌈 🌪️",
            datetime.date(2024, 2, 29): "🌤️ 🌧️ 🌈",  # Leap‑year handling
        }
        for d, expected in cases.items():
            with self.subTest(date=d):
                self.assertEqual(get_forecast(d), expected)

    def test_invalid_input(self):
        # The function expects a datetime.date; passing other types should raise.
        with self.assertRaises(AttributeError):
            # Mock rationale: we deliberately call with a string to trigger
            # an AttributeError when .isoformat() is accessed inside the helper.
            get_forecast("2023-01-01")

if __name__ == "__main__":
    unittest.main()
