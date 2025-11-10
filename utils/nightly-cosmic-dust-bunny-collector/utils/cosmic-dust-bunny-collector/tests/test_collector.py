import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import functions from the utility
from src.collector import (
    get_file_age_days,
    is_file_old,
    is_file_empty,
    matches_pattern,
    scan_directory
)

class TestCosmicDustBunnyCollector(unittest.TestCase):

    # Mock rationale: os.path.getmtime returns the modification time of a file.
    # We need to control this value to simulate files of different ages for testing `is_file_old`.
    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Simulate a file modified 10 days ago
        mock_getmtime.return_value = time.time() - (10 * 24 * 60 * 60)
        self.assertAlmostEqual(get_file_age_days("dummy_path"), 10.0, places=5)

        # Simulate a file modified 0 days ago (current time)
        mock_getmtime.return_value = time.time()
        self.assertAlmostEqual(get_file_age_days("dummy_path"), 0.0, places=5)

    # Mock rationale: os.path.isfile checks if a path points to an existing regular file.
    # We need to control this to ensure `is_file_old` only processes actual files.
    # os.path.getmtime is also mocked to control the file's age.
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    def test_is_file_old(self, mock_getmtime, mock_isfile):
        # File is 40 days old, max_age is 30 -> should be old
        mock_getmtime.return_value = time.time() - (40 * 24 * 60 * 60)
        self.assertTrue(is_file_old("old_file.txt", 30))

        # File is 20 days old, max_age is 30 -> should not be old
        mock_getmtime.return_value = time.time() - (20 * 24 * 60 * 60)
        self.assertFalse(is_file_old("new_file.txt", 30))

        # Mock rationale: Test when path is not a file.
        mock_isfile.return_value = False
        self.assertFalse(is_file_old("not_a_file", 30))

    # Mock rationale: os.path.isfile checks if a path points to an existing regular file.
    # os.path.getsize returns the size of a file.
    # We need to control these to simulate empty and non-empty files.
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    def test_is_file_empty(self, mock_getsize, mock_isfile):
        # Empty file
        mock_getsize.return_value = 0
        self.assertTrue(is_file_empty("empty.txt"))

        # Non-empty file
        mock_getsize.return_value = 100
        self.assertFalse(is_file_empty("not_empty.txt"))

        # Mock rationale: Test when path is not a file.
        mock_isfile.return_value = False
        self.assertFalse(is_file_empty("not_a_file"))

    def test_matches_pattern(self):
        self.assertTrue(matches_pattern("temp.tmp", ["*.tmp"]))
        self.assertTrue(matches_pattern("backup.log", ["backup.*"]))
        self.assertTrue(matches_pattern("my_file.txt", ["my_file.txt"]))
        self.assertFalse(matches_pattern("image.jpg", ["*.tmp"]))
        self.assertFalse(matches_pattern("temp.tmp", [])) # No patterns
        self.assertFalse(matches_pattern("temp.tmp", None)) # None patterns

    # Mock rationale: os.path.isdir checks if a path points to an existing directory.
    # os.walk generates the file names in a directory tree.
    # os.path.join joins path components.
    # os.path.isfile checks if a path points to an existing regular file.
    # os.path.getmtime returns the modification time of a file.
    # os.path.getsize returns the size of a file.
    # We need to mock these to simulate a file system structure and file properties without actual disk I/O.
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join) # Use actual join for paths
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    def test_scan_directory(self, mock_getsize, mock_getmtime, mock_isfile, mock_join, mock_walk, mock_isdir):
        # Setup mock file system
        # root, dirs, files
        mock_walk.return_value = [
            ("/test_dir", [], ["old.log", "empty.txt", "temp.tmp", "recent.txt", "another.bak", "important.txt"]),
            ("/test_dir/subdir", [], ["sub_old.log", "sub_empty.txt"])
        ]

        # Define current time for age calculations
        current_time = time.time()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)
        ten_days_ago = current_time - (10 * 24 * 60 * 60)
        forty_days_ago = current_time - (40 * 24 * 60 * 60)

        # Mock file properties
        def mock_getmtime_side_effect(path):
            if "old.log" in path or "sub_old.log" in path:
                return forty_days_ago # Older than 30 days
            return ten_days_ago # Newer than 30 days

        def mock_getsize_side_effect(path):
            if "empty.txt" in path or "sub_empty.txt" in path:
                return 0
            return 100 # Non-empty

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.side_effect = mock_getsize_side_effect

        # Test case 1: Scan for old files (max_age=30)
        results = scan_directory("/test_dir", max_age_days=30)
        self.assertIn("/test_dir/old.log", results["old_files"])
        self.assertIn("/test_dir/subdir/sub_old.log", results["old_files"])
        self.assertEqual(len(results["old_files"]), 2)
        self.assertEqual(len(results["empty_files"]), 0)
        self.assertEqual(len(results["pattern_matches"]), 0)

        # Test case 2: Scan for empty files
        results = scan_directory("/test_dir", include_empty=True)
        self.assertIn("/test_dir/empty.txt", results["empty_files"])
        self.assertIn("/test_dir/subdir/sub_empty.txt", results["empty_files"])
        self.assertEqual(len(results["empty_files"]), 2)
        self.assertEqual(len(results["old_files"]), 0)
        self.assertEqual(len(results["pattern_matches"]), 0)

        # Test case 3: Scan for patterns
        results = scan_directory("/test_dir", patterns=["*.tmp", "*.bak"])
        self.assertIn("/test_dir/temp.tmp", results["pattern_matches"])
        self.assertIn("/test_dir/another.bak", results["pattern_matches"])
        self.assertEqual(len(results["pattern_matches"]), 2)
        self.assertEqual(len(results["old_files"]), 0)
        self.assertEqual(len(results["empty_files"]), 0)

        # Test case 4: Combined criteria
        results = scan_directory(
            "/test_dir",
            max_age_days=30,
            include_empty=True,
            patterns=["*.tmp", "*.bak"]
        )
        self.assertIn("/test_dir/old.log", results["old_files"])
        self.assertIn("/test_dir/subdir/sub_old.log", results["old_files"])
        self.assertIn("/test_dir/empty.txt", results["empty_files"])
        self.assertIn("/test_dir/subdir/sub_empty.txt", results["empty_files"])
        self.assertIn("/test_dir/temp.tmp", results["pattern_matches"])
        self.assertIn("/test_dir/another.bak", results["pattern_matches"])
        self.assertEqual(len(results["old_files"]), 2)
        self.assertEqual(len(results["empty_files"]), 2)
        self.assertEqual(len(results["pattern_matches"]), 2)

        # Test case 5: Directory not found
        mock_isdir.return_value = False
        results = scan_directory("/non_existent_dir")
        self.assertEqual(len(results["old_files"]), 0)
        self.assertEqual(len(results["empty_files"]), 0)
        self.assertEqual(len(results["pattern_matches"]), 0)
        mock_isdir.return_value = True # Reset for other tests if needed

if __name__ == '__main__':
    unittest.main()
