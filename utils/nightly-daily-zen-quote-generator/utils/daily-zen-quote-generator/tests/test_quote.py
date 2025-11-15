import unittest
import datetime
from unittest import mock

# Mock rationale: we replace the file‑system read to avoid dependence on the actual JSON content.
# This ensures the test is deterministic and offline.

from daily_zen_quote import quote

class TestDailyZenQuote(unittest.TestCase):
    def setUp(self):
        # Sample deterministic quote list for testing
        self.sample_quotes = [
            "Quote A",
            "Quote B",
            "Quote C",
        ]
        # Patch the _load_quotes function to return our sample list
        self.patcher = mock.patch.object(quote, "_load_quotes", return_value=self.sample_quotes)
        self.mock_load = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_fixed_date_produces_expected_quote(self):
        # Choose a fixed date
        fixed_date = datetime.date(2023, 1, 15)
        # Compute expected index using the same hashing logic as the implementation
        expected_idx = quote._date_hash(fixed_date) % len(self.sample_quotes)
        expected_quote = self.sample_quotes[expected_idx]
        # Call the function under test
        result = quote.get_today_quote(fixed_date)
        self.assertEqual(result, expected_quote)

    def test_today_uses_datetime_today(self):
        # Mock datetime.date.today to return a known date
        with mock.patch.object(datetime.date, "today", return_value=datetime.date(2022, 12, 31)):
            expected_idx = quote._date_hash(datetime.date(2022, 12, 31)) % len(self.sample_quotes)
            expected_quote = self.sample_quotes[expected_idx]
            self.assertEqual(quote.get_today_quote(), expected_quote)

    def test_empty_quote_list_raises(self):
        # Patch _load_quotes to return empty list
        with mock.patch.object(quote, "_load_quotes", return_value=[]):
            with self.assertRaises(ValueError):
                quote.get_today_quote(datetime.date(2023, 1, 1))

if __name__ == "__main__":
    unittest.main()
