import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.collector import find_cosmic_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic tests
        self.mock_current_time = datetime(2023, 10, 26, 10, 0, 0).timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_empty_directory(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [] # No files or subdirectories
        mock_time.return_value = self.mock_current_time

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_no_dust_files(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files that do not meet dust criteria.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        # Simulate a file that is large enough and recent enough
        mock_walk.return_value = [
            ('/test/dir', [], ['large_recent.txt'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 2048 # 2KB, larger than default 1KB max_size
        mock_stat_obj.st_mtime = (datetime(2023, 10, 20, 10, 0, 0)).timestamp() # 6 days old, less than default 90 days max_age
        mock_stat.return_value = mock_stat_obj

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_empty_file(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory containing an empty file.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['empty.txt'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 0 # Empty file
        mock_stat_obj.st_mtime = (datetime(2023, 10, 25, 10, 0, 0)).timestamp()
        mock_stat.return_value = mock_stat_obj

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test/dir', 'empty.txt'))
        self.assertIn('empty', dust[0]['reasons'])
        self.assertNotIn('small', dust[0]['reasons']) # Empty files are not 'small' by definition in this utility

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_small_file(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory containing a small file.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['small.txt'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 500 # 500 bytes, smaller than default 1KB max_size
        mock_stat_obj.st_mtime = (datetime(2023, 10, 25, 10, 0, 0)).timestamp()
        mock_stat.return_value = mock_stat_obj

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test/dir', 'small.txt'))
        self.assertIn('small', dust[0]['reasons'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_old_file(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory containing an old file.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['old.log'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 1500 # Not small, not empty
        # Older than 90 days from self.mock_current_time (Oct 26, 2023)
        mock_stat_obj.st_mtime = (datetime(2023, 7, 1, 10, 0, 0)).timestamp()
        mock_stat.return_value = mock_stat_obj

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test/dir', 'old.log'))
        self.assertIn('old', dust[0]['reasons'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_multiple_reasons_file(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file that is both small and old.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['small_old.tmp'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 100 # Small
        mock_stat_obj.st_mtime = (datetime(2023, 6, 1, 10, 0, 0)).timestamp() # Old
        mock_stat.return_value = mock_stat_obj

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test/dir', 'small_old.tmp'))
        self.assertIn('small', dust[0]['reasons'])
        self.assertIn('old', dust[0]['reasons'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_custom_thresholds(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Test with custom size and age thresholds.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['custom_dust.txt'])
        ]
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 3000 # Larger than default 1KB, but smaller than custom 5KB
        # Older than custom 30 days, but not default 90 days
        mock_stat_obj.st_mtime = (datetime(2023, 9, 1, 10, 0, 0)).timestamp()
        mock_stat.return_value = mock_stat_obj

        # Test with max_size_bytes=5000 (5KB) and max_age_days=30
        dust = find_cosmic_dust('/test/dir', max_size_bytes=5000, max_age_days=30)
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test/dir', 'custom_dust.txt'))
        self.assertIn('small', dust[0]['reasons'])
        self.assertIn('old', dust[0]['reasons'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_file_disappears_during_scan(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a race condition where a file is deleted after os.walk but before os.stat.
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/test/dir', [], ['disappearing.txt'])
        ]
        mock_stat.side_effect = FileNotFoundError # Simulate file deletion

        dust = find_cosmic_dust('/test/dir')
        self.assertEqual(len(dust), 0) # No dust should be reported if file can't be stat'd

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('time.time')
    def test_non_existent_directory(self, mock_time, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Test behavior when the target directory does not exist.
        mock_isdir.return_value = False
        mock_time.return_value = self.mock_current_time

        dust = find_cosmic_dust('/non/existent/dir')
        self.assertEqual(len(dust), 0)
        # The function prints an error, but returns an empty list, which is the expected behavior for the caller.

if __name__ == '__main__':
    unittest.main()
