import unittest
from unittest.mock import patch
from datetime import date, datetime

# Mock rationale: we patch datetime.utcnow() to return a fixed datetime so the
# quote selection becomes deterministic without any network access.

from src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @patch("src.main.datetime")
    def test_fixed_utc_date_selection(self, mock_datetime):
        # Simulate datetime.utcnow() returning 2023-01-01
        mock_datetime.utcnow.return_value = datetime(2023, 1, 1)
        # Expected index: 20230101 % 5 = 1
        expected = "Simplicity is the ultimate sophistication."
        self.assertEqual(get_quote(), expected)

    def test_explicit_date(self):
        # Directly pass a known date
        test_date = date(2022, 12, 31)  # 20221231 % 5 = 1
        expected = "Simplicity is the ultimate sophistication."
        self.assertEqual(get_quote(test_date), expected)

if __name__ == "__main__":
    unittest.main()
