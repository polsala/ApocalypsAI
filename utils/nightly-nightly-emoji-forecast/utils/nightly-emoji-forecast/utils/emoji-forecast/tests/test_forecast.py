import unittest
import datetime
import sys
import pathlib
from unittest.mock import patch

# Adjust path to import the module from the src directory
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from forecast import get_daily_emoji

class TestEmojiForecast(unittest.TestCase):
    @patch("forecast.datetime.date")
    def test_fixed_date(self, mock_date):
        # Mock rationale: Ensure deterministic output without relying on the real current date.
        mock_date.today.return_value = datetime.date(2023, 1, 1)  # day 1
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        self.assertEqual(get_daily_emoji(), "☀️")

    def test_specific_date(self):
        # 2023-03-15 is day 74 → (74-1) % 12 = 1 → second emoji
        test_date = datetime.date(2023, 3, 15)
        self.assertEqual(get_daily_emoji(test_date), "🌤️")

if __name__ == "__main__":
    unittest.main()
