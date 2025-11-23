import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.cleaner import find_files_to_clean, clean_files

class TestCacheCleaner(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_files_by_age(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate valid directories.
        # os.walk is mocked to simulate directory traversal and file discovery.
        # os.path.getmtime is mocked to control the modification time of files for age-based filtering.

        mock_isdir.return_value = True

        # Simulate files:
        # - file_old.txt: older than 30 days
        # - file_new.txt: newer than 30 days
        # - file_ancient.log: older than 30 days, matches pattern
        # - file_recent.log: newer than 30 days, matches pattern

        # Calculate timestamps for mocking
        now = datetime.now()
        old_time = (now - timedelta(days=31)).timestamp()
        new_time = (now - timedelta(days=10)).timestamp()

        # Mock os.walk to return a specific directory structure
        mock_walk.return_value = [
            ('/mock/path', [], ['file_old.txt', 'file_new.txt', 'file_ancient.log', 'file_recent.log'])
        ]

        # Mock os.path.getmtime for each file
        def mock_getmtime_side_effect(filepath):
            if 'file_old.txt' in filepath:
                return old_time
            if 'file_new.txt' in filepath:
                return new_time
            if 'file_ancient.log' in filepath:
                return old_time
            if 'file_recent.log' in filepath:
                return new_time
            return now.timestamp() # Default for any unexpected file

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test 1: Find files older than 30 days, no patterns
        files = find_files_to_clean(['/mock/path'], 30, [])
        self.assertIn('/mock/path/file_old.txt', files)
        self.assertIn('/mock/path/file_ancient.log', files)
        self.assertNotIn('/mock/path/file_new.txt', files)
        self.assertNotIn('/mock/path/file_recent.log', files)
        self.assertEqual(len(files), 2)

        # Test 2: Find files older than 30 days, with pattern '*.log'
        files = find_files_to_clean(['/mock/path'], 30, ['*.log'])
        self.assertNotIn('/mock/path/file_old.txt', files)
        self.assertIn('/mock/path/file_ancient.log', files)
        self.assertNotIn('/mock/path/file_new.txt', files)
        self.assertNotIn('/mock/path/file_recent.log', files)
        self.assertEqual(len(files), 1)

        # Test 3: Find files older than 5 days (should include more files)
        files = find_files_to_clean(['/mock/path'], 5, [])
        self.assertIn('/mock/path/file_old.txt', files)
        self.assertIn('/mock/path/file_new.txt', files)
        self.assertIn('/mock/path/file_ancient.log', files)
        self.assertIn('/mock/path/file_recent.log', files)
        self.assertEqual(len(files), 4)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.print') # Mock rationale: builtins.print is mocked to capture the warning message printed by the utility.
    def test_find_files_with_invalid_path(self, mock_print, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate an invalid directory.
        # os.walk and os.path.getmtime are mocked to simulate file discovery and modification times.
        # builtins.print is mocked to capture the warning message printed by the utility.

        mock_isdir.side_effect = lambda p: p == '/valid/path'

        mock_walk.return_value = [
            ('/valid/path', [], ['file.txt'])
        ]
        mock_getmtime.return_value = (datetime.now() - timedelta(days=31)).timestamp()

        files = find_files_to_clean(['/invalid/path', '/valid/path'], 30, [])
        self.assertIn('/valid/path/file.txt', files)
        self.assertEqual(len(files), 1)
        mock_print.assert_any_call("Warning: Path '/invalid/path' is not a valid directory. Skipping.")

    @patch('builtins.input', return_value='y')
    @patch('os.remove')
    @patch('builtins.print')
    def test_clean_files_deletion(self, mock_print, mock_remove, mock_input):
        # Mock rationale: builtins.input is mocked to simulate user confirmation.
        # os.remove is mocked to prevent actual file deletion during tests.
        # builtins.print is mocked to capture output and verify messages.

        files_to_delete = ['/mock/path/file1.txt', '/mock/path/file2.log']

        # Test 1: Actual deletion with confirmation
        clean_files(files_to_delete, dry_run=False, force=False)
        mock_remove.assert_any_call('/mock/path/file1.txt')
        mock_remove.assert_any_call('/mock/path/file2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_input.assert_called_once_with("\nAre you sure you want to delete these files? (y/N): ")
        mock_print.assert_any_call('Deleted: /mock/path/file1.txt')
        mock_print.assert_any_call('Deleted: /mock/path/file2.log')
        mock_print.assert_any_call('\nSuccessfully deleted 2 files.')

        mock_remove.reset_mock()
        mock_input.reset_mock()
        mock_print.reset_mock()

        # Test 2: Deletion with force flag
        clean_files(files_to_delete, dry_run=False, force=True)
        mock_remove.assert_any_call('/mock/path/file1.txt')
        mock_remove.assert_any_call('/mock/path/file2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_input.assert_not_called() # No confirmation needed with --force
        mock_print.assert_any_call('Deleted: /mock/path/file1.txt')
        mock_print.assert_any_call('Deleted: /mock/path/file2.log')
        mock_print.assert_any_call('\nSuccessfully deleted 2 files.')

    @patch('builtins.input', return_value='n')
    @patch('os.remove')
    @patch('builtins.print')
    def test_clean_files_aborted(self, mock_print, mock_remove, mock_input):
        # Mock rationale: builtins.input is mocked to simulate user declining confirmation.
        # os.remove is mocked to ensure it's not called.
        # builtins.print is mocked to capture output and verify messages.

        files_to_delete = ['/mock/path/file1.txt']
        clean_files(files_to_delete, dry_run=False, force=False)
        mock_remove.assert_not_called()
        mock_input.assert_called_once()
        mock_print.assert_any_call('Aborted. No files were deleted.')

    @patch('os.remove')
    @patch('builtins.print')
    def test_clean_files_dry_run(self, mock_print, mock_remove):
        # Mock rationale: os.remove is mocked to ensure it's not called during a dry run.
        # builtins.print is mocked to capture output and verify messages.

        files_to_delete = ['/mock/path/file1.txt', '/mock/path/file2.log']
        clean_files(files_to_delete, dry_run=True, force=False)
        mock_remove.assert_not_called()
        mock_print.assert_any_call('Found 2 files to consider for deletion:')
        mock_print.assert_any_call('  - /mock/path/file1.txt')
        mock_print.assert_any_call('  - /mock/path/file2.log')
        mock_print.assert_any_call('\nThis was a dry run. No files were deleted.')

    @patch('os.remove', side_effect=OSError('Permission denied'))
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_clean_files_error_on_delete(self, mock_print, mock_input, mock_remove):
        # Mock rationale: os.remove is mocked to simulate an OSError (e.g., permission denied).
        # builtins.input is mocked to simulate user confirmation.
        # builtins.print is mocked to capture output and verify error messages.

        files_to_delete = ['/mock/path/file_unwritable.txt']
        clean_files(files_to_delete, dry_run=False, force=False)
        mock_remove.assert_called_once_with('/mock/path/file_unwritable.txt')
        mock_print.assert_any_call("Error deleting file '/mock/path/file_unwritable.txt': Permission denied")
        mock_print.assert_any_call('\nSuccessfully deleted 0 files.')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.print') # Mock rationale: builtins.print is mocked to capture the error message printed by the utility.
    def test_find_files_os_error_on_getmtime(self, mock_print, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid directory.
        # os.walk is mocked to simulate directory traversal.
        # os.path.getmtime is mocked to raise an OSError for a specific file, simulating permission issues or corrupted metadata.
        # builtins.print is mocked to capture the error message printed by the utility.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file_ok.txt', 'file_error.txt'])
        ]

        now = datetime.now()
        old_time = (now - timedelta(days=31)).timestamp()

        def mock_getmtime_side_effect(filepath):
            if 'file_error.txt' in filepath:
                raise OSError('Cannot access file')
            return old_time

        mock_getmtime.side_effect = mock_getmtime_side_effect

        files = find_files_to_clean(['/mock/path'], 30, [])
        self.assertIn('/mock/path/file_ok.txt', files)
        self.assertNotIn('/mock/path/file_error.txt', files)
        self.assertEqual(len(files), 1)
        mock_print.assert_any_call("Error accessing file '/mock/path/file_error.txt': Cannot access file")


if __name__ == '__main__':
    unittest.main()
