import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta

# Import the functions to be tested
from src.cleaner import should_delete_file, clean_directory

class TestCleaner(unittest.TestCase):

    # Define a fixed current time for deterministic age calculations
    FIXED_CURRENT_TIME = datetime(2023, 10, 26, 12, 0, 0)

    @patch('os.path.getmtime')
    @patch('os.path.basename')
    def test_should_delete_file_by_age(self, mock_basename, mock_getmtime):
        # Mock rationale: `os.path.getmtime` is mocked to control file modification times
        # for deterministic age calculations. `os.path.basename` is mocked to control
        # the filename for pattern matching.

        # File modified 40 days ago (older than 30 days threshold)
        mock_getmtime.return_value = (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp()
        mock_basename.return_value = 'old_file.log'
        self.assertTrue(should_delete_file('path/to/old_file.log', 30, [], [], self.FIXED_CURRENT_TIME))

        # File modified 20 days ago (younger than 30 days threshold)
        mock_getmtime.return_value = (self.FIXED_CURRENT_TIME - timedelta(days=20)).timestamp()
        mock_basename.return_value = 'new_file.log'
        self.assertFalse(should_delete_file('path/to/new_file.log', 30, [], [], self.FIXED_CURRENT_TIME))

    @patch('os.path.getmtime')
    @patch('os.path.basename')
    def test_should_delete_file_with_include_patterns(self, mock_basename, mock_getmtime):
        # Mock rationale: `os.path.getmtime` and `os.path.basename` are mocked
        # to control file properties for pattern matching and age.

        # Setup: file is old enough (40 days old)
        mock_getmtime.return_value = (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp()
        age_days = 30

        # File matches include pattern
        mock_basename.return_value = 'temp_data.tmp'
        self.assertTrue(should_delete_file('path/temp_data.tmp', age_days, ['*.tmp'], [], self.FIXED_CURRENT_TIME))

        # File does not match include pattern
        mock_basename.return_value = 'important.log'
        self.assertFalse(should_delete_file('path/important.log', age_days, ['*.tmp'], [], self.FIXED_CURRENT_TIME))

        # File matches one of multiple include patterns
        mock_basename.return_value = 'cache.bak'
        self.assertTrue(should_delete_file('path/cache.bak', age_days, ['*.tmp', '*.bak'], [], self.FIXED_CURRENT_TIME))

        # No include patterns, should delete if old enough and not excluded
        mock_basename.return_value = 'any_file.txt'
        self.assertTrue(should_delete_file('path/any_file.txt', age_days, [], [], self.FIXED_CURRENT_TIME))

    @patch('os.path.getmtime')
    @patch('os.path.basename')
    def test_should_delete_file_with_exclude_patterns(self, mock_basename, mock_getmtime):
        # Mock rationale: `os.path.getmtime` and `os.path.basename` are mocked
        # to control file properties for pattern matching and age.

        # Setup: file is old enough (40 days old)
        mock_getmtime.return_value = (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp()
        age_days = 30

        # File matches exclude pattern
        mock_basename.return_value = 'do_not_touch.log'
        self.assertFalse(should_delete_file('path/do_not_touch.log', age_days, [], ['*.log'], self.FIXED_CURRENT_TIME))

        # File does not match exclude pattern
        mock_basename.return_value = 'temp_file.tmp'
        self.assertTrue(should_delete_file('path/temp_file.tmp', age_days, [], ['*.log'], self.FIXED_CURRENT_TIME))

        # Exclude takes precedence over include
        mock_basename.return_value = 'temp_log.log'
        self.assertFalse(should_delete_file('path/temp_log.log', age_days, ['*.log'], ['*.log'], self.FIXED_CURRENT_TIME))

        # Exclude takes precedence over include (different patterns)
        mock_basename.return_value = 'temp_log.log'
        self.assertFalse(should_delete_file('path/temp_log.log', age_days, ['*.tmp', '*.log'], ['*log'], self.FIXED_CURRENT_TIME))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.basename')
    @patch('src.cleaner.datetime') # Mock datetime to control current_time
    def test_clean_directory_dry_run(self, mock_datetime, mock_basename, mock_getmtime, mock_remove, mock_walk, mock_isdir):
        # Mock rationale: `os.path.isdir` is mocked to confirm the path exists.
        # `os.walk` is mocked to simulate a directory structure. `os.remove` is mocked
        # to ensure it's not called during a dry run. `os.path.getmtime` and
        # `os.path.basename` are mocked for file properties. `datetime` is mocked
        # to provide a fixed 'now' for age calculations.

        mock_datetime.now.return_value = self.FIXED_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta # Ensure timedelta is available

        # Simulate a directory with files
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.tmp', 'new_file.log', 'important.txt'])
        ]

        # old_file.tmp: 40 days old, should be deleted
        # new_file.log: 20 days old, too new
        # important.txt: 40 days old, but excluded by pattern
        file_mtimes = {
            '/test_dir/old_file.tmp': (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp(),
            '/test_dir/new_file.log': (self.FIXED_CURRENT_TIME - timedelta(days=20)).timestamp(),
            '/test_dir/important.txt': (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp(),
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, 0)
        mock_basename.side_effect = lambda p: os.path.basename(p)

        # Run in dry-run mode
        with patch('builtins.print') as mock_print:
            clean_directory(
                '/test_dir', 
                30, 
                True, 
                ['*.tmp'], 
                ['important.txt']
            )
            mock_remove.assert_not_called() # No deletion in dry-run
            mock_print.assert_any_call('[DRY RUN] Would delete: /test_dir/old_file.tmp')
            # Check that new_file.log and important.txt were not marked for deletion
            self.assertNotIn('[DRY RUN] Would delete: /test_dir/new_file.log', [call.args[0] for call in mock_print.call_args_list])
            self.assertNotIn('[DRY RUN] Would delete: /test_dir/important.txt', [call.args[0] for call in mock_print.call_args_list])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.basename')
    @patch('src.cleaner.datetime') # Mock datetime to control current_time
    def test_clean_directory_actual_run(self, mock_datetime, mock_basename, mock_getmtime, mock_remove, mock_walk, mock_isdir):
        # Mock rationale: Similar to dry-run, but `os.remove` is expected to be called.

        mock_datetime.now.return_value = self.FIXED_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta

        # Simulate a directory with files
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.tmp', 'new_file.log', 'another_old.tmp'])
        ]

        # old_file.tmp: 40 days old, should be deleted
        # new_file.log: 20 days old, too new
        # another_old.tmp: 40 days old, should be deleted
        file_mtimes = {
            '/test_dir/old_file.tmp': (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp(),
            '/test_dir/new_file.log': (self.FIXED_CURRENT_TIME - timedelta(days=20)).timestamp(),
            '/test_dir/another_old.tmp': (self.FIXED_CURRENT_TIME - timedelta(days=40)).timestamp(),
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, 0)
        mock_basename.side_effect = lambda p: os.path.basename(p)

        # Run in actual deletion mode
        with patch('builtins.print'): # Suppress print output for cleaner test results
            clean_directory(
                '/test_dir', 
                30, 
                False, 
                ['*.tmp'], 
                []
            )
            mock_remove.assert_any_call('/test_dir/old_file.tmp')
            mock_remove.assert_any_call('/test_dir/another_old.tmp')
            self.assertEqual(mock_remove.call_count, 2) # Only two files should be removed

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_clean_directory_invalid_path(self, mock_print, mock_isdir):
        # Mock rationale: `os.path.isdir` is mocked to simulate an invalid path.
        # `builtins.print` is mocked to capture error messages.

        clean_directory('/non_existent_dir', 30, False, [], [])
        mock_print.assert_any_call('Error: Directory not found or not accessible: /non_existent_dir')

    @patch('os.path.getmtime')
    @patch('os.path.basename')
    def test_should_delete_file_os_error(self, mock_basename, mock_getmtime):
        # Mock rationale: `os.path.getmtime` is mocked to raise an OSError,
        # simulating a file that becomes inaccessible or is deleted mid-scan.

        mock_getmtime.side_effect = OSError("Permission denied")
        mock_basename.return_value = 'inaccessible.file'
        self.assertFalse(should_delete_file('path/to/inaccessible.file', 30, [], [], self.FIXED_CURRENT_TIME))
