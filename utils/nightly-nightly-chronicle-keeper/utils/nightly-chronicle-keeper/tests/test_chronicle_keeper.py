import unittest
from unittest.mock import patch, mock_open, call
import os
import sys
from io import StringIO
from datetime import datetime

# Import the functions to be tested
# Assuming chronicle_keeper.py is in src/ and tests are run from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from chronicle_keeper import append_entry, view_entries, get_timestamp, DEFAULT_CHRONICLE_FILE, main
sys.path.pop(0)

class TestChronicleKeeper(unittest.TestCase):

    @patch('chronicle_keeper.datetime')
    def test_get_timestamp(self, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_datetime.datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        self.assertEqual(get_timestamp(), "2023-10-27 10:30:00")

    @patch('chronicle_keeper.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle_keeper.get_timestamp', return_value="2023-10-27 10:30:00")
    @patch('sys.stdout', new_callable=StringIO)
    def test_append_entry_new_file(self, mock_stdout, mock_get_timestamp, mock_file_open, mock_makedirs):
        # Mock rationale: Simulate file system operations without actual disk I/O.
        # mock_open: Controls what happens when `open()` is called.
        # mock_get_timestamp: Ensures a consistent timestamp for the test.
        # mock_makedirs: Prevents actual directory creation.
        # mock_stdout: Captures print statements for verification.

        test_message = "First entry."
        test_file = "test_chronicle.log"

        append_entry(test_message, test_file)

        mock_makedirs.assert_not_called() # No directory specified, so makedirs not called for '.'
        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("[2023-10-27 10:30:00] First entry.\n")
        self.assertIn(f"Entry added to {test_file}", mock_stdout.getvalue())

    @patch('chronicle_keeper.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle_keeper.get_timestamp', return_value="2023-10-27 10:30:00")
    @patch('sys.stdout', new_callable=StringIO)
    def test_append_entry_with_path_new_dir(self, mock_stdout, mock_get_timestamp, mock_file_open, mock_makedirs):
        # Mock rationale: Simulate appending to a file in a new directory.
        test_message = "Entry in new path."
        test_file = "new_dir/test_chronicle.log"

        append_entry(test_message, test_file)

        mock_makedirs.assert_called_once_with('new_dir', exist_ok=True)
        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("[2023-10-27 10:30:00] Entry in new path.\n")
        self.assertIn(f"Entry added to {test_file}", mock_stdout.getvalue())

    @patch('chronicle_keeper.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle_keeper.get_timestamp', return_value="2023-10-27 10:30:00")
    @patch('sys.stdout', new_callable=StringIO)
    def test_append_entry_existing_file(self, mock_stdout, mock_get_timestamp, mock_file_open, mock_makedirs):
        # Mock rationale: Simulate appending to an existing file.
        test_message = "Another entry."
        test_file = "existing_chronicle.log"

        append_entry(test_message, test_file)

        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("[2023-10-27 10:30:00] Another entry.\n")
        self.assertIn(f"Entry added to {test_file}", mock_stdout.getvalue())

    @patch('chronicle_keeper.os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_file_not_exists(self, mock_stdout, mock_exists):
        # Mock rationale: Simulate the scenario where the chronicle file doesn't exist.
        view_entries(5, "non_existent.log")
        mock_exists.assert_called_once_with("non_existent.log")
        self.assertIn("Chronicle file 'non_existent.log' does not exist yet.", mock_stdout.getvalue())

    @patch('chronicle_keeper.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_empty_file(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate viewing an empty chronicle file.
        view_entries(5, "empty.log")
        mock_exists.assert_called_once_with("empty.log")
        mock_file_open.assert_called_once_with("empty.log", 'r', encoding='utf-8')
        self.assertIn("Chronicle file 'empty.log' is empty.", mock_stdout.getvalue())

    @patch('chronicle_keeper.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] Entry 1\n[2023-10-27 10:01:00] Entry 2\n[2023-10-27 10:02:00] Entry 3\n")
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_less_than_num(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate viewing a file with fewer entries than requested.
        view_entries(5, "chronicle.log")
        expected_output = "[2023-10-27 10:00:00] Entry 1\n[2023-10-27 10:01:00] Entry 2\n[2023-10-27 10:02:00] Entry 3\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('chronicle_keeper.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] Entry 1\n[2023-10-27 10:01:00] Entry 2\n[2023-10-27 10:02:00] Entry 3\n[2023-10-27 10:03:00] Entry 4\n[2023-10-27 10:04:00] Entry 5\n[2023-10-27 10:05:00] Entry 6\n")
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_more_than_num(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate viewing a file with more entries than requested, ensuring only the last N are shown.
        view_entries(3, "chronicle.log")
        expected_output = "[2023-10-27 10:03:00] Entry 4\n[2023-10-27 10:04:00] Entry 5\n[2023-10-27 10:05:00] Entry 6\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('chronicle_keeper.append_entry')
    @patch('chronicle_keeper.view_entries')
    @patch('sys.argv', ['chronicle_keeper.py', 'append', 'Test message'])
    def test_main_append_command(self, mock_view, mock_append):
        # Mock rationale: Test the main function's argument parsing and command dispatch.
        # sys.argv: Simulates command-line arguments.
        # mock_append/view: Prevents actual function calls, verifies they were called correctly.
        main()
        mock_append.assert_called_once_with('Test message', DEFAULT_CHRONICLE_FILE)
        mock_view.assert_not_called()

    @patch('chronicle_keeper.append_entry')
    @patch('chronicle_keeper.view_entries')
    @patch('sys.argv', ['chronicle_keeper.py', 'view', '-n', '5', '-f', 'custom.log'])
    def test_main_view_command_with_args(self, mock_view, mock_append):
        # Mock rationale: Test the main function's argument parsing and command dispatch with custom args.
        main()
        mock_view.assert_called_once_with(5, 'custom.log')
        mock_append.assert_not_called()

    @patch('chronicle_keeper.append_entry')
    @patch('chronicle_keeper.view_entries')
    @patch('sys.argv', ['chronicle_keeper.py', 'view'])
    def test_main_view_command_default_args(self, mock_view, mock_append):
        # Mock rationale: Test the main function's argument parsing and command dispatch with default args.
        main()
        mock_view.assert_called_once_with(10, DEFAULT_CHRONICLE_FILE)
        mock_append.assert_not_called()

    @patch('chronicle_keeper.os.makedirs', side_effect=IOError("Permission denied"))
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO) # Capture stdout as well to ensure no unexpected prints
    @patch('sys.exit')
    def test_append_entry_io_error(self, mock_exit, mock_stdout, mock_stderr, mock_file_open, mock_makedirs):
        # Mock rationale: Simulate an IOError during file writing to ensure error handling.
        append_entry("Error test", "bad_path/chronicle.log")
        self.assertIn("Error writing to chronicle file: Permission denied", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('chronicle_keeper.os.path.exists', return_value=True)
    @patch('builtins.open', side_effect=IOError("File locked"))
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_view_entries_io_error(self, mock_exit, mock_stdout, mock_stderr, mock_file_open, mock_exists):
        # Mock rationale: Simulate an IOError during file reading to ensure error handling.
        view_entries(5, "locked.log")
        self.assertIn("Error reading chronicle file: File locked", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
