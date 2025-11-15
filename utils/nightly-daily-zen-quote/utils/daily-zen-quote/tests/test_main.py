import datetime
import unittest
from unittest.mock import patch

from src.main import get_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 is day 1 -> index 0
        date = datetime.date(2023, 1, 1)
        self.assertEqual(
            get_quote(date),
            "The journey of a thousand miles begins with one step."
        )

    def test_wrap_around(self):
        # Day 11 (len(_QUOTES)=10) should wrap to index 0 again
        date = datetime.date(2023, 1, 11)
        self.assertEqual(
            get_quote(date),
            "The journey of a thousand miles begins with one step."
        )

    @patch('src.main.datetime')
    def test_today_mock(self, mock_datetime):
        # Mock today to a known date (2024-02-29, day 60 in a leap year)
        mock_today = datetime.date(2024, 2, 29)
        mock_datetime.date.today.return_value = mock_today
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # day 60 -> index (60-1)%10 = 9
        expected = "Patience is bitter, but its fruit is sweet."
        # Mock rationale: ensure deterministic behavior without network.
        self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
