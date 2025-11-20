import unittest
import os
import sys
import io
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to import sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_days(self, mock_datetime, mock_getmtime):
        # Mock rationale: `os.path.getmtime` returns a timestamp, and `datetime.datetime.now()` returns the current time.
        # We need to control these to ensure deterministic age calculation for testing.
        
        # Scenario 1: File is 10 days old
        mock_getmtime.return_value = (datetime(2023, 1, 1) - timedelta(days=10)).timestamp()
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Allow actual conversion
        
        self.assertEqual(sweeper.get_file_age_days("dummy_path"), 10)

        # Scenario 2: File is 0 days old (today)
        mock_getmtime.return_value = datetime(2023, 1, 1).timestamp()
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        self.assertEqual(sweeper.get_file_age_days("dummy_path"), 0)

        # Scenario 3: File not found
        mock_getmtime.side_effect = FileNotFoundError
        self.assertEqual(sweeper.get_file_age_days("non_existent_path"), -1)
        mock_getmtime.side_effect = None # Reset mock

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('sweeper.get_file_age_days')
    def test_find_dust_bunnies(self, mock_get_file_age_days, mock_os_walk, mock_os_isdir):
        # Mock rationale: `os.path.isdir` checks if a directory exists. `os.walk` simulates traversing a directory structure.
        # `sweeper.get_file_age_days` is already tested and needs to return controlled ages.
        # We need to control these to simulate different file system states and file ages.

        mock_os_isdir.return_value = True # Assume all specified dirs exist

        # Setup mock_os_walk to simulate a directory structure
        # root, dirs, files
        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'recent_tmp.tmp', 'old_data.txt', 'other.file', 'old_backup.bak']),
            ('/test_dir/subdir', [], ['another_old.log', 'new_file.txt'])
        ]

        # Setup mock_get_file_age_days for specific files
        def mock_age_side_effect(filepath):
            if 'old_log.log' in filepath: return 35
            if 'recent_tmp.tmp' in filepath: return 10
            if 'old_data.txt' in filepath: return 40
            if 'other.file' in filepath: return 50
            if 'old_backup.bak' in filepath: return 60
            if 'another_old.log' in filepath: return 45
            if 'new_file.txt' in filepath: return 5
            return 0 # Default for unexpected files

        mock_get_file_age_days.side_effect = mock_age_side_effect

        # Test 1: Basic cleanup, age 30, specific patterns
        bunnies = sweeper.find_dust_bunnies(
            directories=['/test_dir'],
            age_threshold_days=30,
            patterns=['*.log', '*.tmp']
        )
        expected_bunnies = [
            os.path.join('/test_dir', 'old_log.log'),
            os.path.join('/test_dir/subdir', 'another_old.log')
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        # Test 2: All files, age 30
        bunnies = sweeper.find_dust_bunnies(
            directories=['/test_dir'],
            age_threshold_days=30,
            patterns=['*']
        )
        expected_bunnies = [
            os.path.join('/test_dir', 'old_log.log'),
            os.path.join('/test_dir', 'old_data.txt'),
            os.path.join('/test_dir', 'other.file'),
            os.path.join('/test_dir', 'old_backup.bak'),
            os.path.join('/test_dir/subdir', 'another_old.log')
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        # Test 3: No files match age
        bunnies = sweeper.find_dust_bunnies(
            directories=['/test_dir'],
            age_threshold_days=100, # Very high age threshold
            patterns=['*']
        )
        self.assertEqual(bunnies, [])

        # Test 4: Non-existent directory
        mock_os_isdir.side_effect = lambda path: path != '/non_existent'
        captured_output = io.StringIO()
        sys.stdout = captured_output
        bunnies = sweeper.find_dust_bunnies(
            directories=['/test_dir', '/non_existent'],
            age_threshold_days=30,
            patterns=['*']
        )
        sys.stdout = sys.__stdout__
        self.assertIn("Warning: Directory not found or not accessible: /non_existent. Skipping.", captured_output.getvalue())
        self.assertGreater(len(bunnies), 0) # Should still find bunnies in /test_dir

    @patch('os.remove')
    @patch('sweeper.get_file_age_days') # To avoid actual age calculation during sweep output
    def test_sweep_dust_bunnies_dry_run(self, mock_get_file_age_days, mock_os_remove):
        # Mock rationale: `os.remove` is the core action of the sweeper. We must mock it to prevent actual file deletion.
        # `sweeper.get_file_age_days` is mocked to provide consistent output for the print statements.

        mock_get_file_age_days.return_value = 42 # Consistent age for output
        file_list = ['/path/to/file1.log', '/path/to/file2.tmp']
        
        captured_output = io.StringIO()
        sys.stdout = captured_output

        sweeper.sweep_dust_bunnies(file_list, dry_run=True)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("DRY RUN: Files that would be deleted", output)
        self.assertIn("[DRY RUN] Would delete: /path/to/file1.log (Age: 42 days)", output)
        self.assertIn("[DRY RUN] Would delete: /path/to/file2.tmp (Age: 42 days)", output)
        self.assertIn("Total files identified: 2", output)
        mock_os_remove.assert_not_called()

    @patch('os.remove')
    @patch('sweeper.get_file_age_days') # To avoid actual age calculation during sweep output
    def test_sweep_dust_bunnies_actual_run(self, mock_get_file_age_days, mock_os_remove):
        # Mock rationale: `os.remove` is the core action of the sweeper. We must mock it to prevent actual file deletion.
        # `sweeper.get_file_age_days` is mocked to provide consistent output for the print statements.

        mock_get_file_age_days.return_value = 42 # Consistent age for output
        file_list = ['/path/to/file1.log', '/path/to/file2.tmp']
        
        captured_output = io.StringIO()
        sys.stdout = captured_output

        sweeper.sweep_dust_bunnies(file_list, dry_run=False)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("DELETING Files", output)
        self.assertIn("Deleted: /path/to/file1.log", output)
        self.assertIn("Deleted: /path/to/file2.tmp", output)
        self.assertIn("Total files processed: 2", output)
        mock_os_remove.assert_called_with('/path/to/file1.log')
        mock_os_remove.assert_called_with('/path/to/file2.tmp')
        self.assertEqual(mock_os_remove.call_count, 2)

    @patch('os.remove')
    @patch('sweeper.get_file_age_days')
    def test_sweep_dust_bunnies_no_files(self, mock_get_file_age_days, mock_os_remove):
        # Mock rationale: `os.remove` is the core action of the sweeper. We must mock it to prevent actual file deletion.
        # `sweeper.get_file_age_days` is mocked to provide consistent output for the print statements.

        captured_output = io.StringIO()
        sys.stdout = captured_output

        sweeper.sweep_dust_bunnies([], dry_run=True)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("No digital dust bunnies found to sweep!", output)
        mock_os_remove.assert_not_called()

    @patch('os.remove')
    @patch('sweeper.get_file_age_days')
    def test_sweep_dust_bunnies_deletion_error(self, mock_get_file_age_days, mock_os_remove):
        # Mock rationale: `os.remove` is the core action of the sweeper. We must mock it to prevent actual file deletion.
        # We simulate an OSError to ensure error handling is correct.
        # `sweeper.get_file_age_days` is mocked to provide consistent output for the print statements.

        mock_os_remove.side_effect = OSError("Permission denied")
        mock_get_file_age_days.return_value = 42
        file_list = ['/path/to/unwritable_file.log']

        captured_output = io.StringIO()
        sys.stdout = captured_output

        sweeper.sweep_dust_bunnies(file_list, dry_run=False)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error deleting /path/to/unwritable_file.log: Permission denied", output)
        mock_os_remove.assert_called_once_with('/path/to/unwritable_file.log')


if __name__ == '__main__':
    unittest.main()
