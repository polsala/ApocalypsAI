import unittest
from unittest.mock import patch, MagicMock
import os
import time
import datetime
import sys
from io import StringIO

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age calculations
        self.mock_current_time = time.time()
        self.mock_cutoff_time_30_days = self.mock_current_time - (30 * 24 * 60 * 60)
        self.mock_cutoff_time_7_days = self.mock_current_time - (7 * 24 * 60 * 60)

        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: os.walk is a system call that traverses the filesystem.
        # We need to mock its behavior to provide a deterministic directory structure
        # for testing the logic of identifying empty directories without actual disk access.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir'], ['file1.txt']),
            ('/root/dir1', ['subdir1'], ['file2.txt']),
            ('/root/dir1/subdir1', [], []), # This should be found as empty
            ('/root/dir2', [], ['file3.txt']),
            ('/root/empty_dir', [], []) # This should be found as empty
        ]

        expected_empty_dirs = ['/root/empty_dir', '/root/dir1/subdir1']
        found_empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertCountEqual(expected_empty_dirs, found_empty_dirs)

    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_stale_files(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk and os.path.getmtime are system calls.
        # We mock os.walk to control the file structure and os.path.getmtime
        # to provide deterministic modification times, allowing us to test
        # the 'staleness' logic without relying on actual file timestamps.

        # Simulate files:
        # - old_tmp.tmp: stale, matches pattern
        # - recent_log.log: not stale, matches pattern
        # - old_other.txt: stale, but doesn't match pattern
        # - recent_other.txt: not stale, doesn't match pattern
        # - old_cache_file.txt: stale, matches custom pattern

        mock_os_walk.return_value = [
            ('/root', [], ['old_tmp.tmp', 'recent_log.log', 'old_other.txt', 'recent_other.txt', 'old_cache_file.txt'])
        ]

        # Set specific modification times
        mock_getmtime.side_effect = lambda path: {
            '/root/old_tmp.tmp': self.mock_cutoff_time_30_days - 100, # Older than 30 days
            '/root/recent_log.log': self.mock_current_time - 100, # Newer than 30 days
            '/root/old_other.txt': self.mock_cutoff_time_30_days - 100,
            '/root/recent_other.txt': self.mock_current_time - 100,
            '/root/old_cache_file.txt': self.mock_cutoff_time_30_days - 100
        }.get(path, self.mock_current_time)

        # Test with default patterns and age
        expected_stale_default = ['/root/old_tmp.tmp']
        found_stale_default = sweeper.find_stale_files('/root', 30, ['.tmp', '.log'])
        self.assertCountEqual(expected_stale_default, found_stale_default)

        # Test with custom patterns and age
        expected_stale_custom = ['/root/old_tmp.tmp', '/root/old_cache_file.txt']
        found_stale_custom = sweeper.find_stale_files('/root', 30, ['.tmp', 'cache_*.txt'])
        self.assertCountEqual(expected_stale_custom, found_stale_custom)

        # Test with a shorter age (7 days)
        mock_getmtime.side_effect = lambda path: {
            '/root/old_tmp.tmp': self.mock_cutoff_time_7_days - 100, # Older than 7 days
            '/root/recent_log.log': self.mock_current_time - 100, # Newer than 7 days
        }.get(path, self.mock_current_time)
        expected_stale_7_days = ['/root/old_tmp.tmp']
        found_stale_7_days = sweeper.find_stale_files('/root', 7, ['.tmp', '.log'])
        self.assertCountEqual(expected_stale_7_days, found_stale_7_days)

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('builtins.input', return_value='y') # Mock user confirmation
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_mode_confirm(self, mock_parse_args, mock_os_walk, mock_getmtime, mock_input, mock_os_remove, mock_os_rmdir):
        # Mock rationale: We need to simulate the full execution of the main function
        # including argument parsing, file system traversal, and user interaction.
        # Mocks for os.walk, os.path.getmtime, os.remove, os.rmdir, and input
        # ensure that the test is deterministic, offline, and doesn't affect the actual filesystem.

        mock_parse_args.return_value = MagicMock(
            path='/mock_root',
            delete=True,
            age_days=30,
            patterns='.tmp,.log'
        )

        mock_os_walk.return_value = [
            ('/mock_root', ['empty_dir'], ['old_tmp.tmp', 'recent_log.log']),
            ('/mock_root/empty_dir', [], [])
        ]

        mock_getmtime.side_effect = lambda path: {
            '/mock_root/old_tmp.tmp': self.mock_cutoff_time_30_days - 100, # Stale
            '/mock_root/recent_log.log': self.mock_current_time - 100 # Not stale
        }.get(path, self.mock_current_time)

        # Mock os.path.isdir to return True for the mocked root path
        with patch('os.path.isdir', return_value=True):
            sweeper.main()

        mock_input.assert_called_once_with('Are you sure you want to sweep these dust bunnies away? (y/N): ')
        mock_os_remove.assert_called_once_with('/mock_root/old_tmp.tmp')
        mock_os_rmdir.assert_called_once_with('/mock_root/empty_dir')
        self.assertIn('Swept away 2 digital dust bunnies!', self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('builtins.input', return_value='n') # Mock user denial
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_mode_deny(self, mock_parse_args, mock_os_walk, mock_getmtime, mock_input, mock_os_remove, mock_os_rmdir):
        # Mock rationale: Similar to test_main_delete_mode_confirm, but specifically
        # to verify that no deletion occurs if the user denies the confirmation prompt.

        mock_parse_args.return_value = MagicMock(
            path='/mock_root',
            delete=True,
            age_days=30,
            patterns='.tmp,.log'
        )

        mock_os_walk.return_value = [
            ('/mock_root', ['empty_dir'], ['old_tmp.tmp']),
            ('/mock_root/empty_dir', [], [])
        ]

        mock_getmtime.side_effect = lambda path: {
            '/mock_root/old_tmp.tmp': self.mock_cutoff_time_30_days - 100
        }.get(path, self.mock_current_time)

        with patch('os.path.isdir', return_value=True):
            sweeper.main()

        mock_input.assert_called_once_with('Are you sure you want to sweep these dust bunnies away? (y/N): ')
        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()
        self.assertIn('Deletion cancelled. Dust bunnies live to see another day. 😔', self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_mode(self, mock_parse_args, mock_os_walk, mock_getmtime, mock_os_remove, mock_os_rmdir):
        # Mock rationale: Test the default listing behavior without deletion.
        # Mocks ensure deterministic output and no side effects on the filesystem.

        mock_parse_args.return_value = MagicMock(
            path='/mock_root',
            delete=False,
            age_days=30,
            patterns='.tmp,.log'
        )

        mock_os_walk.return_value = [
            ('/mock_root', ['empty_dir'], ['old_tmp.tmp', 'recent_log.log']),
            ('/mock_root/empty_dir', [], [])
        ]

        mock_getmtime.side_effect = lambda path: {
            '/mock_root/old_tmp.tmp': self.mock_cutoff_time_30_days - 100,
            '/mock_root/recent_log.log': self.mock_current_time - 100
        }.get(path, self.mock_current_time)

        with patch('os.path.isdir', return_value=True):
            sweeper.main()

        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()
        self.assertIn('Found 2 digital dust bunnies:', self.mock_stdout.getvalue())
        self.assertIn('[DIR] /mock_root/empty_dir', self.mock_stdout.getvalue())
        self.assertIn('[FILE] /mock_root/old_tmp.tmp', self.mock_stdout.getvalue())
        self.assertNotIn('[FILE] /mock_root/recent_log.log', self.mock_stdout.getvalue())
        self.assertIn("To delete these items, run with the '--delete' flag.", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_isdir):
        # Mock rationale: Test the error handling for an invalid path without actual filesystem checks.
        # os.path.isdir is mocked to simulate an invalid path.

        mock_parse_args.return_value = MagicMock(
            path='/non_existent_path',
            delete=False,
            age_days=30,
            patterns='.tmp,.log'
        )

        with self.assertRaises(SystemExit) as cm:
            sweeper.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Path '/non_existent_path' is not a valid directory.", self.mock_stdout.getvalue())

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_bunnies(self, mock_parse_args, mock_os_walk, mock_getmtime):
        # Mock rationale: Test the scenario where no dust bunnies are found.
        # Mocks ensure a clean, predictable state for this test.

        mock_parse_args.return_value = MagicMock(
            path='/mock_root',
            delete=False,
            age_days=30,
            patterns='.tmp,.log'
        )

        mock_os_walk.return_value = [
            ('/mock_root', ['non_empty_dir'], ['clean_file.txt']),
            ('/mock_root/non_empty_dir', [], ['another_clean_file.txt'])
        ]

        mock_getmtime.return_value = self.mock_current_time # All files are recent

        with patch('os.path.isdir', return_value=True):
            with self.assertRaises(SystemExit) as cm:
                sweeper.main()
            self.assertEqual(cm.exception.code, 0)
            self.assertIn('✨ All clear! No digital dust bunnies found. Your system is sparkling! ✨', self.mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
