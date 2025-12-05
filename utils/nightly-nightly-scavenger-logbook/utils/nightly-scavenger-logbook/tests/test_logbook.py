import unittest
import os
import datetime
from unittest.mock import patch, mock_open
from io import StringIO

# Import the functions from the logbook script
# We need to adjust the import path for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import logbook
sys.path.pop(0)


class TestScavengerLogbook(unittest.TestCase):

    def setUp(self):
        # Ensure the log file doesn't exist before each test
        self.test_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src', logbook.LOG_FILE)
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_entry(self, mock_stdout, mock_datetime, mock_open_file, mock_exists):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic timestamps for testing.
        # - builtins.open: To prevent actual file system writes and read from a mock file.
        # - sys.stdout: To capture print output for assertion.
        # - os.path.exists: To control file existence checks.

        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 15, 0, 0)
        mock_exists.return_value = False # Assume log file doesn't exist initially

        location = "Abandoned Gas Station"
        note = "Found a rusty wrench and a half-eaten bag of chips."
        expected_entry = "[2023-10-27 15:00:00] Location: Abandoned Gas Station | Note: Found a rusty wrench and a half-eaten bag of chips.\n"
        expected_print_output = f"Log entry added: {expected_entry.strip()}\n"

        logbook.add_entry(location, note)

        mock_open_file.assert_called_once_with(self.test_log_path, "a")
        mock_open_file().write.assert_called_once_with(expected_entry)
        self.assertEqual(mock_stdout.getvalue(), expected_print_output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_no_file(self, mock_stdout, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file not existing.
        # - builtins.open: To ensure it's not called if file doesn't exist.
        # - sys.stdout: To capture print output.

        mock_exists.return_value = False
        expected_output = "No log entries found yet.\n"

        logbook.view_entries()

        mock_exists.assert_called_once_with(self.test_log_path)
        mock_open_file.assert_not_called()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_with_content(self, mock_stdout, mock_open_file, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the log file existing.
        # - builtins.open: To provide mock content for the log file.
        # - sys.stdout: To capture print output.

        mock_exists.return_value = True
        mock_file_content = (
            "[2023-10-27 15:00:00] Location: A | Note: N1\n"
            "[2023-10-27 15:01:00] Location: B | Note: N2\n"
        )
        mock_open_file.return_value.__enter__.return_value.readlines.return_value = mock_file_content.splitlines(keepends=True)
        mock_open_file.return_value.__enter__.return_value.__iter__.return_value = iter(mock_file_content.splitlines(keepends=True))


        expected_output = (
            "--- Scavenger Log ---\n"
            "[2023-10-27 15:00:00] Location: A | Note: N1\n"
            "[2023-10-27 15:01:00] Location: B | Note: N2\n"
            "---------------------\n"
        )

        logbook.view_entries()

        mock_exists.assert_called_once_with(self.test_log_path)
        mock_open_file.assert_called_once_with(self.test_log_path, "r")
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.argv', ['logbook.py', 'add', '--location', 'TestLoc', '--note', 'TestNote'])
    @patch('logbook.add_entry')
    def test_main_add_command(self, mock_add_entry):
        # Mock rationale:
        # - sys.argv: To simulate command-line arguments for the main function.
        # - logbook.add_entry: To check if the correct function is called with correct arguments.

        logbook.main()
        mock_add_entry.assert_called_once_with(location='TestLoc', note='TestNote')

    @patch('sys.argv', ['logbook.py', 'view'])
    @patch('logbook.view_entries')
    def test_main_view_command(self, mock_view_entries):
        # Mock rationale:
        # - sys.argv: To simulate command-line arguments for the main function.
        # - logbook.view_entries: To check if the correct function is called.

        logbook.main()
        mock_view_entries.assert_called_once()

    @patch('sys.argv', ['logbook.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        # Mock rationale:
        # - sys.argv: To simulate no command-line arguments.
        # - argparse.ArgumentParser.print_help: To check if help is printed.

        logbook.main()
        mock_print_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
