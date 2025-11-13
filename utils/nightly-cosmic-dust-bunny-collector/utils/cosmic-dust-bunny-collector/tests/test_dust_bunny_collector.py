import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.dust_bunny_collector import find_dust_bunnies

class TestDustBunnyCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_empty_dir(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory that exists but contains no files or subdirectories.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', [], [])
        ]
        mock_getmtime.return_value = time.time() # Not relevant for empty dir test, but good practice to mock

        bunnies = find_dust_bunnies('/mock_root')
        self.assertEqual(len(bunnies['empty_dirs']), 0) # Root itself is not considered empty
        self.assertEqual(len(bunnies['aged_log_files']), 0)
        self.assertEqual(len(bunnies['temp_files']), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_empty_subdir(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with one empty subdirectory.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', ['subdir1', 'empty_subdir'], ['file.txt']),
            ('/mock_root/subdir1', [], ['another.txt']),
            ('/mock_root/empty_subdir', [], []) # This is the empty one
        ]
        mock_getmtime.return_value = time.time() # Not relevant for empty dir test

        bunnies = find_dust_bunnies('/mock_root')
        self.assertIn('/mock_root/empty_subdir', bunnies['empty_dirs'])
        self.assertEqual(len(bunnies['empty_dirs']), 1)
        self.assertEqual(len(bunnies['aged_log_files']), 0)
        self.assertEqual(len(bunnies['temp_files']), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_aged_log_file(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with an old log file.
        mock_isdir.return_value = True
        # Simulate a log file modified 100 days ago (older than default 90 days)
        old_timestamp = (datetime.now() - timedelta(days=100)).timestamp()
        mock_walk.return_value = [
            ('/mock_root', [], ['app.log', 'recent.log'])
        ]
        # Mock getmtime to return old_timestamp for 'app.log' and recent for 'recent.log'
        def getmtime_side_effect(path):
            if 'app.log' in path:
                return old_timestamp
            return time.time() # Recent file

        mock_getmtime.side_effect = getmtime_side_effect

        bunnies = find_dust_bunnies('/mock_root')
        self.assertEqual(len(bunnies['empty_dirs']), 0)
        self.assertEqual(len(bunnies['aged_log_files']), 1)
        self.assertIn(('/mock_root/app.log', (datetime.fromtimestamp(old_timestamp).strftime('%Y-%m-%d'))), bunnies['aged_log_files'])
        self.assertEqual(len(bunnies['temp_files']), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_temp_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with various temporary files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', [], ['config.tmp', 'backup.bak', '~edit.txt', 'normal.txt'])
        ]
        mock_getmtime.return_value = time.time() # Not relevant for temp file test

        bunnies = find_dust_bunnies('/mock_root')
        self.assertEqual(len(bunnies['empty_dirs']), 0)
        self.assertEqual(len(bunnies['aged_log_files']), 0)
        self.assertEqual(len(bunnies['temp_files']), 3)
        self.assertIn('/mock_root/config.tmp', bunnies['temp_files'])
        self.assertIn('/mock_root/backup.bak', bunnies['temp_files'])
        self.assertIn('/mock_root/~edit.txt', bunnies['temp_files'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_non_existent_dir(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a non-existent root directory.
        mock_isdir.return_value = False

        bunnies = find_dust_bunnies('/non_existent_root')
        self.assertEqual(len(bunnies['empty_dirs']), 0)
        self.assertEqual(len(bunnies['aged_log_files']), 0)
        self.assertEqual(len(bunnies['temp_files']), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_custom_log_age(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test with a custom log age threshold.
        mock_isdir.return_value = True
        # Simulate a log file modified 60 days ago
        old_timestamp_60_days = (datetime.now() - timedelta(days=60)).timestamp()
        # Simulate a log file modified 100 days ago
        old_timestamp_100_days = (datetime.now() - timedelta(days=100)).timestamp()

        mock_walk.return_value = [
            ('/mock_root', [], ['log_60.log', 'log_100.log'])
        ]

        def getmtime_side_effect(path):
            if 'log_60.log' in path:
                return old_timestamp_60_days
            if 'log_100.log' in path:
                return old_timestamp_100_days
            return time.time()

        mock_getmtime.side_effect = getmtime_side_effect

        # Test with max_log_age_days = 70 (log_60.log should not be found, log_100.log should)
        bunnies = find_dust_bunnies('/mock_root', max_log_age_days=70)
        self.assertEqual(len(bunnies['aged_log_files']), 1)
        self.assertIn(('/mock_root/log_100.log', (datetime.fromtimestamp(old_timestamp_100_days).strftime('%Y-%m-%d'))), bunnies['aged_log_files'])

        # Test with max_log_age_days = 50 (neither should be found)
        bunnies = find_dust_bunnies('/mock_root', max_log_age_days=50)
        self.assertEqual(len(bunnies['aged_log_files']), 0)

        # Test with max_log_age_days = 110 (both should be found)
        bunnies = find_dust_bunnies('/mock_root', max_log_age_days=110)
        self.assertEqual(len(bunnies['aged_log_files']), 2)
        self.assertIn(('/mock_root/log_60.log', (datetime.fromtimestamp(old_timestamp_60_days).strftime('%Y-%m-%d'))), bunnies['aged_log_files'])
        self.assertIn(('/mock_root/log_100.log', (datetime.fromtimestamp(old_timestamp_100_days).strftime('%Y-%m-%d'))), bunnies['aged_log_files'])


if __name__ == '__main__':
    unittest.main()
