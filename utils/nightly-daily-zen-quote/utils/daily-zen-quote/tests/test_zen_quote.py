import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.date.today() to make the test deterministic offline.
from utils.daily-zen-quote.src.zen_quote import get_zen_quote, QUOTES

class TestZenQuote(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 is a known date; compute expected index manually.
        test_date = datetime.date(2023, 1, 1)
        expected_index = test_date.toordinal() % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        self.assertEqual(get_zen_quote(test_date), expected_quote)

    @patch('utils.daily-zen-quote.src.zen_quote.datetime.date')
    def test_today_mocked(self, mock_date_class):
        # Mock datetime.date.today() to return a fixed date.
        mock_today = datetime.date(2025, 12, 31)
        mock_date_class.today.return_value = mock_today
        mock_date_class.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected_index = mock_today.toordinal() % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        self.assertEqual(get_zen_quote(), expected_quote)

if __name__ == "__main__":
    unittest.main()
