import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.tidy_upper import get_file_age_days, is_file_old, find_old_files, find_empty_dirs, clean_up, main

class TestTidyUpper(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the modification time of a file.
        # We need to control this value to simulate different file ages deterministically.
        current_time = time.time()
        mock_getmtime.return_value = current_time - (5 * 24 * 60 * 60) # 5 days ago
        self.assertAlmostEqual(get_file_age_days('dummy_file.txt'), 5.0, places=2)

        mock_getmtime.return_value = current_time - (30 * 24 * 60 * 60) # 30 days ago
        self.assertAlmostEqual(get_file_age_days('dummy_file.txt'), 30.0, places=2)

    @patch('src.tidy_upper.get_file_age_days')
    def test_is_file_old(self, mock_get_file_age_days):
        # Mock rationale: get_file_age_days is a dependency of is_file_old.
        # We mock it to control the age returned and test is_file_old in isolation.
        mock_get_file_age_days.return_value = 10
        self.assertTrue(is_file_old('file1.txt', 5)) # 10 > 5
        self.assertFalse(is_file_old('file2.txt', 15)) # 10 < 15
        self.assertFalse(is_file_old('file3.txt', 10)) # 10 is not > 10

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('src.tidy_upper.is_file_old')
    def test_find_old_files(self, mock_is_file_old, mock_isfile, mock_walk):
        # Mock rationale: os.walk simulates the directory traversal.
        # os.path.isfile ensures we only process actual files.
        # is_file_old determines if a file meets the age criteria.
        # We need to control these to simulate a file system and file ages.

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['fileA.txt', 'fileB.log']),
            ('/root/dir1', [], ['fileC.tmp']),
            ('/root/dir2', [], ['fileD.txt']),
        ]

        # All are files
        mock_isfile.return_value = True

        # Simulate which files are old
        def is_old_side_effect(filepath, age):
            return 'fileA.txt' in filepath or 'fileC.tmp' in filepath
        mock_is_file_old.side_effect = is_old_side_effect

        old_files = list(find_old_files('/root', 30))
        expected_files = [
            os.path.join('/root', 'fileA.txt'),
            os.path.join('/root/dir1', 'fileC.tmp')
        ]
        self.assertCountEqual(old_files, expected_files)

    @patch('os.walk')
    @patch('os.listdir')
    def test_find_empty_dirs(self, mock_listdir, mock_walk):
        # Mock rationale: os.walk simulates directory traversal, especially bottom-up.
        # os.listdir is used to confirm if a directory is truly empty at the time of check.
        # We control these to simulate various directory states.

        # Simulate a directory structure with some empty and some non-empty
        mock_walk.return_value = [
            ('/root/dir1/subdir1', [], []), # Empty
            ('/root/dir1', ['subdir1'], ['file.txt']), # Not empty (has file)
            ('/root/dir2', [], []), # Empty
            ('/root', ['dir1', 'dir2'], []), # Not empty (has subdirs)
        ]

        # Mock os.listdir to confirm emptiness
        def listdir_side_effect(path):
            if 'subdir1' in path or 'dir2' in path: # These are the truly empty ones
                return []
            return ['something'] # For non-empty dirs
        mock_listdir.side_effect = listdir_side_effect

        empty_dirs = list(find_empty_dirs('/root'))
        expected_dirs = [
            os.path.join('/root/dir1/subdir1'),
            os.path.join('/root/dir2')
        ]
        self.assertCountEqual(empty_dirs, expected_dirs)

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('src.tidy_upper.find_old_files', return_value=['/path/to/old_file.tmp'])
    @patch('src.tidy_upper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('src.tidy_upper.get_file_age_days', return_value=45)
    def test_clean_up_dry_run(self, mock_get_file_age_days, mock_find_empty_dirs, mock_find_old_files, mock_rmdir, mock_remove, mock_isdir, mock_print):
        # Mock rationale: We mock all file system operations and output functions.
        # os.path.isdir ensures the path is valid.
        # find_old_files and find_empty_dirs provide the lists of items to be processed.
        # os.remove and os.rmdir are mocked to ensure they are *not* called in dry-run mode.
        # builtins.print is mocked to capture output and verify messages.

        clean_up('/test_path', 30, dry_run=True, delete=False)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()
        mock_print.assert_any_call('  - /path/to/old_file.tmp (Age: 45.0 days)')
        mock_print.assert_any_call('  (Run with --delete to remove these 1 files.)')
        mock_print.assert_any_call('  - /path/to/empty_dir')
        mock_print.assert_any_call('  (Run with --delete to remove these 1 directories.)')
        mock_print.assert_any_call('\nCleanup complete. (Dry run)')

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('src.tidy_upper.find_old_files', return_value=['/path/to/old_file.tmp'])
    @patch('src.tidy_upper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('src.tidy_upper.get_file_age_days', return_value=45)
    def test_clean_up_delete(self, mock_get_file_age_days, mock_find_empty_dirs, mock_find_old_files, mock_rmdir, mock_remove, mock_isdir, mock_print):
        # Mock rationale: Similar to dry-run, but we expect os.remove and os.rmdir to be called.
        # We verify these calls and the output messages.

        clean_up('/test_path', 30, dry_run=False, delete=True)

        mock_remove.assert_called_once_with('/path/to/old_file.tmp')
        mock_rmdir.assert_called_once_with('/path/to/empty_dir')
        mock_print.assert_any_call('    [DELETED] /path/to/old_file.tmp')
        mock_print.assert_any_call('    [DELETED] /path/to/empty_dir')
        mock_print.assert_any_call('\nCleanup complete. ')

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=False)
    def test_clean_up_invalid_path(self, mock_isdir, mock_print):
        # Mock rationale: os.path.isdir is mocked to simulate an invalid path.
        # We expect an error message to be printed and no further operations.

        clean_up('/invalid_path', 30, dry_run=True, delete=False)
        mock_print.assert_called_once_with("Error: Path '/invalid_path' is not a valid directory.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tidy_upper.clean_up')
    def test_main_dry_run_default(self, mock_clean_up, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # clean_up is mocked to verify it's called with the correct parameters.

        mock_parse_args.return_value = MagicMock(path='./test', age=10, dry_run=False, delete=False)
        main()
        # When delete=False, clean_up's internal is_dry_run will be True
        mock_clean_up.assert_called_once_with('./test', 10, False, False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tidy_upper.clean_up')
    def test_main_delete_explicit(self, mock_clean_up, mock_parse_args):
        # Mock rationale: Same as above, but testing the --delete flag.

        mock_parse_args.return_value = MagicMock(path='./test', age=10, dry_run=False, delete=True)
        main()
        # When delete=True, clean_up's internal is_dry_run will be False
        mock_clean_up.assert_called_once_with('./test', 10, False, True)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tidy_upper.clean_up')
    def test_main_dry_run_explicit(self, mock_clean_up, mock_parse_args):
        # Mock rationale: Same as above, testing explicit --dry-run.

        mock_parse_args.return_value = MagicMock(path='./test', age=10, dry_run=True, delete=False)
        main()
        # When delete=False, clean_up's internal is_dry_run will be True
        mock_clean_up.assert_called_once_with('./test', 10, True, False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tidy_upper.clean_up')
    def test_main_dry_run_and_delete_conflict(self, mock_clean_up, mock_parse_args):
        # Mock rationale: Testing the scenario where both --dry-run and --delete are passed.
        # The logic in clean_up should prioritize --delete, making its internal is_dry_run False.

        mock_parse_args.return_value = MagicMock(path='./test', age=10, dry_run=True, delete=True)
        main()
        # When delete=True, clean_up's internal is_dry_run will be False, regardless of --dry-run flag
        mock_clean_up.assert_called_once_with('./test', 10, True, True)
