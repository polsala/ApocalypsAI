import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from datetime import datetime, timedelta

# Mock rationale: We need to test file system operations and date/time generation
# without actually touching the disk or relying on the current system time.
# `os.makedirs` is mocked to prevent real directory creation.
# `builtins.open` is mocked to simulate file reading/writing in memory.
# `datetime.datetime` is mocked to provide a fixed, deterministic "current" time.

# Import the module to be tested
# Adjust path for testing if necessary, assuming tests are run from the utils/nightly-apocalypse-logbook/ directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import logbook
sys.path.pop(0)

class TestApocalypseLogbook(unittest.TestCase):

    def setUp(self):
        # Set a fixed "now" for deterministic testing
        self.mock_now = datetime(2023, 10, 27, 10, 30, 0)
        self.mock_today_str = "2023-10-27"
        self.mock_yesterday = datetime(2023, 10, 26, 15, 0, 0)
        self.mock_yesterday_str = "2023-10-26"

        # Create a temporary directory for logbook_data to ensure isolation
        # This is for testing the _get_log_path and _ensure_log_dir logic, but actual file I/O will be mocked.
        self.test_dir = "test_logbook_data"
        self.original_log_dir_name = logbook.LOG_DIR_NAME
        logbook.LOG_DIR_NAME = self.test_dir
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_dir)
        logbook.LOG_DIR_NAME = self.original_log_dir_name # Restore original

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation on disk.
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate logbook_data not existing initially.
    def test_init_logbook_creates_dir(self, mock_exists, mock_makedirs):
        logbook.init_logbook()
        mock_makedirs.assert_called_once_with(self.test_dir)

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation on disk.
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate logbook_data already existing.
    def test_init_logbook_dir_exists(self, mock_exists, mock_makedirs):
        logbook.init_logbook()
        mock_makedirs.assert_not_called()

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate file writing in memory.
    @patch('os.path.exists', side_effect=[True, False]) # Mock rationale: Simulate logbook_data existing, then log file not existing (new file).
    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation on disk.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_new_entry_creates_new_file_with_header(self, mock_dt, mock_makedirs, mock_exists, mock_file):
        mock_dt.now.return_value = self.mock_now
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        category = "scavenge"
        message = "Found a rare byte-gem."
        logbook.new_entry(category, message)

        expected_path = os.path.join(self.test_dir, "2023", "10", "27.md")
        mock_file.assert_called_once_with(expected_path, "a", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_any_call(f"# Logbook Entry for {self.mock_today_str}\n\n")
        handle.write.assert_any_call(f"### [10:30:00] SCAVENGE - {message}\n")

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate file writing in memory.
    @patch('os.path.exists', side_effect=[True, True]) # Mock rationale: Simulate logbook_data existing, then log file existing (append).
    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation on disk.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_new_entry_appends_to_existing_file_no_header(self, mock_dt, mock_makedirs, mock_exists, mock_file):
        mock_dt.now.return_value = self.mock_now
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        category = "build"
        message = "Fixed the flux capacitor."
        logbook.new_entry(category, message)

        handle = mock_file()
        # Ensure header is NOT written if file exists
        self.assertFalse(any(f"# Logbook Entry" in call.args[0] for call in handle.write.call_args_list))
        handle.write.assert_called_once_with(f"### [10:30:00] BUILD - {message}\n")

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate file writing in memory.
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate log file not existing.
    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation on disk.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_new_entry_invalid_category(self, mock_dt, mock_makedirs, mock_exists, mock_file):
        mock_dt.now.return_value = self.mock_now
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        category = "invalid_cat"
        message = "This should not be logged."
        
        with patch('sys.stdout', new=MagicMock()) as mock_stdout: # Mock rationale: Capture print output for assertion.
            logbook.new_entry(category, message)
            self.assertIn("Error: Invalid category", mock_stdout.write.call_args[0][0])
        mock_file.assert_not_called() # Ensure no file operations occurred

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate file reading in memory.
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate log file existing.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_view_entries_for_today(self, mock_dt, mock_exists, mock_file):
        mock_dt.now.return_value = self.mock_now
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        mock_file.return_value.read.return_value = (
            f"# Logbook Entry for {self.mock_today_str}\n\n"
            f"### [09:00:00] OBSERVE - Sun rose in the east.\n"
            f"### [10:30:00] REFLECT - Good day to be alive.\n"
        )

        with patch('sys.stdout', new=MagicMock()) as mock_stdout: # Mock rationale: Capture print output for assertion.
            logbook.view_entries()
            expected_output = (
                f"# Logbook Entry for {self.mock_today_str}\n\n"
                f"### [09:00:00] OBSERVE - Sun rose in the east.\n"
                f"### [10:30:00] REFLECT - Good day to be alive.\n"
            )
            self.assertIn(expected_output, mock_stdout.write.call_args[0][0])
        
        expected_path = os.path.join(self.test_dir, "2023", "10", "27.md")
        mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate file reading in memory.
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate log file existing.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_view_entries_for_specific_date(self, mock_dt, mock_exists, mock_file):
        mock_dt.now.return_value = self.mock_now # Still mock now, but view_entries uses the date_str
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        mock_file.return_value.read.return_value = (
            f"# Logbook Entry for {self.mock_yesterday_str}\n\n"
            f"### [12:00:00] REPORT - Daily summary submitted.\n"
        )

        with patch('sys.stdout', new=MagicMock()) as mock_stdout: # Mock rationale: Capture print output for assertion.
            logbook.view_entries(self.mock_yesterday_str)
            expected_output = (
                f"# Logbook Entry for {self.mock_yesterday_str}\n\n"
                f"### [12:00:00] REPORT - Daily summary submitted.\n"
            )
            self.assertIn(expected_output, mock_stdout.write.call_args[0][0])
        
        expected_path = os.path.join(self.test_dir, "2023", "10", "26.md")
        mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")

    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate log file not existing.
    @patch('datetime.datetime') # Mock rationale: Provide a fixed, deterministic "current" time.
    def test_view_entries_no_logs_found(self, mock_dt, mock_exists):
        mock_dt.now.return_value = self.mock_now
        mock_dt.strptime = datetime.strptime # Keep original strptime functionality

        with patch('sys.stdout', new=MagicMock()) as mock_stdout: # Mock rationale: Capture print output for assertion.
            logbook.view_entries(self.mock_yesterday_str)
            self.assertIn(f"No log entries found for {self.mock_yesterday_str}.", mock_stdout.write.call_args[0][0])

    @patch('sys.stdout', new=MagicMock()) # Mock rationale: Capture print output for assertion.
    def test_list_categories(self, mock_stdout):
        logbook.list_categories()
        output = mock_stdout.write.call_args[0][0]
        self.assertIn("Available categories:", output)
        for cat in logbook.DEFAULT_CATEGORIES:
            self.assertIn(f"- {cat}", output)

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Simulate command-line arguments without actual CLI parsing.
    @patch('logbook.init_logbook') # Mock rationale: Isolate the test to ensure the correct function is called.
    def test_main_init_command(self, mock_init, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command="init")
        logbook.main()
        mock_init.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Simulate command-line arguments without actual CLI parsing.
    @patch('logbook.new_entry') # Mock rationale: Isolate the test to ensure the correct function is called.
    def test_main_new_command(self, mock_new_entry, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command="new", category="build", message="Test message.")
        logbook.main()
        mock_new_entry.assert_called_once_with("build", "Test message.")

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Simulate command-line arguments without actual CLI parsing.
    @patch('logbook.view_entries') # Mock rationale: Isolate the test to ensure the correct function is called.
    def test_main_view_command(self, mock_view_entries, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command="view", date="2023-01-01")
        logbook.main()
        mock_view_entries.assert_called_once_with("2023-01-01")

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Simulate command-line arguments without actual CLI parsing.
    @patch('logbook.list_categories') # Mock rationale: Isolate the test to ensure the correct function is called.
    def test_main_categories_command(self, mock_list_categories, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command="categories")
        logbook.main()
        mock_list_categories.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Simulate command-line arguments without actual CLI parsing.
    @patch('argparse.ArgumentParser.print_help') # Mock rationale: Capture help output for assertion.
    def test_main_no_command(self, mock_print_help, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command=None)
        logbook.main()
        mock_print_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
