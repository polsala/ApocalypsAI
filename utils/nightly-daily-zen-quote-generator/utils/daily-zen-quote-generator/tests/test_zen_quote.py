import unittest
from unittest.mock import patch
import datetime
import sys
import io
import pathlib
import sys as _sys

# Ensure the src package is importable
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in _sys.path:
    _sys.path.insert(0, str(src_path))

from zen_quote import get_quote, main


class TestZenQuote(unittest.TestCase):
    def test_deterministic_quote_for_fixed_date(self):
        # Mock date to 2023-01-01
        fixed_date = datetime.date(2023, 1, 1)
        expected = "The mind is everything. What you think you become."
        self.assertEqual(get_quote(fixed_date), expected)

    @patch('zen_quote.datetime.date')
    def test_cli_output_uses_today(self, mock_date):
        # Mock today() to return a known date
        mock_date.today.return_value = datetime.date(2022, 12, 25)
        expected_quote = "When the mind is still, the universe surrenders."
        captured = io.StringIO()
        _sys.stdout = captured
        try:
            main()
        finally:
            _sys.stdout = _sys.__stdout__
        output = captured.getvalue().strip()
        self.assertIn(expected_quote, output)


if __name__ == "__main__":
    unittest.main()
