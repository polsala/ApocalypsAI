import datetime
import unittest
from unittest.mock import patch

from src.quote import get_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_known_date(self):
        """A fixed date should always return the same quote."""
        test_date = datetime.date(2023, 1, 1)  # 2023 + 1 + 1 = 2025 -> 2025 % 10 = 5
        expected = "In the middle of difficulty lies opportunity."
        self.assertEqual(get_quote(test_date), expected)

    @patch('src.quote.datetime')
    def test_today_mock(self, mock_datetime):
        """Mock datetime.date.today() to ensure deterministic CLI output.
        # Mock rationale: we replace today's date with a known value so the test
        # does not depend on the actual current date, keeping it offline and
        # deterministic.
        """
        mock_today = datetime.date(2025, 12, 31)  # 2025 + 12 + 31 = 2068 -> 2068 % 10 = 8
        mock_datetime.date.today.return_value = mock_today
        self.assertEqual(get_quote(), "The obstacle is the path.")

if __name__ == '__main__':
    unittest.main()
