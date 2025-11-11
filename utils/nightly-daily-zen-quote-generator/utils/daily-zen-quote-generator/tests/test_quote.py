import unittest
import datetime
from pathlib import Path

# Mock rationale: we import the module directly from its relative path to avoid package installation.
# This mirrors how the CI runner will execute the tests in an isolated environment.

# Add the src directory to sys.path for import
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from quote import get_quote_of_day

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date_consistency(self):
        """Ensure that a known date always returns the same quote.

        The expected quote is derived from the deterministic hash algorithm.
        """
        test_date = datetime.date(2025, 11, 11)
        quote = get_quote_of_day(test_date)
        # The expected index for 2025-11-11 with the current quote list is 3
        # (computed via the same algorithm used in the implementation).
        expected_quote = "Let go of the past, embrace the present."
        self.assertEqual(quote, expected_quote)

    def test_today_returns_a_quote(self):
        """Calling without a date should return a non‑empty string.
        """
        quote = get_quote_of_day()
        self.assertIsInstance(quote, str)
        self.assertTrue(len(quote) > 0)

    def test_empty_quote_file_raises(self):
        """If the quotes JSON is empty, the function should raise ValueError.
        # Mock rationale: we temporarily replace the _load_quotes function.
        """
        from quote import _load_quotes
        original_loader = _load_quotes
        try:
            # Monkey‑patch to return an empty list
            quote._load_quotes = lambda: []  # type: ignore
            with self.assertRaises(ValueError):
                get_quote_of_day(datetime.date(2025, 1, 1))
        finally:
            # Restore original loader
            quote._load_quotes = original_loader  # type: ignore

if __name__ == "__main__":
    unittest.main()
