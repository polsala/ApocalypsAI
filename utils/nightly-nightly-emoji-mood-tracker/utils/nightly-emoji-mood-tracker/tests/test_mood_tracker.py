import datetime
import json
import pathlib
import tempfile
import unittest
from unittest import mock

# Mock rationale: All filesystem interactions are redirected to a temporary directory so tests are deterministic and do not affect the real user environment.

from utils.nightly_emoji_mood_tracker.src.mood_tracker import MoodTracker


class TestMoodTracker(unittest.TestCase):
    def setUp(self) -> None:
        # Create an isolated temporary directory for the JSON storage file.
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = pathlib.Path(self.tmp_dir.name) / "mood.json"
        self.tracker = MoodTracker(storage_path=self.storage_path)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_add_and_get_entry(self):
        test_date = datetime.date(2023, 10, 31)
        self.tracker.add_entry(test_date, "🎃")
        # Verify that the entry is persisted correctly.
        self.assertEqual(self.tracker.get_entry(test_date), "🎃")
        # Directly read the JSON file to ensure proper serialization.
        with self.storage_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("2023-10-31", data)
        self.assertEqual(data["2023-10-31"], "🎃")

    def test_summary_counts(self):
        # Populate several entries.
        entries = [
            (datetime.date(2023, 10, 1), "😊"),
            (datetime.date(2023, 10, 2), "😊"),
            (datetime.date(2023, 10, 3), "😢"),
            (datetime.date(2023, 10, 4), "😊"),
        ]
        for d, e in entries:
            self.tracker.add_entry(d, e)
        # Mock rationale: Use a fixed date range to make the test deterministic.
        start = datetime.date(2023, 10, 1)
        end = datetime.date(2023, 10, 4)
        summary = self.tracker.summary(start, end)
        self.assertEqual(summary, {"😊": 3, "😢": 1})

    def test_summary_excludes_out_of_range(self):
        self.tracker.add_entry(datetime.date(2023, 9, 30), "😎")
        self.tracker.add_entry(datetime.date(2023, 10, 1), "😊")
        self.tracker.add_entry(datetime.date(2023, 10, 5), "😢")
        start = datetime.date(2023, 10, 1)
        end = datetime.date(2023, 10, 4)
        summary = self.tracker.summary(start, end)
        self.assertEqual(summary, {"😊": 1})

    @mock.patch("datetime.date")
    def test_add_entry_defaults_to_today(self, mock_date):
        # Mock rationale: Force datetime.date.today() to a known value.
        mock_date.today.return_value = datetime.date(2023, 11, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        tracker = MoodTracker(storage_path=self.storage_path)
        tracker.add_entry(datetime.date.today(), "🤖")
        self.assertEqual(tracker.get_entry(datetime.date(2023, 11, 1)), "🤖")


if __name__ == "__main__":
    unittest.main()
