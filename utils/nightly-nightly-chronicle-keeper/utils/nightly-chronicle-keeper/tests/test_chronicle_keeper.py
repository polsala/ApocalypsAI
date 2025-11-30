import unittest
import argparse
import datetime
import os
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add the src directory to the path to allow importing chronicle_keeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper

class TestChronicleKeeper(unittest.TestCase):

    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False) # Mock that 'logs' directory does not exist initially
    @patch('os.getcwd', return_value='/mock/current/dir') # Mock current working directory
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture prints
    def test_chronicle_entry_creation(self, mock_stdout, mock_file_open, mock_getcwd, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale:
        # - datetime.datetime: Ensures deterministic timestamps for testing.
        # - os.makedirs: Prevents actual directory creation on the filesystem.
        # - os.path.exists: Controls the mock behavior for directory existence checks.
        # - os.getcwd: Provides a consistent mock current working directory for path resolution.
        # - builtins.open: Prevents actual file writes and allows inspection of written content.
        # - sys.stdout: Captures print statements to verify output messages.

        # Setup mock datetime
        mock_now = MagicMock(spec=datetime.datetime)
        mock_now.strftime.side_effect = lambda fmt: datetime.datetime(2023, 10, 27, 14, 30, 0).strftime(fmt)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow datetime.datetime(Y,M,D) calls

        # Setup mock argparse args
        mock_args = argparse.Namespace(message="Test entry for the chronicle.")
        with patch('argparse.ArgumentParser.parse_args', return_value=mock_args):
            chronicle_keeper.main()

        # Assertions
        # 1. Check if log directory was attempted to be created
        mock_makedirs.assert_called_once_with('/mock/current/dir/logs')

        # 2. Check if the correct file was opened in append mode
        expected_log_path = '/mock/current/dir/logs/2023-10-27_chronicle.log'
        mock_file_open.assert_called_once_with(expected_log_path, "a", encoding="utf-8")

        # 3. Check the content written to the file
        mock_file_open().write.assert_called_once_with("[14:30:00] Test entry for the chronicle.\n")

        # 4. Check the success message printed to stdout
        mock_stdout.write.assert_any_call(f"Chronicle entry added to '{expected_log_path}'\n")

    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True) # Mock that 'logs' directory already exists
    @patch('os.getcwd', return_value='/mock/current/dir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_chronicle_entry_existing_dir(self, mock_stdout, mock_file_open, mock_getcwd, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale: Same as above, but specifically testing the case where the log directory already exists.

        mock_now = MagicMock(spec=datetime.datetime)
        mock_now.strftime.side_effect = lambda fmt: datetime.datetime(2023, 10, 28, 9, 0, 0).strftime(fmt)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_args = argparse.Namespace(message="Another day, another entry.")
        with patch('argparse.ArgumentParser.parse_args', return_value=mock_args):
            chronicle_keeper.main()

        # Assertions
        # 1. Check that os.makedirs was NOT called since directory exists
        mock_makedirs.assert_not_called()

        # 2. Check if the correct file was opened
        expected_log_path = '/mock/current/dir/logs/2023-10-28_chronicle.log'
        mock_file_open.assert_called_once_with(expected_log_path, "a", encoding="utf-8")

        # 3. Check the content written
        mock_file_open().write.assert_called_once_with("[09:00:00] Another day, another entry.\n")

    @patch('datetime.datetime')
    @patch('os.makedirs', side_effect=OSError("Permission denied")) # Mock failed directory creation
    @patch('os.path.exists', return_value=False)
    @patch('os.getcwd', return_value='/mock/current/dir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock) # Mock stderr to capture error prints
    def test_chronicle_entry_makedirs_failure_fallback(self, mock_stderr, mock_stdout, mock_file_open, mock_getcwd, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale:
        # - os.makedirs: Simulates a permission error when creating the 'logs' directory.
        # - sys.stderr: Captures error messages printed to stderr.
        # Other mocks: Same as above for deterministic behavior and preventing side effects.

        mock_now = MagicMock(spec=datetime.datetime)
        mock_now.strftime.side_effect = lambda fmt: datetime.datetime(2023, 10, 29, 10, 0, 0).strftime(fmt)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_args = argparse.Namespace(message="Entry during directory creation failure.")
        with patch('argparse.ArgumentParser.parse_args', return_value=mock_args):
            chronicle_keeper.main()

        # Assertions
        # 1. Check that os.makedirs was called and raised an error
        mock_makedirs.assert_called_once_with('/mock/current/dir/logs')
        
        # 2. Check that an error message was printed to stderr about directory creation
        mock_stderr.write.assert_any_call("Error creating log directory '/mock/current/dir/logs': Permission denied\n")
        mock_stderr.write.assert_any_call("Falling back to current working directory: '/mock/current/dir'\n")

        # 3. Check that the file was opened in the fallback directory (current working directory)
        expected_log_path = '/mock/current/dir/2023-10-29_chronicle.log'
        mock_file_open.assert_called_once_with(expected_log_path, "a", encoding="utf-8")

        # 4. Check the content written
        mock_file_open().write.assert_called_once_with("[10:00:00] Entry during directory creation failure.\n")

        # 5. Check the success message printed to stdout
        mock_stdout.write.assert_any_call(f"Chronicle entry added to '{expected_log_path}'\n")

    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True)
    @patch('os.getcwd', return_value='/mock/current/dir')
    @patch('builtins.open', new_callable=mock_open, side_effect=IOError("Disk full")) # Mock file write failure
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_chronicle_entry_file_write_failure(self, mock_exit, mock_stderr, mock_stdout, mock_file_open, mock_getcwd, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale:
        # - builtins.open: Simulates an IOError during file writing (e.g., disk full).
        # - sys.exit: Prevents the test runner from exiting when chronicle_keeper.py calls sys.exit(1).
        # Other mocks: Same as above for deterministic behavior and preventing side effects.

        mock_now = MagicMock(spec=datetime.datetime)
        mock_now.strftime.side_effect = lambda fmt: datetime.datetime(2023, 10, 30, 11, 0, 0).strftime(fmt)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_args = argparse.Namespace(message="Entry during file write failure.")
        with patch('argparse.ArgumentParser.parse_args', return_value=mock_args):
            chronicle_keeper.main()

        # Assertions
        # 1. Check that an error message was printed to stderr about file writing
        expected_log_path = '/mock/current/dir/logs/2023-10-30_chronicle.log'
        mock_stderr.write.assert_any_call(f"Error writing to log file '{expected_log_path}': Disk full\n")

        # 2. Check that sys.exit(1) was called
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
