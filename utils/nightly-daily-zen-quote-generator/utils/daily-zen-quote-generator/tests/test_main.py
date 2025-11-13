import pathlib
import sys
import unittest
from unittest.mock import patch
import datetime

# Ensure the ``src`` package is importable from the test runner.
CURRENT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT / 'src'))

from main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @patch('datetime.date')
    def test_known_date_returns_expected_quote(self, mock_date):
        """# Mock rationale: Freeze the date to 2023‑01‑01 so the output is deterministic.
        The ordinal of 2023‑01‑01 is 738521, and 738521 % 5 == 1, which should select the second
        quote in ``quotes.json``.
        """
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_quote()
        self.assertEqual(
            quote,
            "Be yourself; everyone else is already taken.",
            "Quote for 2023‑01‑01 should be the second entry in the list."
        )

    def test_default_today_is_consistent(self):
        """# Mock rationale: Verify that calling ``get_quote`` twice on the same day yields the same result.
        This does not rely on external time sources because the function uses ``datetime.date.today``.
        """
        first = get_quote()
        second = get_quote()
        self.assertEqual(first, second, "Calling get_quote multiple times on the same day should be idempotent.")

if __name__ == '__main__':
    unittest.main()
