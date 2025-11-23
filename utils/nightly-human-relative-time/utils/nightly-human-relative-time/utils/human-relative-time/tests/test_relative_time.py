import unittest
import sys
import os
from datetime import datetime, timezone, timedelta

# Adjust path so the src module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from relative_time import format_relative


class TestRelativeTime(unittest.TestCase):
    def setUp(self):
        # Fixed reference time for deterministic tests
        self.now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_just_now(self):
        self.assertEqual(format_relative(self.now, self.now), "just now")

    def test_seconds_ago(self):
        past = self.now - timedelta(seconds=30)
        self.assertEqual(format_relative(past, self.now), "30 seconds ago")

    def test_seconds_future(self):
        future = self.now + timedelta(seconds=45)
        self.assertEqual(format_relative(future, self.now), "in 45 seconds")

    def test_minutes_ago(self):
        past = self.now - timedelta(minutes=5)
        self.assertEqual(format_relative(past, self.now), "5 minutes ago")

    def test_hours_future(self):
        future = self.now + timedelta(hours=2)
        self.assertEqual(format_relative(future, self.now), "in 2 hours")

    def test_days_ago(self):
        past = self.now - timedelta(days=1)
        self.assertEqual(format_relative(past, self.now), "1 day ago")

    def test_weeks_future(self):
        future = self.now + timedelta(weeks=3)
        self.assertEqual(format_relative(future, self.now), "in 3 weeks")

    # Mock rationale: No external network calls; deterministic timestamps ensure offline testing.


if __name__ == "__main__":
    unittest.main()
