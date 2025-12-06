import unittest
from unittest import mock
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os
import io
import sys

# Import the functions from the journal script
# Mock rationale: We need to mock the _get_log_path function to ensure tests are self-contained
# and don't create actual files in the source directory or rely on relative paths.
with patch('os.path.dirname', return_value='/mock/path/src'), \
     patch('os.path.abspath', return_value='/mock/path/src/journal.py'):
    from src.journal import add_entry, view_entries, search_entries, main, LOG_FILE

# Define a fixed datetime for deterministic tests
FIXED_DATETIME_STR = '2023-10-27 10:00:00'
FIXED_DATETIME_OBJ = datetime.datetime.strptime(FIXED_DATETIME_STR, '%Y-%m-%d %H:%M:%S')

class TestJournal(unittest.TestCase):

    def setUp(self):
        # Mock rationale: We don't want tests to create real files. Instead, we'll use an in-memory mock.
        self.mock_log_file_path = '/mock/path/src/gratitude_log.txt'

        # Mock datetime.datetime.now() to ensure consistent timestamps
        # Mock rationale: `datetime.datetime.now()` is non-deterministic. Patching it ensures tests always use the same timestamp.
        self.mock_datetime = patch('datetime.datetime')
        self.mock_datetime_obj = self.mock_datetime.start()
        self.mock_datetime_obj.now.return_value = FIXED_DATETIME_OBJ
        self.mock_datetime_obj.strptime = datetime.datetime.strptime # Keep original strptime
        self.mock_datetime_obj.strftime = datetime.datetime.strftime # Keep original strftime

        # Mock _get_log_path to return our mock path
        # Mock rationale: Ensures the utility tries to access a controlled path, not a real file system path.
        self.patch_get_log_path = patch('src.journal._get_log_path', return_value=self.mock_log_file_path)
        self.patch_get_log_path.start()

        # Capture stdout for testing print statements
        # Mock rationale: `print()` writes to stdout, which is non-testable directly. Capturing it allows assertion on output.
        self.held_stdout = io.StringIO()
        sys.stdout = self.held_stdout

    def tearDown(self):
        self.mock_datetime.stop()
        self.patch_get_log_path.stop()
        sys.stdout = sys.__stdout__ # Restore stdout

    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_file_open):
        entry_text = "A beautiful sunrise today."
        add_entry(entry_text, log_file_path=self.mock_log_file_path)

        mock_file_open.assert_called_once_with(self.mock_log_file_path, 'a', encoding='utf-8')
        expected_content = f"[{FIXED_DATETIME_STR}] {entry_text}\n"
        mock_file_open().write.assert_called_once_with(expected_content)
        self.assertIn(f"Gratitude logged: '{entry_text}'", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('os.path.exists', return_value=False)
    def test_view_entries_no_file(self, mock_exists, mock_file_open):
        view_entries(log_file_path=self.mock_log_file_path)
        mock_file_open.assert_not_called()
        self.assertIn("No gratitude log file found. Start by adding your first entry!", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('os.path.exists', return_value=True)
    def test_view_entries_empty_file(self, mock_exists, mock_file_open):
        view_entries(log_file_path=self.mock_log_file_path)
        mock_file_open.assert_called_once_with(self.mock_log_file_path, 'r', encoding='utf-8')
        self.assertIn("No gratitude entries found yet. Start logging some!", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data=f"[{FIXED_DATETIME_STR}] Entry 1\n[{FIXED_DATETIME_STR}] Entry 2\n")
    @patch('os.path.exists', return_value=True)
    def test_view_entries_with_content(self, mock_exists, mock_file_open):
        view_entries(log_file_path=self.mock_log_file_path)
        mock_file_open.assert_called_once_with(self.mock_log_file_path, 'r', encoding='utf-8')
        output = self.held_stdout.getvalue()
        self.assertIn("--- Your Gratitude Log ---", output)
        self.assertIn(f"[{FIXED_DATETIME_STR}] Entry 1", output)
        self.assertIn(f"[{FIXED_DATETIME_STR}] Entry 2", output)

    @patch('builtins.open', new_callable=mock_open, read_data=f"[{FIXED_DATETIME_STR}] Found a shiny bolt.\n[{FIXED_DATETIME_STR}] Saw a resilient flower.\n")
    @patch('os.path.exists', return_value=True)
    def test_search_entries_found(self, mock_exists, mock_file_open):
        search_entries("flower", log_file_path=self.mock_log_file_path)
        mock_file_open.assert_called_once_with(self.mock_log_file_path, 'r', encoding='utf-8')
        output = self.held_stdout.getvalue()
        self.assertIn("--- Search Results for 'flower' ---", output)
        self.assertIn(f"[{FIXED_DATETIME_STR}] Saw a resilient flower.", output)
        self.assertNotIn("shiny bolt", output)

    @patch('builtins.open', new_callable=mock_open, read_data=f"[{FIXED_DATETIME_STR}] Found a shiny bolt.\n[{FIXED_DATETIME_STR}] Saw a resilient flower.\n")
    @patch('os.path.exists', return_value=True)
    def test_search_entries_not_found(self, mock_exists, mock_file_open):
        search_entries("zombie", log_file_path=self.mock_log_file_path)
        mock_file_open.assert_called_once_with(self.mock_log_file_path, 'r', encoding='utf-8')
        self.assertIn("No entries found containing 'zombie'.", self.held_stdout.getvalue())

    @patch('src.journal.add_entry')
    @patch('sys.argv', ['journal.py', 'add', 'Survived another day.'])
    def test_main_add_command(self, mock_add_entry):
        main()
        mock_add_entry.assert_called_once_with('Survived another day.')
        # The add_entry function itself prints the 'Gratitude logged' message
        # so we check for that in the captured stdout.
        self.assertIn("Gratitude logged: 'Survived another day.'", self.held_stdout.getvalue())

    @patch('src.journal.view_entries')
    @patch('sys.argv', ['journal.py', 'view'])
    def test_main_view_command(self, mock_view_entries):
        main()
        mock_view_entries.assert_called_once_with()

    @patch('src.journal.search_entries')
    @patch('sys.argv', ['journal.py', 'search', 'hope'])
    def test_main_search_command(self, mock_search_entries):
        main()
        mock_search_entries.assert_called_once_with('hope')

    @patch('builtins.print') # Mock print to prevent actual output during help message test
    @patch('sys.argv', ['journal.py'])
    def test_main_no_command(self, mock_print):
        # Mock rationale: argparse exits with SystemExit when no command is provided.
        # We catch this to prevent the test runner from stopping.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for no command
        # We don't assert on print content directly as argparse's help message can vary slightly.
        # Just ensure it tries to print help and exits.

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_add_entry_io_error(self, mock_file_open):
        add_entry("Test entry", log_file_path=self.mock_log_file_path)
        self.assertIn("Error writing to log file: Permission denied", self.held_stdout.getvalue())

    @patch('builtins.open', side_effect=IOError("Disk full"))
    @patch('os.path.exists', return_value=True)
    def test_view_entries_io_error(self, mock_exists, mock_file_open):
        view_entries(log_file_path=self.mock_log_file_path)
        self.assertIn("Error reading log file: Disk full", self.held_stdout.getvalue())

    @patch('builtins.open', side_effect=IOError("Network error"))
    @patch('os.path.exists', return_value=True)
    def test_search_entries_io_error(self, mock_exists, mock_file_open):
        search_entries("test", log_file_path=self.mock_log_file_path)
        self.assertIn("Error reading log file: Network error", self.held_stdout.getvalue())
