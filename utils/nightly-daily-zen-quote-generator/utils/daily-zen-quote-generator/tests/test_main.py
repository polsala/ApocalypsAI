import unittest
import datetime
from unittest.mock import patch

# Mock rationale: we patch datetime.date.today to control the date for deterministic test.

from utils.daily-zen-quote-generator.src.main import get_quote_of_the_day, _QUOTES

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date_returns_expected_quote(self):
        # Choose a known date and compute expected index manually.
        test_date = datetime.date(2023, 1, 1)  # ordinal = 738156
        expected_index = test_date.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote_of_the_day(test_date), expected_quote)

    def test_today_uses_datetime_today(self):
        fixed_today = datetime.date(2025, 12, 31)
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_today
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            # The function should call date.today() and use the patched value.
            expected_index = fixed_today.toordinal() % len(_QUOTES)
            expected_quote = _QUOTES[expected_index]
            self.assertEqual(get_quote_of_the_day(), expected_quote)

    def test_invalid_date_argument_raises(self):
        # The CLI parsing is exercised via the module's __main__ guard; however,
        # we test the internal parsing function indirectly by feeding an invalid
        # date string to the helper that would raise SystemExit.
        from utils.daily-zen-quote-generator.src.main import _parse_args
        parser = _parse_args.__self__ if hasattr(_parse_args, '__self__') else None
        # Since _parse_args is a simple function, we simulate the error path by
        # calling the module's _main with an invalid date.
        from utils.daily-zen-quote-generator.src.main import _main
        import sys
        test_argv = ['prog', '--date', 'invalid-date']
        with patch.object(sys, 'argv', test_argv):
            with self.assertRaises(SystemExit) as cm:
                _main()
            self.assertIn('Invalid date format', str(cm.exception))

if __name__ == '__main__':
    unittest.main()
