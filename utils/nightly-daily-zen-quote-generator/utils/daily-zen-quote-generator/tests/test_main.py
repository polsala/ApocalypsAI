import unittest
import datetime
from unittest import mock

# Mock rationale: we replace datetime.datetime.utcnow to control "today" without network.

from daily_zen_quote_generator import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Ensure deterministic ordering by fixing the hash seed (Python 3.11 randomizes hash by default).
        # Mock rationale: set PYTHONHASHSEED env var is not possible here, so we monkey‑patch hash for dates.
        self.original_hash = __builtins__['hash']
        def deterministic_hash(value):
            # Simple deterministic hash for ISO date strings: sum of char codes.
            return sum(ord(c) for c in value)
        __builtins__['hash'] = deterministic_hash

    def tearDown(self):
        __builtins__['hash'] = self.original_hash

    def test_known_date(self):
        test_date = datetime.date(2023, 1, 1)
        quote = get_quote(test_date)
        # Compute expected index manually using deterministic_hash
        idx = sum(ord(c) for c in test_date.isoformat()) % 10  # there are 10 quotes
        # Load quotes directly to compare
        from daily_zen_quote_generator import _QUOTES
        expected = _QUOTES[idx]
        self.assertEqual(quote, expected)

    @mock.patch('datetime.datetime')
    def test_default_today(self, mock_datetime):
        # Mock datetime.utcnow() to return a fixed datetime
        mock_datetime.utcnow.return_value = datetime.datetime(2025, 5, 4, 12, 0, 0)
        mock_datetime.utcnow.return_value.date.return_value = datetime.date(2025, 5, 4)
        # Ensure our deterministic hash is used
        quote = get_quote()
        idx = sum(ord(c) for c in '2025-05-04') % 10
        from daily_zen_quote_generator import _QUOTES
        expected = _QUOTES[idx]
        self.assertEqual(quote, expected)

if __name__ == '__main__':
    unittest.main()
