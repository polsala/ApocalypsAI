import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the collector script
# Assuming collector.py is in src/ and tests/ is at the same level as src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from collector import find_dust_bunnies, clean_dust_bunnies
sys.path.pop(0)

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Set a fixed 'now' for deterministic age calculations
        self.fixed_now = datetime(2023, 10, 26, 10, 0, 0) # October 26, 2023, 10:00:00
        self.fixed_now_timestamp = self.fixed_now.timestamp()

    @patch('os.walk')
    @patch('os.path.islink', return_value=False) # Mock rationale: Prevent actual symlink checks
    @patch('os.path.getmtime')
    @patch('time.time') # Mock rationale: Control the 'current time' for age calculations
    def test_find_dust_bunnies_patterns(self, mock_time, mock_getmtime, mock_islink, mock_walk):
        # Mock rationale: Ensure deterministic time for age calculations.
        mock_time.return_value = self.fixed_now_timestamp

        # Mock rationale: Simulate file system structure without actual files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'temp.tmp', 'log.log', 'backup.bak', '.~lock.txt', 'old_file.txt']),
            ('/test_dir/subdir', [], ['another.tmp', 'data.csv', 'config.ini'])
        ]

        # Mock rationale: Provide deterministic modification times for files.
        # All files are 'old' enough for default age=0, but we can control for specific age tests.
        mock_getmtime.side_effect = lambda x: self.fixed_now_timestamp - (10 * 24 * 60 * 60) # 10 days old

        # Test with default patterns
        bunnies = find_dust_bunnies('/test_dir', ['*.tmp', '*.log', '*.bak', '.~*'])
        expected = [
            os.path.join('/test_dir', 'temp.tmp'),
            os.path.join('/test_dir', 'log.log'),
            os.path.join('/test_dir', 'backup.bak'),
            os.path.join('/test_dir', '.~lock.txt'),
            os.path.join('/test_dir/subdir', 'another.tmp')
        ]
        self.assertCountEqual(bunnies, expected)

        # Test with custom patterns
        bunnies = find_dust_bunnies('/test_dir', ['*.txt'])
        expected = [
            os.path.join('/test_dir', 'file1.txt'),
            os.path.join('/test_dir', 'old_file.txt')
        ]
        self.assertCountEqual(bunnies, expected)

    @patch('os.walk')
    @patch('os.path.islink', return_value=False) # Mock rationale: Prevent actual symlink checks
    @patch('os.path.getmtime')
    @patch('time.time') # Mock rationale: Control the 'current time' for age calculations
    def test_find_dust_bunnies_age_filter(self, mock_time, mock_getmtime, mock_islink, mock_walk):
        mock_time.return_value = self.fixed_now_timestamp

        # Mock rationale: Simulate file system structure.
        mock_walk.return_value = [
            ('/test_dir', [], ['old.tmp', 'recent.tmp', 'very_old.log'])
        ]

        # Mock rationale: Define specific modification times for files.
        # old.tmp: 10 days old
        # recent.tmp: 1 day old
        # very_old.log: 60 days old
        file_mtimes = {
            os.path.join('/test_dir', 'old.tmp'): self.fixed_now_timestamp - (10 * 24 * 60 * 60),
            os.path.join('/test_dir', 'recent.tmp'): self.fixed_now_timestamp - (1 * 24 * 60 * 60),
            os.path.join('/test_dir', 'very_old.log'): self.fixed_now_timestamp - (60 * 24 * 60 * 60),
        }
        mock_getmtime.side_effect = lambda x: file_mtimes.get(x, self.fixed_now_timestamp) # Default to 'now' if not specified

        # Test with age filter 5 days (should find old.tmp and very_old.log)
        bunnies = find_dust_bunnies('/test_dir', ['*.tmp', '*.log'], min_age_days=5)
        expected = [
            os.path.join('/test_dir', 'old.tmp'),
            os.path.join('/test_dir', 'very_old.log')
        ]
        self.assertCountEqual(bunnies, expected)

        # Test with age filter 20 days (should find very_old.log only)
        bunnies = find_dust_bunnies('/test_dir', ['*.tmp', '*.log'], min_age_days=20)
        expected = [
            os.path.join('/test_dir', 'very_old.log')
        ]
        self.assertCountEqual(bunnies, expected)

        # Test with age filter 90 days (should find nothing)
        bunnies = find_dust_bunnies('/test_dir', ['*.tmp', '*.log'], min_age_days=90)
        self.assertEqual(bunnies, [])

    @patch('os.remove')
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_clean_dust_bunnies_dry_run(self, mock_print, mock_remove):
        dust_bunnies = [
            os.path.join('/test_dir', 'file1.tmp'),
            os.path.join('/test_dir', 'file2.log')
        ]

        processed_count = clean_dust_bunnies(dust_bunnies, dry_run=True, verbose=True)

        self.assertEqual(processed_count, 2)
        mock_remove.assert_not_called() # Mock rationale: Ensure no actual deletion in dry run.
        # Verify print calls for dry run
        mock_print.assert_any_call('\n--- Dry Run Mode: No files will be deleted ---')
        mock_print.assert_any_call(f"  [DRY RUN] Would delete: {dust_bunnies[0]}")
        mock_print.assert_any_call(f"  [DRY RUN] Would delete: {dust_bunnies[1]}")
        mock_print.assert_any_call('Processed 2 cosmic dust bunnies.')

    @patch('os.remove')
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_clean_dust_bunnies_delete_mode(self, mock_print, mock_remove):
        dust_bunnies = [
            os.path.join('/test_dir', 'file1.tmp'),
            os.path.join('/test_dir', 'file2.log')
        ]

        processed_count = clean_dust_bunnies(dust_bunnies, dry_run=False, verbose=True)

        self.assertEqual(processed_count, 2)
        # Mock rationale: Ensure os.remove is called for each file in delete mode.
        mock_remove.assert_any_call(dust_bunnies[0])
        mock_remove.assert_any_call(dust_bunnies[1])
        self.assertEqual(mock_remove.call_count, 2)
        # Verify print calls for deletion
        mock_print.assert_any_call('\n--- Deletion Mode: Files will be permanently removed ---')
        mock_print.assert_any_call(f"  Deleting: {dust_bunnies[0]}")
        mock_print.assert_any_call(f"  Deleting: {dust_bunnies[1]}")
        mock_print.assert_any_call('Processed 2 cosmic dust bunnies.')

    @patch('os.remove')
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_clean_dust_bunnies_error_on_delete(self, mock_print, mock_remove):
        dust_bunnies = [
            os.path.join('/test_dir', 'unremovable.tmp')
        ]
        # Mock rationale: Simulate an OSError during file deletion.
        mock_remove.side_effect = OSError("Permission denied")

        processed_count = clean_dust_bunnies(dust_bunnies, dry_run=False, verbose=True)

        self.assertEqual(processed_count, 0) # No files successfully processed
        mock_remove.assert_called_once_with(dust_bunnies[0])
        mock_print.assert_any_call(f"Error Deleting {dust_bunnies[0]}: Permission denied", file=sys.stderr)

    @patch('os.walk')
    @patch('os.path.islink', return_value=True) # Mock rationale: Test symlink skipping
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_find_dust_bunnies_skip_symlink(self, mock_time, mock_getmtime, mock_islink, mock_walk):
        mock_time.return_value = self.fixed_now_timestamp
        mock_getmtime.return_value = self.fixed_now_timestamp - (10 * 24 * 60 * 60)

        mock_walk.return_value = [
            ('/test_dir', [], ['symlink.tmp', 'regular.tmp'])
        ]

        # Mock rationale: Make 'symlink.tmp' appear as a symlink, 'regular.tmp' as a normal file
        def islink_side_effect(path):
            return path == os.path.join('/test_dir', 'symlink.tmp')
        mock_islink.side_effect = islink_side_effect

        bunnies = find_dust_bunnies('/test_dir', ['*.tmp'], verbose=True)
        expected = [
            os.path.join('/test_dir', 'regular.tmp')
        ]
        self.assertCountEqual(bunnies, expected)

if __name__ == '__main__':
    unittest.main()
