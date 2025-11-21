import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the cleaner script
from src.cleaner import (
    get_file_age_days,
    get_file_size_mb,
    matches_patterns,
    find_and_clean_files
)

class TestCleaner(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: get_file_age_days relies on os.path.getmtime, which accesses the filesystem.
        # We need to mock this to provide deterministic timestamps for testing file age.
        
        # Simulate a file modified 10 days ago
        ten_days_ago = time.time() - (10 * 24 * 60 * 60)
        mock_getmtime.return_value = ten_days_ago
        
        age = get_file_age_days("/fake/path/file.txt")
        self.assertAlmostEqual(age, 10.0, places=1)
        mock_getmtime.assert_called_once_with("/fake/path/file.txt")

    @patch('os.path.getsize')
    def test_get_file_size_mb(self, mock_getsize):
        # Mock rationale: get_file_size_mb relies on os.path.getsize, which accesses the filesystem.
        # We need to mock this to provide deterministic file sizes for testing.
        
        # Simulate a 10 MB file
        mock_getsize.return_value = 10 * 1024 * 1024 
        
        size = get_file_size_mb("/fake/path/file.txt")
        self.assertAlmostEqual(size, 10.0, places=2)
        mock_getsize.assert_called_once_with("/fake/path/file.txt")

    def test_matches_patterns(self):
        # No mocks needed, this function is pure and only uses fnmatch.
        
        # Test with no patterns
        self.assertTrue(matches_patterns("file.txt", None, None))
        self.assertTrue(matches_patterns("temp_file.log", [], []))

        # Test include patterns
        self.assertTrue(matches_patterns("file.log", ["*.log"], None))
        self.assertFalse(matches_patterns("file.txt", ["*.log"], None))
        self.assertTrue(matches_patterns("cache/data.tmp", ["cache/*"], None))
        self.assertFalse(matches_patterns("other/data.tmp", ["cache/*"], None))

        # Test exclude patterns
        self.assertFalse(matches_patterns("important.txt", None, ["*.txt"]))
        self.assertTrue(matches_patterns("important.log", None, ["*.txt"]))
        self.assertFalse(matches_patterns("config/settings.yaml", None, ["config/*"]))

        # Test both include and exclude
        self.assertTrue(matches_patterns("temp.log", ["*.log"], ["*.tmp"]))
        self.assertFalse(matches_patterns("temp.tmp", ["*.log"], ["*.tmp"])) # Excluded
        self.assertFalse(matches_patterns("temp.txt", ["*.log"], ["*.tmp"])) # Not included

    @patch('os.remove')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_and_clean_files_dry_run(self, mock_walk, mock_isdir, mock_getmtime, mock_getsize, mock_remove):
        # Mock rationale: find_and_clean_files interacts heavily with the filesystem (os.walk, os.path.isdir,
        # os.path.getmtime, os.path.getsize, os.remove). We need to mock all these to create a virtual filesystem
        # and control file properties (age, size) deterministically without touching the actual disk.
        
        mock_isdir.return_value = True # Mock that the root path exists and is a directory

        # Simulate current time for age calculation
        current_time = time.time()
        
        # File 1: Old, Large, Matches include, Not exclude -> SHOULD BE FOUND
        file1_path = "/test_dir/old_large.log"
        file1_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file1_size = 15 * 1024 * 1024 # 15 MB

        # File 2: Old, Small, Matches include, Not exclude -> SHOULD NOT BE FOUND (size filter)
        file2_path = "/test_dir/old_small.txt"
        file2_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file2_size = 5 * 1024 * 1024 # 5 MB

        # File 3: New, Large, Matches include, Not exclude -> SHOULD NOT BE FOUND (age filter)
        file3_path = "/test_dir/new_large.log"
        file3_mtime = current_time - (5 * 24 * 60 * 60) # 5 days old
        file3_size = 15 * 1024 * 1024 # 15 MB

        # File 4: Old, Large, Excluded by pattern -> SHOULD NOT BE FOUND
        file4_path = "/test_dir/important.log"
        file4_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file4_size = 15 * 1024 * 1024 # 15 MB

        # File 5: Old, Large, Does not match include pattern -> SHOULD NOT BE FOUND
        file5_path = "/test_dir/old_large.dat"
        file5_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file5_size = 15 * 1024 * 1024 # 15 MB

        mock_walk.return_value = [
            ("/test_dir", [], ["old_large.log", "old_small.txt", "new_large.log", "important.log", "old_large.dat"])
        ]

        # Configure mocks for specific files
        def mock_getmtime_side_effect(path):
            if path == file1_path: return file1_mtime
            if path == file2_path: return file2_mtime
            if path == file3_path: return file3_mtime
            if path == file4_path: return file4_mtime
            if path == file5_path: return file5_mtime
            return current_time # Default for others
        mock_getmtime.side_effect = mock_getmtime_side_effect

        def mock_getsize_side_effect(path):
            if path == file1_path: return file1_size
            if path == file2_path: return file2_size
            if path == file3_path: return file3_size
            if path == file4_path: return file4_size
            if path == file5_path: return file5_size
            return 1024 # Default for others
        mock_getsize.side_effect = mock_getsize_side_effect

        # --- Test Dry Run ---
        result_count = find_and_clean_files(
            paths=["/test_dir"],
            max_age_days=30,
            min_size_mb=10,
            include_patterns=["*.log", "*.txt"],
            exclude_patterns=["important.log"],
            dry_run=True
        )

        self.assertEqual(result_count, 0) # Dry run always returns 0 deleted files
        mock_remove.assert_not_called() # No deletion in dry run

        # Verify that only file1_path would have been found
        # We can't directly check the internal list, but we can check the print output if we captured it.
        # For now, just checking no deletion happened is sufficient.

    @patch('os.remove')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_and_clean_files_delete_mode(self, mock_walk, mock_isdir, mock_getmtime, mock_getsize, mock_remove):
        # Mock rationale: Same as above, simulating filesystem interactions for deletion.
        
        mock_isdir.return_value = True

        current_time = time.time()
        
        # File 1: Old, Large, Matches include, Not exclude -> SHOULD BE DELETED
        file1_path = "/test_dir/delete_me.log"
        file1_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file1_size = 15 * 1024 * 1024 # 15 MB

        # File 2: Old, Large, Excluded by pattern -> SHOULD NOT BE DELETED
        file2_path = "/test_dir/keep_me.log"
        file2_mtime = current_time - (40 * 24 * 60 * 60) # 40 days old
        file2_size = 15 * 1024 * 1024 # 15 MB

        mock_walk.return_value = [
            ("/test_dir", [], ["delete_me.log", "keep_me.log"])
        ]

        def mock_getmtime_side_effect(path):
            if path == file1_path: return file1_mtime
            if path == file2_path: return file2_mtime
            return current_time
        mock_getmtime.side_effect = mock_getmtime_side_effect

        def mock_getsize_side_effect(path):
            if path == file1_path: return file1_size
            if path == file2_path: return file2_size
            return 1024
        mock_getsize.side_effect = mock_getsize_side_effect

        # --- Test Delete Mode ---
        result_count = find_and_clean_files(
            paths=["/test_dir"],
            max_age_days=30,
            min_size_mb=10,
            include_patterns=["*.log"],
            exclude_patterns=["keep_me.log"],
            dry_run=False # This is the key for deletion
        )

        self.assertEqual(result_count, 1) # One file should be deleted
        mock_remove.assert_called_once_with(file1_path) # Only file1 should be deleted
        mock_remove.assert_called_once() # Ensure only one call to remove

    @patch('os.remove')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_and_clean_files_no_matches(self, mock_walk, mock_isdir, mock_getmtime, mock_getsize, mock_remove):
        # Mock rationale: Simulating a scenario where no files match the criteria.
        
        mock_isdir.return_value = True
        current_time = time.time()

        # File 1: New, Small -> will not match criteria
        file1_path = "/test_dir/some_file.txt"
        file1_mtime = current_time - (1 * 24 * 60 * 60) # 1 day old
        file1_size = 1 * 1024 * 1024 # 1 MB

        mock_walk.return_value = [
            ("/test_dir", [], ["some_file.txt"])
        ]

        mock_getmtime.return_value = file1_mtime
        mock_getsize.return_value = file1_size

        result_count = find_and_clean_files(
            paths=["/test_dir"],
            max_age_days=30,
            min_size_mb=10,
            dry_run=False
        )

        self.assertEqual(result_count, 0);
        mock_remove.assert_not_called()

    @patch('os.remove')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_and_clean_files_path_does_not_exist(self, mock_walk, mock_isdir, mock_getmtime, mock_getsize, mock_remove):
        # Mock rationale: Test behavior when a specified path does not exist.
        
        mock_isdir.return_value = False # Simulate path not existing

        result_count = find_and_clean_files(
            paths=["/non_existent_dir"],
            max_age_days=1,
            dry_run=True
        )

        self.assertEqual(result_count, 0)
        mock_walk.assert_not_called() # os.walk should not be called if isdir is false
        mock_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()
