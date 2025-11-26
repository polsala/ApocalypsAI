import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

# Adjust sys.path so we can import the module under src/ without installing a package.
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import mood_tracker

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to act as the JSON store.
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.addCleanup(os.unlink, self.temp_file.name)

        # Patch get_data_path to return the temporary file path.
        # Mock rationale: isolates file I/O from the real user home directory.
        patcher = mock.patch.object(mood_tracker, "get_data_path", return_value=self.temp_file.name)
        self.mock_path = patcher.start()
        self.addCleanup(patcher.stop)

    def test_add_and_load(self):
        mood_tracker.add_mood("😊", "2023-01-01")
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, {"2023-01-01": "😊"})

    def test_summary_counts(self):
        mood_tracker.add_mood("😊", "2023-01-01")
        mood_tracker.add_mood("😢", "2023-01-02")
        mood_tracker.add_mood("😊", "2023-01-03")
        summary = mood_tracker.get_summary()
        self.assertEqual(summary, {"😊": 2, "😢": 1})

    def test_overwrite_same_date(self):
        mood_tracker.add_mood("😊", "2023-01-01")
        mood_tracker.add_mood("😎", "2023-01-01")  # Overwrite existing entry
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, {"2023-01-01": "😎"})

if __name__ == "__main__":
    unittest.main()
