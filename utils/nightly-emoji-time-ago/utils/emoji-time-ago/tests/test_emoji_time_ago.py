import unittest
import datetime
from src.emoji_time_ago import format_time_ago

class TestEmojiTimeAgo(unittest.TestCase):
    def setUp(self):
        # Fixed reference point for deterministic tests.
        self.fixed_now = datetime.datetime(2025, 11, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_just_now(self):
        ts = "2025-11-15T12:00:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        self.assertEqual(result, "⏱️ just now")

    def test_minutes_ago(self):
        ts = "2025-11-15T11:45:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        self.assertEqual(result, "⏱️ 15 minutes ago")

    def test_hours_ago(self):
        ts = "2025-11-15T09:00:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        self.assertEqual(result, "🕒 3 hours ago")

    def test_days_ago(self):
        ts = "2025-11-13T12:00:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        self.assertEqual(result, "🌅 2 days ago")

    def test_weeks_ago(self):
        ts = "2025-10-31T12:00:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        self.assertEqual(result, "📆 2 weeks ago")

    def test_future_timestamp(self):
        ts = "2025-11-16T00:00:00Z"
        result = format_time_ago(ts, now=self.fixed_now)
        # Future timestamps are treated as "just now" with the smallest emoji.
        self.assertEqual(result, "⏱️ just now")

    def test_invalid_timestamp(self):
        ts = "not-a-timestamp"
        with self.assertRaises(ValueError) as ctx:
            format_time_ago(ts, now=self.fixed_now)
        self.assertIn("Invalid ISO‑8601 timestamp", str(ctx.exception))

# Mock rationale:
# The tests inject a deterministic ``now`` datetime, avoiding any real‑time dependency.
# No external network calls are performed; all logic is pure Python.

if __name__ == "__main__":
    unittest.main()
