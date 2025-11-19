import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the forager module
from src.forager import scan_directory, filter_by_age, delete_files, get_current_time_timestamp, get_file_modification_time

class TestForgottenFileForager(unittest.TestCase):

    # Define a fixed current time for deterministic tests
    FIXED_CURRENT_TIME = datetime(2023, 10, 26, 10, 0, 0)
    FIXED_CURRENT_TIMESTAMP = FIXED_CURRENT_TIME.timestamp()

    # Mock rationale: We need to control the current time for age calculations
    # to ensure deterministic test results regardless of when the tests are run.
    @patch('src.forager.time.time', return_value=FIXED_CURRENT_TIMESTAMP)
    def test_get_current_time_timestamp(self, mock_time):
        self.assertEqual(get_current_time_timestamp(), self.FIXED_CURRENT_TIMESTAMP)

    # Mock rationale: We need to simulate file modification times without actually
    # creating files or relying on the host filesystem, ensuring deterministic tests.
    @patch('src.forager.os.path.getmtime')
    def test_get_file_modification_time(self, mock_getmtime):
        mock_getmtime.return_value = self.FIXED_CURRENT_TIMESTAMP - (timedelta(days=10).total_seconds())
        self.assertEqual(get_file_modification_time('/fake/path/file.txt'), mock_getmtime.return_value)
        mock_getmtime.assert_called_once_with('/fake/path/file.txt')

    # Mock rationale: We need to simulate a directory structure without actually
    # creating directories and files on the filesystem, ensuring isolation and speed.
    @patch('src.forager.os.path.isdir', return_value=True)
    @patch('src.forager.os.walk')
    def test_scan_directory(self, mock_walk, mock_isdir):
        mock_walk.return_value = [
            ('/mock_root', ['subdir1'], ['file1.txt', 'file2.log']),
            ('/mock_root/subdir1', [], ['nested_file.tmp'])
        ]
        expected_files = [
            os.path.join('/mock_root', 'file1.txt'),
            os.path.join('/mock_root', 'file2.log'),
            os.path.join('/mock_root/subdir1', 'nested_file.tmp')
        ]
        self.assertCountEqual(scan_directory('/mock_root'), expected_files)
        mock_isdir.assert_called_once_with('/mock_root')
        mock_walk.assert_called_once_with('/mock_root')

    # Mock rationale: Test the error handling for invalid paths without needing
    # to create or check actual filesystem paths.
    @patch('src.forager.os.path.isdir', return_value=False)
    def test_scan_directory_invalid_path(self, mock_isdir):
        with patch('builtins.print') as mock_print:
            result = scan_directory('/nonexistent_path')
            self.assertEqual(result, [])
            mock_print.assert_called_once_with("Error: Path '/nonexistent_path' is not a valid directory.")

    # Mock rationale: We need to control both the current time and individual
    # file modification times to precisely test the age-based filtering logic.
    @patch('src.forager.get_current_time_timestamp', return_value=FIXED_CURRENT_TIMESTAMP)
    @patch('src.forager.get_file_modification_time')
    def test_filter_by_age(self, mock_getmtime, mock_current_time):
        # File 1: 40 days old (should be forgotten if cutoff is 30 days)
        file1_path = '/path/to/old_file.txt'
        file1_mod_time = self.FIXED_CURRENT_TIMESTAMP - timedelta(days=40).total_seconds()

        # File 2: 20 days old (should NOT be forgotten)
        file2_path = '/path/to/recent_file.log'
        file2_mod_time = self.FIXED_CURRENT_TIMESTAMP - timedelta(days=20).total_seconds()

        # File 3: 30 days old exactly (should NOT be forgotten, as it's 'older than')
        file3_path = '/path/to/exact_file.tmp'
        file3_mod_time = self.FIXED_CURRENT_TIMESTAMP - timedelta(days=30).total_seconds()

        # File 4: 30 days and 1 second old (should be forgotten)
        file4_path = '/path/to/just_old_file.bak'
        file4_mod_time = self.FIXED_CURRENT_TIMESTAMP - timedelta(days=30, seconds=1).total_seconds()

        mock_getmtime.side_effect = lambda p: {
            file1_path: file1_mod_time,
            file2_path: file2_mod_time,
            file3_path: file3_mod_time,
            file4_path: file4_mod_time,
        }.get(p, self.FIXED_CURRENT_TIMESTAMP) # Default to current if not specified

        files_to_check = [file1_path, file2_path, file3_path, file4_path]
        forgotten = filter_by_age(files_to_check, 30)

        self.assertCountEqual(forgotten, [file1_path, file4_path])
        self.assertEqual(mock_getmtime.call_count, len(files_to_check))
        mock_current_time.assert_called_once()

    # Mock rationale: We need to prevent actual file deletion during tests and
    # verify that `os.remove` would have been called with the correct arguments.
    # Also, we mock `input` to control user confirmation for deterministic tests.
    @patch('src.forager.os.remove')
    @patch('src.forager.get_file_modification_time', return_value=FIXED_CURRENT_TIMESTAMP - timedelta(days=60).total_seconds())
    @patch('builtins.print')
    @patch('builtins.input', return_value='yes') # Mock user input for confirmation
    def test_delete_files_with_confirmation(self, mock_input, mock_print, mock_getmtime, mock_remove):
        files_to_delete = ['/mock/file1.txt', '/mock/file2.log']
        delete_files(files_to_delete, dry_run=False, confirm=False)

        mock_print.assert_any_call("\nFound 2 forgotten files:")
        mock_print.assert_any_call("\nProceeding with deletion...")
        mock_remove.assert_any_call('/mock/file1.txt')
        mock_remove.assert_any_call('/mock/file2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_input.assert_called_once_with("\nDo you want to proceed with deleting these files? (yes/no): ")

    # Mock rationale: Verify that `os.remove` is not called during a dry run.
    @patch('src.forager.os.remove')
    @patch('src.forager.get_file_modification_time', return_value=FIXED_CURRENT_TIMESTAMP - timedelta(days=60).total_seconds())
    @patch('builtins.print')
    def test_delete_files_dry_run(self, mock_print, mock_getmtime, mock_remove):
        files_to_delete = ['/mock/file1.txt', '/mock/file2.log']
        delete_files(files_to_delete, dry_run=True, confirm=False)

        mock_print.assert_any_call("\nFound 2 forgotten files:")
        mock_print.assert_any_call("\nDry run complete. No files were actually deleted.")
        mock_remove.assert_not_called()

    # Mock rationale: Verify that `os.remove` is called when `confirm=True` without user input.
    @patch('src.forager.os.remove')
    @patch('src.forager.get_file_modification_time', return_value=FIXED_CURRENT_TIMESTAMP - timedelta(days=60).total_seconds())
    @patch('builtins.print')
    @patch('builtins.input') # Ensure input is NOT called
    def test_delete_files_auto_confirm(self, mock_input, mock_print, mock_getmtime, mock_remove):
        files_to_delete = ['/mock/file1.txt']
        delete_files(files_to_delete, dry_run=False, confirm=True)

        mock_print.assert_any_call("\nFound 1 forgotten file:")
        mock_print.assert_any_call("\nProceeding with deletion...")
        mock_remove.assert_called_once_with('/mock/file1.txt')
        mock_input.assert_not_called()

    # Mock rationale: Test cancellation logic when user input is 'no'.
    @patch('src.forager.os.remove')
    @patch('src.forager.get_file_modification_time', return_value=FIXED_CURRENT_TIMESTAMP - timedelta(days=60).total_seconds())
    @patch('builtins.print')
    @patch('builtins.input', return_value='no')
    def test_delete_files_cancellation(self, mock_input, mock_print, mock_getmtime, mock_remove):
        files_to_delete = ['/mock/file1.txt']
        delete_files(files_to_delete, dry_run=False, confirm=False)

        mock_print.assert_any_call("Deletion cancelled.")
        mock_remove.assert_not_called()
        mock_input.assert_called_once()

    # Mock rationale: Test behavior when no files are passed for deletion.
    @patch('builtins.print')
    def test_delete_files_no_files(self, mock_print):
        delete_files([], dry_run=False, confirm=False)
        mock_print.assert_called_once_with("No forgotten files found to delete.")

    # Mock rationale: Test error handling during file deletion.
    @patch('src.forager.os.remove', side_effect=OSError("Permission denied"))
    @patch('src.forager.get_file_modification_time', return_value=FIXED_CURRENT_TIMESTAMP - timedelta(days=60).total_seconds())
    @patch('builtins.print')
    @patch('builtins.input', return_value='yes')
    def test_delete_files_os_error(self, mock_input, mock_print, mock_getmtime, mock_remove):
        files_to_delete = ['/mock/unwritable_file.txt']
        delete_files(files_to_delete, dry_run=False, confirm=False)

        mock_remove.assert_called_once_with('/mock/unwritable_file.txt')
        mock_print.assert_any_call("  Error deleting '/mock/unwritable_file.txt': Permission denied")
        mock_print.assert_any_call("\nDeletion complete. Successfully deleted 0 files.")

    # Mock rationale: Test error handling when getting modification time fails.
    @patch('src.forager.get_file_modification_time', side_effect=OSError("File not found"))
    @patch('src.forager.get_current_time_timestamp', return_value=FIXED_CURRENT_TIMESTAMP)
    @patch('builtins.print')
    def test_filter_by_age_os_error(self, mock_print, mock_current_time, mock_getmtime):
        files_to_check = ['/path/to/missing_file.txt']
        forgotten = filter_by_age(files_to_check, 30)

        self.assertEqual(forgotten, [])
        mock_print.assert_called_once_with("Warning: Could not get modification time for '/path/to/missing_file.txt': File not found")


if __name__ == '__main__':
    unittest.main()
