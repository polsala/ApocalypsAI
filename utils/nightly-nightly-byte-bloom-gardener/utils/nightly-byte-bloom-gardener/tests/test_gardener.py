import unittest
from unittest.mock import patch, MagicMock
import datetime
import os

# Mock rationale: We need to simulate file system interactions (walking directories, getting file stats)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't rely on
# the state of the actual file system.

# Import the function to be tested
from src.gardener import find_byte_blooms, convert_bytes_to_mb, convert_mb_to_bytes

class TestGardener(unittest.TestCase):

    def setUp(self):
        # Define common thresholds for tests
        self.size_threshold_mb = 100
        self.age_threshold_days = 90

        # Define some dates for mocking file modification times
        self.now = datetime.datetime.now()
        self.old_date = self.now - datetime.timedelta(days=self.age_threshold_days + 10)
        self.new_date = self.now - datetime.timedelta(days=self.age_threshold_days - 10)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_no_byte_blooms_found(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory or one with files not meeting criteria.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['small_new.txt', 'large_new.log'])
        ]

        # Mock os.stat for files that don't meet criteria
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'small_new.txt' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(10) # Small file
                mock_stat_obj.st_mtime = self.old_date.timestamp() # Old, but small
            elif 'large_new.log' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(self.size_threshold_mb + 10) # Large file
                mock_stat_obj.st_mtime = self.new_date.timestamp() # New, but large
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        blooms = find_byte_blooms('/root', self.size_threshold_mb, self.age_threshold_days)
        self.assertEqual(len(blooms), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_byte_blooms_found(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files that meet both size and age criteria.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['old_large_file.zip', 'another_old_large.dat'])
        ]

        # Mock os.stat for files that meet criteria
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_size = convert_mb_to_bytes(self.size_threshold_mb + 50) # Large file
            mock_stat_obj.st_mtime = self.old_date.timestamp() # Old file
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        blooms = find_byte_blooms('/root', self.size_threshold_mb, self.age_threshold_days)
        self.assertEqual(len(blooms), 2)
        self.assertEqual(blooms[0]['path'], os.path.join('/root', 'old_large_file.zip'))
        self.assertAlmostEqual(blooms[0]['size_mb'], self.size_threshold_mb + 50, places=1)
        self.assertEqual(blooms[0]['modified_date'], self.old_date.strftime('%Y-%m-%d'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_mixed_directory(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with a mix of files, some meeting criteria, some not.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['small_new.txt', 'large_new.log', 'old_large_file.zip', 'small_old.csv'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'small_new.txt' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(10)
                mock_stat_obj.st_mtime = self.new_date.timestamp()
            elif 'large_new.log' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(self.size_threshold_mb + 10)
                mock_stat_obj.st_mtime = self.new_date.timestamp()
            elif 'old_large_file.zip' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(self.size_threshold_mb + 50)
                mock_stat_obj.st_mtime = self.old_date.timestamp()
            elif 'small_old.csv' in path:
                mock_stat_obj.st_size = convert_mb_to_bytes(5)
                mock_stat_obj.st_mtime = self.old_date.timestamp()
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        blooms = find_byte_blooms('/root', self.size_threshold_mb, self.age_threshold_days)
        self.assertEqual(len(blooms), 1)
        self.assertEqual(blooms[0]['path'], os.path.join('/root', 'old_large_file.zip'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_non_existent_directory(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Test the error handling for an invalid root directory.
        mock_isdir.return_value = False
        blooms = find_byte_blooms('/nonexistent', self.size_threshold_mb, self.age_threshold_days)
        self.assertEqual(len(blooms), 0)
        mock_walk.assert_not_called() # os.walk should not be called if dir doesn't exist

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_file_disappears_during_scan(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a FileNotFoundError during os.stat, which can happen in real-world scenarios.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['file_that_disappears.txt'])
        ]

        def mock_stat_side_effect(path):
            if 'file_that_disappears.txt' in path:
                raise FileNotFoundError
            return MagicMock()

        mock_stat.side_effect = mock_stat_side_effect

        blooms = find_byte_blooms('/root', self.size_threshold_mb, self.age_threshold_days)
        self.assertEqual(len(blooms), 0)

    def test_convert_bytes_to_mb(self):
        self.assertEqual(convert_bytes_to_mb(1024 * 1024), 1.0)
        self.assertEqual(convert_bytes_to_mb(0), 0.0)
        self.assertAlmostEqual(convert_bytes_to_mb(500 * 1024 * 1024), 500.0)

    def test_convert_mb_to_bytes(self):
        self.assertEqual(convert_mb_to_bytes(1), 1024 * 1024)
        self.assertEqual(convert_mb_to_bytes(0), 0)
        self.assertEqual(convert_mb_to_bytes(500), 500 * 1024 * 1024)

if __name__ == '__main__':
    unittest.main()
