import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.date.today() to make the test deterministic.
# This ensures the utility works offline and does not depend on the actual current date.

from src.main import quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 is day 1 of the year, should map to first quote.
        test_date = datetime.date(2023, 1, 1)
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(quote_of_the_day(test_date), expected)

    def test_wrap_around(self):
        # Choose a date far enough that the modulo wraps.
        # There are 30 quotes; day 31 should map to the first quote again.
        test_date = datetime.date(2023, 2, 1)  # 2023 is not a leap year, Feb 1 = day 32
        # day_of_year = 32, (32-1)%30 = 1 -> second quote
        expected = "When the mind is still, the universe surrenders."
        self.assertEqual(quote_of_the_day(test_date), expected)

    @patch('src.main.datetime')
    def test_cli_output(self, mock_datetime):
        # Mock datetime.date.today() to a known date and capture stdout.
        mock_today = datetime.date(2024, 12, 31)  # day 366 (leap year)
        mock_datetime.date.today.return_value = mock_today
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        mock_datetime.timedelta = datetime.timedelta
        mock_datetime.datetime = datetime.datetime
        mock_datetime.time = datetime.time
        mock_datetime.timetuple = datetime.date.timetuple

        from io import StringIO
        import sys
        captured = StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            # Import the module's _main function directly to avoid running on import.
            from src.main import _main
            _main()
        finally:
            sys.stdout = sys_stdout
        output = captured.getvalue().strip()
        # Compute expected quote for day 366.
        expected = quote_of_the_day(mock_today)
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
