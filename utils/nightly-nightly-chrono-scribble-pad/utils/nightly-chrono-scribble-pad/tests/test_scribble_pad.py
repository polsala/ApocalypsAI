import unittest
import os
import json
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta

# Import functions from the main script
# Adjust path for testing context
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scribble_pad

# Define a mock notes file path for tests
MOCK_NOTES_FILE = os.path.join(os.path.dirname(__file__), 'mock_chrono_scribble_notes.json')
scribble_pad.NOTES_FILE = MOCK_NOTES_FILE # Redirect the notes file for testing

class TestChronoScribblePad(unittest.TestCase):

    def setUp(self):
        # Ensure the mock file is clean before each test
        if os.path.exists(MOCK_NOTES_FILE):
            os.remove(MOCK_NOTES_FILE)
        self.mock_file_content = "[]"

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(MOCK_NOTES_FILE):
            os.remove(MOCK_NOTES_FILE)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_load_notes_empty_file(self, mock_exists, mock_open_func):
        # Mock rationale: Simulate an empty or non-existent notes file.
        self.assertEqual(scribble_pad._load_notes(), [])
        mock_exists.assert_called_with(MOCK_NOTES_FILE)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "content": "Test", "created_at": "2023-01-01T10:00:00", "expires_at": "2023-01-01T11:00:00"}]')
    @patch('os.path.exists', return_value=True)
    def test_load_notes_existing_file(self, mock_exists, mock_open_func):
        # Mock rationale: Simulate an existing notes file with content.
        expected_notes = [{'id': 1, 'content': 'Test', 'created_at': '2023-01-01T10:00:00', 'expires_at': '2023-01-01T11:00:00'}]
        self.assertEqual(scribble_pad._load_notes(), expected_notes)
        mock_exists.assert_called_with(MOCK_NOTES_FILE)
        mock_open_func.assert_called_with(MOCK_NOTES_FILE, 'r')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_notes(self, mock_open_func):
        # Mock rationale: Simulate saving notes to a file.
        notes_to_save = [{'id': 1, 'content': 'New Note', 'created_at': '2023-01-01T12:00:00', 'expires_at': '2023-01-01T13:00:00'}]
        scribble_pad._save_notes(notes_to_save)
        mock_open_func.assert_called_with(MOCK_NOTES_FILE, 'w')
        handle = mock_open_func()
        handle.write.assert_called_once_with(json.dumps(notes_to_save, indent=2))

    def test_parse_duration_valid(self):
        self.assertEqual(scribble_pad.parse_duration("10s"), timedelta(seconds=10))
        self.assertEqual(scribble_pad.parse_duration("5m"), timedelta(minutes=5))
        self.assertEqual(scribble_pad.parse_duration("2h"), timedelta(hours=2))
        self.assertEqual(scribble_pad.parse_duration("3d"), timedelta(days=3))
        self.assertEqual(scribble_pad.parse_duration("1w"), timedelta(weeks=1))

    def test_parse_duration_default(self):
        self.assertEqual(scribble_pad.parse_duration(None), timedelta(hours=24))

    def test_parse_duration_invalid(self):
        with self.assertRaises(ValueError):
            scribble_pad.parse_duration("10x")
        with self.assertRaises(ValueError):
            scribble_pad.parse_duration("abc")

    @patch('scribble_pad._load_notes', return_value=[])
    @patch('scribble_pad._save_notes')
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_add_note(self, mock_print, mock_datetime, mock_save, mock_load):
        # Mock rationale: Control current time and file operations for deterministic testing.
        mock_now = datetime(2023, 1, 1, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for parsing
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime object creation

        scribble_pad.add_note("Test Note", timedelta(hours=1))

        expected_expiry = (mock_now + timedelta(hours=1)).isoformat()
        mock_save.assert_called_once()
        saved_notes = mock_save.call_args[0][0]
        self.assertEqual(len(saved_notes), 1)
        self.assertEqual(saved_notes[0]['content'], "Test Note")
        self.assertEqual(saved_notes[0]['expires_at'], expected_expiry)
        mock_print.assert_called_once_with(f"Note added (ID: 1). Expires at: {expected_expiry}")

    @patch('scribble_pad._load_notes', return_value=[])
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_list_notes_empty(self, mock_datetime, mock_print, mock_load):
        # Mock rationale: Simulate no notes existing.
        mock_now = datetime(2023, 1, 1, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat

        scribble_pad.list_notes()
        mock_print.assert_called_once_with("No active chrono-scribbles found.")

    @patch('scribble_pad._load_notes')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_list_notes_active_and_expired(self, mock_datetime, mock_print, mock_load):
        # Mock rationale: Simulate notes with mixed expiry states.
        mock_now = datetime(2023, 1, 1, 10, 30, 0) # Current time
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat

        # Note 1: Active (expires in future)
        # Note 2: Expired (expires in past)
        # Note 3: Active (expires in future)
        mock_notes = [
            {'id': 1, 'content': 'Active Note 1', 'created_at': '2023-01-01T10:00:00', 'expires_at': '2023-01-01T11:00:00'},
            {'id': 2, 'content': 'Expired Note', 'created_at': '2023-01-01T09:00:00', 'expires_at': '2023-01-01T10:00:00'},
            {'id': 3, 'content': 'Active Note 2', 'created_at': '2023-01-01T10:15:00', 'expires_at': '2023-01-01T10:45:00'}
        ]
        mock_load.return_value = mock_notes

        scribble_pad.list_notes()

        expected_calls = [
            unittest.mock.call("--- Active Chrono-Scribbles ---"),
            unittest.mock.call("ID: 1\n  Content: Active Note 1\n  Expires in: 0:30:00\n"),
            unittest.mock.call("ID: 3\n  Content: Active Note 2\n  Expires in: 0:15:00\n"),
            unittest.mock.call("-------------------------------")
        ]
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(mock_print.call_count, 4)

    @patch('scribble_pad._load_notes')
    @patch('scribble_pad._save_notes')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_clean_expired_notes(self, mock_datetime, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate notes with mixed expiry states and verify cleanup.
        mock_now = datetime(2023, 1, 1, 10, 30, 0) # Current time
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat

        mock_notes = [
            {'id': 1, 'content': 'Active Note 1', 'created_at': '2023-01-01T10:00:00', 'expires_at': '2023-01-01T11:00:00'},
            {'id': 2, 'content': 'Expired Note', 'created_at': '2023-01-01T09:00:00', 'expires_at': '2023-01-01T10:00:00'},
            {'id': 3, 'content': 'Active Note 2', 'created_at': '2023-01-01T10:15:00', 'expires_at': '2023-01-01T10:45:00'}
        ]
        mock_load.return_value = mock_notes

        scribble_pad.clean_expired_notes()

        expected_active_notes = [
            {'id': 1, 'content': 'Active Note 1', 'created_at': '2023-01-01T10:00:00', 'expires_at': '2023-01-01T11:00:00'},
            {'id': 3, 'content': 'Active Note 2', 'created_at': '2023-01-01T10:15:00', 'expires_at': '2023-01-01T10:45:00'}
        ]
        mock_save.assert_called_once_with(expected_active_notes)
        mock_print.assert_called_once_with("Cleaned up 1 expired chrono-scribbles.")

    @patch('scribble_pad._load_notes', return_value=[{'id': 1, 'content': 'Active Note', 'created_at': '2023-01-01T10:00:00', 'expires_at': '2023-01-01T11:00:00'}])
    @patch('scribble_pad._save_notes')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_clean_expired_notes_no_cleanup_needed(self, mock_datetime, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate no expired notes to ensure correct message.
        mock_now = datetime(2023, 1, 1, 10, 30, 0) # Current time
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat

        scribble_pad.clean_expired_notes()

        # Should save the same list back if nothing expired
        mock_save.assert_called_once_with(mock_load.return_value)
        mock_print.assert_called_once_with("No expired chrono-scribbles to clean.")

    @patch('sys.argv', ['scribble_pad.py', 'add', 'Test CLI Note', '--expires-in', '1h'])
    @patch('scribble_pad.add_note')
    @patch('scribble_pad.parse_duration', return_value=timedelta(hours=1))
    def test_main_add_command(self, mock_parse_duration, mock_add_note):
        # Mock rationale: Simulate command-line arguments and verify function calls.
        scribble_pad.main()
        mock_parse_duration.assert_called_once_with('1h')
        mock_add_note.assert_called_once_with('Test CLI Note', timedelta(hours=1))

    @patch('sys.argv', ['scribble_pad.py', 'list'])
    @patch('scribble_pad.list_notes')
    def test_main_list_command(self, mock_list_notes):
        # Mock rationale: Simulate command-line arguments and verify function calls.
        scribble_pad.main()
        mock_list_notes.assert_called_once()

    @patch('sys.argv', ['scribble_pad.py', 'clean'])
    @patch('scribble_pad.clean_expired_notes')
    def test_main_clean_command(self, mock_clean_expired_notes):
        # Mock rationale: Simulate command-line arguments and verify function calls.
        scribble_pad.main()
        mock_clean_expired_notes.assert_called_once()

    @patch('sys.argv', ['scribble_pad.py', 'add', 'Invalid Duration', '--expires-in', '1x'])
    @patch('scribble_pad.parse_duration', side_effect=ValueError('Invalid unit'))
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_add_command_invalid_duration_error(self, mock_exit, mock_print, mock_parse_duration):
        # Mock rationale: Test error handling for invalid duration input.
        mock_exit.side_effect = SystemExit # Prevent actual exit during test
        with self.assertRaises(SystemExit):
            scribble_pad.main()
        mock_print.assert_called_once_with("Error: Invalid unit", file=sys.stderr)
        mock_exit.assert_called_once_with(1)
