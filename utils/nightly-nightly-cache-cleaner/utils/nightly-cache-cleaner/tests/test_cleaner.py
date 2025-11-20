import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the cleaner module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cleaner import find_old_files, delete_files

class TestCleaner(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    def test_find_old_files_no_old_files(self, mock_isdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory structure without needing actual files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Mock rationale: Make all files appear recent.
        mock_getmtime.side_effect = [time.time(), time.time()]
        mock_isdir.return_value = True

        old_files = find_old_files('/test_dir', 30)
        self.assertEqual(len(old_files), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    def test_find_old_files_with_old_files(self, mock_isdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory structure with some old files.
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_file1.txt', 'recent_file.log']),
            ('/test_dir/subdir', [], ['old_file2.tmp'])
        ]

        # Mock rationale: Set specific modification times for files.
        # old_file1.txt (40 days old)
        # recent_file.log (10 days old)
        # old_file2.tmp (60 days old)
        now = datetime.now()
        mock_getmtime.side_effect = [
            (now - timedelta(days=40)).timestamp(),
            (now - timedelta(days=10)).timestamp(),
            (now - timedelta(days=60)).timestamp(),
        ]
        mock_isdir.return_value = True

        old_files = find_old_files('/test_dir', 30)
        self.assertEqual(len(old_files), 2)
        self.assertIn('/test_dir/old_file1.txt', old_files)
        self.assertIn('/test_dir/subdir/old_file2.tmp', old_files)
        self.assertNotIn('/test_dir/recent_file.log', old_files)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    def test_find_old_files_os_error(self, mock_isdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a file system error when accessing a file.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied")
        mock_isdir.return_value = True

        old_files = find_old_files('/test_dir', 30)
        self.assertEqual(len(old_files), 0) # No files should be added if an error occurs

    @patch('os.remove')
    def test_delete_files_success(self, mock_remove):
        # Mock rationale: Prevent actual file deletion during tests.
        files_to_delete = ['/path/to/file1.txt', '/path/to/file2.log']
        delete_files(files_to_delete)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/file1.txt')
        mock_remove.assert_any_call('/path/to/file2.log')

    @patch('os.remove')
    def test_delete_files_with_error(self, mock_remove):
        # Mock rationale: Simulate an error during file deletion.
        files_to_delete = ['/path/to/file1.txt', '/path/to/file2.log']
        mock_remove.side_effect = [None, OSError("Permission denied")]

        delete_files(files_to_delete)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/file1.txt')
        mock_remove.assert_any_call('/path/to/file2.log')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('cleaner.find_old_files')
    @patch('cleaner.delete_files')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_dry_run_no_files(self, mock_print, mock_isdir, mock_delete_files, mock_find_old_files, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/test_dir', days=30, delete=False)
        mock_isdir.return_value = True
        mock_find_old_files.return_value = []

        with self.assertRaises(SystemExit) as cm:
            from cleaner import main
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_find_old_files.assert_called_once_with('/test_dir', 30)
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call('No old files found. Your digital landscape is pristine!')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('cleaner.find_old_files')
    @patch('cleaner.delete_files')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_dry_run_with_files(self, mock_print, mock_isdir, mock_delete_files, mock_find_old_files, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/test_dir', days=30, delete=False)
        mock_isdir.return_value = True
        mock_find_old_files.return_value = ['/test_dir/old_file.txt']

        from cleaner import main
        main()
        mock_find_old_files.assert_called_once_with('/test_dir', 30)
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call('This was a dry run. No files were deleted. Use --delete to remove them.')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('cleaner.find_old_files')
    @patch('cleaner.delete_files')
    @patch('os.path.isdir') # Mock rationale: Prevent actual file system checks for directory existence.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_delete_with_files(self, mock_print, mock_isdir, mock_delete_files, mock_find_old_files, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/test_dir', days=30, delete=True)
        mock_isdir.return_value = True
        mock_find_old_files.return_value = ['/test_dir/old_file.txt']

        from cleaner import main
        main()
        mock_find_old_files.assert_called_once_with('/test_dir', 30)
        mock_delete_files.assert_called_once_with(['/test_dir/old_file.txt'])
        mock_print.assert_any_call('Deletion complete. Disk space reclaimed!')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir') # Mock rationale: Simulate a non-existent directory.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_invalid_path(self, mock_print, mock_isdir, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/non_existent_dir', days=30, delete=False)
        mock_isdir.return_value = False

        with self.assertRaises(SystemExit) as cm:
            from cleaner import main
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Directory '/non_existent_dir' does not exist or is not a directory.")
