import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Mock rationale: ensure the test runs in isolation without touching the repository's data files.
# Mock rationale: add the utility's src directory to sys.path so we can import the module.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from mood_tracker import MoodTracker


class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the JSON storage.
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.tmp_dir.name) / "mood_data.json"
        self.tracker = MoodTracker(data_path=self.data_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    @mock.patch("datetime.date")
    def test_add_and_summary(self, mock_date):
        # Mock rationale: fix today's date to a known value for deterministic behavior.
        mock_date.today.return_value = mock.Mock()
        mock_date.today.return_value.isoformat.return_value = "2023-01-01"

        # Add three moods (two identical emojis).
        self.tracker.add_mood("2023-01-01", "😊")
        self.tracker.add_mood("2023-01-02", "😢")
        self.tracker.add_mood("2023-01-03", "😊")

        # Verify summary counts.
        summary = self.tracker.get_summary()
        self.assertEqual(summary, {"😊": 2, "😢": 1})

        # Verify that data persisted to the JSON file.
        with self.data_path.open("r", encoding="utf-8") as f:
            persisted = json.load(f)
        self.assertEqual(
            persisted,
            {
                "2023-01-01": "😊",
                "2023-01-02": "😢",
                "2023-01-03": "😊",
            },
        )


if __name__ == "__main__":
    unittest.main()
