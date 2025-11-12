import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime

# Import the function to be tested
from src.dust_collector import find_dust_bunnies

class TestDustCollector(unittest.TestCase):

    # Mock rationale: We need to simulate a file system without actually creating files
    # or interacting with the real disk. This ensures tests are fast, deterministic,
    # and don't leave artifacts. `os.walk`, `os.path.getmtime`, `os.path.getsize`,
    # `os.path.isfile`, and `time.time` are the primary functions that interact with
    # the file system and current time, so they are mocked.

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.mock_current_time = datetime(2024, 1, 1, 12, 0, 0).timestamp()

    @patch('time.time')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_no_dust_bunnies_found(self, mock_isdir, mock_walk, mock_isfile, mock_getmtime, mock_getsize, mock_time):
        mock_time.return_value = self.mock_current_time
        mock_isdir.return_value = True # Assume root_dir exists
        mock_walk.return_value = [
            ('/mock/root', [], ['new_file.txt', 'large_file.log'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/mock/root/new_file.txt', '/mock/root/large_file.log']

        # new_file.txt: recent, small (not a dust bunny)
        # large_file.log: old, but too large (not a dust bunny)
        mock_getmtime.side_effect = lambda p: {
            '/mock/root/new_file.txt': (self.mock_current_time - 1 * 24 * 60 * 60), # 1 day old
            '/mock/root/large_file.log': (self.mock_current_time - 60 * 24 * 60 * 60) # 60 days old
        }.get(p, self.mock_current_time)

        mock_getsize.side_effect = lambda p: {
            '/mock/root/new_file.txt': 100, # 100 bytes
            '/mock/root/large_file.log': 2 * 1024 * 1024 # 2 MB (too large)
        }.get(p, 0)

        bunnies = find_dust_bunnies('/mock/root', age_days=30, max_size_bytes=1024 * 1024) # 1MB max size
        self.assertEqual(len(bunnies), 0)

    @patch('time.time')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_some_dust_bunnies_found(self, mock_isdir, mock_walk, mock_isfile, mock_getmtime, mock_getsize, mock_time):
        mock_time.return_value = self.mock_current_time
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['old_small.txt', 'new_small.txt', 'old_large.log']),
            ('/mock/root/subdir', [], ['another_old_small.tmp'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/mock/root/old_small.txt',
            '/mock/root/new_small.txt',
            '/mock/root/old_large.log',
            '/mock/root/subdir/another_old_small.tmp'
        ]

        # Define specific mtimes and sizes for mocked files
        file_data = {
            '/mock/root/old_small.txt': {
                'mtime': (self.mock_current_time - 45 * 24 * 60 * 60), # 45 days old
                'size': 500 # 500 bytes
            },
            '/mock/root/new_small.txt': {
                'mtime': (self.mock_current_time - 5 * 24 * 60 * 60), # 5 days old
                'size': 600 # 600 bytes
            },
            '/mock/root/old_large.log': {
                'mtime': (self.mock_current_time - 50 * 24 * 60 * 60), # 50 days old
                'size': 2 * 1024 * 1024 # 2 MB
            },
            '/mock/root/subdir/another_old_small.tmp': {
                'mtime': (self.mock_current_time - 70 * 24 * 60 * 60), # 70 days old
                'size': 300 # 300 bytes
            }
        }

        mock_getmtime.side_effect = lambda p: file_data.get(p, {}).get('mtime', self.mock_current_time)
        mock_getsize.side_effect = lambda p: file_data.get(p, {}).get('size', 0)

        bunnies = find_dust_bunnies('/mock/root', age_days=30, max_size_bytes=1024 * 1024)

        self.assertEqual(len(bunnies), 2)
        self.assertIn({
            'path': '/mock/root/old_small.txt',
            'size': 500,
            'mtime': (self.mock_current_time - 45 * 24 * 60 * 60)
        }, bunnies)
        self.assertIn({
            'path': '/mock/root/subdir/another_old_small.tmp',
            'size': 300,
            'mtime': (self.mock_current_time - 70 * 24 * 60 * 60)
        }, bunnies)

    @patch('time.time')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_empty_directory(self, mock_isdir, mock_walk, mock_isfile, mock_getmtime, mock_getsize, mock_time):
        mock_time.return_value = self.mock_current_time
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/empty', [], [])
        ]
        mock_isfile.return_value = False # No files exist in this mock setup

        bunnies = find_dust_bunnies('/mock/empty', age_days=30, max_size_bytes=1024 * 1024)
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir')
    def test_invalid_directory_path(self, mock_isdir):
        mock_isdir.return_value = False
        bunnies = find_dust_bunnies('/nonexistent/path', age_days=30, max_size_bytes=1024 * 1024)
        self.assertEqual(len(bunnies), 0)

    @patch('time.time')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_file_inaccessibility_handled(self, mock_isdir, mock_walk, mock_isfile, mock_getmtime, mock_getsize, mock_time):
        mock_time.return_value = self.mock_current_time
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['accessible_file.txt', 'inaccessible_file.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/mock/root/accessible_file.txt', '/mock/root/inaccessible_file.txt']

        # Make 'inaccessible_file.txt' raise an OSError when its properties are accessed
        def getmtime_side_effect(path):
            if path == '/mock/root/inaccessible_file.txt':
                raise OSError("Permission denied")
            return self.mock_current_time - 60 * 24 * 60 * 60 # 60 days old

        def getsize_side_effect(path):
            if path == '/mock/root/inaccessible_file.txt':
                raise OSError("Permission denied")
            return 100 # 100 bytes

        mock_getmtime.side_effect = getmtime_side_effect
        mock_getsize.side_effect = getsize_side_effect

        bunnies = find_dust_bunnies('/mock/root', age_days=30, max_size_bytes=1024 * 1024)

        # Only the accessible file should be found if it meets criteria
        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0]['path'], '/mock/root/accessible_file.txt')

if __name__ == '__main__':
    unittest.main()
