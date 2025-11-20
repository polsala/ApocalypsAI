import json
import unittest
from pathlib import Path
from unittest import mock

# Mock rationale: we patch Path.home() to a temporary directory so the real user file is untouched.

from src.mood_tracker import add_mood, show_summary, DATA_FILE

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the fake home
        self.tmp_dir = Path(__file__).parent / "tmp_home"
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.patcher = mock.patch('pathlib.Path.home', return_value=self.tmp_dir)
        self.mock_home = self.patcher.start()
        # Ensure the data file path points inside the temp dir
        global DATA_FILE
        DATA_FILE = self.tmp_dir / ".emoji_mood_tracker.json"

    def tearDown(self):
        self.patcher.stop()
        # Clean up temporary files
        if DATA_FILE.exists():
            DATA_FILE.unlink()
        for child in self.tmp_dir.iterdir():
            child.unlink()
        self.tmp_dir.rmdir()

    @mock.patch('src.mood_tracker.date')
    def test_add_and_show(self, mock_date):
        # Mock rationale: fix today's date to a known value for deterministic output.
        mock_date.today.return_value = mock.Mock(isoformat=lambda: "2025-11-20")
        # Add two moods on the same day (second should overwrite)
        add_mood("😊")
        add_mood("😢")
        # Add a mood for a different day
        add_mood("😊", on_date="2025-11-19")
        # Verify file content directly
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        expected = {
            "2025-11-20": "😢",
            "2025-11-19": "😊"
        }
        self.assertEqual(data, expected)
        # Capture stdout of show_summary
        with mock.patch('sys.stdout') as mock_stdout:
            show_summary()
            # Build expected printed lines (order may vary, but Counter.most_common ensures deterministic order)
            expected_calls = [
                mock.call.write('Mood histogram:\n'),
                mock.call.write('😢 : 1 (50.0%)\n'),
                mock.call.write('😊 : 1 (50.0%)\n')
            ]
            # Flatten actual calls to write()
            actual_calls = [c for c in mock_stdout.method_calls if c[0] == 'write']
            self.assertEqual(actual_calls, expected_calls)

if __name__ == '__main__':
    unittest.main()
