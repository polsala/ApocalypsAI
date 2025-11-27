import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Assume collector.py is in the parent directory for testing purposes
# In a real setup, you might adjust sys.path or use a test runner that handles this.
from src.collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print') # Mock print to suppress output during tests
    def test_collect_dust_dry_run_no_dust(self, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory or files that are not old enough.
        # This allows testing the 'no dust found' scenario without actual file system interaction.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Make files appear recent
        mock_getmtime.return_value = time.time() - (1 * 24 * 60 * 60) # 1 day old

        path = '/test_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=True)

        self.assertEqual(result, [])
        mock_remove.assert_not_called()
        mock_print.assert_any_call("No cosmic dust found. Your digital space is pristine!")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_collect_dust_dry_run_with_dust(self, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with old files.
        # This tests identification of old files in dry-run mode.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_file.txt', 'recent_file.log']),
            ('/test_dir/subdir', [], ['another_old.tmp'])
        ]

        # Set modification times: old_file.txt and another_old.tmp are old, recent_file.log is new
        def getmtime_side_effect(file_path):
            if 'old_file.txt' in file_path or 'another_old.tmp' in file_path:
                return time.time() - (60 * 24 * 60 * 60) # 60 days old
            return time.time() - (1 * 24 * 60 * 60) # 1 day old
        mock_getmtime.side_effect = getmtime_side_effect

        path = '/test_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=True)

        expected_dust = [
            os.path.join('/test_dir', 'old_file.txt'),
            os.path.join('/test_dir/subdir', 'another_old.tmp')
        ]
        self.assertCountEqual(result, expected_dust)
        mock_remove.assert_not_called()
        mock_print.assert_any_call(f"\nIdentified {len(expected_dust)} pieces of cosmic dust:")
        mock_print.assert_any_call("This was a dry run. No files were deleted. Use --delete to jettison cosmic dust.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_collect_dust_delete_mode(self, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with old files and test the deletion logic.
        # This verifies that os.remove is called for the correct files when dry_run is False.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file1.txt', 'old_file2.log'])
        ]
        mock_getmtime.return_value = time.time() - (60 * 24 * 60 * 60) # 60 days old

        path = '/test_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=False)

        expected_dust = [
            os.path.join('/test_dir', 'old_file1.txt'),
            os.path.join('/test_dir', 'old_file2.log')
        ]
        self.assertCountEqual(result, expected_dust)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call(os.path.join('/test_dir', 'old_file1.txt'))
        mock_remove.assert_any_call(os.path.join('/test_dir', 'old_file2.log'))
        mock_print.assert_any_call("\nInitiating cosmic dust collection (deletion)...")
        mock_print.assert_any_call(f"\nSuccessfully jettisoned {len(expected_dust)} pieces of cosmic dust.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_collect_dust_delete_mode_with_os_error(self, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test error handling during file deletion.
        # This ensures the utility gracefully handles cases where a file cannot be deleted.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file1.txt', 'old_file2.log'])
        ]
        mock_getmtime.return_value = time.time() - (60 * 24 * 60 * 60) # 60 days old

        # Make one remove call fail
        mock_remove.side_effect = [None, OSError("Permission denied")]

        path = '/test_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=False)

        expected_dust = [
            os.path.join('/test_dir', 'old_file1.txt'),
            os.path.join('/test_dir', 'old_file2.log')
        ]
        self.assertCountEqual(result, expected_dust)
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call(f"  - FAILED to jettison '{os.path.join('/test_dir', 'old_file2.log')}': Permission denied")
        mock_print.assert_any_call(f"\nSuccessfully jettisoned 1 pieces of cosmic dust.") # Only one was successful

    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_collect_dust_invalid_path(self, mock_print, mock_isdir):
        # Mock rationale: Test behavior when an invalid directory path is provided.
        # This ensures the utility handles invalid input gracefully.
        mock_isdir.return_value = False

        path = '/non_existent_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=True)

        self.assertEqual(result, [])
        mock_print.assert_any_call(f"ERROR: Path '{path}' is not a valid directory.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.print')
    def test_collect_dust_getmtime_os_error(self, mock_print, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test error handling when os.path.getmtime fails for a file.
        # This ensures the utility can continue processing other files even if one is inaccessible.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Make getmtime fail for file1.txt
        def getmtime_side_effect(file_path):
            if 'file1.txt' in file_path:
                raise OSError("File not found")
            return time.time() - (60 * 24 * 60 * 60) # 60 days old for file2.log
        mock_getmtime.side_effect = getmtime_side_effect

        path = '/test_dir'
        age_days = 30
        result = collect_dust(path, age_days, dry_run=True)

        expected_dust = [os.path.join('/test_dir', 'file2.log')]
        self.assertCountEqual(result, expected_dust)
        mock_print.assert_any_call(f"WARNING: Could not access '{os.path.join('/test_dir', 'file1.txt')}': File not found")


if __name__ == '__main__':
    unittest.main()
