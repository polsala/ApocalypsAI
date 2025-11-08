import unittest
from unittest.mock import patch, MagicMock
import os
import time
import io
import sys
from datetime import datetime, timedelta

# Import the functions to be tested
from src.collector import find_dust_bunnies, collect_dust_bunnies

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

        # Mock current time for deterministic age calculations
        # Mock rationale: Fixes the 'current time' for age calculations, making tests deterministic.
        self.mock_time = 1678886400.0  # March 15, 2023 12:00:00 PM UTC
        self.patcher_time = patch('time.time', return_value=self.mock_time)
        self.patcher_time.start()

    def tearDown(self):
        sys.stdout = self.held_stdout  # Restore stdout
        self.patcher_time.stop()

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_no_old_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure without creating actual files.
        mock_walk.return_value = [
            ('/mock/dir', ['subdir'], ['file1.txt', 'file2.log']),
            ('/mock/dir/subdir', [], ['subfile.txt'])
        ]

        # Mock rationale: Control modification times to ensure no files are older than threshold.
        # All files are 'new' (modified after the age threshold)
        mock_getmtime.side_effect = [
            self.mock_time - timedelta(days=10).total_seconds(), # file1.txt
            self.mock_time - timedelta(days=15).total_seconds(), # file2.log
            self.mock_time - timedelta(days=5).total_seconds()   # subfile.txt
        ]

        age_days = 20 # Files older than 20 days
        result = find_dust_bunnies('/mock/dir', age_days)
        self.assertEqual(result, [])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_old_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure without creating actual files.
        mock_walk.return_value = [
            ('/mock/dir', ['subdir'], ['old_file.txt', 'new_file.log']),
            ('/mock/dir/subdir', [], ['another_old.txt', 'current.py'])
        ]

        # Mock rationale: Control modification times to simulate old and new files.
        # old_file.txt and another_old.txt are older than 30 days
        mock_getmtime.side_effect = [
            self.mock_time - timedelta(days=40).total_seconds(), # old_file.txt (OLD)
            self.mock_time - timedelta(days=10).total_seconds(), # new_file.log (NEW)
            self.mock_time - timedelta(days=35).total_seconds(), # another_old.txt (OLD)
            self.mock_time - timedelta(days=5).total_seconds()    # current.py (NEW)
        ]

        age_days = 30 # Files older than 30 days
        result = find_dust_bunnies('/mock/dir', age_days)
        expected_files = [
            '/mock/dir/old_file.txt',
            '/mock/dir/subdir/another_old.txt'
        ]
        self.assertCountEqual(result, expected_files)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_exclusion_patterns(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure without creating actual files.
        mock_walk.return_value = [
            ('/mock/dir', ['temp_data', 'logs'], ['old_report.csv', 'config.ini']),
            ('/mock/dir/temp_data', [], ['temp_file.tmp', 'another_temp.txt']),
            ('/mock/dir/logs', [], ['error.log', 'access.log'])
        ]

        # Mock rationale: Control modification times to simulate old files.
        # All files are old, but some should be excluded by pattern.
        old_timestamp = self.mock_time - timedelta(days=100).total_seconds()
        mock_getmtime.side_effect = [
            old_timestamp, # old_report.csv
            old_timestamp, # config.ini
            old_timestamp, # temp_file.tmp
            old_timestamp, # another_temp.txt
            old_timestamp, # error.log
            old_timestamp  # access.log
        ]

        age_days = 50
        exclude_patterns = ['*.tmp', '*/logs/*', '/mock/dir/temp_data/another_temp.txt']
        result = find_dust_bunnies('/mock/dir', age_days, exclude_patterns)

        expected_files = [
            '/mock/dir/old_report.csv',
            '/mock/dir/config.ini'
        ]
        self.assertCountEqual(result, expected_files)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_excluded_directory(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure with an excluded directory.
        mock_walk.return_value = [
            ('/mock/dir', ['important_data', 'temp_logs'], ['file1.txt']),
            ('/mock/dir/important_data', [], ['data.db'])
            # Note: /mock/dir/temp_logs will not be walked into if excluded
        ]

        old_timestamp = self.mock_time - timedelta(days=100).total_seconds()
        mock_getmtime.side_effect = [
            old_timestamp, # file1.txt
            old_timestamp  # data.db
        ]

        age_days = 50
        exclude_patterns = ['*/temp_logs*'] # Exclude the directory itself
        result = find_dust_bunnies('/mock/dir', age_days, exclude_patterns)

        expected_files = [
            '/mock/dir/file1.txt',
            '/mock/dir/important_data/data.db'
        ]
        self.assertCountEqual(result, expected_files)

        # Ensure os.walk was called with the modified dirnames
        # This is a bit tricky to assert directly on the modified list in os.walk
        # but the result implicitly confirms it.

    @patch('os.path.isdir', return_value=False)
    def test_find_dust_bunnies_invalid_directory(self, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        result = find_dust_bunnies('/nonexistent/dir', 30)
        self.assertEqual(result, [])
        self.assertIn("Error: Directory not found", self.mock_stdout.getvalue())

    def test_collect_dust_bunnies_dry_run(self):
        files_to_collect = ['/path/to/old_file1.txt', '/path/to/old_file2.log']
        collect_dust_bunnies(files_to_collect, dry_run=True)

        output = self.mock_stdout.getvalue()
        self.assertIn("Identified 2 cosmic dust bunnies that would be collected (deleted)", output)
        self.assertIn("  - /path/to/old_file1.txt", output)
        self.assertIn("  - /path/to/old_file2.log", output)
        self.assertIn("💡 Run with `--collect` to permanently remove these files. 💡", output)
        self.assertNotIn("[COLLECTED]", output)

    @patch('os.remove')
    def test_collect_dust_bunnies_actual_collection(self, mock_remove):
        # Mock rationale: Prevent actual file deletion during tests.
        files_to_collect = ['/path/to/old_file1.txt', '/path/to/old_file2.log']
        collect_dust_bunnies(files_to_collect, dry_run=False)

        output = self.mock_stdout.getvalue()
        self.assertIn("Identified 2 cosmic dust bunnies that are being collected (deleted)", output)
        self.assertIn("  - /path/to/old_file1.txt", output)
        self.assertIn("  - /path/to/old_file2.log", output)
        self.assertIn("[COLLECTED] /path/to/old_file1.txt", output)
        self.assertIn("[COLLECTED] /path/to/old_file2.log", output)
        self.assertIn("🧹 Collection complete! Your digital realm is a bit cleaner. 🧹", output)
        mock_remove.assert_any_call('/path/to/old_file1.txt')
        mock_remove.assert_any_call('/path/to/old_file2.log')
        self.assertEqual(mock_remove.call_count, 2)

    @patch('os.remove', side_effect=OSError("Permission denied"))
    def test_collect_dust_bunnies_collection_error(self, mock_remove):
        # Mock rationale: Simulate a file deletion error (e.g., permission denied).
        files_to_collect = ['/path/to/protected_file.txt']
        collect_dust_bunnies(files_to_collect, dry_run=False)

        output = self.mock_stdout.getvalue()
        self.assertIn("Identified 1 cosmic dust bunnies that are being collected (deleted)", output)
        self.assertIn("  - /path/to/protected_file.txt", output)
        self.assertIn("[ERROR] Failed to collect /path/to/protected_file.txt: Permission denied", output)
        mock_remove.assert_called_once_with('/path/to/protected_file.txt')

    def test_collect_dust_bunnies_no_files(self):
        collect_dust_bunnies([], dry_run=True)
        output = self.mock_stdout.getvalue()
        self.assertIn("✨ No cosmic dust bunnies found! Your digital space is pristine. ✨", output)
