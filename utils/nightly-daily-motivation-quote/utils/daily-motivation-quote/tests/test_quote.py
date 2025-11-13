import unittest
from unittest import mock
from datetime import date

# Import the module under test
from src.quote import get_random_quote, get_quote_of_the_day

class TestDailyMotivationQuote(unittest.TestCase):
    def setUp(self):
        # Ensure the original QUOTES list is untouched for each test
        from src.quote import QUOTES
        self.original_quotes = list(QUOTES)

    def tearDown(self):
        # Restore the original list (defensive, not strictly needed)
        from src.quote import QUOTES
        QUOTES[:] = self.original_quotes

    def test_random_quote_returns_expected_when_mocked(self):
        # Mock rationale: deterministic test without randomness.
        with mock.patch('random.choice', return_value='Mocked Quote') as mock_choice:
            result = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Mocked Quote')

    def test_random_quote_respects_max_length(self):
        # Mock rationale: ensure length filter works and random.choice receives filtered list.
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:
            result = get_random_quote(max_length=30)
            # All quotes longer than 30 chars are filtered out; the first remaining should be returned.
            self.assertTrue(len(result) <= 30)
            mock_choice.assert_called_once()

    def test_random_quote_raises_when_no_match(self):
        # Mock rationale: verify proper error handling for impossible constraints.
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(max_length=5)  # No quote that short
        self.assertIn('No quotes satisfy the length constraint', str(ctx.exception))

    def test_quote_of_the_day_is_deterministic(self):
        # Mock rationale: fixed date should always map to the same quote.
        fixed_date = date(2023, 1, 15)  # 15th day of the year
        first = get_quote_of_the_day(date=fixed_date)
        second = get_quote_of_the_day(date=fixed_date)
        self.assertEqual(first, second)

    def test_quote_of_the_day_respects_max_length(self):
        # Mock rationale: length filter should affect the deterministic selection.
        fixed_date = date(2023, 12, 31)  # Day 365
        # Use a very small max_length to force a different subset.
        result = get_quote_of_the_day(date=fixed_date, max_length=40)
        self.assertTrue(len(result) <= 40)

    def test_quote_of_the_day_raises_when_no_match(self):
        # Mock rationale: same as random version, but for deterministic path.
        with self.assertRaises(ValueError):
            get_quote_of_the_day(date=date(2023, 1, 1), max_length=1)

if __name__ == '__main__':
    unittest.main()
