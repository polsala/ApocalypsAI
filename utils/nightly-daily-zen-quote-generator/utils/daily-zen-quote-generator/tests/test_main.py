import unittest
import sys
import os
import datetime
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import get_quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date(self):
        # Mock rationale: ensure deterministic output without real date dependency
        test_date = datetime.date(2023, 1, 1)  # days since epoch = 19358
        expected = "Let go or be dragged."  # 19358 % 5 = 3
        self.assertEqual(get_quote_of_the_day(test_date), expected)

    @patch('main.datetime')
    def test_today_mocked(self, mock_datetime):
        # Mock rationale: simulate today as 2025-12-31
        mock_today = datetime.date(2025, 12, 31)
        mock_datetime.date.today.return_value = mock_today
        # Preserve normal date construction for other calls
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        days = (mock_today - datetime.date(1970, 1, 1)).days
        expected = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "Let go or be dragged.",
            "The obstacle is the path.",
        ][days % 5]
        self.assertEqual(get_quote_of_the_day(), expected)

if __name__ == '__main__':
    unittest.main()
