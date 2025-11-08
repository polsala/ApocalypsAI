import unittest
from unittest.mock import mock_open, patch, MagicMock
from datetime import date

# Mock rationale: we replace file system interactions and the current date to keep tests deterministic and offline.

from emoji_mood_tracker.src.tracker import log_mood, summary, _load_log, _save_log, LOG_PATH

class TestEmojiMoodTracker(unittest.TestCase):
    def setUp(self):
        # Ensure LOG_PATH is mocked to avoid touching real home directory.
        self.patcher_path = patch('emoji_mood_tracker.src.tracker.LOG_PATH', new=MagicMock())
        self.mock_path = self.patcher_path.start()
        self.addCleanup(self.patcher_path.stop)
        # Mock the open function used by _load_log/_save_log.
        self.mock_file = mock_open()
        self.patcher_open = patch('emoji_mood_tracker.src.tracker.open', self.mock_file)
        self.patcher_open.start()
        self.addCleanup(self.patcher_open.stop)
        # Mock json.load/dump to work with the mock file.
        self.patcher_json_load = patch('emoji_mood_tracker.src.tracker.json.load', return_value=[])
        self.mock_json_load = self.patcher_json_load.start()
        self.addCleanup(self.patcher_json_load.stop)
        self.patcher_json_dump = patch('emoji_mood_tracker.src.tracker.json.dump')
        self.mock_json_dump = self.patcher_json_dump.start()
        self.addCleanup(self.patcher_json_dump.stop)

    def test_log_mood_appends_entry(self):
        fake_today = date(2023, 1, 15)
        with patch('emoji_mood_tracker.src.tracker.date') as mock_date:
            mock_date.today.return_value = fake_today
            log_mood('😊', 'Feeling great')
        # Verify that json.load was called (reading existing entries)
        self.mock_json_load.assert_called_once()
        # Verify that json.dump was called with a list containing our entry
        args, _ = self.mock_json_dump.call_args
        saved_entries = args[0]
        self.assertEqual(len(saved_entries), 1)
        entry = saved_entries[0]
        self.assertEqual(entry['emoji'], '😊')
        self.assertEqual(entry['note'], 'Feeling great')
        self.assertEqual(entry['date'], fake_today.isoformat())

    def test_summary_counts_correctly(self):
        # Prepare a fake log with entries spanning several days.
        fake_entries = [
            {"date": "2023-01-10", "emoji": "😊", "note": "", "timestamp": ""},
            {"date": "2023-01-11", "emoji": "😢", "note": "", "timestamp": ""},
            {"date": "2023-01-12", "emoji": "😊", "note": "", "timestamp": ""},
            {"date": "2023-01-13", "emoji": "😡", "note": "", "timestamp": ""},
            {"date": "2023-01-14", "emoji": "😊", "note": "", "timestamp": ""},
        ]
        self.mock_json_load.return_value = fake_entries
        fake_today = date(2023, 1, 14)
        with patch('emoji_mood_tracker.src.tracker.date') as mock_date, 
             patch('builtins.print') as mock_print:
            mock_date.today.return_value = fake_today
            summary(days=5)
        # Expect counts: 😊 -> 3, 😢 -> 1, 😡 -> 1
        mock_print.assert_any_call('Mood summary for the last 5 days (including 2023-01-14):')
        mock_print.assert_any_call('😊: 3')
        mock_print.assert_any_call('😢: 1')
        mock_print.assert_any_call('😡: 1')

    def test_summary_no_entries(self):
        self.mock_json_load.return_value = []
        fake_today = date(2023, 1, 14)
        with patch('emoji_mood_tracker.src.tracker.date') as mock_date, 
             patch('builtins.print') as mock_print:
            mock_date.today.return_value = fake_today
            summary(days=7)
        mock_print.assert_called_once_with('No mood entries in the requested period.')

if __name__ == '__main__':
    unittest.main()
