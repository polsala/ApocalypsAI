import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime

# Import the functions from the logbook script
# Assuming the test file is in 'tests/' and the script is in 'src/'
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from logbook import add_entry, view_entries, _get_log_file_path, LOG_FILE_NAME

class TestLogbook(unittest.TestCase):

    def setUp(self):
        # Ensure the log file path is consistent for testing
        self.test_log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src', LOG_FILE_NAME)

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.load')
    @patch('logbook.json.dump')
    @patch('logbook.datetime')
    @patch('builtins.print') # Mock print to capture output
    def test_add_entry_new_file(self, mock_print, mock_datetime, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file not existing initially.
        # - builtins.open: To control file I/O without touching the actual filesystem.
        # - json.load: To simulate loading an empty list when the file doesn't exist.
        # - json.dump: To capture the data that would be written to the file.
        # - datetime: To ensure a deterministic date for the log entry.
        # - builtins.print: To prevent actual printing during tests and allow checking output.

        mock_exists.return_value = False # File does not exist
        mock_json_load.return_value = [] # No existing entries
        mock_datetime.now.return_value = datetime(2024, 7, 20)
        mock_datetime.now().strftime.return_value = "2024-07-20"

        add_entry("Found some rusty tools.", "Managed to fix the loose hinge.")

        expected_log_entry = {
            "date": "2024-07-20",
            "gloom": "Found some rusty tools.",
            "glimmer": "Managed to fix the loose hinge."
        }

        mock_exists.assert_called_once_with(self.test_log_file_path)
        mock_open_file.assert_called_once_with(self.test_log_file_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with([expected_log_entry], mock_open_file(), indent=4, ensure_ascii=False)
        mock_print.assert_called_once_with("Log entry added for 2024-07-20.")

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.load')
    @patch('logbook.json.dump')
    @patch('logbook.datetime')
    @patch('builtins.print')
    def test_add_entry_existing_file(self, mock_print, mock_datetime, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Same as above, but simulating an existing file with content.

        mock_exists.return_value = True # File exists
        existing_entries = [
            {"date": "2024-07-19", "gloom": "Rain all day.", "glimmer": "Found dry shelter."}
        ]
        mock_json_load.return_value = existing_entries
        mock_datetime.now.return_value = datetime(2024, 7, 20)
        mock_datetime.now().strftime.return_value = "2024-07-20"

        add_entry("Today I found a working flashlight.", "The flashlight has new batteries!")

        expected_new_entry = {
            "date": "2024-07-20",
            "gloom": "Today I found a working flashlight.",
            "glimmer": "The flashlight has new batteries!"
        }
        expected_final_entries = existing_entries + [expected_new_entry]

        mock_exists.assert_called_once_with(self.test_log_file_path)
        mock_open_file.assert_any_call(self.test_log_file_path, 'r', encoding='utf-8') # For loading
        mock_open_file.assert_any_call(self.test_log_file_path, 'w', encoding='utf-8') # For saving
        mock_json_dump.assert_called_once_with(expected_final_entries, mock_open_file(), indent=4, ensure_ascii=False)
        mock_print.assert_called_once_with("Log entry added for 2024-07-20.")

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.load')
    @patch('builtins.print')
    def test_view_entries_empty(self, mock_print, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file existing or not.
        # - builtins.open: To control file I/O.
        # - json.load: To simulate loading an empty list.
        # - builtins.print: To capture output.

        mock_exists.return_value = False # File does not exist, or is empty
        mock_json_load.return_value = []

        view_entries()

        mock_exists.assert_called_once_with(self.test_log_file_path)
        mock_print.assert_called_once_with("No entries in the logbook yet.")

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.load')
    @patch('builtins.print')
    def test_view_entries_with_content(self, mock_print, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Same as above, but simulating a file with content.

        mock_exists.return_value = True
        mock_json_load.return_value = [
            {"date": "2024-07-19", "gloom": "Rain all day.", "glimmer": "Found dry shelter."},
            {"date": "2024-07-20", "gloom": "Found a working flashlight.", "glimmer": "New batteries!"}
        ]

        view_entries()

        mock_exists.assert_called_once_with(self.test_log_file_path)
        mock_open_file.assert_called_once_with(self.test_log_file_path, 'r', encoding='utf-8')
        
        # Check that print was called with the expected output
        mock_print.assert_any_call("--- Log Entry: 2024-07-19 ---")
        mock_print.assert_any_call("Gloom: Rain all day.")
        mock_print.assert_any_call("Glimmer: Found dry shelter.")
        mock_print.assert_any_call("-----------------------------")
        mock_print.assert_any_call("--- Log Entry: 2024-07-20 ---")
        mock_print.assert_any_call("Gloom: Found a working flashlight.")
        mock_print.assert_any_call("Glimmer: New batteries!")
        mock_print.assert_any_call("-----------------------------")
        self.assertEqual(mock_print.call_count, 6) # 3 lines per entry * 2 entries

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.load')
    @patch('builtins.print')
    def test_load_log_corrupted_json(self, mock_print, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file existing.
        # - builtins.open: To control file I/O.
        # - json.load: To simulate a JSONDecodeError.
        # - builtins.print: To capture warning messages.

        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        # Call the internal function directly to test error handling
        log_entries = logbook._load_log(self.test_log_file_path)

        self.assertEqual(log_entries, [])
        mock_print.assert_called_once_with(f"Warning: {LOG_FILE_NAME} is corrupted or empty. Starting a new log.")

    @patch('logbook.os.path.exists')
    @patch('logbook.open', new_callable=mock_open)
    @patch('logbook.json.dump')
    @patch('builtins.print')
    def test_save_log_error(self, mock_print, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file existing.
        # - builtins.open: To control file I/O.
        # - json.dump: To simulate an error during saving.
        # - builtins.print: To capture error messages.

        mock_exists.return_value = True
        mock_json_dump.side_effect = IOError("Disk full")

        # Call the internal function directly to test error handling
        logbook._save_log(self.test_log_file_path, [{"date": "2024-07-20", "gloom": "test", "glimmer": "test"}])

        mock_print.assert_called_once_with("Error saving log file: Disk full")


if __name__ == '__main__':
    unittest.main()
