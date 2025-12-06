import unittest
from unittest.mock import patch, mock_open
import json
import pathlib
import sys

# Adjust sys.path so the src module can be imported
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from src.mood_tracker import add_mood, get_summary, DATA_FILE

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Mock today's date to a fixed value for deterministic tests
        self.patcher_date = patch('src.mood_tracker.date')
        mock_date = self.patcher_date.start()
        mock_date.today.return_value = type('d', (), {'isoformat': lambda: '2025-01-01'})()

    def tearDown(self):
        self.patcher_date.stop()

    @patch.object(DATA_FILE, 'exists')
    @patch.object(DATA_FILE, 'write_text')
    @patch.object(DATA_FILE, 'read_text')
    def test_add_mood_creates_entry(self, mock_read, mock_write, mock_exists):
        # Mock file does not exist initially
        mock_exists.return_value = False
        add_mood('😊')
        # Verify that write_text was called with correct JSON content
        expected = {'2025-01-01': '😊'}
        mock_write.assert_called_once()
        written_content = mock_write.call_args[0][0]
        self.assertEqual(json.loads(written_content), expected)

    @patch.object(DATA_FILE, 'exists')
    @patch.object(DATA_FILE, 'read_text')
    def test_summary_counts_emojis(self, mock_read, mock_exists):
        # Mock existing data with multiple entries
        mock_exists.return_value = True
        mock_read.return_value = json.dumps({
            '2025-01-01': '😊',
            '2025-01-02': '😢',
            '2025-01-03': '😊'
        })
        summary = get_summary()
        self.assertEqual(summary['😊'], 2)
        self.assertEqual(summary['😢'], 1)

    # Mock rationale: ensure no real file I/O occurs during tests, keeping them deterministic and offline.

if __name__ == '__main__':
    unittest.main()
