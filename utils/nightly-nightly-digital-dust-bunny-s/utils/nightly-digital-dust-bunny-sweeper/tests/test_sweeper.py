import unittest
import os
import sys
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_days(self, mock_datetime, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, datetime.datetime.now() returns current time.
        # We need to control these to simulate specific file ages deterministically.

        # Simulate current time
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Keep original behavior for fromtimestamp

        # Test file modified 30 days ago
        mock_getmtime.return_value = datetime(2023, 9, 26, 12, 0, 0).timestamp()
        self.assertEqual(sweeper.get_file_age_days("dummy_file"), 30)

        # Test file modified 10 days ago
        mock_getmtime.return_value = datetime(2023, 10, 16, 12, 0, 0).timestamp()
        self.assertEqual(sweeper.get_file_age_days("dummy_file"), 10)

        # Test file modified less than a day ago (should be 0 days)
        mock_getmtime.return_value = datetime(2023, 10, 26, 1, 0, 0).timestamp()
        self.assertEqual(sweeper.get_file_age_days("dummy_file"), 0)

        # Test OSError
        mock_getmtime.side_effect = OSError
        self.assertEqual(sweeper.get_file_age_days("unreadable_file"), -1)

    @patch('sweeper.get_file_age_days')
    def test_should_delete_file_age(self, mock_get_file_age_days):
        # Mock rationale: get_file_age_days is already tested and provides the age.
        # We want to isolate the age-based decision logic.

        # File is old enough
        mock_get_file_age_days.return_value = 31
        self.assertTrue(sweeper.should_delete_file("old_file.txt", 30, [], [], verbose=False))

        # File is not old enough
        mock_get_file_age_days.return_value = 29
        self.assertFalse(sweeper.should_delete_file("new_file.txt", 30, [], [], verbose=False))

        # File is exactly the threshold age
        mock_get_file_age_days.return_value = 30
        self.assertTrue(sweeper.should_delete_file("threshold_file.txt", 30, [], [], verbose=False))

        # Unreadable file
        mock_get_file_age_days.return_value = -1
        self.assertFalse(sweeper.should_delete_file("unreadable_file.txt", 30, [], [], verbose=False))

    @patch('sweeper.get_file_age_days')
    def test_should_delete_file_patterns(self, mock_get_file_age_days):
        # Mock rationale: get_file_age_days is already tested. Focus on pattern matching.
        mock_get_file_age_days.return_value = 100 # Ensure file is always old enough

        # No patterns, should delete
        self.assertTrue(sweeper.should_delete_file("any_file.txt", 30, [], [], verbose=False))

        # Include pattern match
        self.assertTrue(sweeper.should_delete_file("log_file.log", 30, ["*.log"], [], verbose=False))
        self.assertFalse(sweeper.should_delete_file("text_file.txt", 30, ["*.log"], [], verbose=False))

        # Exclude pattern match
        self.assertFalse(sweeper.should_delete_file("important.log", 30, [], ["important.log"], verbose=False))
        self.assertTrue(sweeper.should_delete_file("other.log", 30, [], ["important.log"], verbose=False))

        # Both include and exclude
        self.assertTrue(sweeper.should_delete_file("app.log", 30, ["*.log"], ["debug.log"], verbose=False))
        self.assertFalse(sweeper.should_delete_file("debug.log", 30, ["*.log"], ["debug.log"], verbose=False))
        self.assertFalse(sweeper.should_delete_file("config.ini", 30, ["*.log"], ["debug.log"], verbose=False)) # Fails include

    @patch('os.walk')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('sweeper.get_file_age_days')
    def test_sweep_directory_dry_run(self, mock_get_file_age_days, mock_isdir, mock_remove, mock_walk):
        # Mock rationale:
        # os.walk simulates the file system structure.
        # os.remove is mocked to prevent actual file deletion during tests.
        # os.path.isdir is mocked to confirm the directory exists.
        # sweeper.get_file_age_days is mocked to control file ages deterministically.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'new_data.txt', 'important.log', 'temp_file.tmp'])
        ]
        # Simulate ages: old_log.log (40 days), new_data.txt (10 days), important.log (40 days), temp_file.tmp (40 days)
        mock_get_file_age_days.side_effect = lambda f: {
            '/test_dir/old_log.log': 40,
            '/test_dir/new_data.txt': 10,
            '/test_dir/important.log': 40,
            '/test_dir/temp_file.tmp': 40,
        }.get(f, 0)

        # Test dry run with basic age threshold
        processed, deleted = sweeper.sweep_directory(
            '/test_dir', age_threshold_days=30, include_patterns=[], exclude_patterns=[], dry_run=True, verbose=False
        )
        self.assertEqual(processed, 4)
        self.assertEqual(deleted, 3) # old_log, important.log, temp_file.tmp should be marked
        mock_remove.assert_not_called() # No actual deletion in dry run

        # Test dry run with include pattern
        processed, deleted = sweeper.sweep_directory(
            '/test_dir', age_threshold_days=30, include_patterns=['*.log'], exclude_patterns=[], dry_run=True, verbose=False
        )
        self.assertEqual(processed, 4)
        self.assertEqual(deleted, 2) # old_log.log, important.log should be marked
        mock_remove.assert_not_called()

        # Test dry run with exclude pattern
        processed, deleted = sweeper.sweep_directory(
            '/test_dir', age_threshold_days=30, include_patterns=[], exclude_patterns=['important.log'], dry_run=True, verbose=False
        )
        self.assertEqual(processed, 4)
        self.assertEqual(deleted, 2) # old_log.log, temp_file.tmp should be marked (important.log is excluded)
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('sweeper.get_file_age_days')
    def test_sweep_directory_actual_delete(self, mock_get_file_age_days, mock_isdir, mock_remove, mock_walk):
        # Mock rationale: Same as dry run, but verify os.remove is called.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'new_data.txt'])
        ]
        # Simulate ages: old_log.log (40 days), new_data.txt (10 days)
        mock_get_file_age_days.side_effect = lambda f: {
            '/test_dir/old_log.log': 40,
            '/test_dir/new_data.txt': 10,
        }.get(f, 0)

        # Test actual deletion
        processed, deleted = sweeper.sweep_directory(
            '/test_dir', age_threshold_days=30, include_patterns=[], exclude_patterns=[], dry_run=False, verbose=False
        )
        self.assertEqual(processed, 2)
        self.assertEqual(deleted, 1) # old_log.log should be deleted
        mock_remove.assert_called_once_with('/test_dir/old_log.log')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.sweep_directory')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_isdir, mock_sweep_directory, mock_parse_args):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # sweeper.sweep_directory is mocked to prevent actual file system interaction and test its call.
        # os.path.isdir is mocked to control directory existence.
        # builtins.print is mocked to capture output and prevent console spam during tests.

        # Configure mock arguments
        mock_args = MagicMock()
        mock_args.dirs = ['/dir1', '/dir2']
        mock_args.age = 10
        mock_args.include = ['*.tmp']
        mock_args.exclude = ['important.tmp']
        mock_args.dry_run = False
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args

        mock_isdir.side_effect = [True, True] # Both directories exist
        mock_sweep_directory.side_effect = [(5, 2), (3, 1)] # (processed, deleted) for each dir

        sweeper.main()

        # Verify sweep_directory was called correctly for each directory
        mock_sweep_directory.assert_any_call(
            '/dir1', 10, ['*.tmp'], ['important.tmp'], False, False
        )
        mock_sweep_directory.assert_any_call(
            '/dir2', 10, ['*.tmp'], ['important.tmp'], False, False
        )
        self.assertEqual(mock_sweep_directory.call_count, 2)

        # Verify total counts are correct
        # The print calls are mocked, so we check if the final summary was printed.
        # This is a bit fragile as it depends on print order, but good enough for a basic check.
        mock_print.assert_any_call("Scan complete. Total files processed: 8")
        mock_print.assert_any_call("Total files deleted: 3")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.sweep_directory')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_main_function_non_existent_dir(self, mock_print, mock_isdir, mock_sweep_directory, mock_parse_args):
        # Mock rationale: Test handling of non-existent directories.
        mock_args = MagicMock()
        mock_args.dirs = ['/dir_exists', '/dir_not_exists']
        mock_args.age = 10
        mock_args.include = []
        mock_args.exclude = []
        mock_args.dry_run = False
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args

        mock_isdir.side_effect = [True, False] # First dir exists, second doesn't
        mock_sweep_directory.return_value = (5, 2) # Only called for the existing dir

        sweeper.main()

        # Verify sweep_directory was called only for the existing directory
        mock_sweep_directory.assert_called_once_with(
            '/dir_exists', 10, [], [], False, False
        )
        mock_print.assert_any_call("Warning: Directory not found or not a directory: /dir_not_exists. Skipping.")
        mock_print.assert_any_call("Scan complete. Total files processed: 5")
        mock_print.assert_any_call("Total files deleted: 2")


if __name__ == '__main__':
    unittest.main()
