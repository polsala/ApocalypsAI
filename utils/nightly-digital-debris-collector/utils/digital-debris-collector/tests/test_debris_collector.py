import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.debris_collector import get_file_stats, is_file_old, is_file_empty, collect_debris

class TestDebrisCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed "current time" for deterministic tests
        self.mock_current_time_timestamp = datetime(2023, 10, 26, 10, 0, 0).timestamp()
        self.days_threshold = 30 # 30 days for testing

    @patch('os.stat')
    def test_get_file_stats_success(self, mock_stat):
        # Mock rationale: os.stat is a system call, needs to be mocked for deterministic tests.
        mock_stat_result = MagicMock()
        mock_stat_result.st_atime = self.mock_current_time_timestamp - (10 * 24 * 3600) # 10 days ago
        mock_stat_result.st_mtime = self.mock_current_time_timestamp - (5 * 24 * 3600)  # 5 days ago
        mock_stat_result.st_size = 1024 # 1KB
        mock_stat.return_value = mock_stat_result

        atime, mtime, size = get_file_stats("/fake/path/file.txt")
        self.assertEqual(atime, mock_stat_result.st_atime)
        self.assertEqual(mtime, mock_stat_result.st_mtime)
        self.assertEqual(size, mock_stat_result.st_size)
        mock_stat.assert_called_once_with("/fake/path/file.txt")

    @patch('os.stat', side_effect=OSError("No such file"))
    def test_get_file_stats_failure(self, mock_stat):
        # Mock rationale: os.stat can fail if file doesn't exist, needs to be mocked.
        atime, mtime, size = get_file_stats("/nonexistent/file.txt")
        self.assertIsNone(atime)
        self.assertIsNone(mtime)
        self.assertIsNone(size)
        mock_stat.assert_called_once_with("/nonexistent/file.txt")

    @patch('src.debris_collector.get_file_stats')
    def test_is_file_old(self, mock_get_file_stats):
        # Mock rationale: get_file_stats is an internal dependency, mock it to isolate is_file_old.
        
        # Case 1: File is old (accessed and modified > threshold)
        old_atime = self.mock_current_time_timestamp - (self.days_threshold + 5) * 24 * 3600
        old_mtime = self.mock_current_time_timestamp - (self.days_threshold + 10) * 24 * 3600
        mock_get_file_stats.return_value = (old_atime, old_mtime, 100)
        is_accessed_old, is_modified_old = is_file_old("/fake/old_file.txt", self.days_threshold, self.mock_current_time_timestamp)
        self.assertTrue(is_accessed_old)
        self.assertTrue(is_modified_old)

        # Case 2: File is recent (accessed and modified < threshold)
        recent_atime = self.mock_current_time_timestamp - (self.days_threshold - 5) * 24 * 3600
        recent_mtime = self.mock_current_time_timestamp - (self.days_threshold - 10) * 24 * 3600
        mock_get_file_stats.return_value = (recent_atime, recent_mtime, 100)
        is_accessed_old, is_modified_old = is_file_old("/fake/recent_file.txt", self.days_threshold, self.mock_current_time_timestamp)
        self.assertFalse(is_accessed_old)
        self.assertFalse(is_modified_old)

        # Case 3: File accessed old, modified recent
        mock_get_file_stats.return_value = (old_atime, recent_mtime, 100)
        is_accessed_old, is_modified_old = is_file_old("/fake/mixed_file.txt", self.days_threshold, self.mock_current_time_timestamp)
        self.assertTrue(is_accessed_old)
        self.assertFalse(is_modified_old)

        # Case 4: File stats unavailable
        mock_get_file_stats.return_value = (None, None, None)
        is_accessed_old, is_modified_old = is_file_old("/fake/no_stats.txt", self.days_threshold, self.mock_current_time_timestamp)
        self.assertFalse(is_accessed_old)
        self.assertFalse(is_modified_old)

    @patch('src.debris_collector.get_file_stats')
    def test_is_file_empty(self, mock_get_file_stats):
        # Mock rationale: get_file_stats is an internal dependency, mock it to isolate is_file_empty.

        # Case 1: Empty file
        mock_get_file_stats.return_value = (123, 456, 0)
        self.assertTrue(is_file_empty("/fake/empty.txt"))

        # Case 2: Non-empty file
        mock_get_file_stats.return_value = (123, 456, 100)
        self.assertFalse(is_file_empty("/fake/non_empty.txt"))

        # Case 3: File stats unavailable
        mock_get_file_stats.return_value = (None, None, None)
        self.assertFalse(is_file_empty("/fake/no_stats.txt"))

    @patch('src.debris_collector.time.time')
    @patch('os.walk')
    @patch('src.debris_collector.get_file_stats')
    def test_collect_debris(self, mock_get_file_stats, mock_os_walk, mock_time_time):
        # Mock rationale:
        # - time.time: for deterministic current time.
        # - os.walk: to simulate directory structure without actual filesystem access.
        # - get_file_stats: to control file properties (atime, mtime, size) for each mocked file.

        mock_time_time.return_value = self.mock_current_time_timestamp

        # Define mock file system structure
        mock_os_walk.return_value = [
            ('/mock_dir', [], ['recent_file.txt', 'old_file.txt', 'empty_file.txt', 'old_empty_file.txt', 'error_file.txt']),
            ('/mock_dir/subdir', [], ['another_recent.txt', 'another_old.txt'])
        ]

        # Define file stats for each mocked file
        # Helper to create stat tuples
        def create_stats(atime_days_ago, mtime_days_ago, size):
            atime = self.mock_current_time_timestamp - (atime_days_ago * 24 * 3600)
            mtime = self.mock_current_time_timestamp - (mtime_days_ago * 24 * 3600)
            return (atime, mtime, size)

        # Map file paths to their mocked stats
        file_stats_map = {
            '/mock_dir/recent_file.txt': create_stats(10, 5, 500), # Recent
            '/mock_dir/old_file.txt': create_stats(40, 35, 200), # Old
            '/mock_dir/empty_file.txt': create_stats(10, 5, 0), # Empty, recent
            '/mock_dir/old_empty_file.txt': create_stats(40, 35, 0), # Old AND Empty
            '/mock_dir/error_file.txt': (None, None, None), # Error getting stats
            '/mock_dir/subdir/another_recent.txt': create_stats(20, 15, 700), # Recent
            '/mock_dir/subdir/another_old.txt': create_stats(50, 45, 300), # Old
        }

        mock_get_file_stats.side_effect = lambda path: file_stats_map.get(path, (None, None, None))

        old_files, empty_files = collect_debris("/mock_dir", self.days_threshold)

        # Assertions for old files
        self.assertEqual(len(old_files), 3)
        old_paths = {f['path'] for f in old_files}
        self.assertIn('/mock_dir/old_file.txt', old_paths)
        self.assertIn('/mock_dir/old_empty_file.txt', old_paths)
        self.assertIn('/mock_dir/subdir/another_old.txt', old_paths)

        # Check details for one old file
        old_file_entry = next(f for f in old_files if f['path'] == '/mock_dir/old_file.txt')
        self.assertTrue(old_file_entry['accessed_old'])
        self.assertTrue(old_file_entry['modified_old'])
        # Check datetime format
        self.assertIsInstance(datetime.fromisoformat(old_file_entry['atime']), datetime)
        self.assertIsInstance(datetime.fromisoformat(old_file_entry['mtime']), datetime)


        # Assertions for empty files
        self.assertEqual(len(empty_files), 2)
        empty_paths = {f['path'] for f in empty_files}
        self.assertIn('/mock_dir/empty_file.txt', empty_paths)
        self.assertIn('/mock_dir/old_empty_file.txt', empty_paths)

        # Ensure error_file.txt is not in results
        self.assertNotIn('/mock_dir/error_file.txt', old_paths)
        self.assertNotIn('/mock_dir/error_file.txt', empty_paths)

if __name__ == '__main__':
    unittest.main()
