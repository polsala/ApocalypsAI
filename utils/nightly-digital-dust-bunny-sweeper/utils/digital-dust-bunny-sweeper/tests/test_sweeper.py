import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import get_file_age_days, is_empty_dir, find_dust_bunnies, delete_dust_bunnies

class TestDigitalDustBunnySweeper(unittest.TestCase):

    # Mock rationale: os.path.getmtime is a system call, needs to be mocked for deterministic tests.
    # We'll mock this to return specific timestamps for testing file age.
    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Simulate a file modified 10 days ago
        mock_getmtime.return_value = (time.time() - (10 * 24 * 60 * 60))
        self.assertAlmostEqual(get_file_age_days("dummy_file.txt"), 10, delta=0.1)

        # Simulate a file modified 0 days ago (current time)
        mock_getmtime.return_value = time.time()
        self.assertAlmostEqual(get_file_age_days("dummy_file.txt"), 0, delta=0.1)

        # Simulate a file that doesn't exist (or error)
        mock_getmtime.side_effect = OSError
        self.assertEqual(get_file_age_days("non_existent_file.txt"), -1)

    # Mock rationale: os.listdir is a system call, needs to be mocked for deterministic tests.
    # We'll mock this to return specific directory contents for testing empty directories.
    @patch('os.listdir')
    def test_is_empty_dir(self, mock_listdir):
        mock_listdir.return_value = []
        self.assertTrue(is_empty_dir("empty_dir"))

        mock_listdir.return_value = ["file.txt"]
        self.assertFalse(is_empty_dir("non_empty_dir"))

        mock_listdir.return_value = ["subdir/"]
        self.assertFalse(is_empty_dir("non_empty_dir_with_subdir"))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('src.sweeper.get_file_age_days') # Patch the internal function
    @patch('src.sweeper.is_empty_dir')     # Patch the internal function
    def test_find_dust_bunnies(self, mock_is_empty_dir, mock_get_file_age_days, mock_os_walk, mock_os_path_isdir):
        mock_os_path_isdir.return_value = True # Assume root_path is a directory

        # Mock rationale: os.walk is a system call, needs to be mocked for deterministic tests.
        # We'll mock this to simulate a file system structure without actual file system access.
        # Structure:
        # /root
        # ├── old_file.txt (100 days old)
        # ├── recent_file.txt (10 days old)
        # ├── empty_subdir/
        # └── non_empty_subdir/
        #     └── another_old_file.txt (120 days old)
        
        mock_os_walk.return_value = [
            ('/root/non_empty_subdir', [], ['another_old_file.txt']),
            ('/root/empty_subdir', [], []),
            ('/root', ['empty_subdir', 'non_empty_subdir'], ['old_file.txt', 'recent_file.txt'])
        ]

        # Mock rationale: get_file_age_days is an internal function, mocked for isolation.
        # We'll control the age returned for specific files.
        def mock_age_side_effect(filepath):
            if 'old_file.txt' in filepath:
                return 100
            elif 'recent_file.txt' in filepath:
                return 10
            elif 'another_old_file.txt' in filepath:
                return 120
            return 0 # Default for others
        mock_get_file_age_days.side_effect = mock_age_side_effect

        # Mock rationale: is_empty_dir is an internal function, mocked for isolation.
        # We'll control whether a directory is considered empty.
        def mock_empty_side_effect(path):
            return 'empty_subdir' in path
        mock_is_empty_dir.side_effect = mock_empty_side_effect

        # Test with age threshold 90 days
        old_files, empty_dirs = find_dust_bunnies('/root', 90)

        self.assertEqual(len(old_files), 2)
        self.assertIn(('/root/old_file.txt', 100), old_files)
        self.assertIn(('/root/non_empty_subdir/another_old_file.txt', 120), old_files)
        
        self.assertEqual(len(empty_dirs), 1)
        self.assertIn('/root/empty_subdir', empty_dirs)

        # Test with age threshold 110 days
        old_files_110, empty_dirs_110 = find_dust_bunnies('/root', 110)
        self.assertEqual(len(old_files_110), 1)
        self.assertIn(('/root/non_empty_subdir/another_old_file.txt', 120), old_files_110)
        self.assertEqual(len(empty_dirs_110), 1)
        self.assertIn('/root/empty_subdir', empty_dirs_110)

        # Test with invalid path
        mock_os_path_isdir.return_value = False
        old_files_invalid, empty_dirs_invalid = find_dust_bunnies('/invalid_path', 90)
        self.assertEqual(old_files_invalid, [])
        self.assertEqual(empty_dirs_invalid, [])
        mock_os_path_isdir.return_value = True # Reset for other tests

    @patch('os.remove')
    @patch('os.rmdir')
    def test_delete_dust_bunnies(self, mock_rmdir, mock_remove):
        old_files = [
            ("file1.txt", 100),
            ("file2.log", 150)
        ]
        empty_dirs = [
            "dir1",
            "dir2/subdir"
        ]

        deleted_count = delete_dust_bunnies(old_files, empty_dirs)

        self.assertEqual(deleted_count, 4) # 2 files + 2 dirs
        mock_remove.assert_any_call("file1.txt")
        mock_remove.assert_any_call("file2.log")
        mock_rmdir.assert_any_call("dir1")
        mock_rmdir.assert_any_call("dir2/subdir")
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_rmdir.call_count, 2)

        # Test with errors during deletion
        mock_remove.reset_mock()
        mock_rmdir.reset_mock()
        mock_remove.side_effect = [None, OSError("Permission denied")] # First file ok, second fails
        mock_rmdir.side_effect = [OSError("Dir not empty"), None] # First dir fails, second ok

        deleted_count_with_errors = delete_dust_bunnies(old_files, empty_dirs)
        self.assertEqual(deleted_count_with_errors, 2) # Only file1.txt and dir2/subdir should succeed
        mock_remove.assert_any_call("file1.txt")
        mock_remove.assert_any_call("file2.log")
        mock_rmdir.assert_any_call("dir1")
        mock_rmdir.assert_any_call("dir2/subdir")
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_rmdir.call_count, 2)


if __name__ == '__main__':
    unittest.main()
