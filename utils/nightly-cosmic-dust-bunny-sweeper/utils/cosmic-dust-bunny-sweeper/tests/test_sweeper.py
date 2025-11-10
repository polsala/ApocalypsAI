import unittest
from unittest.mock import patch, MagicMock
import os
import time
import datetime

# Import the function to be tested
from utils.cosmic-dust-bunny-sweeper.src.sweeper import sweep_dust_bunnies, get_file_age_days, is_directory_empty

class TestCosmicDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.mock_current_time = datetime.datetime(2023, 10, 26, 12, 0, 0)
        self.mock_current_timestamp = self.mock_current_time.timestamp()

    @patch('os.path.getmtime')
    @patch('time.time')
    def test_get_file_age_days(self, mock_time_time, mock_getmtime):
        # Mock rationale: `time.time()` and `os.path.getmtime()` are external system calls
        # that return non-deterministic values (current time, file modification time).
        # Patching them ensures tests are deterministic and offline.

        mock_time_time.return_value = self.mock_current_timestamp

        # File modified 10 days ago
        mock_getmtime.return_value = (self.mock_current_time - datetime.timedelta(days=10)).timestamp()
        self.assertAlmostEqual(get_file_age_days('/fake/path/file.txt'), 10.0, places=5)

        # File modified 0 days ago (current time)
        mock_getmtime.return_value = self.mock_current_timestamp
        self.assertAlmostEqual(get_file_age_days('/fake/path/file2.txt'), 0.0, places=5)

        # Test OSError (file not found)
        mock_getmtime.side_effect = OSError
        self.assertEqual(get_file_age_days('/nonexistent/file.txt'), float('inf'))

    @patch('os.listdir')
    def test_is_directory_empty(self, mock_listdir):
        # Mock rationale: `os.listdir()` is an external system call that interacts with the file system.
        # Patching it ensures tests are deterministic and offline, controlling directory contents.

        # Empty directory
        mock_listdir.return_value = []
        self.assertTrue(is_directory_empty('/fake/empty_dir'))

        # Non-empty directory
        mock_listdir.return_value = ['file.txt', 'subdir']
        self.assertFalse(is_directory_empty('/fake/non_empty_dir'))

        # Test OSError (directory not found)
        mock_listdir.side_effect = OSError
        self.assertFalse(is_directory_empty('/nonexistent/dir'))

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.walk')
    @patch('time.time')
    def test_sweep_dust_bunnies_dry_run(self, mock_time_time, mock_os_walk, mock_os_listdir, mock_os_getmtime, mock_os_path_isdir, mock_os_remove, mock_os_rmdir):
        # Mock rationale: `os.walk`, `os.path.isdir`, `os.path.getmtime`, `os.listdir`, `os.remove`, `os.rmdir`,
        # and `time.time()` are all external system calls interacting with the file system and current time.
        # Patching them ensures the test is deterministic, offline, and does not modify the actual file system.

        mock_time_time.return_value = self.mock_current_timestamp
        mock_os_path_isdir.return_value = True # Assume target_path is a valid directory

        # Define a mock file system structure and modification times
        # Structure: target_path/ (root)
        #   - old_file.txt (35 days old)
        #   - recent_file.txt (5 days old)
        #   - empty_dir/
        #   - non_empty_dir/
        #     - another_old_file.log (40 days old)
        #     - sub_empty_dir/

        # Mock os.walk to simulate directory traversal (topdown=False for both passes)
        mock_os_walk.side_effect = [
            # First pass for files
            [('/mock/target_path/non_empty_dir/sub_empty_dir', [], []), 
             ('/mock/target_path/non_empty_dir', ['sub_empty_dir'], ['another_old_file.log']),
             ('/mock/target_path/empty_dir', [], []),
             ('/mock/target_path', ['empty_dir', 'non_empty_dir'], ['old_file.txt', 'recent_file.txt'])],
            # Second pass for empty directories
            [('/mock/target_path/non_empty_dir/sub_empty_dir', [], []), 
             ('/mock/target_path/non_empty_dir', ['sub_empty_dir'], ['another_old_file.log']),
             ('/mock/target_path/empty_dir', [], []),
             ('/mock/target_path', ['empty_dir', 'non_empty_dir'], ['old_file.txt', 'recent_file.txt'])]
        ]

        # Mock os.path.getmtime for specific files
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return (self.mock_current_time - datetime.timedelta(days=35)).timestamp()
            elif 'recent_file.txt' in path:
                return (self.mock_current_time - datetime.timedelta(days=5)).timestamp()
            elif 'another_old_file.log' in path:
                return (self.mock_current_time - datetime.timedelta(days=40)).timestamp()
            return self.mock_current_timestamp # Default for directories or other files
        mock_os_getmtime.side_effect = mock_getmtime_side_effect

        # Mock os.listdir for checking empty directories
        def mock_listdir_side_effect(path):
            if path == '/mock/target_path/empty_dir':
                return []
            if path == '/mock/target_path/non_empty_dir/sub_empty_dir':
                return []
            return ['some_content'] # Default for non-empty dirs (e.g., /mock/target_path/non_empty_dir)
        mock_os_listdir.side_effect = mock_listdir_side_effect

        # Run in dry-run mode
        report = sweep_dust_bunnies('/mock/target_path', age_days=30, dry_run=True, verbose=False)

        self.assertEqual(report['found_files'], 2)
        self.assertEqual(report['removed_files'], 0) # Dry run, so nothing removed
        self.assertEqual(report['found_empty_dirs'], 2)
        self.assertEqual(report['removed_empty_dirs'], 0) # Dry run, so nothing removed

        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.walk')
    @patch('time.time')
    def test_sweep_dust_bunnies_actual_run(self, mock_time_time, mock_os_walk, mock_os_listdir, mock_os_getmtime, mock_os_path_isdir, mock_os_remove, mock_os_rmdir):
        # Mock rationale: Same as `test_sweep_dust_bunnies_dry_run`.
        # Ensures actual file system operations are mocked for deterministic and offline testing.

        mock_time_time.return_value = self.mock_current_timestamp
        mock_os_path_isdir.return_value = True

        # Define a mock file system structure and modification times
        # Structure: target_path/ (root)
        #   - old_file.txt (35 days old)
        #   - recent_file.txt (5 days old)
        #   - empty_dir/
        #   - non_empty_dir/
        #     - another_old_file.log (40 days old)
        #     - sub_empty_dir/

        # Mock os.walk to simulate directory traversal (topdown=False for both passes)
        mock_os_walk.side_effect = [
            # First pass for files
            [('/mock/target_path/non_empty_dir/sub_empty_dir', [], []), 
             ('/mock/target_path/non_empty_dir', ['sub_empty_dir'], ['another_old_file.log']),
             ('/mock/target_path/empty_dir', [], []),
             ('/mock/target_path', ['empty_dir', 'non_empty_dir'], ['old_file.txt', 'recent_file.txt'])],
            # Second pass for empty directories
            [('/mock/target_path/non_empty_dir/sub_empty_dir', [], []), 
             ('/mock/target_path/non_empty_dir', ['sub_empty_dir'], ['another_old_file.log']),
             ('/mock/target_path/empty_dir', [], []),
             ('/mock/target_path', ['empty_dir', 'non_empty_dir'], ['old_file.txt', 'recent_file.txt'])]
        ]

        # Mock os.path.getmtime for specific files
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return (self.mock_current_time - datetime.timedelta(days=35)).timestamp()
            elif 'recent_file.txt' in path:
                return (self.mock_current_time - datetime.timedelta(days=5)).timestamp()
            elif 'another_old_file.log' in path:
                return (self.mock_current_time - datetime.timedelta(days=40)).timestamp()
            return self.mock_current_timestamp # Default for directories or other files
        mock_os_getmtime.side_effect = mock_getmtime_side_effect

        # Mock os.listdir for checking empty directories
        def mock_listdir_side_effect(path):
            if path == '/mock/target_path/empty_dir':
                return []
            if path == '/mock/target_path/non_empty_dir/sub_empty_dir':
                return []
            return ['some_content'] # Default for non-empty dirs
        mock_os_listdir.side_effect = mock_listdir_side_effect

        # Run in actual run mode
        report = sweep_dust_bunnies('/mock/target_path', age_days=30, dry_run=False, verbose=False)

        self.assertEqual(report['found_files'], 2)
        self.assertEqual(report['removed_files'], 2) # Actual run, so files should be 'removed'
        self.assertEqual(report['found_empty_dirs'], 2)
        self.assertEqual(report['removed_empty_dirs'], 2) # Actual run, so dirs should be 'removed'

        # Assert that os.remove and os.rmdir were called for the correct items
        mock_os_remove.assert_any_call('/mock/target_path/old_file.txt')
        mock_os_remove.assert_any_call('/mock/target_path/non_empty_dir/another_old_file.log')
        self.assertEqual(mock_os_remove.call_count, 2)

        mock_os_rmdir.assert_any_call('/mock/target_path/empty_dir')
        mock_os_rmdir.assert_any_call('/mock/target_path/non_empty_dir/sub_empty_dir')
        self.assertEqual(mock_os_rmdir.call_count, 2)

    @patch('os.path.isdir')
    def test_sweep_dust_bunnies_invalid_path(self, mock_os_path_isdir):
        # Mock rationale: `os.path.isdir` is an external system call.
        # Patching it allows simulating an invalid target path without actual file system interaction.
        mock_os_path_isdir.return_value = False

        report = sweep_dust_bunnies('/nonexistent/path', age_days=10, dry_run=True)
        self.assertEqual(report['found_files'], 0)
        self.assertEqual(report['removed_files'], 0)
        self.assertEqual(report['found_empty_dirs'], 0)
        self.assertEqual(report['removed_empty_dirs'], 0)

if __name__ == '__main__':
    unittest.main()
