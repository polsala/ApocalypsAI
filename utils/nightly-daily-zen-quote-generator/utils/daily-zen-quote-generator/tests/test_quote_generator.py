import unittest
from unittest import mock
import datetime

# Import the module under test
from src.quote_generator import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Mock rationale: we want a deterministic set of dates without hitting the real clock.
        # This ensures offline, repeatable tests.
        self.patcher = mock.patch('src.quote_generator.datetime.date')
        self.mock_date_class = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def _mock_today(self, year, month, day):
        mock_today = datetime.date(year, month, day)
        self.mock_date_class.today.return_value = mock_today
        self.mock_date_class.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

    def test_known_date_quotes(self):
        # Test a few specific dates and verify the expected quote.
        test_cases = [
            ((2023, 1, 1), "The journey of a thousand miles begins with one step."),
            ((2023, 1, 2), "When the mind is still, the universe surrenders."),
            ((2023, 12, 31), "Know the road, but walk the path."),
        ]
        for (y, m, d), expected in test_cases:
            with self.subTest(date=f"{y}-{m}-{d}"):
                self._mock_today(y, m, d)
                self.assertEqual(get_quote(), expected)

    def test_default_today_uses_real_date(self):
        # Mock rationale: ensure that calling get_quote() without a date falls back to datetime.date.today().
        real_today = datetime.date(2025, 11, 11)
        self.mock_date_class.today.return_value = real_today
        self.mock_date_class.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Compute expected quote manually using the same algorithm.
        seed = real_today.year * 10000 + real_today.month * 100 + real_today.day
        from src.quote_generator import _QUOTES
        expected = _QUOTES[seed % len(_QUOTES)]
        self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
