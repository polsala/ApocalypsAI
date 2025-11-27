import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace the internal seed function to produce a known value (42)
# so the forecast outcome is predictable without relying on the actual hash algorithm.

from src.forecast import get_forecast, _seed_for_date

class TestEmojiForecast(unittest.TestCase):
    def test_forecast_deterministic_with_mocked_seed(self):
        with patch('__main__._seed_for_date', return_value=42):
            # The seed 42 maps to emojis[6] and emojis[3] based on the EMOJIS list (len=12)
            expected = "🌧️🌥️"
            result = get_forecast(datetime.date(2000, 1, 1))
            self.assertEqual(result, expected)

    def test_cli_output_today(self):
        # Ensure the CLI runs without error and prints something.
        # We mock datetime.date.today to a fixed date for reproducibility.
        fixed_today = datetime.date(2025, 12, 31)
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_today
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            # Use the real function; the output will be deterministic for the mocked date.
            forecast = get_forecast()
            self.assertIsInstance(forecast, str)
            self.assertTrue(len(forecast) >= 2)

if __name__ == "__main__":
    unittest.main()
