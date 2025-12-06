import unittest
from unittest.mock import patch, mock_open, call
import os
import time
from datetime import datetime, timedelta

# Import the functions from the forager script
# Assuming forager.py is in src/ and tests/ is at the same level as src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from forager import find_forgotten_files, delete_files

class TestForgottenFileForager(unittest.TestCase):

    # Mock rationale: We need to control the current time for age calculations
    # without relying on the actual system clock, ensuring deterministic tests.
    @patch('forager.datetime')
    def test_find_forgotten_files_basic(self, mock_datetime):
        # Mock rationale: Simulate a fixed current time for consistent age calculations.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_datetime.timedelta = timedelta # Use real timedelta

        # Mock rationale: Simulate the file system structure and modification times
        # without actual disk I/O, ensuring tests are fast, isolated, and deterministic.
        mock_walk_data = [
            ('/mock/path', [], ['old_file.txt', 'new_file.log', 'temp.tmp']),
            ('/mock/path/subdir', [], ['another_old.txt'])
        ]
        # Mock rationale: Simulate os.path.getmtime for specific files.
        mock_mtime_map = {
            '/mock/path/old_file.txt': (datetime(2023, 9, 1, 9, 0, 0)).timestamp(), # Older than 30 days
            '/mock/path/new_file.log': (datetime(2023, 10, 20, 9, 0, 0)).timestamp(), # Newer than 30 days
            '/mock/path/temp.tmp': (datetime(2023, 9, 15, 9, 0, 0)).timestamp(), # Older than 30 days
            '/mock/path/subdir/another_old.txt': (datetime(2023, 8, 1, 9, 0, 0)).timestamp(), # Older than 30 days
        }

        with patch('os.walk', return_value=mock_walk_data),
             patch('os.path.isdir', return_value=True),
             patch('os.path.isfile', side_effect=lambda p: p in mock_mtime_map),
             patch('os.path.getmtime', side_effect=lambda p: mock_mtime_map.get(p, 0)):

            # Test with no patterns
            forgotten = find_forgotten_files('/mock/path', 30)
            expected = [
                '/mock/path/old_file.txt',
                '/mock/path/temp.tmp',
                '/mock/path/subdir/another_old.txt'
            ]
            self.assertCountEqual(forgotten, expected)

            # Test with patterns
            forgotten_patterns = find_forgotten_files('/mock/path', 30, patterns=['*.txt'])
            expected_patterns = [
                '/mock/path/old_file.txt',
                '/mock/path/subdir/another_old.txt'
            ]
            self.assertCountEqual(forgotten_patterns, expected_patterns)

            # Test with a pattern that includes path separators (e.g., for __pycache__)
            mock_walk_data_with_cache = [
                ('/mock/path', [], ['file.txt']),
                ('/mock/path/__pycache__', [], ['cache_file.pyc']),
                ('/mock/path/other_dir', [], ['another_file.txt'])
            ]
            mock_mtime_map_with_cache = {
                '/mock/path/file.txt': (datetime(2023, 9, 1, 9, 0, 0)).timestamp(),
                '/mock/path/__pycache__/cache_file.pyc': (datetime(2023, 9, 1, 9, 0, 0)).timestamp(),
                '/mock/path/other_dir/another_file.txt': (datetime(2023, 9, 1, 9, 0, 0)).timestamp(),
            }
            with patch('os.walk', return_value=mock_walk_data_with_cache),
                 patch('os.path.isfile', side_effect=lambda p: p in mock_mtime_map_with_cache),
                 patch('os.path.getmtime', side_effect=lambda p: mock_mtime_map_with_cache.get(p, 0)):
                forgotten_cache = find_forgotten_files('/mock/path', 30, patterns=['__pycache__/*'])
                expected_cache = [
                    '/mock/path/__pycache__/cache_file.pyc'
                ]
                self.assertCountEqual(forgotten_cache, expected_cache)

    # Mock rationale: We need to control the current time for age calculations
    # without relying on the actual system clock, ensuring deterministic tests.
    @patch('forager.datetime')
    def test_find_forgotten_files_no_old_files(self, mock_datetime):
        # Mock rationale: Simulate a fixed current time for consistent age calculations.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate the file system structure and modification times.
        mock_walk_data = [
            ('/mock/path', [], ['new_file1.txt', 'new_file2.log'])
        ]
        # Mock rationale: Simulate os.path.getmtime for specific files.
        mock_mtime_map = {
            '/mock/path/new_file1.txt': (datetime(2023, 10, 25, 9, 0, 0)).timestamp(), # Newer than 30 days
            '/mock/path/new_file2.log': (datetime(2023, 10, 24, 9, 0, 0)).timestamp(), # Newer than 30 days
        }

        with patch('os.walk', return_value=mock_walk_data),
             patch('os.path.isdir', return_value=True),
             patch('os.path.isfile', side_effect=lambda p: p in mock_mtime_map),
             patch('os.path.getmtime', side_effect=lambda p: mock_mtime_map.get(p, 0)):

            forgotten = find_forgotten_files('/mock/path', 30)
            self.assertEqual(forgotten, [])

    # Mock rationale: We need to control the current time for age calculations
    # without relying on the actual system clock, ensuring deterministic tests.
    @patch('forager.datetime')
    def test_find_forgotten_files_empty_directory(self, mock_datetime):
        # Mock rationale: Simulate a fixed current time for consistent age calculations.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate an empty directory structure.
        mock_walk_data = [
            ('/mock/empty_path', [], [])
        ]

        with patch('os.walk', return_value=mock_walk_data),
             patch('os.path.isdir', return_value=True),
             patch('os.path.isfile', return_value=False),
             patch('os.path.getmtime', return_value=0):

            forgotten = find_forgotten_files('/mock/empty_path', 30)
            self.assertEqual(forgotten, [])

    # Mock rationale: Simulate os.remove without actually deleting files on the disk,
    # ensuring tests are safe, isolated, and deterministic.
    @patch('os.remove')
    def test_delete_files_success(self, mock_os_remove):
        files_to_delete = ['/path/to/file1.txt', '/path/to/file2.log']
        delete_files(files_to_delete)
        mock_os_remove.assert_has_calls([
            call('/path/to/file1.txt'),
            call('/path/to/file2.log')
        ], any_order=True)
        self.assertEqual(mock_os_remove.call_count, 2)

    # Mock rationale: Simulate os.remove failing for some files without actual disk I/O errors,
    # ensuring tests are safe, isolated, and deterministic.
    @patch('os.remove', side_effect=[None, OSError("Permission denied"), None])
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_delete_files_with_errors(self, mock_print, mock_os_remove):
        files_to_delete = ['/path/to/file1.txt', '/path/to/file2.log', '/path/to/file3.tmp']
        delete_files(files_to_delete, verbose=True)

        mock_os_remove.assert_has_calls([
            call('/path/to/file1.txt'),
            call('/path/to/file2.log'),
            call('/path/to/file3.tmp')
        ], any_order=True)
        self.assertEqual(mock_os_remove.call_count, 3)
        # Check if error message was printed
        mock_print.assert_any_call("Error deleting /path/to/file2.log: Permission denied")

    # Mock rationale: Simulate os.remove not being called when the list is empty.
    @patch('os.remove')
    def test_delete_files_empty_list(self, mock_os_remove):
        delete_files([])
        mock_os_remove.assert_not_called()

    # Mock rationale: Simulate a non-existent root path without actual file system checks.
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_find_forgotten_files_invalid_path(self, mock_print, mock_isdir):
        forgotten = find_forgotten_files('/nonexistent/path', 30)
        self.assertEqual(forgotten, [])
        mock_print.assert_any_call("Error: Path '/nonexistent/path' is not a valid directory.")

if __name__ == '__main__':
    unittest.main()
