import unittest
from unittest.mock import patch
from datetime import date, datetime

# Mock rationale: Ensure deterministic behavior without relying on the real system date.

from daily_zen_quote_generator.main import get_quote, parse_cli, main

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_get_quote_deterministic(self):
        # 2025-01-01 has ordinal 738156
        test_date = date(2025, 1, 1)
        expected_index = test_date.toordinal() % 10  # len(_QUOTES) == 10
        # Expected quote from the list defined in main.py
        from daily_zen_quote_generator.main import _QUOTES
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(test_date), expected_quote)

    @patch('daily_zen_quote_generator.main.date')
    def test_cli_default_today(self, mock_date):
        # Mock rationale: Simulate today as 2025-12-31
        mock_date.today.return_value = date(2025, 12, 31)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        # Run main with no arguments
        with patch('builtins.print') as mock_print:
            exit_code = main([])
        self.assertEqual(exit_code, 0)
        # Verify printed quote matches expected for mocked today
        expected_quote = get_quote(date(2025, 12, 31))
        mock_print.assert_called_once_with(expected_quote)

    def test_cli_parses_custom_date(self):
        argv = ["2024-07-04"]
        parsed = parse_cli(argv)
        self.assertEqual(parsed, date(2024, 7, 4))

    def test_cli_invalid_date(self):
        argv = ["invalid-date"]
        with self.assertRaises(SystemExit) as cm:
            parse_cli(argv)
        self.assertNotEqual(cm.exception.code, 0)  # argparse exits with error code

if __name__ == "__main__":
    unittest.main()
