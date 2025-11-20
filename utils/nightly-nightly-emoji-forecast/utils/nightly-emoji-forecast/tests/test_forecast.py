import unittest
from unittest.mock import patch
import datetime
import sys
import pathlib

# Add src to sys.path so the package can be imported
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: ensure deterministic output without relying on random.choice.
from emoji_forecast.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_forecast_returns_expected_emoji(self):
        test_date = datetime.date(2023, 1, 1)
        # Patch random.choice to return a known emoji
        with patch("random.choice", return_value="🌈"):
            forecast = get_forecast(test_date)
        self.assertEqual(forecast, "🌈  Rainbow")

    def test_invalid_date_handling(self):
        # Passing a non‑date should raise an AttributeError when .toordinal() is accessed
        with self.assertRaises(AttributeError):
            get_forecast("not-a-date")  # type: ignore

if __name__ == "__main__":
    unittest.main()
