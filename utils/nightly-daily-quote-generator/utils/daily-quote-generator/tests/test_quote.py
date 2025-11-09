import datetime
import unittest
from unittest import mock

# Import the module under test
from src.quote import get_quote, _QUOTES

class TestDailyQuoteGenerator(unittest.TestCase):
    def test_deterministic_output_for_fixed_date(self):
        """Ensure the same date always yields the same quote.

        This test uses a known date (2023‑01‑01) and checks the exact quote.
        The expected quote is derived from the algorithm itself, so if the
        implementation changes the test will fail – which is the intended
        safeguard.
        """
        fixed_date = datetime.date(2023, 1, 1)
        quote = get_quote(fixed_date)
        # Compute expected index manually using the same hashing logic
        # (replicating the algorithm to avoid hard‑coding the index).
        import hashlib
        date_str = fixed_date.isoformat()
        hashed = int(hashlib.sha256(date_str.encode("utf-8")).hexdigest(), 16)
        expected_index = hashed % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(quote, expected_quote)

    @mock.patch("src.quote.datetime.date")
    def test_cli_uses_today_when_no_date_given(self, mock_date_class):
        """Mock ``datetime.date.today`` to guarantee deterministic CLI output.

        # Mock rationale: The CLI should call ``datetime.date.today()`` internally.
        By patching the ``date`` class in the module's namespace we can control the
        returned ``today`` value without touching the real system clock.
        """
        mock_today = datetime.date(2025, 11, 9)
        mock_date_class.today.return_value = mock_today
        # Import the CLI function lazily to ensure the patch is active
        from src.quote import _cli
        with mock.patch("builtins.print") as mock_print:
            _cli()
            # The printed argument should be the quote for the mocked date
            expected_quote = get_quote(mock_today)
            mock_print.assert_called_once_with(expected_quote)

if __name__ == "__main__":
    unittest.main()
