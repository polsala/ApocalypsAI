import unittest
from unittest.mock import patch, mock_open, call
import datetime
import os
import sys
from io import StringIO

# Import the functions to be tested
# Assuming chronicle.py is in the same directory or importable
from src import chronicle

class TestChronicleKeeper(unittest.TestCase):

    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_file_open, mock_makedirs, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic timestamps for testing.
        # - os.makedirs: To prevent actual directory creation during tests.
        # - builtins.open: To prevent actual file writes and capture file content.

        # Set a fixed datetime for testing
        fixed_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        test_message = "Scavenged 3 cans of irradiated beans."
        expected_log_content = "[14:30:00] Scavenged 3 cans of irradiated beans.\n"
        expected_filepath = os.path.join("logs", "2023-10-27.log")

        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.add_entry(test_message)

        sys.stdout = sys.__stdout__ # Restore stdout

        # Assertions
        mock_makedirs.assert_called_once_with(chronicle.LOG_DIR, exist_ok=True)
        mock_file_open.assert_called_once_with(expected_filepath, "a", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(expected_log_content)
        self.assertIn(f"Entry added to {expected_filepath}", captured_output.getvalue())

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_today(self, mock_file_open, mock_path_exists, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic dates for log file path.
        # - os.path.exists: To simulate the presence or absence of a log file.
        # - builtins.open: To simulate reading from a log file without actual file I/O.

        fixed_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        mock_path_exists.return_value = True # Simulate file exists
        mock_file_open.return_value.readlines.return_value = [
            "[10:00:00] Found a rusty wrench.\n",
            "[12:15:30] Repaired the water purifier.\n"
        ]

        expected_output = (
            "--- Log for 2023-10-27 ---\n"
            "[10:00:00] Found a rusty wrench.\n"
            "[12:15:30] Repaired the water purifier.\n"
            "-----------------------------------\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.view_entries()

        sys.stdout = sys.__stdout__

        expected_filepath = os.path.join("logs", "2023-10-27.log")
        mock_path_exists.assert_called_once_with(expected_filepath)
        mock_file_open.assert_called_once_with(expected_filepath, "r", encoding="utf-8")
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_specific_date(self, mock_file_open, mock_path_exists, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic dates for log file path.
        # - os.path.exists: To simulate the presence or absence of a log file.
        # - builtins.open: To simulate reading from a log file without actual file I/O.

        # Mock datetime.datetime.now() to ensure it doesn't interfere with date parsing
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 28, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        mock_path_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = [
            "[08:00:00] Explored sector Gamma-7.\n"
        ]

        expected_output = (
            "--- Log for 2023-10-26 ---\n"
            "[08:00:00] Explored sector Gamma-7.\n"
            "-----------------------------------\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.view_entries(date_str="2023-10-26")

        sys.stdout = sys.__stdout__

        expected_filepath = os.path.join("logs", "2023-10-26.log")
        mock_path_exists.assert_called_once_with(expected_filepath)
        mock_file_open.assert_called_once_with(expected_filepath, "r", encoding="utf-8")
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_last_n(self, mock_file_open, mock_path_exists, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic dates for log file path.
        # - os.path.exists: To simulate the presence or absence of a log file.
        # - builtins.open: To simulate reading from a log file without actual file I/O.

        fixed_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        mock_path_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = [
            "[08:00:00] Entry 1.\n",
            "[09:00:00] Entry 2.\n",
            "[10:00:00] Entry 3.\n",
            "[11:00:00] Entry 4.\n"
        ]

        expected_output = (
            "--- Log for 2023-10-27 ---\n"
            "[10:00:00] Entry 3.\n"
            "[11:00:00] Entry 4.\n"
            "-----------------------------------\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.view_entries(last_n=2)

        sys.stdout = sys.__stdout__

        expected_filepath = os.path.join("logs", "2023-10-27.log")
        mock_path_exists.assert_called_once_with(expected_filepath)
        mock_file_open.assert_called_once_with(expected_filepath, "r", encoding="utf-8")
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('datetime.datetime')
    @patch('os.path.exists')
    def test_view_entries_no_file(self, mock_path_exists, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic dates for log file path.
        # - os.path.exists: To simulate the absence of a log file.

        fixed_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        mock_path_exists.return_value = False # Simulate file does not exist

        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.view_entries()

        sys.stdout = sys.__stdout__

        expected_filepath = os.path.join("logs", "2023-10-27.log")
        mock_path_exists.assert_called_once_with(expected_filepath)
        self.assertIn("No log entries found for 2023-10-27.", captured_output.getvalue())

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_empty_file(self, mock_file_open, mock_path_exists, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: To ensure deterministic dates for log file path.
        # - os.path.exists: To simulate the presence of a log file.
        # - builtins.open: To simulate reading from an empty log file.

        fixed_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls

        mock_path_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = [] # Simulate empty file

        captured_output = StringIO()
        sys.stdout = captured_output

        chronicle.view_entries()

        sys.stdout = sys.__stdout__

        expected_filepath = os.path.join("logs", "2023-10-27.log")
        mock_path_exists.assert_called_once_with(expected_filepath)
        mock_file_open.assert_called_once_with(expected_filepath, "r", encoding="utf-8")
        self.assertIn("No log entries found for 2023-10-27.", captured_output.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_invalid_date_format(self, mock_stdout):
        # Mock rationale:
        # - sys.stdout: To capture the error message printed to stdout.

        chronicle.view_entries(date_str="2023/10/27")
        self.assertIn("Error: Invalid date format. Use YYYY-MM-DD.", mock_stdout.getvalue())


    @patch('sys.argv', ['chronicle.py', 'add', 'Test message.'])
    @patch('src.chronicle.add_entry')
    def test_main_add_command(self, mock_add_entry):
        # Mock rationale:
        # - sys.argv: To simulate command-line arguments passed to the script.
        # - src.chronicle.add_entry: To check if the main function correctly dispatches to add_entry.

        chronicle.main()
        mock_add_entry.assert_called_once_with('Test message.')

    @patch('sys.argv', ['chronicle.py', 'view', '--date', '2023-01-01', '--last', '5'])
    @patch('src.chronicle.view_entries')
    def test_main_view_command(self, mock_view_entries):
        # Mock rationale:
        # - sys.argv: To simulate command-line arguments passed to the script.
        # - src.chronicle.view_entries: To check if the main function correctly dispatches to view_entries.

        chronicle.main()
        mock_view_entries.assert_called_once_with('2023-01-01', 5)

    @patch('sys.argv', ['chronicle.py', 'view'])
    @patch('src.chronicle.view_entries')
    def test_main_view_command_no_args(self, mock_view_entries):
        # Mock rationale:
        # - sys.argv: To simulate command-line arguments passed to the script.
        # - src.chronicle.view_entries: To check if the main function correctly dispatches to view_entries.

        chronicle.main()
        mock_view_entries.assert_called_once_with(None, None)

    @patch('sys.argv', ['chronicle.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        # Mock rationale:
        # - sys.argv: To simulate no command-line arguments.
        # - argparse.ArgumentParser.print_help: To check if help is printed when no command is given.

        chronicle.main()
        mock_print_help.assert_called_once()


if __name__ == '__main__':
    unittest.main()
