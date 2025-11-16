import unittest
from unittest.mock import mock_open, patch
import json
from src.tracker import MoodTracker


class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # In‑memory fake file system
        self.fake_files = {}

        # Mock rationale: intercept file reads/writes to avoid disk I/O.
        def _mock_open(file, mode="r", *args, **kwargs):
            if "b" in mode:
                raise ValueError("binary mode not supported in mock")
            if "r" in mode:
                data = self.fake_files.get(file, "")
                return mock_open(read_data=data).return_value
            elif "w" in mode:
                m = mock_open().return_value
                def write(content):
                    self.fake_files[file] = content
                m.write.side_effect = write
                return m
            else:
                raise ValueError(f"Unsupported mode {mode}")

        self.open_patcher = patch("builtins.open", new=_mock_open)
        self.exists_patcher = patch("os.path.exists", side_effect=lambda p: p in self.fake_files)
        self.open_patcher.start()
        self.exists_patcher.start()

    def tearDown(self):
        self.open_patcher.stop()
        self.exists_patcher.stop()

    def test_add_and_load(self):
        tracker = MoodTracker(db_path="fake.json")
        tracker.add_entry("2025-11-16", "😊")
        # Verify that the file now contains the entry
        self.assertIn("fake.json", self.fake_files)
        data = json.loads(self.fake_files["fake.json"])
        self.assertEqual(data["2025-11-16"], "😊")

        # New instance should load existing data
        tracker2 = MoodTracker(db_path="fake.json")
        self.assertEqual(tracker2._data["2025-11-16"], "😊")

    def test_week_summary(self):
        tracker = MoodTracker(db_path="fake.json")
        tracker.add_entry("2025-11-10", "😀")
        tracker.add_entry("2025-11-12", "😢")
        week = tracker.get_week_summary("2025-11-10")
        expected = [
            ("2025-11-10", "😀"),
            ("2025-11-11", ""),
            ("2025-11-12", "😢"),
            ("2025-11-13", ""),
            ("2025-11-14", ""),
            ("2025-11-15", ""),
            ("2025-11-16", ""),
        ]
        self.assertEqual(week, expected)

    def test_invalid_date_raises(self):
        tracker = MoodTracker(db_path="fake.json")
        with self.assertRaises(ValueError):
            tracker.add_entry("2025-13-01", "🤔")  # invalid month


if __name__ == "__main__":
    unittest.main()
