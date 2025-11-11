import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.dust_bunny_sweeper import find_empty_dirs, find_old_files

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: os.walk is a filesystem traversal function. We need to simulate
        # different directory structures to test the logic for finding empty directories
        # without actually touching the filesystem.
        mock_os_walk.side_effect = [
            ('/root', ['dir1', 'dir2', 'empty_dir'], ['file1.txt']),
            ('/root/dir1', [], ['subfile1.txt']),
            ('/root/dir2', ['subdir_empty'], ['subfile2.txt']),
            ('/root/dir2/subdir_empty', [], []),
            ('/root/empty_dir', [], []),
        ]
        expected_empty_dirs = [
            '/root/dir2/subdir_empty',
            '/root/empty_dir'
        ]
        result = find_empty_dirs('/root')
        self.assertCountEqual(result, expected_empty_dirs)

    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_old_files(self, mock_os_walk, mock_os_isfile, mock_os_getmtime):
        # Mock rationale: os.walk, os.path.isfile, and os.path.getmtime are filesystem
        # interaction functions. We need to control the reported modification times and
        # file existence to deterministically test the 'old file' logic without
        # relying on actual file system state or real-time.

        # Simulate current time for consistent testing
        current_time = time.time()

        # Mock os.walk to simulate a directory structure
        mock_os_walk.side_effect = [
            ('/root', ['data'], ['recent.txt', 'old.log']),
            ('/root/data', [], ['ancient.csv', 'new.json']),
        ]

        # Mock os.path.isfile to confirm files exist
        def isfile_side_effect(path):
            return path in [
                '/root/recent.txt',
                '/root/old.log',
                '/root/data/ancient.csv',
                '/root/data/new.json'
            ]
        mock_os_isfile.side_effect = isfile_side_effect

        # Mock os.path.getmtime to control modification times
        def getmtime_side_effect(path):
            if path == '/root/recent.txt':
                return current_time - (5 * 24 * 60 * 60)  # 5 days old (not old enough for 10 days cutoff)
            elif path == '/root/old.log':
                return current_time - (15 * 24 * 60 * 60)  # 15 days old (old enough)
            elif path == '/root/data/ancient.csv':
                return current_time - (20 * 24 * 60 * 60) # 20 days old (old enough)
            elif path == '/root/data/new.json':
                return current_time - (2 * 24 * 60 * 60)   # 2 days old (not old enough)
            return current_time # Default for others
        mock_os_getmtime.side_effect = getmtime_side_effect

        expected_old_files = [
            '/root/old.log',
            '/root/data/ancient.csv'
        ]

        result = find_old_files('/root', 10) # Look for files older than 10 days
        self.assertCountEqual(result, expected_old_files)

    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_old_files_no_old_files(self, mock_os_walk, mock_os_isfile, mock_os_getmtime):
        # Mock rationale: Similar to the previous test, we need to simulate a scenario
        # where no files meet the 'old' criteria to ensure the function correctly returns
        # an empty list.

        current_time = time.time()

        mock_os_walk.side_effect = [
            ('/root', [], ['file1.txt', 'file2.txt']),
        ]

        def isfile_side_effect(path):
            return path in ['/root/file1.txt', '/root/file2.txt']
        mock_os_isfile.side_effect = isfile_side_effect

        def getmtime_side_effect(path):
            if path == '/root/file1.txt':
                return current_time - (5 * 24 * 60 * 60)
            elif path == '/root/file2.txt':
                return current_time - (8 * 24 * 60 * 60)
            return current_time
        mock_os_getmtime.side_effect = getmtime_side_effect

        result = find_old_files('/root', 10) # Look for files older than 10 days
        self.assertEqual(result, [])

    @patch('os.walk')
    def test_find_empty_dirs_no_empty_dirs(self, mock_os_walk):
        # Mock rationale: Simulate a filesystem where all directories contain files or subdirectories
        # to ensure the function correctly returns an empty list when no empty directories are found.
        mock_os_walk.side_effect = [
            ('/root', ['dir1'], ['file1.txt']),
            ('/root/dir1', [], ['subfile1.txt']),
        ]
        result = find_empty_dirs('/root')
        self.assertEqual(result, [])

    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_old_files_os_error(self, mock_os_walk, mock_os_isfile, mock_os_getmtime):
        # Mock rationale: Simulate an OSError during file access (e.g., permission denied)
        # to ensure the utility handles such exceptions gracefully and continues processing.

        current_time = time.time()
        mock_os_walk.side_effect = [
            ('/root', [], ['accessible.txt', 'inaccessible.txt']),
        ]

        def isfile_side_effect(path):
            return path in ['/root/accessible.txt', '/root/inaccessible.txt']
        mock_os_isfile.side_effect = isfile_side_effect

        def getmtime_side_effect(path):
            if path == '/root/accessible.txt':
                return current_time - (15 * 24 * 60 * 60) # Old and accessible
            elif path == '/root/inaccessible.txt':
                raise OSError("Permission denied") # Simulate error
            return current_time
        mock_os_getmtime.side_effect = getmtime_side_effect

        expected_old_files = ['/root/accessible.txt']
        result = find_old_files('/root', 10)
        self.assertCountEqual(result, expected_old_files)
