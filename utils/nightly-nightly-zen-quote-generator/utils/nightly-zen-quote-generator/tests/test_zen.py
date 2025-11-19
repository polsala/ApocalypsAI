import unittest
from unittest.mock import patch
from datetime import date

# Mock rationale: we patch `date.today` to control the deterministic output without network.
from src.zen import get_zen_quote, QUOTES

class TestZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date_returns_expected_quote(self):
        # For a known date, the hash should map to a specific index.
        test_date = "2025-01-01"
        expected = self._quote_for_date(test_date)
        result = get_zen_quote(test_date)
        self.assertEqual(result, expected)

    def test_today_uses_date_today(self):
        # Patch date.today to a known value and ensure get_zen_quote() without args matches.
        with patch('src.zen.date') as mock_date:
            mock_date.today.return_value = date(2025, 12, 31)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            expected = self._quote_for_date("2025-12-31")
            self.assertEqual(get_zen_quote(), expected)

    def test_invalid_date_format_raises(self):
        with self.assertRaises(ValueError):
            get_zen_quote("31-12-2025")

    @staticmethod
    def _quote_for_date(iso_str: str) -> str:
        """Utility to compute the expected quote using the same algorithm as the module.

        This mirrors the internal selection logic to avoid hard‑coding the expected value,
        keeping the test deterministic even if the QUOTES list changes.
        """
        from hashlib import sha256
        key = iso_str
        digest = sha256(key.encode('utf-8')).hexdigest()
        idx = int(digest[:8], 16) % len(QUOTES)
        return QUOTES[idx]

if __name__ == '__main__':
    unittest.main()
