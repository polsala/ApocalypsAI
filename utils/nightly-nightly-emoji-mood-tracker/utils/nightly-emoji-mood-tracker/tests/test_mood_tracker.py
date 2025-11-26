import unittest
import sys
from pathlib import Path
from unittest import mock

# Ensure the src directory is on the import path
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_PATH))

from mood_tracker import add_entry, summary, DATA_FILE

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Mock rationale: use a temporary file path to keep tests deterministic and offline.
        self.patcher = mock.patch('mood_tracker.DATA_FILE', Path('test_mood_data.json'))
        self.mock_data_file = self.patcher.start()
        # Clean up any leftover file from previous runs
        if self.mock_data_file.exists():
            self.mock_data_file.unlink()

    def tearDown(self):
        self.patcher.stop()
        if self.mock_data_file.exists():
            self.mock_data_file.unlink()

    def test_add_and_summary(self):
        add_entry('2025-11-25', '😊')
        add_entry('2025-11-26', '😢')
        add_entry('2025-11-27', '😊')
        result = summary()
        expected = {'😊': 2, '😢': 1}
        self.assertEqual(result, expected)

    def test_replace_entry(self):
        add_entry('2025-11-25', '😊')
        # Adding another entry for the same date should replace the previous one
        add_entry('2025-11-25', '😎')
        result = summary()
        self.assertEqual(result, {'😎': 1})

if __name__ == '__main__':
    unittest.main()
