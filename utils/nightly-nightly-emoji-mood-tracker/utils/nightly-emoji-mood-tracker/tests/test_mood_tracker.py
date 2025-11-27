import json
import os
import tempfile
import unittest
from pathlib import Path

# Mock rationale: Use a temporary directory so tests never touch the real user file.
from utils.nightly_emoji_mood_tracker.src.mood_tracker import MoodTracker

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for isolated storage
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "test_mood.json"
        self.tracker = MoodTracker(storage_path=self.storage_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_load_entry(self):
        # Add an entry and verify persistence
        self.tracker.add_entry("2025-11-27", "😊")
        # Re‑instantiate to force a reload from disk
        new_tracker = MoodTracker(storage_path=self.storage_path)
        self.assertIn("2025-11-27", new_tracker._data)
        self.assertEqual(new_tracker._data["2025-11-27"], "😊")

    def test_summary_counts(self):
        entries = [
            ("2025-11-20", "😊"),
            ("2025-11-21", "😢"),
            ("2025-11-22", "😊"),
            ("2025-11-23", "🤔"),
            ("2025-11-24", "😊"),
        ]
        for date, emoji in entries:
            self.tracker.add_entry(date, emoji)
        summary = self.tracker.get_summary()
        self.assertEqual(summary["😊"], 3)
        self.assertEqual(summary["😢"], 1)
        self.assertEqual(summary["🤔"], 1)

    def test_invalid_date_raises(self):
        with self.assertRaises(ValueError):
            self.tracker.add_entry("2025-13-01", "😊")  # Invalid month

    def test_empty_emoji_raises(self):
        with self.assertRaises(ValueError):
            self.tracker.add_entry("2025-11-27", "")

    def test_list_entries_sorted(self):
        self.tracker.add_entry("2025-11-25", "😢")
        self.tracker.add_entry("2025-11-20", "😊")
        self.tracker.add_entry("2025-11-22", "🤔")
        entries = self.tracker.list_entries()
        expected = [
            ("2025-11-20", "😊"),
            ("2025-11-22", "🤔"),
            ("2025-11-25", "😢"),
        ]
        self.assertEqual(entries, expected)

if __name__ == "__main__":
    unittest.main()
