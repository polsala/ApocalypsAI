import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import find_dust_bunnies, convert_mb_to_bytes, convert_days_to_seconds

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic tests
        self.mock_current_time = datetime(2023, 10, 26, 12, 0, 0).timestamp()
        # Mock time.time() to return our fixed current time
        self.patcher_time = patch('time.time', return_value=self.mock_current_time)
        self.mock_time = self.patcher_time.start()

    def tearDown(self):
        self.patcher_time.stop()

    def test_convert_mb_to_bytes(self):
        self.assertEqual(convert_mb_to_bytes(1), 1024 * 1024)
        self.assertEqual(convert_mb_to_bytes(10), 10 * 1024 * 1024)
        self.assertEqual(convert_mb_to_bytes(0), 0)

    def test_convert_days_to_seconds(self):
        self.assertEqual(convert_days_to_seconds(1), 24 * 60 * 60)
        self.assertEqual(convert_days_to_seconds(30), 30 * 24 * 60 * 60)
        self.assertEqual(convert_days_to_seconds(0), 0)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_no_dust_bunnies_found(self, mock_stat, mock_walk, mock_isdir, mock_exists):
        # Mock rationale: Simulate a directory with files that do not meet the criteria.
        # os.path.exists: Ensure the base path exists.
        # os.path.isdir: Ensure the base path is a directory.
        # os.walk: Simulate directory traversal, returning one file.
        # os.stat: Provide file metadata (size, modification time).

        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file1.txt'])
        ]

        # File is recent (10 days old) and small (1MB)
        file_mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=10)).timestamp()
        mock_stat.return_value = MagicMock(st_size=convert_mb_to_bytes(1), st_mtime=file_mtime)

        bunnies = find_dust_bunnies('/mock/path', age_days=30, min_size_mb=10)
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_dust_bunny_found_by_age(self, mock_stat, mock_walk, mock_isdir, mock_exists):
        # Mock rationale: Simulate a file that is old but not necessarily large.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['old_log.txt'])
        ]

        # File is old (60 days old) but small (5MB)
        file_mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=60)).timestamp()
        mock_stat.return_value = MagicMock(st_size=convert_mb_to_bytes(5), st_mtime=file_mtime)

        bunnies = find_dust_bunnies('/mock/path', age_days=30, min_size_mb=10)
        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0]['path'], '/mock/path/old_log.txt')
        self.assertEqual(bunnies[0]['size_mb'], 5.0)
        self.assertEqual(bunnies[0]['age_days'], 60)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_dust_bunny_found_by_size(self, mock_stat, mock_walk, mock_isdir, mock_exists):
        # Mock rationale: Simulate a file that is large but not necessarily old.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['large_data.zip'])
        ]

        # File is recent (10 days old) but large (20MB)
        file_mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=10)).timestamp()
        mock_stat.return_value = MagicMock(st_size=convert_mb_to_bytes(20), st_mtime=file_mtime)

        bunnies = find_dust_bunnies('/mock/path', age_days=30, min_size_mb=10)
        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0]['path'], '/mock/path/large_data.zip')
        self.assertEqual(bunnies[0]['size_mb'], 20.0)
        self.assertEqual(bunnies[0]['age_days'], 10)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_multiple_dust_bunnies_found(self, mock_stat, mock_walk, mock_isdir, mock_exists):
        # Mock rationale: Simulate multiple files, some meeting criteria, some not.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', ['subdir'], ['file1.txt', 'old_large.bak']),
            ('/mock/path/subdir', [], ['recent_small.log', 'old_small.csv', 'recent_large.iso'])
        ]

        # Define specific stat results for each file
        def mock_os_stat_side_effect(file_path):
            if file_path == '/mock/path/file1.txt': # Recent, small -> NOT a bunny
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=5)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(2), st_mtime=mtime)
            elif file_path == '/mock/path/old_large.bak': # Old, large -> BUNNY
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=90)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(100), st_mtime=mtime)
            elif file_path == '/mock/path/subdir/recent_small.log': # Recent, small -> NOT a bunny
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=15)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(0.5), st_mtime=mtime)
            elif file_path == '/mock/path/subdir/old_small.csv': # Old, small -> BUNNY
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=45)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(1), st_mtime=mtime)
            elif file_path == '/mock/path/subdir/recent_large.iso': # Recent, large -> BUNNY
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=20)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(50), st_mtime=mtime)
            raise FileNotFoundError # Should not happen with these mocks

        mock_stat.side_effect = mock_os_stat_side_effect

        bunnies = find_dust_bunnies('/mock/path', age_days=30, min_size_mb=10)
        self.assertEqual(len(bunnies), 3)

        # Check specific bunnies
        bunny_paths = {b['path'] for b in bunnies}
        self.assertIn('/mock/path/old_large.bak', bunny_paths)
        self.assertIn('/mock/path/subdir/old_small.csv', bunny_paths)
        self.assertIn('/mock/path/subdir/recent_large.iso', bunny_paths)

        # Verify details for one of them
        old_large_bunny = next(b for b in bunnies if b['path'] == '/mock/path/old_large.bak')
        self.assertEqual(old_large_bunny['size_mb'], 100.0)
        self.assertEqual(old_large_bunny['age_days'], 90)

        old_small_bunny = next(b for b in bunnies if b['path'] == '/mock/path/subdir/old_small.csv')
        self.assertEqual(old_small_bunny['size_mb'], 1.0)
        self.assertEqual(old_small_bunny['age_days'], 45)

        recent_large_bunny = next(b for b in bunnies if b['path'] == '/mock/path/subdir/recent_large.iso')
        self.assertEqual(recent_large_bunny['size_mb'], 50.0)
        self.assertEqual(recent_large_bunny['age_days'], 20)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_path_does_not_exist(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate a non-existent path.
        mock_exists.return_value = False
        mock_isdir.return_value = False # Not strictly needed if exists is False, but good for completeness

        bunnies = find_dust_bunnies('/non/existent/path')
        self.assertEqual(len(bunnies), 0)
        # We could also capture stdout to check the error message, but checking return value is sufficient for utility.

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_path_is_not_directory(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate a path that exists but is a file, not a directory.
        mock_exists.return_value = True
        mock_isdir.return_value = False

        bunnies = find_dust_bunnies('/mock/file.txt')
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_os_error_during_scan(self, mock_stat, mock_walk, mock_isdir, mock_exists):
        # Mock rationale: Simulate an OSError (e.g., permission denied) when accessing a file.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['accessible_file.txt', 'inaccessible_file.txt'])
        ]

        def mock_os_stat_side_effect(file_path):
            if file_path == '/mock/path/accessible_file.txt':
                mtime = (datetime.fromtimestamp(self.mock_current_time) - timedelta(days=40)).timestamp()
                return MagicMock(st_size=convert_mb_to_bytes(15), st_mtime=mtime)
            elif file_path == '/mock/path/inaccessible_file.txt':
                raise OSError("Permission denied")
            raise FileNotFoundError

        mock_stat.side_effect = mock_os_stat_side_effect

        bunnies = find_dust_bunnies('/mock/path', age_days=30, min_size_mb=10)
        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0]['path'], '/mock/path/accessible_file.txt')


if __name__ == '__main__':
    unittest.main()
