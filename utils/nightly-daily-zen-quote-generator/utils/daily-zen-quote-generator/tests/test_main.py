import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.date.today to return a fixed date so the test is deterministic and offline.

from src.main import get_quote_of_day, _QUOTES

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date_returns_expected_quote(self):
        fixed_date = datetime.date(2023, 10, 31)  # Halloween
        # Expected index calculation mirrors the implementation
        date_str = fixed_date.isoformat()
        # Re‑use the private hash function logic (imported indirectly via get_quote_of_day)
        # Since _hash_date is not exported, we compute expected index the same way.
        import hashlib
        digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
        idx = int(digest[:8], 16) % len(_QUOTES)
        expected_quote = _QUOTES[idx]

        with patch.object(datetime.date, "today", return_value=fixed_date):
            result = get_quote_of_day()
        self.assertEqual(result, expected_quote)

    def test_default_today_uses_current_date(self):
        # Ensure that calling without arguments does not raise and returns a string.
        result = get_quote_of_day()
        self.assertIsInstance(result, str)
        self.assertIn(result, _QUOTES)

if __name__ == "__main__":
    unittest.main()
