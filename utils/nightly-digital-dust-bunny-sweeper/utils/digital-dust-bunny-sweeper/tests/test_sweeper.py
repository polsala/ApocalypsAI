import unittest
import os
import sys
import io
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the sweeper module
# Assuming the test file is in utils/digital-dust-bunny-sweeper/tests/
# and the source file is in utils/digital-dust-bunny-sweeper/src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_old_files, delete_files, main

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_find_old_files(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale:
        # - os.path.isdir: To simulate a valid directory without actual filesystem access.
        # - os.walk: To simulate directory traversal and file discovery.
        # - os.path.getmtime: To control file modification times for age-based filtering.
        # - datetime.datetime: To control the current time for consistent age calculation.

        mock_isdir.return_value = True

        # Simulate current time for consistent cutoff
        mock_now = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        # Define a cutoff timestamp (e.g., 90 days before mock_now)
        cutoff_timestamp = (mock_now - timedelta(days=90)).timestamp()

        # Mock os.walk to return a specific directory structure and files
        mock_walk.return_value = [
            ('/mock/dir', [], ['old_file.txt', 'recent_file.log', 'another_old.doc']),
            ('/mock/dir/subdir', [], ['sub_old.txt', 'sub_recent.csv'])
        ]

        # Mock os.path.getmtime for each file
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return (mock_now - timedelta(days=100)).timestamp() # Older than 90 days
            elif 'recent_file.log' in path:
                return (mock_now - timedelta(days=50)).timestamp()  # Newer than 90 days
            elif 'another_old.doc' in path:
                return (mock_now - timedelta(days=91)).timestamp()  # Just older than 90 days
            elif 'sub_old.txt' in path:
                return (mock_now - timedelta(days=120)).timestamp() # Older
            elif 'sub_recent.csv' in path:
                return (mock_now - timedelta(days=10)).timestamp()  # Newer
            return time.time() # Default for unexpected paths

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test with default age (90 days)
        old_files = find_old_files('/mock/dir', 90)
        expected_files = [
            '/mock/dir/old_file.txt',
            '/mock/dir/another_old.doc',
            '/mock/dir/subdir/sub_old.txt'
        ]
        self.assertCountEqual(old_files, expected_files)

        # Test with a different age (e.g., 60 days)
        mock_getmtime.reset_mock() # Reset mocks for new test case
        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_datetime.now.return_value = mock_now # Ensure datetime.now is consistent
        old_files_60_days = find_old_files('/mock/dir', 60)
        # Now 'recent_file.log' (50 days old) is NOT old, but 'another_old.doc' (91 days) and 'old_file.txt' (100 days) and 'sub_old.txt' (120 days) are.
        # The 50-day old file is still newer than 60 days.
        self.assertCountEqual(old_files_60_days, expected_files) # Same expected files as 90 days, because 50-day file is still too new.

        # Test with a directory that doesn't exist
        mock_isdir.return_value = False
        old_files_non_existent = find_old_files('/non/existent/dir', 90)
        self.assertEqual(old_files_non_existent, [])
        self.assertIn("Error: Directory not found", self.mock_stdout.getvalue())
        self.mock_stdout.truncate(0) # Clear stdout for next test

        # Test with OSError during file access
        mock_isdir.return_value = True
        mock_walk.return_value = [('/mock/dir', [], ['unreadable_file.txt'])]
        mock_getmtime.side_effect = OSError("Permission denied")
        old_files_os_error = find_old_files('/mock/dir', 90)
        self.assertEqual(old_files_os_error, [])
        self.assertIn("Warning: Could not access file", self.mock_stdout.getvalue())


    @patch('os.remove')
    def test_delete_files(self, mock_remove):
        # Mock rationale:
        # - os.remove: To prevent actual file deletion during tests.

        files_to_delete = ['/mock/path/file1.txt', '/mock/path/file2.txt']
        delete_files(files_to_delete)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/mock/path/file1.txt')
        mock_remove.assert_any_call('/mock/path/file2.txt')
        output = self.mock_stdout.getvalue()
        self.assertIn("Attempting to delete 2 files...", output)
        self.assertIn("Deleted: /mock/path/file1.txt", output)
        self.assertIn("Deleted: /mock/path/file2.txt", output)
        self.assertIn("Successfully deleted 2 files.", output)

        self.mock_stdout.truncate(0) # Clear stdout for next test

        # Test with no files
        delete_files([])
        self.assertIn("No files to delete.", self.mock_stdout.getvalue())
        self.assertEqual(mock_remove.call_count, 2) # Should not have been called again

        self.mock_stdout.truncate(0) # Clear stdout for next test

        # Test with OSError during deletion
        mock_remove.reset_mock()
        mock_remove.side_effect = OSError("Permission denied")
        files_with_error = ['/mock/path/error_file.txt']
        delete_files(files_with_error)
        mock_remove.assert_called_once_with('/mock/path/error_file.txt')
        output = self.mock_stdout.getvalue()
        self.assertIn("Error deleting /mock/path/error_file.txt: Permission denied", output)
        self.assertIn("Successfully deleted 0 files.", output)


    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_old_files')
    @patch('sweeper.delete_files')
    def test_main_dry_run(self, mock_delete_files, mock_find_old_files, mock_parse_args):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: To simulate command-line arguments.
        # - sweeper.find_old_files: To control the list of files found without actual scanning.
        # - sweeper.delete_files: To ensure deletion is not called during a dry run.

        # Simulate arguments for a dry run
        mock_args = MagicMock()
        mock_args.path = '/test/dir'
        mock_args.age = 30
        mock_args.delete = False
        mock_parse_args.return_value = mock_args

        # Simulate finding some old files
        mock_find_old_files.return_value = ['/test/dir/file_a.txt', '/test/dir/file_b.log']

        main()

        mock_find_old_files.assert_called_once_with('/test/dir', 30)
        mock_delete_files.assert_not_called() # Crucial for dry run
        output = self.mock_stdout.getvalue()
        self.assertIn("Scanning '/test/dir' for files older than 30 days...", output)
        self.assertIn("Found 2 old files (digital dust bunnies):", output)
        self.assertIn("  - /test/dir/file_a.txt", output)
        self.assertIn("  - /test/dir/file_b.log", output)
        self.assertIn("This was a DRY RUN. No files were deleted.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_old_files')
    @patch('sweeper.delete_files')
    def test_main_deletion_mode(self, mock_delete_files, mock_find_old_files, mock_parse_args):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: To simulate command-line arguments.
        # - sweeper.find_old_files: To control the list of files found without actual scanning.
        # - sweeper.delete_files: To ensure deletion is called when --delete is present.

        # Simulate arguments for deletion mode
        mock_args = MagicMock()
        mock_args.path = '/another/dir'
        mock_args.age = 60
        mock_args.delete = True
        mock_parse_args.return_value = mock_args

        # Simulate finding some old files
        found_files = ['/another/dir/old_doc.pdf']
        mock_find_old_files.return_value = found_files

        main()

        mock_find_old_files.assert_called_once_with('/another/dir', 60)
        mock_delete_files.assert_called_once_with(found_files) # Should be called
        output = self.mock_stdout.getvalue()
        self.assertIn("Scanning '/another/dir' for files older than 60 days...", output)
        self.assertIn("Found 1 old files (digital dust bunnies):", output)
        self.assertIn("  - /another/dir/old_doc.pdf", output)
        self.assertIn("--- DELETION MODE ACTIVATED ---", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_old_files')
    @patch('sweeper.delete_files')
    def test_main_no_old_files(self, mock_delete_files, mock_find_old_files, mock_parse_args):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: To simulate command-line arguments.
        # - sweeper.find_old_files: To simulate no files being found.
        # - sweeper.delete_files: To ensure deletion is not called if no files are found.

        mock_args = MagicMock()
        mock_args.path = '/clean/dir'
        mock_args.age = 10
        mock_args.delete = False
        mock_parse_args.return_value = mock_args

        mock_find_old_files.return_value = [] # Simulate no files found

        main()

        mock_find_old_files.assert_called_once_with('/clean/dir', 10)
        mock_delete_files.assert_not_called()
        output = self.mock_stdout.getvalue()
        self.assertIn("No digital dust bunnies found! Your specified directory is sparkling clean.", output)


if __name__ == '__main__':
    unittest.main()
