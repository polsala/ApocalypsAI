"""Tests for Daily Zen Quote Fetcher."""

import datetime
import os
import sys
import unittest
from unittest.mock import patch

# Mock rationale: we patch datetime.date.today to a fixed date to ensure deterministic output without network or real time dependence.
# Adjust sys.path to import the utility module.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quote_fetcher import get_today_quote, _select_quote_for_date


class TestQuoteFetcher(unittest.TestCase):
    def test_select_quote_consistency(self):
        test_date = datetime.date(2023, 1, 1)
        expected = _select_quote_for_date(test_date)
        self.assertEqual(_select_quote_for_date(test_date), expected)

    @patch('quote_fetcher.datetime.date')
    def test_get_today_quote_mocked_date(self, mock_date):
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_today_quote()
        expected = _select_quote_for_date(datetime.date(2023, 1, 1))
        self.assertEqual(quote, expected)


if __name__ == "__main__":
    unittest.main()
