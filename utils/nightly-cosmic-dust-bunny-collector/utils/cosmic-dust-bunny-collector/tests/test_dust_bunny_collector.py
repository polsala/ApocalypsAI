import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta

# Add the src directory to the Python path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_bunny_collector

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.mock_current_datetime = datetime(2023, 10, 26, 10, 0, 0)
        self.mock_current_timestamp = self.mock_current_datetime.timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_dry_run_finds_old_files(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a valid directory structure.
        mock_isdir.return_value = True

        # Mock rationale: Simulate files and their modification times.
        # File 1: 40 days old (older than 30 days threshold)
        old_file_timestamp = (self.mock_current_datetime - timedelta(days=40)).timestamp()
        # File 2: 10 days old (younger than 30 days threshold)
        new_file_timestamp = (self.mock_current_datetime - timedelta(days=10)).timestamp()

        mock_walk.return_value = [
            ('/mock/path', ['subdir'], ['old_file.txt', 'new_file.log']),
            ('/mock/path/subdir', [], ['another_old.tmp'])
        ]
        mock_getmtime.side_effect = {
            '/mock/path/old_file.txt': old_file_timestamp,
            '/mock/path/new_file.log': new_file_timestamp,
            '/mock/path/subdir/another_old.tmp': old_file_timestamp
        }.get

        dust_bunny_collector.collect_dust_bunnies(['/mock/path'], 30, True, [])

        # Assertions
        mock_remove.assert_not_called() # Mock rationale: Ensure no deletion in dry-run mode.
        mock_print.assert_any_call('  Found dust bunny: /mock/path/old_file.txt (Age: 40 days)')
        mock_print.assert_any_call('  Found dust bunny: /mock/path/subdir/another_old.tmp (Age: 40 days)')
        mock_print.assert_any_call('\nFound 2 cosmic dust bunnies.\n')
        mock_print.assert_any_call('🔭 Dry run complete. No files were deleted. To remove them, run without --dry-run.')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_actual_deletion_removes_old_files(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a valid directory structure.
        mock_isdir.return_value = True

        # Mock rationale: Simulate files and their modification times.
        old_file_timestamp = (self.mock_current_datetime - timedelta(days=40)).timestamp()

        mock_walk.return_value = [
            ('/mock/path', [], ['old_file_to_delete.txt'])
        ]
        mock_getmtime.side_effect = {
            '/mock/path/old_file_to_delete.txt': old_file_timestamp
        }.get

        dust_bunny_collector.collect_dust_bunnies(['/mock/path'], 30, False, [])

        # Assertions
        mock_remove.assert_called_once_with('/mock/path/old_file_to_delete.txt') # Mock rationale: Ensure deletion is called for the old file.
        mock_print.assert_any_call('  Removed: /mock/path/old_file_to_delete.txt')
        mock_print.assert_any_call('\n✅ Cosmic dust bunnies successfully swept! Your digital space feels lighter.')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_no_files_found(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a valid directory structure.
        mock_isdir.return_value = True

        # Mock rationale: Simulate only new files.
        new_file_timestamp = (self.mock_current_datetime - timedelta(days=10)).timestamp()

        mock_walk.return_value = [
            ('/mock/path', [], ['new_file.txt'])
        ]
        mock_getmtime.side_effect = {
            '/mock/path/new_file.txt': new_file_timestamp
        }.get

        dust_bunny_collector.collect_dust_bunnies(['/mock/path'], 30, True, [])

        # Assertions
        mock_remove.assert_not_called()
        mock_print.assert_any_call('✨ No cosmic dust bunnies found! Your digital space is pristine.')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_exclusion_patterns(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a valid directory structure.
        mock_isdir.return_value = True

        # Mock rationale: Simulate files and their modification times.
        old_file_timestamp = (self.mock_current_datetime - timedelta(days=40)).timestamp()

        mock_walk.return_value = [
            ('/mock/path', ['node_modules', '.git'], ['old_file.txt', 'temp.log']),
            ('/mock/path/node_modules', [], ['package.json']) # This path should be skipped by os.walk due to exclusion
        ]
        mock_getmtime.side_effect = {
            '/mock/path/old_file.txt': old_file_timestamp,
            '/mock/path/temp.log': old_file_timestamp,
            '/mock/path/node_modules/package.json': old_file_timestamp # This file should not be processed
        }.get

        # Exclude .git directories and *.log files
        dust_bunny_collector.collect_dust_bunnies(['/mock/path'], 30, True, ['.git', '*.log', 'node_modules'])

        # Assertions
        mock_remove.assert_not_called()
        mock_print.assert_any_call('Skipping excluded directory: /mock/path/node_modules')
        mock_print.assert_any_call('Skipping excluded directory: /mock/path/.git')
        mock_print.assert_any_call('  Found dust bunny: /mock/path/old_file.txt (Age: 40 days)')
        # temp.log should be excluded, and node_modules/package.json should not be found because its parent dir is excluded
        mock_print.assert_any_call('\nFound 1 cosmic dust bunnies.\n') # Only old_file.txt should be found
        mock_print.assert_any_call('🔭 Dry run complete. No files were deleted. To remove them, run without --dry-run.')
        # Ensure temp.log was not printed as a dust bunny
        mock_print.assert_not_any_call('  Found dust bunny: /mock/path/temp.log (Age: 40 days)')
        mock_print.assert_not_any_call('  Found dust bunny: /mock/path/node_modules/package.json (Age: 40 days)')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_invalid_path_handling(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate one valid and one invalid directory.
        mock_isdir.side_effect = {'/valid/path': True, '/invalid/path': False}.get

        # Mock rationale: Simulate files in the valid path.
        old_file_timestamp = (self.mock_current_datetime - timedelta(days=40)).timestamp()
        mock_walk.return_value = [
            ('/valid/path', [], ['old_file.txt'])
        ]
        mock_getmtime.side_effect = {
            '/valid/path/old_file.txt': old_file_timestamp
        }.get

        dust_bunny_collector.collect_dust_bunnies(['/valid/path', '/invalid/path'], 30, True, [])

        # Assertions
        mock_print.assert_any_call("⚠️ Warning: Path '/invalid/path' is not a valid directory. Skipping.")
        mock_print.assert_any_call('  Found dust bunny: /valid/path/old_file.txt (Age: 40 days)')
        mock_print.assert_any_call('\nFound 1 cosmic dust bunnies.\n')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_os_error_on_remove(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = self.mock_current_datetime
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a valid directory structure.
        mock_isdir.return_value = True

        # Mock rationale: Simulate an old file.
        old_file_timestamp = (self.mock_current_datetime - timedelta(days=40)).timestamp()

        mock_walk.return_value = [
            ('/mock/path', [], ['problem_file.txt'])
        ]
        mock_getmtime.side_effect = {
            '/mock/path/problem_file.txt': old_file_timestamp
        }.get

        # Mock rationale: Simulate an OSError during file removal.
        mock_remove.side_effect = OSError("Permission denied")

        dust_bunny_collector.collect_dust_bunnies(['/mock/path'], 30, False, [])

        # Assertions
        mock_remove.assert_called_once_with('/mock/path/problem_file.txt')
        mock_print.assert_any_call('  Failed to remove /mock/path/problem_file.txt: Permission denied')

if __name__ == '__main__':
    unittest.main()
