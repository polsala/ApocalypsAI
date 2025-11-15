import unittest
from unittest.mock import patch, MagicMock
import os
import time
import datetime
from utils.digital_dust_bunny_sweeper.src import sweeper

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a base time for mocking os.path.getmtime
        self.now = time.time()
        self.thirty_days_ago = self.now - (30 * 24 * 60 * 60)
        self.sixty_days_ago = self.now - (60 * 24 * 60 * 60)
        self.ten_days_ago = self.now - (10 * 24 * 60 * 60)

    @patch('os.walk')
    def test_find_empty_dirs_with_empty_and_non_empty(self, mock_os_walk):
        # Mock rationale: Simulate a filesystem structure with empty and non-empty directories
        # to test if find_empty_dirs correctly identifies only the empty ones.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir1'], ['file1.txt']),
            ('/root/dir1', ['subdir1'], ['file2.txt']),
            ('/root/dir1/subdir1', [], ['file3.txt']),
            ('/root/dir2', [], ['file4.txt']),
            ('/root/empty_dir1', [], []),
            ('/root/dir1/empty_subdir2', [], []),
        ]
        
        expected_empty_dirs = [
            '/root/empty_dir1',
            '/root/dir1/empty_subdir2',
        ]
        
        result = sweeper.find_empty_dirs('/root')
        self.assertCountEqual(result, expected_empty_dirs)

    @patch('os.walk')
    def test_find_empty_dirs_no_empty_dirs(self, mock_os_walk):
        # Mock rationale: Simulate a filesystem with no empty directories
        # to ensure the function returns an empty list.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/dir2', ['subdir1'], ['file3.txt']),
            ('/root/dir2/subdir1', [], ['file4.txt']),
        ]
        
        result = sweeper.find_empty_dirs('/root')
        self.assertEqual(result, [])

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_old_files_with_various_files(self, mock_os_walk, mock_getmtime, mock_isfile):
        # Mock rationale: Simulate a filesystem with files of different ages and patterns.
        # Mock os.path.getmtime to control file modification times deterministically.
        # Mock os.path.isfile to ensure only files are considered.
        mock_os_walk.return_value = [
            ('/root', [], ['old.log', 'recent.log', 'old.tmp', 'recent.txt', 'another.bak']),
            ('/root/subdir', [], ['very_old.log', 'current.tmp']),
        ]

        # Map file paths to their mocked modification times
        mtime_map = {
            '/root/old.log': self.sixty_days_ago,
            '/root/recent.log': self.ten_days_ago,
            '/root/old.tmp': self.sixty_days_ago,
            '/root/recent.txt': self.sixty_days_ago, # Not a target pattern
            '/root/another.bak': self.thirty_days_ago - 1, # Just older than 30 days
            '/root/subdir/very_old.log': self.sixty_days_ago,
            '/root/subdir/current.tmp': self.ten_days_ago,
        }

        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now)

        # Test with default age (30 days) and default patterns
        patterns = ['*.log', '*.tmp', '*.bak']
        result = sweeper.find_old_files('/root', 30, patterns)
        expected_old_files = [
            '/root/old.log',
            '/root/old.tmp',
            '/root/another.bak',
            '/root/subdir/very_old.log',
        ]
        self.assertCountEqual(result, expected_old_files)

        # Test with a different age (e.g., 60 days)
        result_60_days = sweeper.find_old_files('/root', 60, patterns)
        expected_old_files_60_days = [
            '/root/old.log',
            '/root/old.tmp',
            '/root/subdir/very_old.log',
        ]
        self.assertCountEqual(result_60_days, expected_old_files_60_days)

        # Test with different patterns
        patterns_only_log = ['*.log']
        result_only_log = sweeper.find_old_files('/root', 30, patterns_only_log)
        expected_only_log = [
            '/root/old.log',
            '/root/subdir/very_old.log',
        ]
        self.assertCountEqual(result_only_log, expected_only_log)

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_old_files_no_old_files(self, mock_os_walk, mock_getmtime, mock_isfile):
        # Mock rationale: Simulate a filesystem where all files are recent or don't match patterns.
        # This ensures the function correctly returns an empty list when no 'dust bunnies' are found.
        mock_os_walk.return_value = [
            ('/root', [], ['recent.log', 'current.tmp', 'important.txt']),
        ]
        mtime_map = {
            '/root/recent.log': self.ten_days_ago,
            '/root/current.tmp': self.ten_days_ago,
            '/root/important.txt': self.sixty_days_ago, # Old but not a target pattern
        }
        mock_getmtime.side_effect = lambda path: mtime_map.get(path, self.now)

        patterns = ['*.log', '*.tmp']
        result = sweeper.find_old_files('/root', 30, patterns)
        self.assertEqual(result, [])

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_old_files_ignores_non_files(self, mock_os_walk, mock_getmtime, mock_isfile):
        # Mock rationale: Ensure that the utility correctly ignores non-file entries
        # (like directories or broken symlinks) even if they match patterns.
        mock_os_walk.return_value = [
            ('/root', [], ['broken_link.log']),
        ]
        # os.path.isfile is mocked to return False, so this should not be found
        result = sweeper.find_old_files('/root', 30, ['*.log'])
        self.assertEqual(result, [])

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime', side_effect=OSError("Permission denied"))
    @patch('os.walk')
    def test_find_old_files_handles_os_error(self, mock_os_walk, mock_getmtime, mock_isfile):
        # Mock rationale: Simulate a scenario where os.path.getmtime raises an OSError
        # (e.g., due to permission issues). The utility should gracefully handle this
        # and not include the problematic file in the results.
        mock_os_walk.return_value = [
            ('/root', [], ['inaccessible.log']),
        ]
        result = sweeper.find_old_files('/root', 30, ['*.log'])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
