import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the function to be tested
from src.sweeper import find_dust_bunnies

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age checks
        self.mock_current_time = datetime(2024, 7, 15, 10, 0, 0).timestamp()

    @patch('os.path.isdir')
    def test_invalid_path(self, mock_isdir):
        # Mock rationale: Prevent actual file system access and simulate an invalid path.
        mock_isdir.return_value = False
        with self.assertRaises(ValueError):
            find_dust_bunnies('/nonexistent/path')

    @patch('os.walk')
    @patch('os.path.isdir')
    def test_no_dust_bunnies(self, mock_isdir, mock_walk):
        # Mock rationale: Simulate a clean directory structure with no empty dirs or old files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt'])
        ]
        
        with patch('time.time', return_value=self.mock_current_time):
            results = find_dust_bunnies('/root')
            self.assertEqual(results['empty_dirs'], [])
            self.assertEqual(results['aged_files'], [])

    @patch('os.walk')
    @patch('os.path.isdir')
    def test_empty_directories(self, mock_isdir, mock_walk):
        # Mock rationale: Simulate a directory structure with empty directories.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1', 'empty_dir1'], ['file.txt']),
            ('/root/dir1', ['empty_dir2'], ['another_file.txt']),
            ('/root/empty_dir1', [], []),
            ('/root/dir1/empty_dir2', [], [])
        ]
        
        with patch('time.time', return_value=self.mock_current_time):
            results = find_dust_bunnies('/root')
            expected_empty_dirs = [
                '/root/empty_dir1',
                '/root/dir1/empty_dir2'
            ]
            self.assertCountEqual(results['empty_dirs'], expected_empty_dirs)
            self.assertEqual(results['aged_files'], [])

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_aged_files(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate files with different modification times to test age filtering.
        mock_isdir.return_value = True
        
        # Define modification times relative to mock_current_time (July 15, 2024)
        # 30 days threshold means anything before June 15, 2024 is 'old'
        old_time = datetime(2024, 6, 1, 10, 0, 0).timestamp() # Older than 30 days
        recent_time = datetime(2024, 7, 1, 10, 0, 0).timestamp() # Newer than 30 days

        # Mock os.walk to return a structure with log/tmp files
        mock_walk.return_value = [
            ('/root', [], ['old.log', 'recent.log', 'temp_old.tmp', 'temp_recent.tmp', 'other.txt'])
        ]

        # Mock os.path.getmtime to return specific times for specific files
        def mock_getmtime_side_effect(path):
            if 'old.log' in path or 'temp_old.tmp' in path:
                return old_time
            elif 'recent.log' in path or 'temp_recent.tmp' in path:
                return recent_time
            return self.mock_current_time # Default for other files not explicitly tested

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('time.time', return_value=self.mock_current_time):
            results = find_dust_bunnies('/root', age_days=30, patterns=['*.log', 'temp_*'])
            
            expected_aged_files = [
                {'path': '/root/old.log', 'last_modified': '2024-06-01'},
                {'path': '/root/temp_old.tmp', 'last_modified': '2024-06-01'}
            ]
            
            # Sort for consistent comparison as order from os.walk might vary
            self.assertEqual(sorted(results['aged_files'], key=lambda x: x['path']),
                             sorted(expected_aged_files, key=lambda x: x['path']))
            self.assertEqual(results['empty_dirs'], [])

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_custom_patterns_and_age(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Test custom patterns and age thresholds.
        mock_isdir.return_value = True
        
        # 10 days threshold means anything before July 5, 2024 is 'old' (relative to July 15)
        old_time_custom = datetime(2024, 7, 1, 10, 0, 0).timestamp() # Older than 10 days
        recent_time_custom = datetime(2024, 7, 10, 10, 0, 0).timestamp() # Newer than 10 days

        mock_walk.return_value = [
            ('/root', [], ['data.bak', 'report.csv', 'old_cache.dat', 'recent_cache.dat'])
        ]

        def mock_getmtime_side_effect(path):
            if 'old_cache.dat' in path:
                return old_time_custom
            elif 'recent_cache.dat' in path:
                return recent_time_custom
            return self.mock_current_time # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('time.time', return_value=self.mock_current_time):
            results = find_dust_bunnies('/root', age_days=10, patterns=['*.dat'])
            
            expected_aged_files = [
                {'path': '/root/old_cache.dat', 'last_modified': '2024-07-01'}
            ]
            
            self.assertEqual(results['aged_files'], expected_aged_files)
            self.assertEqual(results['empty_dirs'], [])

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_os_error_handling(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate an OSError during file access (e.g., permissions, file deleted).
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['accessible.log', 'inaccessible.log'])
        ]

        def mock_getmtime_side_effect(path):
            if 'inaccessible.log' in path:
                raise OSError("Permission denied")
            return datetime(2024, 6, 1, 10, 0, 0).timestamp() # Old time

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('time.time', return_value=self.mock_current_time):
            results = find_dust_bunnies('/root', age_days=30, patterns=['*.log'])
            
            expected_aged_files = [
                {'path': '/root/accessible.log', 'last_modified': '2024-06-01'}
            ]
            
            self.assertEqual(results['aged_files'], expected_aged_files)
            self.assertEqual(results['empty_dirs'], [])
