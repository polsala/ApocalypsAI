import unittest
import sys
import os
from unittest.mock import patch, mock_open, MagicMock
import datetime

# Add the src directory to the path so we can import logbook
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import logbook

class TestLogbook(unittest.TestCase):

    # Mock rationale: We need a consistent timestamp for testing log entry generation
    # and file naming, as datetime.datetime.now() changes constantly.
    MOCK_DATETIME_STR = "2023-10-27 10:00:00"
    MOCK_DATE_STR = "2023-10-27"
    MOCK_DATETIME = datetime.datetime.strptime(MOCK_DATETIME_STR, "%Y-%m-%d %H:%M:%S")

    @patch('datetime.datetime')
    def test_get_log_entry(self, mock_dt):
        """Test that log entries are formatted correctly with a timestamp."""
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime # Use real strftime for the mock object
        mock_dt.strptime = datetime.datetime.strptime # Use real strptime for the mock object

        message = "Test message for the log."
        expected_entry = f"### {self.MOCK_DATETIME_STR}\n{message}\n"
        self.assertEqual(logbook.get_log_entry(message), expected_entry)

    @patch('datetime.datetime')
    def test_get_log_filename_default(self, mock_dt):
        """Test default log filename generation."""
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime # Use real strftime for the mock object
        mock_dt.strptime = datetime.datetime.strptime # Use real strptime for the mock object

        self.assertEqual(logbook.get_log_filename("chronicle.md", False), "chronicle.md")

    @patch('datetime.datetime')
    def test_get_log_filename_daily(self, mock_dt):
        """Test daily log filename generation."""
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime # Use real strftime for the mock object
        mock_dt.strptime = datetime.datetime.strptime # Use real strptime for the mock object

        self.assertEqual(logbook.get_log_filename("chronicle.md", True), f"{self.MOCK_DATE_STR}_chronicle.md")
        self.assertEqual(logbook.get_log_filename("my_log.txt", True), f"{self.MOCK_DATE_STR}_my_log.txt")

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_ensure_log_directory_exists_creates_if_not_exists(self, mock_makedirs, mock_exists):
        """
        Mock rationale: We need to simulate file system state without actually creating directories.
        os.path.exists is mocked to return False, and os.makedirs is mocked to check if it's called.
        """
        mock_exists.return_value = False
        logbook.ensure_log_directory_exists("/path/to/logs/file.md")
        mock_makedirs.assert_called_once_with("/path/to/logs")

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_ensure_log_directory_exists_does_not_create_if_exists(self, mock_makedirs, mock_exists):
        """
        Mock rationale: Simulate a directory already existing to ensure os.makedirs is not called unnecessarily.
        """
        mock_exists.return_value = True
        logbook.ensure_log_directory_exists("/path/to/logs/file.md")
        mock_makedirs.assert_not_called()

    @patch('os.path.exists', return_value=True) # Mock rationale: Assume directory exists for simplicity in this test
    @patch('os.makedirs') # Mock rationale: Ensure no directory creation happens if path exists
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock) # Mock rationale: Capture print statements to verify output
    def test_main_logs_message_to_default_file(self, mock_stdout, mock_dt, mock_file_open, mock_makedirs, mock_exists):
        """
        Mock rationale:
        - builtins.open: To prevent actual file I/O and capture the content written to the file.
        - datetime.datetime: To ensure consistent timestamps for log entries.
        - sys.stdout: To capture the script's print output for verification.
        - os.path.exists, os.makedirs: To simulate file system state without actual disk operations.
        """
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime
        mock_dt.strptime = datetime.datetime.strptime

        # Mock argparse.ArgumentParser to control command-line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            message="A new discovery!",
            file="chronicle.md",
            daily=False
        )):
            logbook.main()

            # Construct the expected full path for the log file
            current_test_file_dir = os.path.dirname(os.path.abspath(__file__))
            utility_root_dir = os.path.abspath(os.path.join(current_test_file_dir, '..'))
            expected_log_filepath = os.path.join(utility_root_dir, "logs", "chronicle.md")

            mock_file_open.assert_called_once_with(expected_log_filepath, "a", encoding="utf-8")
            mock_file_open().write.assert_called_once_with(f"### {self.MOCK_DATETIME_STR}\nA new discovery!\n\n")
            mock_stdout.write.assert_any_call(f"Entry logged to {expected_log_filepath}\n")

    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_logs_message_to_daily_file(self, mock_stdout, mock_dt, mock_file_open, mock_makedirs, mock_exists):
        """
        Mock rationale: Same as above, but specifically for daily logging.
        """
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime
        mock_dt.strptime = datetime.datetime.strptime

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            message="Daily report.",
            file="chronicle.md",
            daily=True
        )):
            logbook.main()

            current_test_file_dir = os.path.dirname(os.path.abspath(__file__))
            utility_root_dir = os.path.abspath(os.path.join(current_test_file_dir, '..'))
            expected_log_filepath = os.path.join(utility_root_dir, "logs", f"{self.MOCK_DATE_STR}_chronicle.md")

            mock_file_open.assert_called_once_with(expected_log_filepath, "a", encoding="utf-8")
            mock_file_open().write.assert_called_once_with(f"### {self.MOCK_DATETIME_STR}\nDaily report.\n\n")
            mock_stdout.write.assert_any_call(f"Entry logged to {expected_log_filepath}\n")

    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_logs_message_to_custom_file(self, mock_stdout, mock_dt, mock_file_open, mock_makedirs, mock_exists):
        """
        Mock rationale: Same as above, but for a custom log file name.
        """
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime
        mock_dt.strptime = datetime.datetime.strptime

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            message="Custom log entry.",
            file="my_special_log.txt",
            daily=False
        )):
            logbook.main()

            current_test_file_dir = os.path.dirname(os.path.abspath(__file__))
            utility_root_dir = os.path.abspath(os.path.join(current_test_file_dir, '..'))
            expected_log_filepath = os.path.join(utility_root_dir, "logs", "my_special_log.txt")

            mock_file_open.assert_called_once_with(expected_log_filepath, "a", encoding="utf-8")
            mock_file_open().write.assert_called_once_with(f"### {self.MOCK_DATETIME_STR}\nCustom log entry.\n\n")
            mock_stdout.write.assert_any_call(f"Entry logged to {expected_log_filepath}\n")

    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate directory not existing
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_creates_directory_if_not_exists(self, mock_stdout, mock_dt, mock_file_open, mock_makedirs, mock_exists):
        """
        Mock rationale: Ensure that the directory creation logic is triggered when needed.
        """
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime
        mock_dt.strptime = datetime.datetime.strptime

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            message="Test message.",
            file="test.md",
            daily=False
        )):
            logbook.main()

            current_test_file_dir = os.path.dirname(os.path.abspath(__file__))
            utility_root_dir = os.path.abspath(os.path.join(current_test_file_dir, '..'))
            expected_log_dir = os.path.join(utility_root_dir, "logs")
            mock_makedirs.assert_called_once_with(expected_log_dir)

    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    @patch('builtins.open', side_effect=IOError("Permission denied")) # Mock rationale: Simulate a file write error
    @patch('datetime.datetime')
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr for error messages
    @patch('sys.exit') # Mock rationale: Prevent actual script exit during test
    def test_main_handles_io_error(self, mock_exit, mock_stderr, mock_dt, mock_file_open, mock_makedirs, mock_exists):
        """
        Mock rationale: Test error handling when file writing fails.
        """
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.strftime = datetime.datetime.strftime
        mock_dt.strptime = datetime.datetime.strptime

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            message="Error test.",
            file="error.md",
            daily=False
        )):
            logbook.main()

            current_test_file_dir = os.path.dirname(os.path.abspath(__file__))
            utility_root_dir = os.path.abspath(os.path.join(current_test_file_dir, '..'))
            expected_log_filepath = os.path.join(utility_root_dir, "logs", "error.md")

            mock_stderr.write.assert_any_call(f"Error writing to log file {expected_log_filepath}: Permission denied\n")
            mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
