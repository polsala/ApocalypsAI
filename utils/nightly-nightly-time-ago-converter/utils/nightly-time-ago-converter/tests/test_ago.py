import unittest
from unittest import mock
import datetime

# Mock rationale: we replace the internal _now() helper to return a fixed point in time.
# This guarantees deterministic output without any network or external state.

from src.ago import time_ago

class TestTimeAgo(unittest.TestCase):
    def setUp(self):
        # Fixed reference time: 2025-11-20 12:00:00 UTC
        self.fixed_now = datetime.datetime(2025, 11, 20, 12, 0, 0, tzinfo=datetime.timezone.utc)
        patcher = mock.patch('src.ago._now', return_value=self.fixed_now)
        self.addCleanup(patcher.stop)
        self.mock_now = patcher.start()

    def test_just_now(self):
        ts = self.fixed_now
        self.assertEqual(time_ago(ts), "just now")

    def test_seconds_ago(self):
        ts = self.fixed_now - datetime.timedelta(seconds=45)
        self.assertEqual(time_ago(ts), "45 seconds ago")

    def test_minutes_ago(self):
        ts = self.fixed_now - datetime.timedelta(minutes=5)
        self.assertEqual(time_ago(ts), "5 minutes ago")

    def test_hours_ago(self):
        ts = self.fixed_now - datetime.timedelta(hours=3)
        self.assertEqual(time_ago(ts), "3 hours ago")

    def test_yesterday(self):
        ts = self.fixed_now - datetime.timedelta(days=1)
        self.assertEqual(time_ago(ts), "yesterday")

    def test_days_ago(self):
        ts = self.fixed_now - datetime.timedelta(days=4)
        self.assertEqual(time_ago(ts), "4 days ago")

    def test_last_week(self):
        ts = self.fixed_now - datetime.timedelta(weeks=1)
        self.assertEqual(time_ago(ts), "last week")

    def test_weeks_ago(self):
        ts = self.fixed_now - datetime.timedelta(weeks=3)
        self.assertEqual(time_ago(ts), "3 weeks ago")

    def test_last_month(self):
        ts = self.fixed_now - datetime.timedelta(days=30)
        self.assertEqual(time_ago(ts), "last month")

    def test_months_ago(self):
        ts = self.fixed_now - datetime.timedelta(days=75)  # ~2.5 months
        self.assertEqual(time_ago(ts), "2 months ago")

    def test_last_year(self):
        ts = self.fixed_now - datetime.timedelta(days=365)
        self.assertEqual(time_ago(ts), "last year")

    def test_years_ago(self):
        ts = self.fixed_now - datetime.timedelta(days=800)  # >2 years
        self.assertEqual(time_ago(ts), "2 years ago")

if __name__ == "__main__":
    unittest.main()
