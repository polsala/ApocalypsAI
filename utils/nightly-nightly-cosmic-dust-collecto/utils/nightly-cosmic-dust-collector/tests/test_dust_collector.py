import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the function to be tested
from src.dust_collector import collect_cosmic_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing of file ages
        self.now = datetime(2023, 10, 26, 10, 0, 0) # A fixed point in time
        self.now_timestamp = self.now.timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_dry_run_identifies_old_files(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual file system interaction.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with files of different ages.
        # File 1: old_log.log (older than 30 days)
        # File 2: recent_data.txt (newer than 30 days)
        # File 3: another_old.tmp (older than 30 days)
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'recent_data.txt', 'another_old.tmp'])
        ]

        # Mock rationale: Provide specific modification times for each file.
        # Use self.now to ensure deterministic age calculation.
        def getmtime_side_effect(path):
            if 'old_log.log' in path:
                # Older than 30 days
                return (self.now - timedelta(days=31)).timestamp()
            elif 'recent_data.txt' in path:
                # Newer than 30 days
                return (self.now - timedelta(days=10)).timestamp()
            elif 'another_old.tmp' in path:
                # Older than 30 days
                return (self.now - timedelta(days=45)).timestamp()
            return self.now_timestamp # Default for any other path

        mock_getmtime.side_effect = getmtime_side_effect

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        # Mock rationale: Ensure fromtimestamp and timedelta behave as original for internal calculations.
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        # Run the utility in dry-run mode
        processed = collect_cosmic_dust('/test_dir', age_days=30, dry_run=True)

        # Assertions
        mock_isdir.assert_called_once_with('/test_dir')
        mock_walk.assert_called_once_with('/test_dir')
        self.assertEqual(mock_remove.call_count, 0, "No files should be deleted in dry-run mode")
        self.assertEqual(len(processed), 2, "Should identify 2 old files")
        self.assertIn('/test_dir/old_log.log', processed)
        self.assertIn('/test_dir/another_old.tmp', processed)

        # Check print statements for dry-run messages
        mock_print.assert_any_call("[DRY-RUN] Would delete: /test_dir/old_log.log (Last modified: 2023-09-25 10:00:00)")
        mock_print.assert_any_call("[DRY-RUN] Would delete: /test_dir/another_old.tmp (Last modified: 2023-09-11 10:00:00)")
        mock_print.assert_any_call("Dry-run complete. 2 files would have been deleted.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_deletes_old_files(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with one old file.
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt'])
        ]

        # Mock rationale: Set the modification time for the old file.
        mock_getmtime.return_value = (self.now - timedelta(days=60)).timestamp()

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        # Run the utility in actual deletion mode
        processed = collect_cosmic_dust('/test_dir', age_days=30, dry_run=False)

        # Assertions
        mock_remove.assert_called_once_with('/test_dir/old_file.txt')
        self.assertEqual(len(processed), 1, "Should delete 1 old file")
        self.assertIn('/test_dir/old_file.txt', processed)
        mock_print.assert_any_call("Deleted: /test_dir/old_file.txt (Last modified: 2023-08-27 10:00:00)")
        mock_print.assert_any_call("Collection complete. 1 files deleted.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_pattern_filtering(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate files with different patterns and ages.
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'old_data.txt', 'recent_log.log'])
        ]

        # Mock rationale: Set modification times. All are old enough.
        def getmtime_side_effect(path):
            return (self.now - timedelta(days=40)).timestamp()
        mock_getmtime.side_effect = getmtime_side_effect

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        # Run with a pattern to only target .log files
        processed = collect_cosmic_dust('/test_dir', age_days=30, pattern='*.log', dry_run=True)

        # Assertions
        self.assertEqual(len(processed), 2, "Should identify 2 .log files")
        self.assertIn('/test_dir/old_log.log', processed)
        self.assertIn('/test_dir/recent_log.log', processed)
        self.assertNotIn('/test_dir/old_data.txt', processed)
        mock_print.assert_any_call("[DRY-RUN] Would delete: /test_dir/old_log.log (Last modified: 2023-09-16 10:00:00)")
        mock_print.assert_any_call("[DRY-RUN] Would delete: /test_dir/recent_log.log (Last modified: 2023-09-16 10:00:00)")
        mock_print.assert_any_call("Dry-run complete. 2 files would have been deleted.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_no_old_files_found(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate files that are all recent.
        mock_walk.return_value = [
            ('/test_dir', [], ['recent_file1.txt', 'recent_file2.log'])
        ]

        # Mock rationale: Set modification times to be newer than the age threshold.
        mock_getmtime.return_value = (self.now - timedelta(days=5)).timestamp()

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        processed = collect_cosmic_dust('/test_dir', age_days=10, dry_run=True)

        # Assertions
        self.assertEqual(len(processed), 0, "Should not identify any files")
        mock_remove.assert_not_called()
        mock_print.assert_any_call("No cosmic dust found to collect.")

    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_non_existent_directory(self, mock_print, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False

        processed = collect_cosmic_dust('/non_existent_dir', age_days=10, dry_run=True)

        # Assertions
        self.assertEqual(len(processed), 0, "Should return empty list for non-existent directory")
        mock_print.assert_any_call("Error: Directory '/non_existent_dir' does not exist or is not a directory.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_os_error_on_getmtime(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with one file.
        mock_walk.return_value = [
            ('/test_dir', [], ['problem_file.txt'])
        ]

        # Mock rationale: Simulate an OSError when trying to get modification time.
        mock_getmtime.side_effect = OSError("Permission denied")

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        processed = collect_cosmic_dust('/test_dir', age_days=10, dry_run=True)

        # Assertions
        self.assertEqual(len(processed), 0, "Should not process file if getmtime fails")
        mock_remove.assert_not_called()
        mock_print.assert_any_call("Warning: Could not access or delete '/test_dir/problem_file.txt': Permission denied")
        mock_print.assert_any_call("No cosmic dust found to collect.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.dust_collector.datetime') # Mock datetime module
    def test_os_error_on_remove(self, mock_datetime_module, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with one old file.
        mock_walk.return_value = [
            ('/test_dir', [], ['unremovable_file.txt'])
        ]

        # Mock rationale: Set modification time to be old.
        mock_getmtime.return_value = (self.now - timedelta(days=20)).timestamp()

        # Mock rationale: Simulate an OSError when trying to remove the file.
        mock_remove.side_effect = OSError("File in use")

        # Mock rationale: Ensure datetime.now() is deterministic for age calculation.
        mock_datetime_module.now.return_value = self.now
        mock_datetime_module.fromtimestamp = datetime.fromtimestamp
        mock_datetime_module.timedelta = timedelta

        processed = collect_cosmic_dust('/test_dir', age_days=10, dry_run=False)

        # Assertions
        self.assertEqual(len(processed), 0, "Should not count file as processed if deletion fails")
        mock_remove.assert_called_once_with('/test_dir/unremovable_file.txt')
        mock_print.assert_any_call("Warning: Could not access or delete '/test_dir/unremovable_file.txt': File in use")
        mock_print.assert_any_call("No cosmic dust found to collect.") # Because the deletion failed, it's not counted as 'collected'
