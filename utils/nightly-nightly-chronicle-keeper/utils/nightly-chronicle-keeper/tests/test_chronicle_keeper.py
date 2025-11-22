import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import sys

# Add the src directory to the path to allow importing chronicle_keeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Mock datetime.datetime.now() to ensure deterministic timestamps
        # Mock rationale: We need a consistent time for testing log entry formatting
        # and file path generation, independent of when the test is run.
        self.mock_now = datetime.datetime(2023, 10, 27, 14, 35, 1)
        self.patcher_datetime = patch('datetime.datetime')
        self.mock_datetime = self.patcher_datetime.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow real datetime calls for other purposes

        # Mock os.makedirs to prevent actual directory creation
        # Mock rationale: We don't want tests to create real directories on the filesystem.
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()

        # Mock os.getcwd to ensure a consistent base path
        # Mock rationale: The utility uses os.getcwd() to determine the base for the 'chronicles' directory.
        # We need to control this for deterministic path testing.
        self.patcher_getcwd = patch('os.getcwd', return_value='/mock/current/dir')
        self.mock_getcwd = self.patcher_getcwd.start()

    def tearDown(self):
        self.patcher_datetime.stop()
        self.patcher_makedirs.stop()
        self.patcher_getcwd.stop()
        # Remove src from path
        sys.path.pop(0)

    def test_get_log_dir(self):
        expected_dir = os.path.join('/mock/current/dir', 'chronicles')
        self.assertEqual(chronicle_keeper.get_log_dir(), expected_dir)

    def test_get_log_file_path(self):
        mock_log_dir = '/mock/current/dir/chronicles'
        mock_date = datetime.datetime(2023, 1, 15)
        expected_path = os.path.join(mock_log_dir, '2023-01-15.log')
        self.assertEqual(chronicle_keeper.get_log_file_path(mock_log_dir, mock_date), expected_path)

    def test_format_log_entry(self):
        message = "Test message."
        expected_entry = "[2023-10-27 14:35:01] Test message.\n"
        self.assertEqual(chronicle_keeper.format_log_entry(message, self.mock_now), expected_entry)

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(message="Test message for main."))
    def test_main_writes_to_file(self, mock_args, mock_file_open):
        # Mock rationale: We need to intercept the file open operation to verify
        # that the correct content is written without actually touching the filesystem.
        chronicle_keeper.main()

        expected_log_dir = os.path.join('/mock/current/dir', 'chronicles')
        expected_log_file_path = os.path.join(expected_log_dir, '2023-10-27.log')
        expected_log_entry = "[2023-10-27 14:35:01] Test message for main.\n"

        # Verify os.makedirs was called
        self.mock_makedirs.assert_called_once_with(expected_log_dir, exist_ok=True)

        # Verify file was opened in append mode
        mock_file_open.assert_called_once_with(expected_log_file_path, "a")

        # Verify content was written
        mock_file_open().write.assert_called_once_with(expected_log_entry)

    @patch('builtins.print') # Mock print to avoid output during test
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(message="Another message."))
    def test_main_handles_io_error(self, mock_args, mock_file_open, mock_print):
        # Mock rationale: Simulate an IOError during file writing to ensure
        # the utility handles it gracefully and exits with code 1.
        mock_file_open.side_effect = IOError("Permission denied")

        with self.assertRaises(SystemExit) as cm:
            chronicle_keeper.main()

        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error writing to chronicle file: Permission denied")

if __name__ == '__main__':
    unittest.main()
