import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.getmtime, os.path.isdir)
# without actually touching the disk. This ensures tests are deterministic, fast, and isolated.

# Import the function to test
from src.sweeper import find_dust_bunnies, DustBunny

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a consistent 'current time' for tests to ensure determinism for age calculations.
        self.mock_current_time = datetime(2024, 1, 1, 12, 0, 0)
        self.old_mtime = (self.mock_current_time - timedelta(days=60)).timestamp()
        self.recent_mtime = (self.mock_current_time - timedelta(days=5)).timestamp()

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_empty_directory(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an empty folder.
        # os.walk will return the root and an empty subdirectory.
        # os.path.getmtime is mocked but not directly used for empty dir logic.
        # os.path.isdir is mocked to confirm the root path exists.
        mock_walk.return_value = [
            ('/root', ['empty_dir'], []), # Root contains 'empty_dir'
            ('/root/empty_dir', [], [])   # 'empty_dir' contains nothing
        ]
        mock_getmtime.return_value = self.recent_mtime # Not directly relevant for empty dir test

        bunnies = find_dust_bunnies('/root', current_time=self.mock_current_time)

        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0].type, 'empty directory')
        self.assertEqual(bunnies[0].path, '/root/empty_dir')

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_log_file(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with an old log file.
        # os.walk returns the log file.
        # os.path.getmtime is crucial here to return a timestamp older than 'age_days'.
        mock_walk.return_value = [
            ('/root/logs', [], ['old.log', 'recent.log'])
        ]
        # Mock getmtime to return different times for different files
        def getmtime_side_effect(path):
            if path == '/root/logs/old.log':
                return self.old_mtime
            elif path == '/root/logs/recent.log':
                return self.recent_mtime
            return self.recent_mtime # Default for other files

        mock_getmtime.side_effect = getmtime_side_effect

        bunnies = find_dust_bunnies('/root', age_days=30, current_time=self.mock_current_time)

        self.assertEqual(len(bunnies), 1)
        self.assertEqual(bunnies[0].type, 'old log file')
        self.assertEqual(bunnies[0].path, '/root/logs/old.log')
        self.assertIn('60 days', bunnies[0].rationale) # Check rationale reflects age

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_ignore_recent_log_file(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Ensure recent log files are not flagged.
        # os.walk returns a recent log file.
        # os.path.getmtime returns a timestamp newer than 'age_days'.
        mock_walk.return_value = [
            ('/root/logs', [], ['recent.log'])
        ]
        mock_getmtime.return_value = self.recent_mtime

        bunnies = find_dust_bunnies('/root', age_days=30, current_time=self.mock_current_time)

        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_temporary_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with various temporary files.
        # os.walk returns these files.
        mock_walk.return_value = [
            ('/root/src', [], ['main.py', '__pycache__', 'temp.tmp', 'backup.bak', 'swap.swp', '.DS_Store'])
        ]
        mock_getmtime.return_value = self.recent_mtime # Not directly relevant for temp file logic

        bunnies = find_dust_bunnies('/root', current_time=self.mock_current_time)

        self.assertEqual(len(bunnies), 5)
        temp_file_paths = {b.path for b in bunnies}
        self.assertIn('/root/src/__pycache__', temp_file_paths)
        self.assertIn('/root/src/temp.tmp', temp_file_paths)
        self.assertIn('/root/src/backup.bak', temp_file_paths)
        self.assertIn('/root/src/swap.swp', temp_file_paths)
        self.assertIn('/root/src/.DS_Store', temp_file_paths)

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_mixed_dust_bunnies(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a complex directory structure with all types of dust bunnies.
        # os.walk and os.path.getmtime are mocked to provide the necessary data.
        mock_walk.return_value = [
            ('/root', ['empty_dir', 'logs', 'src'], []), # Root
            ('/root/empty_dir', [], []), # Empty dir
            ('/root/logs', [], ['old.log', 'recent.log']), # Logs dir
            ('/root/src', [], ['main.py', '__pycache__', 'temp.tmp'])
        ]

        def getmtime_side_effect(path):
            if path == '/root/logs/old.log':
                return self.old_mtime
            elif path == '/root/logs/recent.log':
                return self.recent_mtime
            return self.recent_mtime

        mock_getmtime.side_effect = getmtime_side_effect

        bunnies = find_dust_bunnies('/root', age_days=30, current_time=self.mock_current_time)

        self.assertEqual(len(bunnies), 4) # 1 empty, 1 old log, 2 temp files
        types = [b.type for b in bunnies]
        paths = [b.path for b in bunnies]

        self.assertIn('empty directory', types)
        self.assertIn('/root/empty_dir', paths)

        self.assertIn('old log file', types)
        self.assertIn('/root/logs/old.log', paths)

        self.assertIn('temporary file', types)
        self.assertIn('/root/src/__pycache__', paths)
        self.assertIn('/root/src/temp.tmp', paths)

    @patch('os.path.isdir', MagicMock(return_value=False))
    def test_invalid_path(self, mock_isdir):
        # Mock rationale: Test the behavior when the provided root path is not a directory.
        # os.path.isdir is mocked to return False.
        bunnies = find_dust_bunnies('/nonexistent/path', current_time=self.mock_current_time)
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_directory_with_only_subdirs_is_not_empty(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: A directory containing only other directories (which might contain files) is not empty.
        mock_walk.return_value = [
            ('/root', ['subdir'], []), # Root has a subdir
            ('/root/subdir', [], ['file.txt']) # Subdir has a file
        ]
        mock_getmtime.return_value = self.recent_mtime

        bunnies = find_dust_bunnies('/root', current_time=self.mock_current_time)
        self.assertEqual(len(bunnies), 0) # No dust bunnies, as 'root' is not empty and 'subdir' is not empty

    @patch('os.path.isdir', MagicMock(return_value=True))
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_directory_with_only_empty_subdirs_are_flagged(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: A directory containing only empty subdirectories should not be flagged as empty itself,
        # but its empty subdirectories should be.
        mock_walk.return_value = [
            ('/root', ['subdir1', 'subdir2'], []), # Root has two subdirs
            ('/root/subdir1', [], []), # Subdir1 is empty
            ('/root/subdir2', [], [])  # Subdir2 is empty
        ]
        mock_getmtime.return_value = self.recent_mtime

        bunnies = find_dust_bunnies('/root', current_time=self.mock_current_time)
        self.assertEqual(len(bunnies), 2) # subdir1, subdir2 should be flagged as empty
        paths = {b.path for b in bunnies}
        self.assertNotIn('/root', paths) # Root itself is not empty, it contains subdirs
        self.assertIn('/root/subdir1', paths)
        self.assertIn('/root/subdir2', paths)

if __name__ == '__main__':
    unittest.main()
