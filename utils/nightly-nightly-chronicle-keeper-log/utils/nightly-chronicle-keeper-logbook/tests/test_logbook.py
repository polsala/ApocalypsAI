import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

# Add the src directory to the path to allow importing logbook
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from logbook import ChronicleKeeper, main

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Use a dummy log file name for testing
        self.test_log_file = "test_logbook.txt"
        # Mock os.path.abspath to ensure _get_log_file_path returns a predictable path
        # Mock rationale: Prevents tests from writing to actual files and ensures deterministic path resolution.
        self.mock_abspath = patch('os.path.abspath', return_value='/mock/path/src/logbook.py').start()
        self.mock_dirname = patch('os.path.dirname', return_value='/mock/path/src').start()
        self.keeper = ChronicleKeeper(log_file_path=self.test_log_file)

    def tearDown(self):
        patch.stopall() # Stop all patches started in setUp

    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_add_entry(self, mock_datetime, mock_file):
        # Mock rationale: Prevents actual file I/O and ensures deterministic timestamps.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now().strftime.return_value = "2023-10-27 10:30:00"

        message = "Test entry message."
        self.keeper.add_entry(message)

        mock_file.assert_called_once_with('/mock/path/src/test_logbook.txt', 'a', encoding='utf-8')
        mock_file().write.assert_called_once_with(f"[2023-10-27 10:30:00] {message}\n")

    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:30:00] Entry 1\n[2023-10-27 10:31:00] Entry 2\n")
    @patch('sys.stdout', new_callable=MagicMock)
    def test_list_entries(self, mock_stdout, mock_file):
        # Mock rationale: Provides controlled file content for listing and captures print output.
        self.keeper.list_entries()

        mock_file.assert_called_once_with('/mock/path/src/test_logbook.txt', 'r', encoding='utf-8')
        expected_output = [
            "--- Chronicle Entries ---",
            "Entry 1",
            "Entry 2",
            "-------------------------",
        ]
        # Check if the printed lines contain the expected parts
        actual_output_calls = [call.args[0].strip() for call in mock_stdout.write.call_args_list if call.args[0].strip()]
        for expected_line in expected_output:
            self.assertIn(expected_line, actual_output_calls)


    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:30:00] First entry.\n[2023-10-27 10:31:00] Second entry.\n")
    @patch('sys.stdout', new_callable=MagicMock)
    def test_search_entries_found(self, mock_stdout, mock_file):
        # Mock rationale: Provides controlled file content for searching and captures print output.
        self.keeper.search_entries("first")

        mock_file.assert_called_once_with('/mock/path/src/test_logbook.txt', 'r', encoding='utf-8')
        expected_output = [
            "--- Entries containing 'first' ---",
            "[2023-10-27 10:30:00] First entry.",
            "------------------------------------",
        ]
        actual_output_calls = [call.args[0].strip() for call in mock_stdout.write.call_args_list if call.args[0].strip()]
        for expected_line in expected_output:
            self.assertIn(expected_line, actual_output_calls)

    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:30:00] First entry.\n")
    @patch('sys.stdout', new_callable=MagicMock)
    def test_search_entries_not_found(self, mock_stdout, mock_file):
        # Mock rationale: Provides controlled file content for searching and captures print output.
        self.keeper.search_entries("nonexistent")

        mock_file.assert_called_once_with('/mock/path/src/test_logbook.txt', 'r', encoding='utf-8')
        mock_stdout.write.assert_any_call("No entries found containing 'nonexistent'.\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.input', return_value='yes')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_clear_entries_confirmed(self, mock_stdout, mock_input, mock_file):
        # Mock rationale: Simulates user confirmation and prevents actual file deletion/truncation.
        self.keeper.clear_entries()

        mock_input.assert_called_once()
        mock_file.assert_called_once_with('/mock/path/src/test_logbook.txt', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with("")
        mock_stdout.write.assert_any_call("All chronicle entries have been cleared.\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.input', return_value='no')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_clear_entries_cancelled(self, mock_stdout, mock_input, mock_file):
        # Mock rationale: Simulates user cancellation and ensures no file operation occurs.
        self.keeper.clear_entries()

        mock_input.assert_called_once()
        mock_file.assert_not_called() # Ensure file is not opened for writing
        mock_stdout.write.assert_any_call("Chronicle clearing cancelled.\n")

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_list_entries_file_not_found(self, mock_stdout, mock_open_func):
        # Mock rationale: Simulates the scenario where the log file does not exist.
        self.keeper.list_entries()
        mock_stdout.write.assert_any_call("No chronicle file found. Start by adding an entry!\n")

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_search_entries_file_not_found(self, mock_stdout, mock_open_func):
        # Mock rationale: Simulates the scenario where the log file does not exist.
        self.keeper.search_entries("test")
        mock_stdout.write.assert_any_call("No chronicle file found. Start by adding an entry!\n")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.ChronicleKeeper')
    def test_main_add_command(self, MockChronicleKeeper, mock_parse_args):
        # Mock rationale: Tests the CLI entry point without running actual file operations.
        # Mocks argparse to simulate command line arguments.
        mock_args = MagicMock()
        mock_args.command = "add"
        mock_args.message = "CLI test message"
        mock_args.log_file = "cli_log.txt"
        mock_parse_args.return_value = mock_args

        mock_keeper_instance = MockChronicleKeeper.return_value
        main()

        MockChronicleKeeper.assert_called_once_with(log_file_path="cli_log.txt")
        mock_keeper_instance.add_entry.assert_called_once_with("CLI test message")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.ChronicleKeeper')
    def test_main_list_command(self, MockChronicleKeeper, mock_parse_args):
        # Mock rationale: Tests the CLI entry point without running actual file operations.
        mock_args = MagicMock()
        mock_args.command = "list"
        mock_args.log_file = "cli_log.txt"
        mock_parse_args.return_value = mock_args

        mock_keeper_instance = MockChronicleKeeper.return_value
        main()

        MockChronicleKeeper.assert_called_once_with(log_file_path="cli_log.txt")
        mock_keeper_instance.list_entries.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.ChronicleKeeper')
    def test_main_search_command(self, MockChronicleKeeper, mock_parse_args):
        # Mock rationale: Tests the CLI entry point without running actual file operations.
        mock_args = MagicMock()
        mock_args.command = "search"
        mock_args.keyword = "test"
        mock_args.log_file = "cli_log.txt"
        mock_parse_args.return_value = mock_args

        mock_keeper_instance = MockChronicleKeeper.return_value
        main()

        MockChronicleKeeper.assert_called_once_with(log_file_path="cli_log.txt")
        mock_keeper_instance.search_entries.assert_called_once_with("test")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.ChronicleKeeper')
    def test_main_clear_command(self, MockChronicleKeeper, mock_parse_args):
        # Mock rationale: Tests the CLI entry point without running actual file operations.
        mock_args = MagicMock()
        mock_args.command = "clear"
        mock_args.log_file = "cli_log.txt"
        mock_parse_args.return_value = mock_args

        mock_keeper_instance = MockChronicleKeeper.return_value
        main()

        MockChronicleKeeper.assert_called_once_with(log_file_path="cli_log.txt")
        mock_keeper_instance.clear_entries.assert_called_once()


if __name__ == '__main__':
    unittest.main()
