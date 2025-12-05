import unittest
import os
import datetime
from unittest.mock import patch, mock_open
from src.logbook import add_log_entry, main

class TestLogbook(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('datetime.datetime')
    def test_add_log_entry_new_file(self, mock_datetime, mock_exists, mock_file_open):
        # Mock rationale: Simulate a non-existent file to test creation and writing.
        mock_exists.return_value = False
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 8, 30, 15)

        message = "First entry."
        log_file = "test_chronicle.md"
        
        exit_code = add_log_entry(message, log_file)

        self.assertEqual(exit_code, 0)
        mock_file_open.assert_called_once_with(log_file, 'a')
        mock_file_open().write.assert_called_once_with("### 2023-10-27 08:30:15\nFirst entry.\n\n")
        mock_exists.assert_called_once_with(log_file) # Check if exists was called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('datetime.datetime')
    def test_add_log_entry_existing_file(self, mock_datetime, mock_exists, mock_file_open):
        # Mock rationale: Simulate an existing file to test appending.
        mock_exists.return_value = True
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 45, 0)

        message = "Second entry."
        log_file = "test_chronicle.md"
        
        exit_code = add_log_entry(message, log_file)

        self.assertEqual(exit_code, 0)
        mock_file_open.assert_called_once_with(log_file, 'a')
        mock_file_open().write.assert_called_once_with("### 2023-10-27 10:45:00\nSecond entry.\n\n")
        mock_exists.assert_called_once_with(log_file) # Check if exists was called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('datetime.datetime')
    def test_add_log_entry_io_error(self, mock_datetime, mock_exists, mock_file_open):
        # Mock rationale: Simulate an IOError during file writing to test error handling.
        mock_file_open.side_effect = IOError("Permission denied")
        mock_exists.return_value = False # Doesn't matter much for this test, but good practice
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 11, 0, 0)

        message = "Error entry."
        log_file = "test_chronicle.md"

        with patch('builtins.print') as mock_print: # Mock rationale: Capture print output for assertion.
            exit_code = add_log_entry(message, log_file)
            self.assertEqual(exit_code, 1)
            mock_print.assert_called_once_with(f"Error writing to log file {log_file}: Permission denied")

    @patch('src.logbook.add_log_entry')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent actual sys.exit during test.
    def test_main_function(self, mock_sys_exit, mock_parse_args, mock_add_log_entry):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value.message = "Test message from main."
        mock_parse_args.return_value.file = "custom_chronicle.md"
        # Mock rationale: Control the return value of the core logic.
        mock_add_log_entry.return_value = 0

        main()

        mock_add_log_entry.assert_called_once_with("Test message from main.", "custom_chronicle.md")
        mock_sys_exit.assert_called_once_with(0)

    @patch('src.logbook.add_log_entry')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent actual sys.exit during test.
    def test_main_function_error_exit(self, mock_sys_exit, mock_parse_args, mock_add_log_entry):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value.message = "Error message from main."
        mock_parse_args.return_value.file = "error_chronicle.md"
        # Mock rationale: Simulate an error return from the core logic.
        mock_add_log_entry.return_value = 1

        main()

        mock_add_log_entry.assert_called_once_with("Error message from main.", "error_chronicle.md")
        mock_sys_exit.assert_called_once_with(1)
