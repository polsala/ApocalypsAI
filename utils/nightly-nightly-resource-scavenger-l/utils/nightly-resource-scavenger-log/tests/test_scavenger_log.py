import unittest
from unittest.mock import patch, mock_open
import os
from datetime import datetime

# Adjust sys.path to allow importing scavenger_log from the sibling 'src' directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger_log

class TestScavengerLog(unittest.TestCase):

    TEST_LOG_FILE = 'test_scavenger_log.md'
    MOCK_DATE_STR = '2023-10-27 10:30:00'
    MOCK_DATE_FILTER = '2023-10-27'

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger_log.datetime')
    def test_add_entry(self, mock_datetime, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate file not existing initially, then writing to it.
        # Mock rationale: Control the current timestamp for deterministic tests.
        mock_os_exists.return_value = False # File doesn't exist initially
        mock_datetime.now.return_value = datetime.strptime(self.MOCK_DATE_STR, scavenger_log.DATE_FORMAT)

        category = 'code'
        description = 'Implemented a new feature.'
        expected_entry = f"- [{self.MOCK_DATE_STR}] [{category}] {description}\n"

        scavenger_log.add_entry(category, description)

        mock_file_open.assert_called_once_with(self.TEST_LOG_FILE, 'a')
        mock_file_open().write.assert_called_once_with(expected_entry)
        # Ensure print statement is called (optional, but good for coverage)
        with patch('builtins.print') as mock_print:
            scavenger_log.add_entry(category, description)
            mock_print.assert_called_with(f"Entry added to {os.path.abspath(self.TEST_LOG_FILE)}")

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_entries_no_file(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate the log file not existing.
        mock_os_exists.return_value = False

        with patch('builtins.print') as mock_print:
            scavenger_log.list_entries()
            mock_print.assert_any_call(f"No scavenger log found at {self.TEST_LOG_FILE}.")
            mock_file_open.assert_not_called() # Ensure open is not called if file doesn't exist

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_entries_all(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a log file with multiple entries.
        mock_os_exists.return_value = True
        mock_log_content = (
            f"- [{self.MOCK_DATE_STR}] [code] Implemented feature A.\n"
            f"- [2023-10-28 11:00:00] [docs] Updated README.\n"
            f"- [{self.MOCK_DATE_STR}] [idea] New project idea.\n"
        )
        mock_file_open.return_value.__enter__.return_value.readlines.return_value = mock_log_content.splitlines(keepends=True)

        with patch('builtins.print') as mock_print:
            scavenger_log.list_entries()
            mock_print.assert_any_call(f"--- Scavenger Log ({self.TEST_LOG_FILE}) ---")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [code] Implemented feature A.")
            mock_print.assert_any_call(f"- [2023-10-28 11:00:00] [docs] Updated README.")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [idea] New project idea.")
            mock_print.assert_any_call("---------------------------")

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_entries_filtered_by_date(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a log file and filter entries by a specific date.
        mock_os_exists.return_value = True
        mock_log_content = (
            f"- [{self.MOCK_DATE_STR}] [code] Implemented feature A.\n"
            f"- [2023-10-28 11:00:00] [docs] Updated README.\n"
            f"- [{self.MOCK_DATE_STR}] [idea] New project idea.\n"
        )
        mock_file_open.return_value.__enter__.return_value.readlines.return_value = mock_log_content.splitlines(keepends=True)

        with patch('builtins.print') as mock_print:
            scavenger_log.list_entries(filter_date=self.MOCK_DATE_FILTER)
            mock_print.assert_any_call(f"--- Scavenger Log ({self.TEST_LOG_FILE}) ---")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [code] Implemented feature A.")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [idea] New project idea.")
            # Ensure the entry from a different date is NOT printed
            mock_print.assert_any_call("---------------------------")
            self.assertNotIn(f"- [2023-10-28 11:00:00] [docs] Updated README.", [call.args[0] for call in mock_print.call_args_list])

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_entries_filtered_no_match(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a log file but with no entries matching the filter date.
        mock_os_exists.return_value = True
        mock_log_content = (
            f"- [2023-10-28 11:00:00] [docs] Updated README.\n"
        )
        mock_file_open.return_value.__enter__.return_value.readlines.return_value = mock_log_content.splitlines(keepends=True)

        with patch('builtins.print') as mock_print:
            scavenger_log.list_entries(filter_date=self.MOCK_DATE_FILTER)
            mock_print.assert_any_call(f"--- Scavenger Log ({self.TEST_LOG_FILE}) ---")
            mock_print.assert_any_call(f"No entries found for date: {self.MOCK_DATE_FILTER}")
            mock_print.assert_any_call("---------------------------")
            # Ensure no actual log entries are printed
            self.assertNotIn(f"- [2023-10-28 11:00:00] [docs] Updated README.", [call.args[0] for call in mock_print.call_args_list])

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger_log.datetime')
    @patch('argparse.ArgumentParser')
    def test_main_add_command(self, mock_argparse, mock_datetime, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate command-line arguments for 'add' command.
        # Mock rationale: Control timestamp and file operations.
        mock_args = mock_argparse.return_value.parse_args.return_value
        mock_args.command = 'add'
        mock_args.category = 'test_cat'
        mock_args.description = 'Test description for add.'

        mock_datetime.now.return_value = datetime.strptime(self.MOCK_DATE_STR, scavenger_log.DATE_FORMAT)
        mock_os_exists.return_value = False # File doesn't exist initially

        with patch('builtins.print') as mock_print:
            scavenger_log.main()
            expected_entry = f"- [{self.MOCK_DATE_STR}] [test_cat] Test description for add.\n"
            mock_file_open.assert_called_once_with(self.TEST_LOG_FILE, 'a')
            mock_file_open().write.assert_called_once_with(expected_entry)
            mock_print.assert_called_with(f"Entry added to {os.path.abspath(self.TEST_LOG_FILE)}")

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser')
    def test_main_list_command(self, mock_argparse, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate command-line arguments for 'list' command.
        # Mock rationale: Control file existence and content.
        mock_args = mock_argparse.return_value.parse_args.return_value
        mock_args.command = 'list'
        mock_args.date = None # No date filter

        mock_os_exists.return_value = True
        mock_log_content = f"- [{self.MOCK_DATE_STR}] [code] Test entry.\n"
        mock_file_open.return_value.__enter__.return_value.readlines.return_value = mock_log_content.splitlines(keepends=True)

        with patch('builtins.print') as mock_print:
            scavenger_log.main()
            mock_print.assert_any_call(f"--- Scavenger Log ({self.TEST_LOG_FILE}) ---")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [code] Test entry.")

    @patch('scavenger_log.LOG_FILE', TEST_LOG_FILE)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser')
    def test_main_list_command_with_date(self, mock_argparse, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate command-line arguments for 'list' command with a date filter.
        # Mock rationale: Control file existence and content.
        mock_args = mock_argparse.return_value.parse_args.return_value
        mock_args.command = 'list'
        mock_args.date = self.MOCK_DATE_FILTER

        mock_os_exists.return_value = True
        mock_log_content = (
            f"- [{self.MOCK_DATE_STR}] [code] Entry for today.\n"
            f"- [2023-10-26 09:00:00] [docs] Entry for yesterday.\n"
        )
        mock_file_open.return_value.__enter__.return_value.readlines.return_value = mock_log_content.splitlines(keepends=True)

        with patch('builtins.print') as mock_print:
            scavenger_log.main()
            mock_print.assert_any_call(f"--- Scavenger Log ({self.TEST_LOG_FILE}) ---")
            mock_print.assert_any_call(f"- [{self.MOCK_DATE_STR}] [code] Entry for today.")
            self.assertNotIn(f"- [2023-10-26 09:00:00] [docs] Entry for yesterday.", [call.args[0] for call in mock_print.call_args_list])
