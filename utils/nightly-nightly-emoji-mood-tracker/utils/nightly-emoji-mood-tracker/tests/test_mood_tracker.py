import os
import tempfile
import unittest
from datetime import datetime, timedelta

# Mock rationale: we import the module from the relative path without installing it.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from mood_tracker import MoodTracker

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the log file to avoid polluting the repo.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.temp_dir.name, "mood_log.json")
        self.tracker = MoodTracker(log_path=self.log_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_read_entry(self):
        date = "2025-12-01"
        emoji = "😄"
        self.tracker.add_entry(date, emoji)
        # Re‑instantiate to ensure persistence works.
        new_tracker = MoodTracker(log_path=self.log_path)
        summary = new_tracker.get_summary(days=365)
        self.assertEqual(summary["total_entries"], 1)
        self.assertEqual(summary["counts"].get(emoji), 1)
        self.assertEqual(summary["most_common"], emoji)

    def test_summary_window(self):
        # Add entries spanning 10 days.
        base_date = datetime.utcnow().date()
        emojis = ["😄", "😐", "😢"]
        for i in range(10):
            d = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
            self.tracker.add_entry(d, emojis[i % len(emojis)])
        # Summarize last 5 days.
        summary = self.tracker.get_summary(days=5)
        self.assertEqual(summary["total_entries"], 5)
        # Expect counts: 2 of 😄, 2 of 😐, 1 of 😢 (depending on ordering)
        self.assertEqual(summary["counts"].get("😄"), 2)
        self.assertEqual(summary["counts"].get("😐"), 2)
        self.assertEqual(summary["counts"].get("😢"), 1)
        # Most common should be either 😄 or 😐 (both have same count). Accept either.
        self.assertIn(summary["most_common"], ["😄", "😐"])

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            self.tracker.add_entry("2025/12/01", "😄")

    def test_invalid_emoji(self):
        with self.assertRaises(ValueError):
            self.tracker.add_entry("2025-12-01", "")

    def test_negative_days(self):
        with self.assertRaises(ValueError):
            self.tracker.get_summary(days=-1)

if __name__ == "__main__":
    unittest.main()
