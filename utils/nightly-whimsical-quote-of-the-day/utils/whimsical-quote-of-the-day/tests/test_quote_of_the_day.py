import datetime
import unittest
from unittest import mock

# Mock rationale: We replace ``datetime.date.today`` with a fixed date to make the test deterministic.
# This ensures the utility behaves the same regardless of when the test suite runs.

from src.quote_of_the_day import get_quote, _QUOTES

class TestQuoteOfTheDay(unittest.TestCase):
    def test_deterministic_index(self):
        # Choose a known date and compute expected index manually.
        test_date = datetime.date(2023, 1, 1)  # ordinal = 738156
        expected_index = test_date.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(test_date), expected_quote)

    @mock.patch('src.quote_of_the_day.datetime.date')
    def test_today_uses_mocked_date(self, mock_date_class):
        # Mock ``datetime.date.today`` to return a fixed date.
        mock_today = datetime.date(1999, 12, 31)
        mock_date_class.today.return_value = mock_today
        # Ensure ``toordinal`` works on the mock object (it is a real date instance).
        expected_index = mock_today.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(), expected_quote)

    def test_cli_output(self):
        # Run the module as a script with a known date argument.
        import subprocess
        import sys
        script_path = __file__.replace('test_quote_of_the_day.py', '../src/quote_of_the_day.py')
        result = subprocess.run([sys.executable, script_path, '--date', '2022-02-22'],
                                capture_output=True, text=True, check=True)
        # Compute expected quote for the same date.
        expected = get_quote(datetime.date(2022, 2, 22))
        self.assertEqual(result.stdout.strip(), expected)

if __name__ == '__main__':
    unittest.main()
