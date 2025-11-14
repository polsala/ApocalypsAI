import unittest
import os
import time
import shutil
from unittest.mock import patch, MagicMock

# Import the function to be tested
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "./temp_test_dust_dir"
        os.makedirs(self.test_dir, exist_ok=True)

        # Define some timestamps for test files
        self.now = time.time()
        self.one_day_ago = self.now - (1 * 24 * 60 * 60)
        self.ten_days_ago = self.now - (10 * 24 * 60 * 60)
        self.forty_days_ago = self.now - (40 * 24 * 60 * 60)

        # Create dummy files with specific modification times
        self.old_file_1 = os.path.join(self.test_dir, "old_log_1.txt")
        self.old_file_2 = os.path.join(self.test_dir, "subdir", "old_data.bak")
        self.new_file_1 = os.path.join(self.test_dir, "new_report.pdf")
        self.new_file_2 = os.path.join(self.test_dir, "subdir", "current_config.ini")

        os.makedirs(os.path.join(self.test_dir, "subdir"), exist_ok=True)

        with open(self.old_file_1, "w") as f: f.write("old content")
        os.utime(self.old_file_1, (self.forty_days_ago, self.forty_days_ago))

        with open(self.old_file_2, "w") as f: f.write("more old content")
        os.utime(self.old_file_2, (self.forty_days_ago, self.forty_days_ago))

        with open(self.new_file_1, "w") as f: f.write("new content")
        os.utime(self.new_file_1, (self.one_day_ago, self.one_day_ago))

        with open(self.new_file_2, "w") as f: f.write("current content")
        os.utime(self.new_file_2, (self.ten_days_ago, self.ten_days_ago))

    def tearDown(self):
        # Clean up the temporary directory after tests
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('time.time')
    @patch('os.path.getmtime')
    def test_collect_dust_dry_run(self, mock_getmtime, mock_time):
        # Mock rationale: time.time() is mocked to ensure a consistent 'current' time for age calculations.
        # os.path.getmtime() is mocked to provide deterministic modification times for test files,
        # preventing tests from failing due to actual file system timestamps changing over time.
        mock_time.return_value = self.now # Set a fixed 'current' time

        # Map file paths to their mocked modification times
        mtime_map = {
            self.old_file_1: self.forty_days_ago,
            self.old_file_2: self.forty_days_ago,
            self.new_file_1: self.one_day_ago,
            self.new_file_2: self.ten_days_ago,
        }
        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now) # Default to now if not in map

        # Test with an age threshold that should catch old files (e.g., 30 days)
        identified_files = collect_dust(self.test_dir, age_threshold_days=30, dry_run=True)

        # Assert that the correct old files were identified
        self.assertIn(self.old_file_1, identified_files)
        self.assertIn(self.old_file_2, identified_files)
        self.assertNotIn(self.new_file_1, identified_files)
        self.assertNotIn(self.new_file_2, identified_files)
        self.assertEqual(len(identified_files), 2)

        # Verify no deletion occurred in dry run (files should still exist in the temporary directory)
        self.assertTrue(os.path.exists(self.old_file_1))
        self.assertTrue(os.path.exists(self.old_file_2))

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.remove')
    def test_collect_dust_delete_mode(self, mock_remove, mock_getmtime, mock_time):
        # Mock rationale: time.time() and os.path.getmtime() are mocked for deterministic age calculations.
        # os.remove() is mocked to prevent actual file deletion during tests, allowing verification
        # that the function *would have* called os.remove for the correct files.
        mock_time.return_value = self.now

        mtime_map = {
            self.old_file_1: self.forty_days_ago,
            self.old_file_2: self.forty_days_ago,
            self.new_file_1: self.one_day_ago,
            self.new_file_2: self.ten_days_ago,
        }
        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now)

        # Test with deletion enabled
        identified_files = collect_dust(self.test_dir, age_threshold_days=30, dry_run=False)

        # Assert that the correct old files were identified (and theoretically deleted)
        self.assertIn(self.old_file_1, identified_files)
        self.assertIn(self.old_file_2, identified_files)
        self.assertNotIn(self.new_file_1, identified_files)
        self.assertNotIn(self.new_file_2, identified_files)
        self.assertEqual(len(identified_files), 2)

        # Verify os.remove was called for the old files
        mock_remove.assert_any_call(self.old_file_1)
        mock_remove.assert_any_call(self.old_file_2)
        self.assertEqual(mock_remove.call_count, 2)

    @patch('time.time')
    @patch('os.path.getmtime')
    def test_collect_dust_no_old_files(self, mock_getmtime, mock_time):
        # Mock rationale: time.time() and os.path.getmtime() are mocked for deterministic age calculations.
        mock_time.return_value = self.now

        mtime_map = {
            self.old_file_1: self.one_day_ago, # Make this file 'new'
            self.old_file_2: self.ten_days_ago, # Make this file 'new'
            self.new_file_1: self.one_day_ago,
            self.new_file_2: self.ten_days_ago,
        }
        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now)

        # Test with an age threshold that should not catch any files (e.g., 30 days, but all files are newer)
        identified_files = collect_dust(self.test_dir, age_threshold_days=30, dry_run=True)

        self.assertEqual(len(identified_files), 0)

    @patch('time.time')
    @patch('os.path.getmtime')
    def test_collect_dust_higher_threshold(self, mock_getmtime, mock_time):
        # Mock rationale: time.time() and os.path.getmtime() are mocked for deterministic age calculations.
        mock_time.return_value = self.now

        mtime_map = {
            self.old_file_1: self.forty_days_ago,
            self.old_file_2: self.forty_days_ago,
            self.new_file_1: self.one_day_ago,
            self.new_file_2: self.ten_days_ago,
        }
        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now)

        # Test with a very high age threshold (e.g., 100 days) that should catch no files
        identified_files = collect_dust(self.test_dir, age_threshold_days=100, dry_run=True)

        self.assertEqual(len(identified_files), 0)

    def test_collect_dust_invalid_directory(self):
        # Test with a non-existent directory
        identified_files = collect_dust("./non_existent_dir", age_threshold_days=30, dry_run=True)
        self.assertEqual(len(identified_files), 0)


if __name__ == '__main__':
    unittest.main()
