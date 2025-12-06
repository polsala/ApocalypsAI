import unittest
import datetime
from unittest import mock

# Import the utility under test.
from daily_motivation_generator import get_motivation

class TestDailyMotivationGenerator(unittest.TestCase):
    def test_fixed_date_returns_expected_quote(self):
        # Fixed date chosen for deterministic outcome.
        test_date = datetime.date(2025, 1, 1)
        quote = get_motivation(test_date)
        # Expected quote computed via the same algorithm; hard‑coded for test stability.
        expected = "Your limitation—it's only your imagination."
        self.assertEqual(quote, expected)

    @mock.patch('datetime.datetime')
    def test_today_uses_utc_date(self, mock_datetime):
        # Mock datetime.utcnow() to return a known date.
        mock_utc = datetime.datetime(2023, 12, 31, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_utc
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        # # Mock rationale: we replace utcnow to make the test deterministic without network.
        quote = get_motivation()
        expected = "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt"
        self.assertEqual(quote, expected)

if __name__ == '__main__':
    unittest.main()
