import unittest
from unittest.mock import patch
import datetime
import sys
from pathlib import Path

# Ensure the src directory is on the import path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: we patch ``datetime.date.today`` to return a fixed date,
# ensuring the test is deterministic and offline.

from quote_generator import get_quote, _select_quote, _QUOTES


class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_select_quote_wrap(self):
        # With 5 quotes, day 6 should wrap to the first quote.
        test_quotes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
        original = _QUOTES[:]
        try:
            import quote_generator as dg
            dg._QUOTES = test_quotes
            self.assertEqual(dg._select_quote(6), "Q1")
        finally:
            dg._QUOTES = original

    @patch('quote_generator.datetime.date')
    def test_get_quote_fixed_date(self, mock_date):
        # Mock today as March 1st (day 60 in a non‑leap year).
        mock_date.today.return_value = datetime.date(2023, 3, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = _select_quote(60)
        self.assertEqual(get_quote(), expected)


if __name__ == "__main__":
    unittest.main()
