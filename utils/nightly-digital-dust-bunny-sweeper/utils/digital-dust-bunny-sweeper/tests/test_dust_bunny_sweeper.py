import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import time
import sys

# Import the functions to be tested
# Assuming the script is in src/ and tests are in tests/
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from dust_bunny_sweeper import find_dust_bunnies, sweep_dust_bunnies, DEFAULT_AGE_DAYS, DEFAULT_EXTENSIONS

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.current_time_dt = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.current_timestamp = self.current_time_dt.timestamp()

        # Mock os.path.isdir for the main function's path check
        self.mock_isdir = patch('os.path.isdir', return_value=True).start()
        self.addCleanup(self.mock_isdir.stop)

        # Mock time.time() to control the 'current' time
        self.mock_time = patch('time.time', return_value=self.current_timestamp).start()
        self.addCleanup(self.mock_time.stop)

        # Mock os.path.getmtime for file modification times
        self.mock_getmtime = patch('os.path.getmtime').start()
        self.addCleanup(self.mock_getmtime.stop)

        # Mock os.walk to simulate directory structure
        self.mock_os_walk = patch('os.walk').start()
        self.addCleanup(self.mock_os_walk.stop)

        # Mock os.remove and os.rmdir for deletion operations
        self.mock_os_remove = patch('os.remove').start()
        self.addCleanup(self.mock_os_remove.stop)

        self.mock_os_rmdir = patch('os.rmdir').start()
        self.addCleanup(self.mock_os_rmdir.stop)

        # Mock os.listdir for checking if a directory is empty before rmdir
        self.mock_os_listdir = patch('os.listdir', return_value=[]).start()
        self.addCleanup(self.mock_os_listdir.stop)

        # Mock sys.stdout to capture print output
        self.mock_stdout = patch('sys.stdout', new_callable=MagicMock).start()
        self.addCleanup(self.mock_stdout.stop)

    def _get_timestamp_days_ago(self, days):
        past_dt = self.current_time_dt - datetime.timedelta(days=days)
        return past_dt.timestamp()

    def test_find_empty_directories(self):
        # Mock rationale: Simulate a file system with an empty directory.
        self.mock_os_walk.side_effect = [
            ('/mock/path', ['empty_dir', 'full_dir'], ['file.txt']),
            ('/mock/path/empty_dir', [], []),
            ('/mock/path/full_dir', [], ['another.txt']),
        ]

        empty_dirs, old_files = find_dust_bunnies('/mock/path', DEFAULT_AGE_DAYS, DEFAULT_EXTENSIONS)

        self.assertIn('/mock/path/empty_dir', empty_dirs)
        self.assertEqual(len(empty_dirs), 1)
        self.assertEqual(len(old_files), 0)

    def test_find_old_files(self):
        # Mock rationale: Simulate files with different modification times and extensions.
        old_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS + 1)
        new_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS - 1)

        self.mock_os_walk.side_effect = [
            ('/mock/path', [], ['old.log', 'new.log', 'old.tmp', 'keep.txt']),
        ]
        # Mock rationale: Control the modification time for specific files.
        self.mock_getmtime.side_effect = lambda x: {
            '/mock/path/old.log': old_file_timestamp,
            '/mock/path/new.log': new_file_timestamp,
            '/mock/path/old.tmp': old_file_timestamp,
            '/mock/path/keep.txt': old_file_timestamp, # Should be ignored due to extension
        }.get(x, self.current_timestamp)

        empty_dirs, old_files = find_dust_bunnies('/mock/path', DEFAULT_AGE_DAYS, DEFAULT_EXTENSIONS)

        self.assertIn('/mock/path/old.log', old_files)
        self.assertIn('/mock/path/old.tmp', old_files)
        self.assertNotIn('/mock/path/new.log', old_files)
        self.assertNotIn('/mock/path/keep.txt', old_files)
        self.assertEqual(len(old_files), 2)
        self.assertEqual(len(empty_dirs), 0)

    def test_find_files_with_custom_extensions(self):
        # Mock rationale: Test custom extensions beyond the default set.
        old_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS + 1)
        custom_extensions = ['.data', '.csv']

        self.mock_os_walk.side_effect = [
            ('/mock/path', [], ['report.data', 'archive.csv', 'log.txt']),
        ]
        self.mock_getmtime.side_effect = lambda x: {
            '/mock/path/report.data': old_file_timestamp,
            '/mock/path/archive.csv': old_file_timestamp,
            '/mock/path/log.txt': old_file_timestamp,
        }.get(x, self.current_timestamp)

        empty_dirs, old_files = find_dust_bunnies('/mock/path', DEFAULT_AGE_DAYS, custom_extensions)

        self.assertIn('/mock/path/report.data', old_files)
        self.assertIn('/mock/path/archive.csv', old_files)
        self.assertNotIn('/mock/path/log.txt', old_files)
        self.assertEqual(len(old_files), 2)

    def test_sweep_dry_run(self):
        empty_dirs = ['/mock/path/empty_dir']
        old_files = ['/mock/path/old.log']

        sweep_dust_bunnies(empty_dirs, old_files, dry_run=True)

        # Mock rationale: In dry-run, no actual deletion should occur.
        self.mock_os_remove.assert_not_called()
        self.mock_os_rmdir.assert_not_called()
        self.assertIn('Dry run complete!', self.mock_stdout.getvalue())
        self.assertIn('[DRY RUN] Would delete old file: /mock/path/old.log', self.mock_stdout.getvalue())
        self.assertIn('[DRY RUN] Would delete empty directory: /mock/path/empty_dir', self.mock_stdout.getvalue())

    @patch('builtins.input', return_value='y')
    def test_sweep_actual_deletion(self, mock_input):
        empty_dirs = ['/mock/path/empty_dir']
        old_files = ['/mock/path/old.log']

        sweep_dust_bunnies(empty_dirs, old_files, dry_run=False)

        # Mock rationale: In actual sweep, deletion functions should be called.
        self.mock_os_remove.assert_called_once_with('/mock/path/old.log')
        self.mock_os_rmdir.assert_called_once_with('/mock/path/empty_dir')
        self.assertIn('Sweeping complete!', self.mock_stdout.getvalue())
        self.assertIn('Deleted old file: /mock/path/old.log', self.mock_stdout.getvalue())
        self.assertIn('Deleted empty directory: /mock/path/empty_dir', self.mock_stdout.getvalue())

    @patch('builtins.input', return_value='n')
    def test_sweep_cancelled(self, mock_input):
        # Mock rationale: Test user cancelling the operation.
        with patch('sys.exit') as mock_exit:
            # Simulate main function flow up to confirmation
            empty_dirs = ['/mock/path/empty_dir']
            old_files = ['/mock/path/old.log']
            
            # Call main directly with mocked args to simulate user interaction
            from dust_bunny_sweeper import main
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                path='/mock/path', age=DEFAULT_AGE_DAYS, extensions=DEFAULT_EXTENSIONS,
                dry_run=False, force=False
            )):
                self.mock_os_walk.side_effect = [
                    ('/mock/path', ['empty_dir'], ['old.log']),
                    ('/mock/path/empty_dir', [], []),
                ]
                old_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS + 1)
                self.mock_getmtime.return_value = old_file_timestamp

                main()

                mock_input.assert_called_once()
                self.mock_os_remove.assert_not_called()
                self.mock_os_rmdir.assert_not_called()
                self.assertIn('Dust bunnies spared for now', self.mock_stdout.getvalue())
                mock_exit.assert_called_once_with(2) # Expect exit code 2 for no-op

    def test_sweep_permission_error_file(self):
        empty_dirs = []
        old_files = ['/mock/path/protected.log']

        # Mock rationale: Simulate a permission error during file deletion.
        self.mock_os_remove.side_effect = OSError("Permission denied")

        sweep_dust_bunnies(empty_dirs, old_files, dry_run=False)

        self.mock_os_remove.assert_called_once_with('/mock/path/protected.log')
        self.assertIn("❌ Failed to delete file '/mock/path/protected.log': Permission denied", self.mock_stdout.getvalue())
        self.mock_os_rmdir.assert_not_called()

    def test_sweep_permission_error_dir(self):
        empty_dirs = ['/mock/path/protected_dir']
        old_files = []

        # Mock rationale: Simulate a permission error during directory deletion.
        self.mock_os_rmdir.side_effect = OSError("Permission denied")

        sweep_dust_bunnies(empty_dirs, old_files, dry_run=False)

        self.mock_os_rmdir.assert_called_once_with('/mock/path/protected_dir')
        self.assertIn("❌ Failed to delete directory '/mock/path/protected_dir': Permission denied", self.mock_stdout.getvalue())
        self.mock_os_remove.assert_not_called()

    def test_no_bunnies_found(self):
        # Mock rationale: Simulate a clean directory with no dust bunnies.
        self.mock_os_walk.side_effect = [
            ('/mock/path', ['sub_dir'], ['new_file.txt']),
            ('/mock/path/sub_dir', [], ['another_new.log']),
        ]
        new_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS - 1)
        self.mock_getmtime.return_value = new_file_timestamp

        with patch('sys.exit') as mock_exit:
            from dust_bunny_sweeper import main
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                path='/mock/path', age=DEFAULT_AGE_DAYS, extensions=DEFAULT_EXTENSIONS,
                dry_run=False, force=False
            )):
                main()

                self.assertIn('No digital dust bunnies found', self.mock_stdout.getvalue())
                self.mock_os_remove.assert_not_called()
                self.mock_os_rmdir.assert_not_called()
                mock_exit.assert_called_once_with(0) # Expect exit code 0 for success (no-op in this case)

    def test_directory_not_valid(self):
        # Mock rationale: Test handling of an invalid path argument.
        self.mock_isdir.return_value = False

        with patch('sys.exit') as mock_exit:
            from dust_bunny_sweeper import main
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                path='/invalid/path', age=DEFAULT_AGE_DAYS, extensions=DEFAULT_EXTENSIONS,
                dry_run=False, force=False
            )):
                main()

                self.assertIn("Error: Path '/invalid/path' is not a valid directory.", self.mock_stdout.getvalue())
                mock_exit.assert_called_once_with(1) # Expect exit code 1 for failure

    def test_sweep_force_flag(self):
        empty_dirs = ['/mock/path/empty_dir']
        old_files = ['/mock/path/old.log']

        with patch('sys.exit') as mock_exit:
            from dust_bunny_sweeper import main
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                path='/mock/path', age=DEFAULT_AGE_DAYS, extensions=DEFAULT_EXTENSIONS,
                dry_run=False, force=True
            )):
                self.mock_os_walk.side_effect = [
                    ('/mock/path', ['empty_dir'], ['old.log']),
                    ('/mock/path/empty_dir', [], []),
                ]
                old_file_timestamp = self._get_timestamp_days_ago(DEFAULT_AGE_DAYS + 1)
                self.mock_getmtime.return_value = old_file_timestamp

                main()

                # Mock rationale: With --force, no input is prompted, and deletion proceeds.
                self.mock_os_remove.assert_called_once_with('/mock/path/old.log')
                self.mock_os_rmdir.assert_called_once_with('/mock/path/empty_dir')
                self.assertIn('Proceeding with deletion without confirmation.', self.mock_stdout.getvalue())
                mock_exit.assert_called_once_with(0) # Expect exit code 0 for success

    def test_empty_dir_becomes_non_empty_during_sweep(self):
        empty_dirs = ['/mock/path/dir_that_becomes_non_empty']
        old_files = ['/mock/path/dir_that_becomes_non_empty/file_to_keep.txt']

        # Mock rationale: Simulate a directory that is initially empty, but then a file is 'kept' (not deleted),
        # making the directory non-empty, so it should not be removed.
        # The find_dust_bunnies would find it empty, but sweep_dust_bunnies should re-check.
        self.mock_os_listdir.side_effect = [
            ['file_to_keep.txt'], # First call for '/mock/path/dir_that_becomes_non_empty'
        ]

        sweep_dust_bunnies(empty_dirs, old_files, dry_run=False)

        self.mock_os_rmdir.assert_not_called()
        self.assertIn('Skipped non-empty directory: /mock/path/dir_that_becomes_non_empty', self.mock_stdout.getvalue())
