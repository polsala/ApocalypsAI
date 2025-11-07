import unittest
import datetime
from utils.time_ago_cli.src.main import time_ago, _humanize_delta, _emoji_for_delta

class TestTimeAgo(unittest.TestCase):
    def setUp(self):
        # Fixed reference point for deterministic tests
        self.now = datetime.datetime(2023, 8, 20, 12, 0, 0, tzinfo=datetime.timezone.utc)
        # Monkey‑patch datetime.datetime.now to return the fixed point
        datetime.datetime.now = lambda tz=None: self.now if tz else self.now.replace(tzinfo=None)

    def test_seconds_ago(self):
        ts = self.now - datetime.timedelta(seconds=5)
        self.assertEqual(time_ago(ts), "just now")
        ts = self.now - datetime.timedelta(seconds=45)
        self.assertEqual(time_ago(ts), "45 seconds ago")

    def test_minutes_ago(self):
        ts = self.now - datetime.timedelta(minutes=2)
        self.assertEqual(time_ago(ts), "2 minutes ago")

    def test_hours_ago(self):
        ts = self.now - datetime.timedelta(hours=3, minutes=15)
        self.assertEqual(time_ago(ts), "3 hours ago")

    def test_days_ago(self):
        ts = self.now - datetime.timedelta(days=10)
        self.assertEqual(time_ago(ts), "10 days ago")

    def test_months_ago(self):
        ts = self.now - datetime.timedelta(days=75)  # ~2 months
        self.assertEqual(time_ago(ts), "2 months ago")

    def test_years_ago(self):
        ts = self.now - datetime.timedelta(days=400)  # >1 year
        self.assertEqual(time_ago(ts), "1 year ago")

    def test_future(self):
        ts = self.now + datetime.timedelta(hours=1)
        self.assertEqual(time_ago(ts), "in the future")

    def test_emoji_flag(self):
        ts = self.now - datetime.timedelta(minutes=5)
        self.assertEqual(time_ago(ts, emoji=True), "5 minutes ago 🌱")
        ts = self.now - datetime.timedelta(days=200)
        self.assertEqual(time_ago(ts, emoji=True), "6 months ago 🍂")

    # Direct tests for internal helpers (mock rationale comments)
    def test_humanize_delta(self):
        # Mock rationale: ensure boundary conditions are correct
        self.assertEqual(_humanize_delta(datetime.timedelta(seconds=9)), "just now")
        self.assertEqual(_humanize_delta(datetime.timedelta(seconds=30)), "30 seconds ago")
        self.assertEqual(_humanize_delta(datetime.timedelta(minutes=1)), "1 minute ago")
        self.assertEqual(_humanize_delta(datetime.timedelta(hours=23)), "23 hours ago")
        self.assertEqual(_humanize_delta(datetime.timedelta(days=29)), "29 days ago")
        self.assertEqual(_humanize_delta(datetime.timedelta(days=30)), "1 month ago")
        self.assertEqual(_humanize_delta(datetime.timedelta(days=365)), "1 year ago")

    def test_emoji_for_delta(self):
        # Mock rationale: deterministic mapping for test stability
        self.assertEqual(_emoji_for_delta(datetime.timedelta(seconds=30)), "⏱️")
        self.assertEqual(_emoji_for_delta(datetime.timedelta(minutes=10)), "🌱")
        self.assertEqual(_emoji_for_delta(datetime.timedelta(hours=5)), "🌿")
        self.assertEqual(_emoji_for_delta(datetime.timedelta(days=10)), "🌳")
        self.assertEqual(_emoji_for_delta(datetime.timedelta(days=200)), "🍂")
        self.assertEqual(_emoji_for_delta(datetime.timedelta(days=800)), "🪐")

if __name__ == "__main__":
    unittest.main()
