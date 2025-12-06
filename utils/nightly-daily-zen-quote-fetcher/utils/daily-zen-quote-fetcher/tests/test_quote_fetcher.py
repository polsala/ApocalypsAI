import unittest
from unittest import mock
import datetime
from src.quote_fetcher import get_today_quote

class TestQuoteFetcher(unittest.TestCase):
    def setUp(self):
        # Load the quotes directly to know expected outcomes
        from src.quote_fetcher import _load_quotes
        self.quotes = _load_quotes()

    def test_deterministic_output_fixed_date(self):
        """# Mock rationale: Freeze datetime.date.today() to a known value.
        This ensures the function returns a predictable quote without network.
        """
        fixed_date = datetime.date(2025, 1, 1)
        with mock.patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_today_quote()
        # Compute expected index using the same algorithm
        from src.quote_fetcher import _date_to_key
        expected_index = _date_to_key(fixed_date) % len(self.quotes)
        self.assertEqual(quote, self.quotes[expected_index])

    def test_custom_date_argument(self):
        """# Mock rationale: Directly pass a date to avoid patching.
        Verifies that the public API respects the supplied date.
        """
        custom_date = datetime.date(1999, 12, 31)
        quote = get_today_quote(custom_date)
        from src.quote_fetcher import _date_to_key
        expected_index = _date_to_key(custom_date) % len(self.quotes)
        self.assertEqual(quote, self.quotes[expected_index])

    def test_empty_quote_list_raises(self):
        """# Mock rationale: Patch _load_quotes to return an empty list.
        Ensures the function fails gracefully when no quotes are available.
        """
        with mock.patch('src.quote_fetcher._load_quotes', return_value=[]):
            with self.assertRaises(ValueError):
                get_today_quote(datetime.date(2025, 1, 1))

if __name__ == '__main__':
    unittest.main()
