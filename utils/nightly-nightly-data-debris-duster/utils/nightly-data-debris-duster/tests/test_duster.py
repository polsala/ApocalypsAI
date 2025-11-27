import unittest
import os
import time
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
from datetime import datetime, timedelta

# Adjust path to import duster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import get_old_files, delete_files, main

class TestDuster(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_no_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory for testing.
        mock_isdir.return_value = True
        mock_walk.return_value = [] # No files or directories
        mock_getmtime.return_value = time.time() # Should not be called

        result = get_old_files("/test/dir", 30)
        self.assertEqual(result, [])
        self.assertIn("Scanning '/test/dir' for files older than 30 days...", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_no_old_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with only recent files.
        mock_isdir.return_value = True
        # Simulate files that are all very recent (e.g., 1 day old)
        mock_walk.return_value = [
            ("/test/dir", [], ["recent_file_1.txt", "recent_file_2.log"])
        ]
        # All files modified 1 day ago (less than 30 days threshold)
        mock_getmtime.return_value = time.time() - (1 * 24 * 60 * 60)

        result = get_old_files("/test/dir", 30)
        self.assertEqual(result, [])
        self.assertIn("Scanning '/test/dir' for files older than 30 days...", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_with_old_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with a mix of old and recent files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/test/dir", [], ["old_file_1.txt", "recent_file.log"]),
            ("/test/dir/subdir", [], ["old_file_2.csv"])
        ]

        # Define specific mtimes for each file
        # old_file_1.txt: 60 days old
        # recent_file.log: 10 days old
        # old_file_2.csv: 40 days old
        file_mtimes = {
            os.path.join("/test/dir", "old_file_1.txt"): time.time() - (60 * 24 * 60 * 60),
            os.path.join("/test/dir", "recent_file.log"): time.time() - (10 * 24 * 60 * 60),
            os.path.join("/test/dir/subdir", "old_file_2.csv"): time.time() - (40 * 24 * 60 * 60),
        }

        def mock_getmtime_side_effect(path):
            return file_mtimes.get(path, time.time()) # Default to current if not specified

        mock_getmtime.side_effect = mock_getmtime_side_effect

        result = get_old_files("/test/dir", 30)
        expected_old_files = [
            os.path.join("/test/dir", "old_file_1.txt"),
            os.path.join("/test/dir/subdir", "old_file_2.csv")
        ]
        self.assertCountEqual(result, expected_old_files)
        self.assertIn("Scanning '/test/dir' for files older than 30 days...", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    def test_get_old_files_invalid_directory(self, mock_isdir):
        # Mock rationale: Test behavior when the specified directory does not exist.
        mock_isdir.return_value = False
        result = get_old_files("/nonexistent/dir", 30)
        self.assertEqual(result, [])
        self.assertIn("Error: Directory '/nonexistent/dir' not found.", self.mock_stdout.getvalue())

    @patch('os.remove')
    def test_delete_files_success(self, mock_remove):
        # Mock rationale: Prevent actual file deletion during testing.
        files_to_delete = ["/path/to/file1.txt", "/path/to/file2.log"]
        delete_files(files_to_delete)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call("/path/to/file1.txt")
        mock_remove.assert_any_call("/path/to/file2.log")
        self.assertIn("Attempting to delete 2 files...", self.mock_stdout.getvalue())
        self.assertIn("Successfully deleted 2 out of 2 files.", self.mock_stdout.getvalue())

    @patch('os.remove')
    def test_delete_files_with_error(self, mock_remove):
        # Mock rationale: Simulate a scenario where some files cannot be deleted.
        files_to_delete = ["/path/to/file1.txt", "/path/to/file2.log"]
        mock_remove.side_effect = [None, OSError("Permission denied")] # First succeeds, second fails
        delete_files(files_to_delete)
        self.assertEqual(mock_remove.call_count, 2)
        self.assertIn("Error: Could not delete '/path/to/file2.log': Permission denied", self.mock_stdout.getvalue())
        self.assertIn("Successfully deleted 1 out of 2 files.", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.get_old_files')
    @patch('builtins.input', return_value='yes') # Mock rationale: Simulate user input for confirmation.
    @patch('duster.delete_files')
    def test_main_delete_confirmed(self, mock_delete_files, mock_input, mock_get_old_files, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and the entire workflow.
        mock_parse_args.return_value = MagicMock(
            path="/test/dir",
            days=30,
            delete=True,
            verbose=False
        )
        mock_get_old_files.return_value = ["/test/dir/old_file.txt"]

        main()

        mock_get_old_files.assert_called_once_with("/test/dir", 30, False)
        mock_input.assert_called_once()
        mock_delete_files.assert_called_once_with(["/test/dir/old_file.txt"], False)
        self.assertIn("Found 1 files older than 30 days:", self.mock_stdout.getvalue())
        self.assertIn("- /test/dir/old_file.txt", self.mock_stdout.getvalue())
        self.assertIn("Are you sure you want to delete these files? Type 'yes' to confirm:", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.get_old_files')
    @patch('builtins.input', return_value='no') # Mock rationale: Simulate user input for cancellation.
    @patch('duster.delete_files')
    def test_main_delete_cancelled(self, mock_delete_files, mock_input, mock_get_old_files, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and the entire workflow.
        mock_parse_args.return_value = MagicMock(
            path="/test/dir",
            days=30,
            delete=True,
            verbose=False
        )
        mock_get_old_files.return_value = ["/test/dir/old_file.txt"]

        main()

        mock_get_old_files.assert_called_once_with("/test/dir", 30, False)
        mock_input.assert_called_once()
        mock_delete_files.assert_not_called()
        self.assertIn("Deletion cancelled.", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.get_old_files')
    @patch('duster.delete_files')
    def test_main_dry_run(self, mock_delete_files, mock_get_old_files, mock_parse_args):
        # Mock rationale: Simulate command-line arguments for a dry run (no --delete flag).
        mock_parse_args.return_value = MagicMock(
            path="/test/dir",
            days=30,
            delete=False,
            verbose=False
        )
        mock_get_old_files.return_value = ["/test/dir/old_file.txt"]

        main()

        mock_get_old_files.assert_called_once_with("/test/dir", 30, False)
        mock_delete_files.assert_not_called()
        self.assertIn("Run with --delete to remove these files.", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.get_old_files')
    def test_main_no_old_files(self, mock_get_old_files, mock_parse_args):
        # Mock rationale: Simulate a scenario where no old files are found.
        mock_parse_args.return_value = MagicMock(
            path="/test/dir",
            days=30,
            delete=False,
            verbose=False
        )
        mock_get_old_files.return_value = []

        main()

        mock_get_old_files.assert_called_once_with("/test/dir", 30, False)
        self.assertIn("No files older than 30 days found in '/test/dir'. Your data is pristine!", self.mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
