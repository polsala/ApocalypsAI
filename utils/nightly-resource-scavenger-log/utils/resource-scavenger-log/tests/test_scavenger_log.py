import unittest
import os
import csv
from unittest.mock import patch, mock_open
from datetime import datetime
import sys

# Mock rationale: We need to simulate file system operations (reading/writing CSV) and
# datetime for deterministic timestamps without actually touching the disk or relying on real time.
# We also mock sys.stdout to capture print output for verification.
# This ensures tests are fast, isolated, and repeatable.

# Import the functions to be tested
from src.scavenger_log import add_entry, list_entries, ensure_log_file_exists, LOG_FILE, HEADERS

class TestScavengerLog(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_log_file_exists_creates_file_if_not_exists(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate the log file not existing initially.
        mock_exists.return_value = False
        ensure_log_file_exists()
        mock_exists.assert_called_with(LOG_FILE)
        mock_file_open.assert_called_with(LOG_FILE, 'w', newline='', encoding='utf-8')
        handle = mock_file_open()
        # csv.writer adds platform-specific newline, but for mock_open, we expect what csv.writer passes.
        # On most systems, with newline='', csv.writer will use \n. For robustness, we check for either.
        # However, for deterministic testing, we assume a standard output from csv.writer.
        # The default for csv.writer with newline='' is \n on Unix, \r\n on Windows.
        # Let's test for the common Unix-like behavior as it's more prevalent in CI/CD.
        # If this fails on Windows CI, it might need adjustment to check for both \n and \r\n.
        handle.write.assert_called_once_with(','.join(HEADERS) + '\n')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_log_file_exists_does_nothing_if_exists(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate the log file already existing.
        mock_exists.return_value = True
        ensure_log_file_exists()
        mock_exists.assert_called_with(LOG_FILE)
        mock_file_open.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger_log.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_add_entry(self, mock_stdout, mock_datetime, mock_file_open, mock_exists):
        mock_exists.return_value = True # Assume file exists for simplicity, ensure_log_file_exists handles creation
        mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
        expected_timestamp = '2024-01-01T10:00:00'

        add_entry('Water Bottle', '2', 'Desert Oasis')

        mock_file_open.assert_called_with(LOG_FILE, 'a', newline='', encoding='utf-8')
        handle = mock_file_open()
        handle.write.assert_called_once_with(f'{expected_timestamp},Water Bottle,2,Desert Oasis\n')
        mock_stdout.write.assert_any_call("Logged: Water Bottle (x2) at Desert Oasis\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_list_entries_no_log_file(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate the log file not existing.
        mock_exists.return_value = False
        list_entries()
        mock_stdout.write.assert_any_call("No scavenger log found. Start logging your finds!\n")
        mock_file_open.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_list_entries_empty_log_file_only_headers(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty log file (only headers).
        mock_exists.return_value = True
        # Simulate file content with only headers
        log_content = ','.join(HEADERS) + '\n'
        mock_file_open.return_value.__enter__.return_value = iter(log_content.splitlines(keepends=True))
        list_entries()
        mock_stdout.write.assert_any_call("Scavenger log is empty. Time to explore!\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_list_entries_with_data(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with data.
        mock_exists.return_value = True
        log_content = (
            ','.join(HEADERS) + '\n' +
            '2024-01-01T10:00:00,Canned Beans,5,Old Supermart\n' +
            '2024-01-02T11:30:00,Scrap Metal,10kg,Collapsed Bridge\n'
        )
        mock_file_open.return_value.__enter__.return_value = iter(log_content.splitlines(keepends=True))

        list_entries()

        expected_output_lines = [
            'Timestamp           | Item         | Quantity | Location         \n',
            '--------------------|--------------|----------|------------------\n',
            '2024-01-01T10:00:00 | Canned Beans | 5        | Old Supermart    \n',
            '2024-01-02T11:30:00 | Scrap Metal  | 10kg     | Collapsed Bridge \n'
        ]
        actual_output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        for line in expected_output_lines:
            self.assertIn(line, actual_output)

    @patch('src.scavenger_log.add_entry')
    @patch('src.scavenger_log.list_entries')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_add_command(self, mock_parse_args, mock_list_entries, mock_add_entry):
        # Mock rationale: Simulate CLI arguments for the 'add' command.
        mock_parse_args.return_value = unittest.mock.Mock(
            command='add',
            item='Medkit',
            quantity='1',
            location='Hospital Ruin'
        )
        # Import main after patching to ensure argparse is mocked correctly
        from src.scavenger_log import main
        main()
        mock_add_entry.assert_called_once_with('Medkit', '1', 'Hospital Ruin')
        mock_list_entries.assert_not_called()

    @patch('src.scavenger_log.add_entry')
    @patch('src.scavenger_log.list_entries')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_command(self, mock_parse_args, mock_list_entries, mock_add_entry):
        # Mock rationale: Simulate CLI arguments for the 'list' command.
        mock_parse_args.return_value = unittest.mock.Mock(
            command='list'
        )
        # Import main after patching to ensure argparse is mocked correctly
        from src.scavenger_log import main
        main()
        mock_list_entries.assert_called_once()
        mock_add_entry.assert_not_called()
