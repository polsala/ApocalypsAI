import unittest
from unittest.mock import patch
import datetime

# Mock rationale: We patch datetime.date.today to return a fixed date,
# ensuring deterministic output without relying on the actual current date.

from src.quote_generator import get_quote


class TestQuoteGenerator(unittest.TestCase):
    def test_known_date(self):
        test_date = datetime.date(2023, 1, 1)  # Day 1 of the year
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_quote(test_date), expected)

    def test_day_of_year_modulo(self):
        # 2023-12-31 is day 365 (non‑leap year)
        test_date = datetime.date(2023, 12, 31)
        # 365 - 1 = 364; 364 % 10 = 4
        expected = "Let go or be dragged."
        self.assertEqual(get_quote(test_date), expected)

    @patch('src.quote_generator.datetime.date')
    def test_today_patch(self, mock_date):
        # Mock today to be 2024-02-29 (leap year day 60)
        mock_date.today.return_value = datetime.date(2024, 2, 29)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Day 60 -> index (60-1)%10 = 9
        expected = "Be present, not perfect."
        self.assertEqual(get_quote(), expected)


if __name__ == "__main__":
    unittest.main()
