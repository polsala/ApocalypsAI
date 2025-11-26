import unittest
from unittest.mock import patch
import datetime
import sys
from io import StringIO

# Mock rationale: we patch datetime.date.today to a fixed date to make the output deterministic.
# This avoids reliance on the actual current date and ensures offline repeatability.

from src.quote import main as quote_main

class TestZenQuote(unittest.TestCase):
    @patch('datetime.date')
    def test_fixed_today_output(self, mock_date):
        # Simulate today() returning 2023-01-01
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        # Ensure that constructing a date works normally inside the module
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        captured = StringIO()
        sys.stdout = captured
        try:
            exit_code = quote_main([])
        finally:
            sys.stdout = sys.__stdout__

        self.assertEqual(exit_code, 0)
        # 2023-01-01 ordinal % 10 == 6 -> quote at index 6
        expected = "When the mind is still, the universe surrenders."
        self.assertEqual(captured.getvalue().strip(), expected)

    def test_explicit_date_argument(self):
        # No mocking needed because we pass an explicit date
        captured = StringIO()
        sys.stdout = captured
        try:
            exit_code = quote_main(["--date", "2022-12-25"])
        finally:
            sys.stdout = sys.__stdout__

        self.assertEqual(exit_code, 0)
        # 2022-12-25 ordinal % 10 == 9 -> quote at index 9
        expected = "Silence is a source of great strength."
        self.assertEqual(captured.getvalue().strip(), expected)

if __name__ == "__main__":
    unittest.main()
