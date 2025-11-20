import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import datetime
import io
import sys

# Import the functions directly for testing
# Assuming the test is run from the utils/nightly-chronicle-keeper-logbook/tests directory
# and src/logbook.py is one level up.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from logbook import add_entry, view_entries, DEFAULT_LOG_FILE

class TestLogbook(unittest.TestCase):

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_add_entry(self, mock_print, mock_file_open, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0)
        
        test_message = "Test entry message."
        expected_log_content = "[2023-10-27 10:30:00] Test entry message.\n"

        add_entry(test_message, "test_log.log")

        # Mock rationale: Verify file operations without actually touching the filesystem.
        mock_file_open.assert_called_once_with("test_log.log", "a", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(expected_log_content)
        mock_print.assert_called_once_with("Entry added to test_log.log")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_view_entries_all(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: Simulate the existence of a log file.
        mock_exists.return_value = True
        
        # Mock rationale: Provide specific content for the log file.
        mock_file_open.return_value.readlines.return_value = [
            "[2023-10-27 10:00:00] First entry.\n",
            "[2023-10-27 10:05:00] Second entry.\n",
            "[2023-10-27 10:10:00] Third entry.\n",
        ]

        view_entries(None, "test_log.log")

        mock_exists.assert_called_once_with("test_log.log")
        mock_file_open.assert_called_once_with("test_log.log", "r", encoding="utf-8")
        mock_print.assert_any_call("First entry.")
        mock_print.assert_any_call("Second entry.")
        mock_print.assert_any_call("Third entry.")
        self.assertEqual(mock_print.call_count, 3)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_view_entries_last_n(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: Simulate the existence of a log file.
        mock_exists.return_value = True
        
        # Mock rationale: Provide specific content for the log file.
        mock_file_open.return_value.readlines.return_value = [
            "[2023-10-27 10:00:00] First entry.\n",
            "[2023-10-27 10:05:00] Second entry.\n",
            "[2023-10-27 10:10:00] Third entry.\n",
            "[2023-10-27 10:15:00] Fourth entry.\n",
            "[2023-10-27 10:20:00] Fifth entry.\n",
        ]

        view_entries(2, "test_log.log")

        mock_exists.assert_called_once_with("test_log.log")
        mock_file_open.assert_called_once_with("test_log.log", "r", encoding="utf-8")
        mock_print.assert_any_call("Fourth entry.")
        mock_print.assert_any_call("Fifth entry.")
        self.assertEqual(mock_print.call_count, 2)

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_view_entries_file_not_found(self, mock_print, mock_exists):
        # Mock rationale: Simulate a non-existent log file.
        mock_exists.return_value = False

        view_entries(None, "non_existent.log")

        mock_exists.assert_called_once_with("non_existent.log")
        mock_print.assert_called_once_with("Log file 'non_existent.log' not found. No entries to display.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_view_entries_empty_file(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing but empty log file.
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = []

        view_entries(None, "empty.log")

        mock_exists.assert_called_once_with("empty.log")
        mock_file_open.assert_called_once_with("empty.log", "r", encoding="utf-8")
        mock_print.assert_called_once_with("Log file 'empty.log' is empty.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_add_entry_io_error(self, mock_print, mock_file_open):
        # Mock rationale: Simulate an IOError during file writing.
        mock_file_open.side_effect = IOError("Permission denied")

        add_entry("Error test", "protected.log")

        mock_print.assert_called_once_with("Error writing to log file protected.log: Permission denied")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_view_entries_io_error(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: Simulate an IOError during file reading.
        mock_exists.return_value = True
        mock_file_open.side_effect = IOError("Disk full")

        view_entries(None, "corrupt.log")

        mock_print.assert_called_once_with("Error reading log file corrupt.log: Disk full")

if __name__ == '__main__':
    unittest.main()
