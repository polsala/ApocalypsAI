import unittest
from unittest import mock
import datetime
import pathlib
import sys

# Ensure the src directory is on the path
src_path = pathlib.Path(__file__).resolve().parents[2] / "src"
sys.path.append(str(src_path))

from main import get_quote_of_day, load_quotes

class TestQuoteOfDay(unittest.TestCase):
    def setUp(self):
        # Load quotes once for reference
        self.quotes = load_quotes()

    @mock.patch("datetime.date")
    def test_fixed_date(self, mock_date):
        # Mock rationale: ensure deterministic date without network or real clock.
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        quote = get_quote_of_day()
        expected_index = datetime.date(2023, 1, 1).toordinal() % len(self.quotes)
        self.assertEqual(quote, self.quotes[expected_index])

    def test_explicit_date(self):
        specific_date = datetime.date(2025, 12, 31)
        quote = get_quote_of_day(specific_date)
        expected_index = specific_date.toordinal() % len(self.quotes)
        self.assertEqual(quote, self.quotes[expected_index])

if __name__ == "__main__":
    unittest.main()
