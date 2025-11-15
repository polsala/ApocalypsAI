import unittest
from datetime import date

# Import the function from the utility's source module.
# The path works because the test runner adds the utils/daily-zen-quote-generator directory to PYTHONPATH.
from src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date(self):
        """Ensure a fixed date yields the expected quote.

        Mock rationale: using a hard‑coded date makes the test deterministic and offline.
        """
        test_date = date(2023, 1, 1)  # 2023‑01‑01
        expected = "Simplicity is the ultimate sophistication."
        self.assertEqual(get_quote(test_date), expected)

    def test_default_today_consistency(self):
        """Calling ``get_quote()`` without arguments should be consistent with the same date passed explicitly.

        Mock rationale: we manually compute the expected quote for the current UTC date and compare.
        """
        today = date.today()
        # Compute expected using the same algorithm (ensures deterministic behavior).
        expected = get_quote(today)
        self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
