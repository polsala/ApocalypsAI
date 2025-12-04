import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the scavenger functions
from src.scavenger import scavenge, get_file_age_days, is_empty_dir, is_temp_or_log_file, should_exclude

class TestScavenger(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the modification time of a file.
        # We need to control this value to test different file ages deterministically.
        
        # Test a file modified exactly 10 days ago
        current_time = time.time()
        mock_getmtime.return_value = current_time - (10 * 24 * 60 * 60) # 10 days ago
        self.assertAlmostEqual(get_file_age_days("dummy_file.txt"), 10.0, places=5)

        # Test a file modified in the future (should result in negative age)
        mock_getmtime.return_value = current_time + (5 * 24 * 60 * 60) # 5 days in future
        self.assertAlmostEqual(get_file_age_days("future_file.txt"), -5.0, places=5)

        # Test error case (e.g., file not found)
        mock_getmtime.side_effect = OSError
        self.assertEqual(get_file_age_days("non_existent_file.txt"), -1)

    def test_is_empty_dir(self):
        # Mock rationale: os.listdir is used to check directory contents.
        # We need to control its return value to simulate empty or non-empty directories.
        
        with patch('os.listdir', return_value=[]):
            self.assertTrue(is_empty_dir("empty_dir"))
        with patch('os.listdir', return_value=['file.txt']):
            self.assertFalse(is_empty_dir("non_empty_dir"))
        with patch('os.listdir', return_value=['subdir/']):
            self.assertFalse(is_empty_dir("non_empty_dir_with_subdir"))

    def test_is_temp_or_log_file(self):
        # Mock rationale: This function relies on string matching, no OS calls.
        # No mocking needed, direct testing of logic.
        
        self.assertTrue(is_temp_or_log_file("app.log", "/path/to/app.log"))
        self.assertTrue(is_temp_or_log_file("cache.tmp", "/path/to/cache.tmp"))
        self.assertTrue(is_temp_or_log_file("my_script.pyc", "/path/to/my_script.pyc"))
        self.assertTrue(is_temp_or_log_file("__pycache__", "/path/to/__pycache__"))
        self.assertTrue(is_temp_or_log_file("build", "/path/to/build")) # Directory name
        self.assertTrue(is_temp_or_log_file("node_modules", "/path/to/node_modules")) # Directory name
        self.assertFalse(is_temp_or_log_file("important.txt", "/path/to/important.txt"))
        self.assertFalse(is_temp_or_log_file("main.py", "/path/to/main.py"))

    def test_should_exclude(self):
        # Mock rationale: This function relies on string matching, no OS calls.
        # No mocking needed, direct testing of logic.
        
        exclude_patterns = ["*.git*", "*/node_modules/*", "temp_dir"]
        self.assertTrue(should_exclude("/repo/.git/config", exclude_patterns))
        self.assertTrue(should_exclude("/repo/node_modules/package.js", exclude_patterns))
        self.assertTrue(should_exclude("/repo/temp_dir/file.txt", exclude_patterns))
        self.assertTrue(should_exclude("temp_dir", exclude_patterns)) # Base name match
        self.assertFalse(should_exclude("/repo/src/main.py", exclude_patterns))
        self.assertFalse(should_exclude("/repo/docs/report.md", exclude_patterns))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scavenge_basic(self, mock_time_time, mock_getmtime, mock_os_walk, mock_os_path_isdir):
        # Mock rationale:
        # os.path.isdir: To simulate if the root_path is a valid directory.
        # os.walk: To control the directory structure and files found during the scan.
        # os.path.getmtime: To control the modification time of files for 'old file' detection.
        # time.time: To control the current time for calculating file age.

        mock_os_path_isdir.return_value = True
        mock_time_time.return_value = time.mktime(datetime(2024, 1, 1).timetuple()) # Current time for age calculation

        # Simulate a directory structure
        # root/
        #   empty_dir/
        #   old_file.txt (modified 400 days ago)
        #   recent_file.txt (modified 10 days ago)
        #   temp_file.tmp
        #   logs/
        #     app.log
        #   __pycache__/
        #     cache.pyc
        #   subdir/
        #     another_empty_dir/
        #     important.py

        mock_os_walk.return_value = [
            ('/root', ['empty_dir', 'logs', '__pycache__', 'subdir'], ['old_file.txt', 'recent_file.txt', 'temp_file.tmp']),
            ('/root/empty_dir', [], []),
            ('/root/logs', [], ['app.log']),
            ('/root/__pycache__', [], ['cache.pyc']),
            ('/root/subdir', ['another_empty_dir'], ['important.py']),
            ('/root/subdir/another_empty_dir', [], []),
        ]

        # Set modification times
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                # 400 days old
                return time.mktime((datetime(2024, 1, 1) - timedelta(days=400)).timetuple())
            elif 'recent_file.txt' in path:
                # 10 days old
                return time.mktime((datetime(2024, 1, 1) - timedelta(days=10)).timetuple())
            else:
                # Default to recent for others
                return mock_time_time.return_value - (10 * 24 * 60 * 60)
        mock_getmtime.side_effect = mock_getmtime_side_effect

        results = scavenge('/root', max_age_days=365)

        self.assertIn('/root/empty_dir', results['empty_dirs'])
        self.assertIn('/root/subdir/another_empty_dir', results['empty_dirs'])
        self.assertEqual(len(results['empty_dirs']), 2)

        self.assertIn('/root/old_file.txt (Last modified: 2022-11-27)', results['old_files'])
        self.assertEqual(len(results['old_files']), 1)

        self.assertIn('/root/temp_file.tmp', results['temp_files'])
        self.assertIn('/root/logs/app.log', results['temp_files'])
        self.assertIn('/root/__pycache__/', results['temp_files']) # Check for directory matching temp pattern
        self.assertEqual(len(results['temp_files']), 3) # temp_file.tmp, app.log, __pycache__/

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scavenge_with_excludes(self, mock_time_time, mock_getmtime, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Same as basic test, but specifically for testing exclusion logic.
        
        mock_os_path_isdir.return_value = True
        mock_time_time.return_value = time.mktime(datetime(2024, 1, 1).timetuple())

        # root/
        #   .git/
        #     config
        #   node_modules/
        #     package.js
        #   src/
        #     main.py
        #   temp_data/
        #     cache.tmp
        #   old_file.txt (400 days old)

        mock_os_walk.return_value = [
            ('/root', ['.git', 'node_modules', 'src', 'temp_data'], ['old_file.txt']),
            ('/root/.git', [], ['config']),
            ('/root/node_modules', [], ['package.js']),
            ('/root/src', [], ['main.py']),
            ('/root/temp_data', [], ['cache.tmp']),
        ]

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return time.mktime((datetime(2024, 1, 1) - timedelta(days=400)).timetuple())
            return mock_time_time.return_value - (10 * 24 * 60 * 60) # Default recent
        mock_getmtime.side_effect = mock_getmtime_side_effect

        exclude_patterns = ["*/.git/*", "*/node_modules/*", "*/temp_data/*"]
        results = scavenge('/root', max_age_days=365, exclude_patterns=exclude_patterns)

        self.assertNotIn('/root/.git/config', results['old_files'])
        self.assertNotIn('/root/.git/config', results['temp_files'])
        self.assertNotIn('/root/node_modules/package.js', results['old_files'])
        self.assertNotIn('/root/node_modules/package.js', results['temp_files'])
        self.assertNotIn('/root/temp_data/cache.tmp', results['temp_files']) # Excluded by pattern

        self.assertIn('/root/old_file.txt (Last modified: 2022-11-27)', results['old_files'])
        self.assertEqual(len(results['old_files']), 1)
        self.assertEqual(len(results['empty_dirs']), 0)
        self.assertEqual(len(results['temp_files']), 0) # All temp files are excluded by patterns

    @patch('os.path.isdir', return_value=False)
    def test_scavenge_invalid_path(self, mock_os_path_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate an invalid root path.
        
        results = scavenge('/nonexistent_path')
        self.assertEqual(results['empty_dirs'], [])
        self.assertEqual(results['old_files'], [])
        self.assertEqual(results['temp_files'], [])

if __name__ == '__main__':
    unittest.main()
