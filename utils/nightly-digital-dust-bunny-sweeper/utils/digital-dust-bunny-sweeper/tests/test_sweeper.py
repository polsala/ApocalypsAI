import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import find_dust_bunnies, sweep_dust_bunnies

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: time.time is mocked to fix the 'current time' for age calculations,
        # ensuring deterministic results regardless of when the test is run.
        self.mock_time = patch('time.time', return_value=datetime(2023, 10, 26, 12, 0, 0).timestamp())
        self.mock_time.start()
        self.addCleanup(self.mock_time.stop)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_by_age(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.walk is mocked to simulate a directory structure and files
        # without creating actual files, ensuring tests are fast, isolated, and deterministic.
        mock_walk.return_value = [
            ('/mock/dir', [], ['old_file.log', 'new_file.txt', 'another_old.tmp'])
        ]

        # Mock rationale: os.path.getmtime is mocked to control the modification time of
        # simulated files, allowing precise testing of age-based filtering.
        # Current time is 2023-10-26. Cutoff for 30 days is 2023-09-26.
        old_timestamp = (datetime(2023, 9, 1, 10, 0, 0)).timestamp() # Older than 30 days
        new_timestamp = (datetime(2023, 10, 20, 10, 0, 0)).timestamp() # Newer than 30 days

        def getmtime_side_effect(path):
            if 'old_file.log' in path or 'another_old.tmp' in path:
                return old_timestamp
            elif 'new_file.txt' in path:
                return new_timestamp
            return new_timestamp # Default for safety

        mock_getmtime.side_effect = getmtime_side_effect

        paths = ['/mock/dir']
        age_days = 30
        patterns = [] # No patterns, all old files should be found

        result = find_dust_bunnies(paths, age_days, patterns)
        self.assertIn('/mock/dir/old_file.log', result)
        self.assertIn('/mock/dir/another_old.tmp', result)
        self.assertNotIn('/mock/dir/new_file.txt', result)
        self.assertEqual(len(result), 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_patterns(self, mock_getmtime, mock_walk, mock_isdir):
        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.log', 'file2.tmp', 'file3.txt', 'file4.bak'])
        ]

        # All files are old enough (e.g., 60 days old)
        old_timestamp = (datetime(2023, 8, 1, 10, 0, 0)).timestamp()
        mock_getmtime.return_value = old_timestamp

        paths = ['/mock/dir']
        age_days = 30
        patterns = ['*.log', '*.bak']

        result = find_dust_bunnies(paths, age_days, patterns)
        self.assertIn('/mock/dir/file1.log', result)
        self.assertIn('/mock/dir/file4.bak', result)
        self.assertNotIn('/mock/dir/file2.tmp', result)
        self.assertNotIn('/mock/dir/file3.txt', result)
        self.assertEqual(len(result), 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_no_matching_files(self, mock_getmtime, mock_walk, mock_isdir):
        mock_walk.return_value = [
            ('/mock/dir', [], ['new_file.txt', 'another_new.log'])
        ]

        # All files are newer than the cutoff
        new_timestamp = (datetime(2023, 10, 20, 10, 0, 0)).timestamp()
        mock_getmtime.return_value = new_timestamp

        paths = ['/mock/dir']
        age_days = 30
        patterns = []

        result = find_dust_bunnies(paths, age_days, patterns)
        self.assertEqual(len(result), 0)

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_find_dust_bunnies_invalid_path(self, mock_print, mock_isdir):
        paths = ['/non/existent/dir']
        age_days = 30
        patterns = []

        result = find_dust_bunnies(paths, age_days, patterns)
        self.assertEqual(len(result), 0)
        mock_print.assert_called_with("Warning: Path '/non/existent/dir' is not a directory or does not exist. Skipping.")

    @patch('os.remove')
    @patch('builtins.print')
    def test_sweep_dust_bunnies_dry_run(self, mock_print, mock_remove):
        file_list = ['/mock/dir/old_file1.log', '/mock/dir/old_file2.tmp']
        sweep_dust_bunnies(file_list, dry_run=True)

        # Mock rationale: os.remove is mocked to prevent actual file deletion.
        # In dry run, os.remove should not be called.
        mock_remove.assert_not_called()
        mock_print.assert_any_call("[DRY RUN] Would delete: /mock/dir/old_file1.log")
        mock_print.assert_any_call("[DRY RUN] Would delete: /mock/dir/old_file2.tmp")

    @patch('os.remove')
    @patch('builtins.print')
    def test_sweep_dust_bunnies_delete(self, mock_print, mock_remove):
        file_list = ['/mock/dir/old_file1.log', '/mock/dir/old_file2.tmp']
        sweep_dust_bunnies(file_list, dry_run=False)

        # Mock rationale: os.remove is mocked to prevent actual file deletion.
        # It should be called for each file in the list.
        mock_remove.assert_any_call('/mock/dir/old_file1.log')
        mock_remove.assert_any_call('/mock/dir/old_file2.tmp')
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("Deleted: /mock/dir/old_file1.log")
        mock_print.assert_any_call("Deleted: /mock/dir/old_file2.tmp")
        mock_print.assert_any_call("Successfully swept away 2 dust bunnies.")

    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('builtins.print')
    def test_sweep_dust_bunnies_delete_with_error(self, mock_print, mock_remove):
        file_list = ['/mock/dir/old_file1.log']
        sweep_dust_bunnies(file_list, dry_run=False)

        mock_remove.assert_called_once_with('/mock/dir/old_file1.log')
        mock_print.assert_any_call("Error deleting '/mock/dir/old_file1.log': Permission denied")
        mock_print.assert_any_call("Successfully swept away 0 dust bunnies.")

    @patch('os.remove')
    @patch('builtins.print')
    def test_sweep_dust_bunnies_empty_list(self, mock_print, mock_remove):
        file_list = []
        sweep_dust_bunnies(file_list, dry_run=False)

        mock_remove.assert_not_called()
        mock_print.assert_called_once_with("No digital dust bunnies found to sweep.")
