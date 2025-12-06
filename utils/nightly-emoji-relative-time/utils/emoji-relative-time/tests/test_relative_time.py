import unittest
from datetime import datetime, timedelta, timezone

# Import the function under test
from src.relative_time import format_relative_time

class TestEmojiRelativeTime(unittest.TestCase):
    def setUp(self):
        # Fixed reference point for deterministic tests
        self.now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_seconds(self):
        past = self.now - timedelta(seconds=45)
        self.assertEqual(format_relative_time(past, self.now), "🕐 45 seconds ago")

    def test_one_minute(self):
        past = self.now - timedelta(minutes=1)
        self.assertEqual(format_relative_time(past, self.now), "🕑 1 minute ago")

    def test_multiple_minutes(self):
        past = self.now - timedelta(minutes=5, seconds=10)
        self.assertEqual(format_relative_time(past, self.now), "🕑 5 minutes ago")

    def test_hours(self):
        past = self.now - timedelta(hours=2, minutes=15)
        self.assertEqual(format_relative_time(past, self.now), "🕒 2 hours ago")

    def test_days(self):
        past = self.now - timedelta(days=3, hours=4)
        self.assertEqual(format_relative_time(past, self.now), "📅 3 days ago")

    def test_weeks(self):
        past = self.now - timedelta(weeks=2, days=1)
        self.assertEqual(format_relative_time(past, self.now), "📆 2 weeks ago")

    def test_months(self):
        # Approximate month as 30 days per implementation
        past = self.now - timedelta(days=65)  # >2 months but <1 year
        self.assertEqual(format_relative_time(past, self.now), "🌙 2 months ago")

    def test_years(self):
        past = self.now - timedelta(days=400)
        self.assertEqual(format_relative_time(past, self.now), "🎉 1 year ago")

    def test_future_error(self):
        future = self.now + timedelta(seconds=10)
        with self.assertRaises(ValueError):
            format_relative_time(future, self.now)

# Mock rationale comments (no external calls in this utility)
# Mock rationale: All datetime calculations are performed locally; no network I/O.

if __name__ == "__main__":
    unittest.main()
