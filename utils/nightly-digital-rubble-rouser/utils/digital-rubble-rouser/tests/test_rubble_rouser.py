import unittest
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import patch

# Import the functions to be tested
from src.rubble_rouser import find_rubble, get_file_info

class TestRubbleRouser(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.now = datetime.now()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_mock_file(self, filename, size_bytes, mtime_offset_days):
        """Helper to create a file with specific size and modification time."""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'wb') as f:
            f.seek(size_bytes - 1)
            f.write(b'\0')
        
        # Set modification time
        mtime_dt = self.now - timedelta(days=mtime_offset_days)
        os.utime(filepath, (mtime_dt.timestamp(), mtime_dt.timestamp()))
        return filepath

    def test_get_file_info(self):
        filepath = self._create_mock_file("test_file.txt", 1024 * 1024, 10) # 1MB, 10 days old
        size_mb, last_modified_dt = get_file_info(filepath)
        self.assertAlmostEqual(size_mb, 1.0, places=2)
        self.assertIsInstance(last_modified_dt, datetime)
        # Check if the modification date is roughly 10 days ago (allowing for test execution time)
        self.assertLess(last_modified_dt, self.now - timedelta(days=9))
        self.assertGreater(last_modified_dt, self.now - timedelta(days=11))

    def test_find_rubble_by_age(self):
        # Create files: one old, one new
        old_file = self._create_mock_file("old_doc.txt", 100, 30) # 30 days old
        new_file = self._create_mock_file("new_report.pdf", 200, 5) # 5 days old

        # Search for files older than 10 days
        rubble = find_rubble(self.test_dir, max_age_days=10)
        self.assertEqual(len(rubble), 1)
        self.assertEqual(rubble[0][0], old_file)
        self.assertAlmostEqual(rubble[0][1], 100 / (1024 * 1024), places=5)

    def test_find_rubble_by_size(self):
        # Create files: one large, one small
        large_file = self._create_mock_file("big_data.zip", 50 * 1024 * 1024, 1) # 50MB
        small_file = self._create_mock_file("config.ini", 10, 1) # 10 bytes

        # Search for files larger than 20MB
        rubble = find_rubble(self.test_dir, min_size_mb=20)
        self.assertEqual(len(rubble), 1)
        self.assertEqual(rubble[0][0], large_file)
        self.assertAlmostEqual(rubble[0][1], 50.0, places=2)

    def test_find_rubble_by_age_and_size(self):
        # Create files:
        # 1. Old & Large (matches criteria)
        old_large = self._create_mock_file("archive.tar.gz", 60 * 1024 * 1024, 40) # 60MB, 40 days old
        # 2. Old & Small (doesn't match size)
        old_small = self._create_mock_file("log.txt", 100, 40) # 100 bytes, 40 days old
        # 3. New & Large (doesn't match age)
        new_large = self._create_mock_file("video.mp4", 70 * 1024 * 1024, 5) # 70MB, 5 days old
        # 4. New & Small (doesn't match either)
        new_small = self._create_mock_file("script.py", 50, 5) # 50 bytes, 5 days old

        # Search for files older than 30 days AND larger than 50MB
        rubble = find_rubble(self.test_dir, max_age_days=30, min_size_mb=50)
        self.assertEqual(len(rubble), 1)
        self.assertEqual(rubble[0][0], old_large)
        self.assertAlmostEqual(rubble[0][1], 60.0, places=2)

    def test_find_rubble_no_match(self):
        # Create files that don't match criteria
        self._create_mock_file("recent_small.txt", 100, 1)
        self._create_mock_file("recent_large.bin", 10 * 1024 * 1024, 2)

        rubble = find_rubble(self.test_dir, max_age_days=30, min_size_mb=20)
        self.assertEqual(len(rubble), 0)

    def test_find_rubble_recursive(self):
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)

        # File in root dir (matches criteria)
        root_file = self._create_mock_file("root_old.txt", 100, 30)
        # File in subdir (matches criteria)
        subdir_file_path = os.path.join(subdir, "subdir_old.txt")
        with open(subdir_file_path, 'wb') as f:
            f.seek(100 - 1)
            f.write(b'\0')
        mtime_dt = self.now - timedelta(days=30)
        os.utime(subdir_file_path, (mtime_dt.timestamp(), mtime_dt.timestamp()))

        # Non-recursive search (should only find root_file)
        rubble_non_recursive = find_rubble(self.test_dir, max_age_days=10, recursive=False)
        self.assertEqual(len(rubble_non_recursive), 1)
        self.assertEqual(rubble_non_recursive[0][0], root_file)

        # Recursive search (should find both)
        rubble_recursive = find_rubble(self.test_dir, max_age_days=10, recursive=True)
        self.assertEqual(len(rubble_recursive), 2)
        found_paths = {r[0] for r in rubble_recursive}
        self.assertIn(root_file, found_paths)
        self.assertIn(subdir_file_path, found_paths)

    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_get_file_info_os_error(self, mock_getmtime, mock_getsize):
        # Mock rationale: Test error handling for OS-level file access issues (e.g., permission denied, file not found).
        mock_getsize.side_effect = OSError("Permission denied")
        mock_getmtime.side_effect = OSError("Permission denied") # This might not be called if getsize fails first

        size, mtime = get_file_info("/nonexistent/path")
        self.assertIsNone(size)
        self.assertIsNone(mtime)

    def test_find_rubble_no_criteria_passed(self):
        # This test ensures that if no criteria are passed to find_rubble, it returns nothing.
        # The main function handles argument parsing and exits if no criteria are given, 
        # but find_rubble should also be robust if called directly without criteria.
        self._create_mock_file("any_file.txt", 100, 10)
        rubble = find_rubble(self.test_dir) # No age or size criteria
        self.assertEqual(len(rubble), 0)


if __name__ == '__main__':
    unittest.main()
