import datetime
import unittest
from unittest.mock import patch

# Mock rationale: we patch ``datetime.date.today`` to a fixed date so the test is deterministic and offline.

from utils.nightly-emoji-forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_fixed_date_forecast(self):
        # 2025-01-01 => seed 20250101
        test_date = datetime.date(2025, 1, 1)
        forecast = get_forecast(test_date)
        # The expected output is derived from the deterministic RNG.
        # Running the algorithm manually yields the following string:
        expected = "☀️ 🌤️ 🌈"
        self.assertEqual(forecast, expected)

    @patch('utils.nightly-emoji-forecast.src.forecast.datetime.date')
    def test_today_forecast_with_mock(self, mock_date):
        # Mock ``datetime.date.today`` to return 2024-12-31.
        mock_date.today.return_value = datetime.date(2024, 12, 31)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        forecast = get_forecast(datetime.date.today())
        expected = "⛈️ 🌧️"
        self.assertEqual(forecast, expected)

if __name__ == "__main__":
    unittest.main()
