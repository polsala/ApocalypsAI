import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os
import io

# Import the functions to be tested
from src.chronicle_log import add_entry, view_entries, LOG_FILE_NAME, main

class TestChronicleLog(unittest.TestCase):

    FIXED_TIMESTAMP_STR = "2077-10-23 13:37:00"
    FIXED_TIMESTAMP_DT = datetime.datetime(2077, 10, 23, 13, 37, 0)

    @patch('src.chronicle_log.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock file existence for add_entry
    def test_add_entry(self, mock_exists, mock_file_open, mock_datetime):
        # Mock rationale:
        # 1. `src.chronicle_log.datetime`: To ensure `_get_timestamp` returns a consistent value for deterministic tests.
        # 2. `builtins.open`: To prevent actual file I/O and simulate file writing in memory.
        # 3. `os.path.exists`: To simulate the log file existing when `add_entry` is called, preventing unnecessary file creation checks in the mock.

        mock_datetime.datetime.now.return_value = self.FIXED_TIMESTAMP_DT
        test_message = "Found a can of irradiated beans."
        expected_entry = f"[{self.FIXED_TIMESTAMP_STR}] - {test_message}\n"

        add_entry(test_message, "test_log.log")

        mock_file_open.assert_called_once_with("test_log.log", 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_entry)

    @patch('src.chronicle_log.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock file existence for view_entries
    def test_view_entries(self, mock_exists, mock_file_open, mock_datetime):
        # Mock rationale:
        # 1. `src.chronicle_log.datetime`: Not strictly needed for `view_entries` but included for consistency if `_get_timestamp` were ever called.
        # 2. `builtins.open`: To prevent actual file I/O and simulate file reading from a predefined string.
        # 3. `os.path.exists`: To simulate the log file existing when `view_entries` is called.

        log_content = (
            "[2077-10-22 08:00:00] - Day 1: The sky turned green.\n"
            "[2077-10-22 12:00:00] - Day 1: Scavenged some water.\n"
            "[2077-10-23 09:00:00] - Day 2: Heard strange noises.\n"
            "[2077-10-23 13:37:00] - Day 2: Found a can of irradiated beans.\n"
            "[2077-10-24 07:00:00] - Day 3: The dust storms are relentless.\n"
        )
        mock_file_open.return_value.readlines.return_value = log_content.splitlines(keepends=True)

        # Test viewing last 3 entries
        entries = view_entries(3, "test_log.log")
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0], "[2077-10-23 13:37:00] - Day 2: Found a can of irradiated beans.")
        self.assertEqual(entries[2], "[2077-10-24 07:00:00] - Day 3: The dust storms are relentless.")

        mock_file_open.assert_called_once_with("test_log.log", 'r', encoding='utf-8')
        mock_file_open.reset_mock() # Reset for next assertion

        # Test viewing all entries if num_entries is greater than total
        entries = view_entries(10, "test_log.log")
        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0], "[2077-10-22 08:00:00] - Day 1: The sky turned green.")

    @patch('os.path.exists', return_value=False)
    def test_view_entries_no_file(self, mock_exists):
        # Mock rationale:
        # 1. `os.path.exists`: To simulate the log file not existing, ensuring `view_entries` handles this gracefully.
        entries = view_entries(5, "non_existent_log.log")
        self.assertEqual(entries, [])
        mock_exists.assert_called_once_with("non_existent_log.log")

    @patch('src.chronicle_log.add_entry')
    @patch('src.chronicle_log.view_entries')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_add_entry(self, mock_parse_args, mock_stderr, mock_stdout, mock_view_entries, mock_add_entry):
        # Mock rationale:
        # 1. `argparse.ArgumentParser.parse_args`: To control the command-line arguments passed to `main` without actually running from CLI.
        # 2. `sys.stdout`, `sys.stderr`: To capture print output for verification.
        # 3. `src.chronicle_log.add_entry`, `src.chronicle_log.view_entries`: To isolate the `main` function's logic and ensure it calls the correct underlying functions with the right arguments.

        mock_args = MagicMock()
        mock_args.add = "A new day, a new struggle."
        mock_args.view = 0
        mock_args.log_file = "custom_chronicle.log"
        mock_parse_args.return_value = mock_args

        main()

        mock_add_entry.assert_called_once_with("A new day, a new struggle.", "custom_chronicle.log")
        mock_view_entries.assert_not_called()
        self.assertIn("Chronicle updated: 'A new day, a new struggle.'", mock_stdout.getvalue())


    @patch('src.chronicle_log.add_entry')
    @patch('src.chronicle_log.view_entries', return_value=[
        "[2077-10-23 13:37:00] - Entry 1",
        "[2077-10-24 07:00:00] - Entry 2"
    ])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_view_entries(self, mock_parse_args, mock_stderr, mock_stdout, mock_view_entries, mock_add_entry):
        # Mock rationale:
        # 1. `argparse.ArgumentParser.parse_args`: To control the command-line arguments passed to `main`.
        # 2. `sys.stdout`, `sys.stderr`: To capture print output for verification.
        # 3. `src.chronicle_log.add_entry`, `src.chronicle_log.view_entries`: To isolate the `main` function's logic and ensure it calls the correct underlying functions with the right arguments and handles their return values.

        mock_args = MagicMock()
        mock_args.add = None
        mock_args.view = 2
        mock_args.log_file = "custom_chronicle.log"
        mock_parse_args.return_value = mock_args

        main()

        mock_view_entries.assert_called_once_with(2, "custom_chronicle.log")
        mock_add_entry.assert_not_called()
        output = mock_stdout.getvalue()
        self.assertIn("--- Chronicle Log (Last 2 Entries) ---", output)
        self.assertIn("[2077-10-23 13:37:00] - Entry 1", output)
        self.assertIn("[2077-10-24 07:00:00] - Entry 2", output)

    @patch('src.chronicle_log.add_entry')
    @patch('src.chronicle_log.view_entries', return_value=[])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_view_no_entries(self, mock_parse_args, mock_stderr, mock_stdout, mock_view_entries, mock_add_entry):
        # Mock rationale:
        # 1. `argparse.ArgumentParser.parse_args`: To control the command-line arguments passed to `main`.
        # 2. `sys.stdout`, `sys.stderr`: To capture print output for verification.
        # 3. `src.chronicle_log.add_entry`, `src.chronicle_log.view_entries`: To isolate the `main` function's logic and ensure it calls the correct underlying functions and handles an empty return.

        mock_args = MagicMock()
        mock_args.add = None
        mock_args.view = 5
        mock_args.log_file = "empty_chronicle.log"
        mock_parse_args.return_value = mock_args

        main()

        mock_view_entries.assert_called_once_with(5, "empty_chronicle.log")
        mock_add_entry.assert_not_called()
        self.assertIn("No entries found in 'empty_chronicle.log'.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_args(self, mock_print_help, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale:
        # 1. `argparse.ArgumentParser.parse_args`: To control the command-line arguments passed to `main`.
        # 2. `sys.stdout`, `sys.stderr`: To capture print output for verification.
        # 3. `argparse.ArgumentParser.print_help`: To verify that the help message is printed when no valid arguments are provided.

        mock_args = MagicMock()
        mock_args.add = None
        mock_args.view = 0 # Default value when --view is not present or just --view
        mock_args.log_file = LOG_FILE_NAME
        mock_parse_args.return_value = mock_args

        main()

        mock_print_help.assert_called_once()
        self.assertEqual(mock_stdout.getvalue(), "") # print_help goes to stderr by default, but we mocked stdout for general capture.
