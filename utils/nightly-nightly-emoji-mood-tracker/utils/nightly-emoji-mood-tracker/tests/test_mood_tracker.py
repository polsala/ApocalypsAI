import json
import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

# Import the module under test. Adjust sys.path to point to the src directory.
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import mood_tracker

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to isolate the log file.
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.original_home = os.environ.get("HOME", "")
        os.environ["HOME"] = self.tmp_dir.name
        # Ensure the module picks up the new HOME path.
        mood_tracker.LOG_PATH = Path(self.tmp_dir.name) / ".emoji_mood_log.json"

    def tearDown(self):
        # Restore original HOME and clean up.
        os.environ["HOME"] = self.original_home
        self.tmp_dir.cleanup()

    def test_add_and_retrieve_today(self):
        today = date.today()
        mood_tracker.add_mood(today, "😊", "Feeling good")
        # Load the file directly to verify persistence.
        with open(mood_tracker.LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn(today.isoformat(), data)
        entry = data[today.isoformat()]
        self.assertEqual(entry["emoji"], "😊")
        self.assertEqual(entry["note"], "Feeling good")

    def test_summary_includes_correct_range(self):
        # Mock date.today() to a fixed point for determinism.
        fixed_today = date(2025, 11, 25)
        with mock.patch.object(mood_tracker.date, "today", return_value=fixed_today):
            # Add entries for the last 3 days.
            for i in range(3):
                d = fixed_today - timedelta(days=i)
                mood_tracker.add_mood(d, "😀", f"Day {i}")
            # Request a 5‑day summary – should include the 3 entries and skip missing days.
            summary = mood_tracker.get_recent_summary(5)
            self.assertEqual(len(summary), 3)
            # Verify ordering: oldest first.
            self.assertEqual(summary[0]["timestamp"], (fixed_today - timedelta(days=2)).isoformat())
            self.assertEqual(summary[-1]["timestamp"], fixed_today.isoformat())

    def test_add_invalid_emoji_raises(self):
        with self.assertRaises(ValueError):
            mood_tracker.add_mood(date.today(), "", "No emoji")

    def test_summary_zero_days_raises(self):
        with self.assertRaises(ValueError):
            mood_tracker.get_recent_summary(0)

    def test_cli_add_today_via_argv(self):
        # Simulate CLI call: mood_tracker add 😊 "A note"
        test_argv = ["add", "😊", "A note"]
        with mock.patch.object(sys, "argv", ["mood_tracker"] + test_argv):
            mood_tracker.main()
        # Verify file content.
        with open(mood_tracker.LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn(date.today().isoformat(), data)
        self.assertEqual(data[date.today().isoformat()]["emoji"], "😊")
        self.assertEqual(data[date.today().isoformat()]["note"], "A note")

    def test_cli_add_specific_date(self):
        test_date = "2025-11-20"
        test_argv = ["add", test_date, "😢", "Bad day"]
        with mock.patch.object(sys, "argv", ["mood_tracker"] + test_argv):
            mood_tracker.main()
        with open(mood_tracker.LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn(test_date, data)
        self.assertEqual(data[test_date]["emoji"], "😢")
        self.assertEqual(data[test_date]["note"], "Bad day")

    def test_cli_summary_output(self):
        # Populate two days of data.
        today = date(2025, 11, 25)
        yesterday = today - timedelta(days=1)
        with mock.patch.object(mood_tracker.date, "today", return_value=today):
            mood_tracker.add_mood(yesterday, "🤔", "Thinking")
            mood_tracker.add_mood(today, "😁", "Happy")
            # Capture stdout.
            with mock.patch('sys.stdout') as mock_stdout:
                mood_tracker.main(["summary", "2"])  # request 2‑day summary
                # Ensure the printed lines contain both dates.
                printed = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
                self.assertIn(yesterday.isoformat(), printed)
                self.assertIn(today.isoformat(), printed)
                self.assertIn("🤔", printed)
                self.assertIn("😁", printed)

# Mock rationale: All external interactions (filesystem, date) are mocked or isolated via a temporary HOME directory,
# ensuring the tests run deterministically offline.

if __name__ == "__main__":
    unittest.main()
