import unittest
from unittest.mock import patch
from datetime import date

# Import the module under test. The relative import works because tests are run
# with the repository root on ``sys.path``.
from utils.daily_motivation_generator.src.main import get_quote_for_date

class TestDailyMotivationGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        """Ensure the same date always yields the same quote.

        # Mock rationale: We patch ``date.today`` to a fixed date to make the
        # test deterministic without relying on the actual current day.
        """
        fixed_date = date(2025, 1, 1)
        with patch('utils.daily_motivation_generator.src.main.date') as mock_date:
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            quote = get_quote_for_date(fixed_date)
            # The expected quote is derived from the deterministic index algorithm.
            # Compute it manually using the same logic to avoid hard‑coding the index.
            from utils.daily_motivation_generator.src.main import _deterministic_index, QUOTES
            idx = _deterministic_index(fixed_date)
            expected_text, expected_author = QUOTES[idx]
            expected = f'"{expected_text}" – {expected_author}'
            self.assertEqual(quote, expected)

    def test_future_date(self):
        """A future date should still produce a valid quote.

        # Mock rationale: No network calls; we simply verify the function returns
        # a string that matches the internal list format.
        """
        future = date(2100, 12, 31)
        quote = get_quote_for_date(future)
        self.assertIsInstance(quote, str)
        self.assertIn('"', quote)  # basic sanity check for formatting

if __name__ == '__main__':
    unittest.main()
