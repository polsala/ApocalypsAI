import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions directly from the module
from src.sweeper import find_empty_directories, find_stale_files, main, get_current_timestamp

class TestDigitalDustBunnySweeper(unittest.TestCase):

    # Mock rationale: We need to control the 'current time' for deterministic stale file detection.
    # This ensures tests don't fail based on when they are run.
    MOCK_CURRENT_TIME = datetime(2023, 10, 26, 10, 0, 0) # A fixed point in time
    MOCK_CURRENT_TIMESTAMP = MOCK_CURRENT_TIME.timestamp()

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    def test_find_empty_directories(self, mock_get_current_timestamp):
        # Mock rationale: Simulate a file system structure without actual disk I/O.
        # This makes tests fast, deterministic, and isolated from the host system.
        mock_os_walk_data = [
            ('/mock/root', ['dir1', 'dir2', 'empty_dir', 'another_empty'], ['file1.txt']),
            ('/mock/root/dir1', [], ['subfile1.txt']),
            ('/mock/root/dir2', ['subdir_empty'], ['subfile2.txt']),
            ('/mock/root/empty_dir', [], []),
            ('/mock/root/dir2/subdir_empty', [], []),
            ('/mock/root/another_empty', [], []),
        ]

        with patch('os.walk', return_value=mock_os_walk_data):
            empty_dirs = find_empty_directories('/mock/root', self.MOCK_CURRENT_TIMESTAMP)
            # Expecting empty_dir, subdir_empty, another_empty. Sorted by length descending.
            self.assertEqual(len(empty_dirs), 3)
            self.assertIn('/mock/root/empty_dir', empty_dirs)
            self.assertIn('/mock/root/dir2/subdir_empty', empty_dirs)
            self.assertIn('/mock/root/another_empty', empty_dirs)
            # Check sorting for deletion order (longest path first)
            self.assertEqual(empty_dirs[0], '/mock/root/dir2/subdir_empty')
            self.assertEqual(empty_dirs[1], '/mock/root/empty_dir')
            self.assertEqual(empty_dirs[2], '/mock/root/another_empty')

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    def test_find_stale_files(self, mock_get_current_timestamp):
        # Mock rationale: Simulate file modification times and existence without actual disk I/O.
        # This allows precise control over which files are considered 'stale'.
        stale_cutoff_timestamp = self.MOCK_CURRENT_TIMESTAMP - (30 * 24 * 60 * 60)

        # Simulate os.walk output
        mock_os_walk_data = [
            ('/mock/root', [], ['old_file.log', 'recent_file.txt', 'non_existent.tmp']),
            ('/mock/root/subdir', [], ['very_old.bak']),
        ]

        # Simulate os.path.getmtime and os.path.exists
        def mock_getmtime(path):
            if path == '/mock/root/old_file.log':
                return stale_cutoff_timestamp - 100 # Older than cutoff
            elif path == '/mock/root/recent_file.txt':
                return self.MOCK_CURRENT_TIMESTAMP - 100 # Newer than cutoff
            elif path == '/mock/root/subdir/very_old.bak':
                return stale_cutoff_timestamp - (60 * 24 * 60 * 60) # Much older
            return self.MOCK_CURRENT_TIMESTAMP # Default for others

        def mock_exists(path):
            return path != '/mock/root/non_existent.tmp' # Simulate a file that doesn't exist

        with patch('os.walk', return_value=mock_os_walk_data),
             patch('os.path.getmtime', side_effect=mock_getmtime),
             patch('os.path.exists', side_effect=mock_exists):

            stale_files = find_stale_files('/mock/root', 30, self.MOCK_CURRENT_TIMESTAMP)
            self.assertEqual(len(stale_files), 2)
            self.assertIn('/mock/root/old_file.log', stale_files)
            self.assertIn('/mock/root/subdir/very_old.bak', stale_files)
            self.assertNotIn('/mock/root/recent_file.txt', stale_files)
            self.assertNotIn('/mock/root/non_existent.tmp', stale_files)

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', return_value=[]) # Mock rationale: Ensure os.listdir returns empty for rmdir check
    @patch('builtins.print') # Mock rationale: Capture print output for assertion, avoid console spam
    def test_main_dry_run(self, mock_print, mock_listdir, mock_rmdir, mock_remove, mock_isdir, mock_get_current_timestamp):
        # Mock rationale: Simulate a full run of the main function without actual file system changes.
        # This involves mocking os.walk, os.path.getmtime, os.path.exists, and the deletion functions.
        # Mocking print allows verifying the output messages.

        # Simulate os.walk for empty dirs and stale files
        mock_os_walk_data = [
            ('/mock/root', ['empty_dir'], ['old_file.log', 'recent_file.txt']),
            ('/mock/root/empty_dir', [], []),
        ]

        # Simulate os.path.getmtime
        stale_cutoff_timestamp = self.MOCK_CURRENT_TIMESTAMP - (30 * 24 * 60 * 60)
        def mock_getmtime(path):
            if path == '/mock/root/old_file.log':
                return stale_cutoff_timestamp - 100
            return self.MOCK_CURRENT_TIMESTAMP

        with patch('os.walk', return_value=mock_os_walk_data),
             patch('os.path.getmtime', side_effect=mock_getmtime),
             patch('os.path.exists', return_value=True),
             patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path=['/mock/root'], stale_days=30, dry_run=True, clean=False
             )):

            main()

            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called()
            mock_print.assert_any_call('  Found 1 empty directories:')
            mock_print.assert_any_call('    - /mock/root/empty_dir')
            mock_print.assert_any_call('  Found 1 stale files:')
            mock_print.assert_any_call('    - /mock/root/old_file.log')
            mock_print.assert_any_call('--- Dry Run Complete ---')
            mock_print.assert_any_call('Would delete 1 stale files and 1 empty directories.')

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', return_value=[]) # Mock rationale: Ensure os.listdir returns empty for rmdir check
    @patch('builtins.print') # Mock rationale: Capture print output for assertion, avoid console spam
    def test_main_clean_mode(self, mock_print, mock_listdir, mock_rmdir, mock_remove, mock_isdir, mock_get_current_timestamp):
        # Mock rationale: Simulate a full run of the main function in 'clean' mode, verifying deletion calls.
        # This ensures the utility attempts to remove the correct files/directories.

        # Simulate os.walk for empty dirs and stale files
        mock_os_walk_data = [
            ('/mock/root', ['empty_dir'], ['old_file.log']),
            ('/mock/root/empty_dir', [], []),
        ]

        # Simulate os.path.getmtime
        stale_cutoff_timestamp = self.MOCK_CURRENT_TIMESTAMP - (30 * 24 * 60 * 60)
        def mock_getmtime(path):
            if path == '/mock/root/old_file.log':
                return stale_cutoff_timestamp - 100
            return self.MOCK_CURRENT_TIMESTAMP

        with patch('os.walk', return_value=mock_os_walk_data),
             patch('os.path.getmtime', side_effect=mock_getmtime),
             patch('os.path.exists', return_value=True),
             patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path=['/mock/root'], stale_days=30, dry_run=False, clean=True
             )):

            main()

            mock_remove.assert_called_once_with('/mock/root/old_file.log')
            mock_rmdir.assert_called_once_with('/mock/root/empty_dir')
            mock_print.assert_any_call('  Deleted stale file: /mock/root/old_file.log')
            mock_print.assert_any_call('  Deleted empty directory: /mock/root/empty_dir')
            mock_print.assert_any_call('  Successfully deleted 1 stale files.')
            mock_print.assert_any_call('  Successfully deleted 1 empty directories.')

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', return_value=['file.txt']) # Mock rationale: Simulate a directory that is NOT empty when rmdir is called
    @patch('builtins.print')
    def test_main_clean_mode_dir_not_empty_after_scan(self, mock_print, mock_listdir, mock_rmdir, mock_remove, mock_isdir, mock_get_current_timestamp):
        # Mock rationale: Test the scenario where an empty directory found during scan becomes non-empty before deletion.
        # This ensures robustness against race conditions or external changes.

        mock_os_walk_data = [
            ('/mock/root', ['empty_dir'], []),
            ('/mock/root/empty_dir', [], []),
        ]

        with patch('os.walk', return_value=mock_os_walk_data),
             patch('os.path.getmtime', return_value=self.MOCK_CURRENT_TIMESTAMP),
             patch('os.path.exists', return_value=True),
             patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path=['/mock/root'], stale_days=30, dry_run=False, clean=True
             )):

            main()

            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called() # Should not be called because listdir returns non-empty
            mock_print.assert_any_call('  Skipped non-empty directory (after scanning): /mock/root/empty_dir')

    @patch('src.sweeper.get_current_timestamp', return_value=MOCK_CURRENT_TIMESTAMP)
    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate an invalid path argument.
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_isdir, mock_get_current_timestamp):
        # Mock rationale: Test how the utility handles an invalid (non-directory) path provided as input.

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path=['/invalid/path'], stale_days=30, dry_run=True, clean=False
             )):
            main()
            mock_print.assert_any_call("Error: Path '/invalid/path' is not a valid directory. Skipping.")

if __name__ == '__main__':
    unittest.main()
