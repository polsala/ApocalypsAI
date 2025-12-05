import unittest
import os
import sys
import yaml
import datetime
from unittest.mock import patch, mock_open

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import sweep_ephemeral_data, get_file_age_days

class TestEphemeralDataSweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Fixes the 'current time' for deterministic age calculation.
        self.mock_now = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.patcher_datetime_now = patch('datetime.datetime.now', return_value=self.mock_now)
        self.patcher_datetime_now.start()

        # Mock rationale: Prevents actual file system operations during tests.
        self.mock_os_remove = patch('os.remove')
        self.mock_os_remove_instance = self.mock_os_remove.start()

        # Mock rationale: Prevents actual file system operations during tests.
        self.mock_os_path_exists = patch('os.path.exists', return_value=True)
        self.mock_os_path_exists_instance = self.mock_os_path_exists.start()

        # Mock rationale: Prevents actual file system operations during tests.
        self.mock_os_path_getsize = patch('os.path.getsize', return_value=1024 * 1024) # 1MB
        self.mock_os_path_getsize_instance = self.mock_os_path_getsize.start()

    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.mock_os_remove.stop()
        self.mock_os_path_exists.stop()
        self.mock_os_path_getsize.stop()

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: Provides a fixed modification time for testing age calculation.
        # File modified 10 days ago
        mock_getmtime.return_value = (self.mock_now - datetime.timedelta(days=10)).timestamp()
        self.assertEqual(get_file_age_days('/fake/path/file.txt'), 10)

        # File modified 0 days ago (today)
        mock_getmtime.return_value = self.mock_now.timestamp()
        self.assertEqual(get_file_age_days('/fake/path/file.txt'), 0)

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /test/logs\n    max_age_days: 7\n    patterns: ["*.log"]')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_sweep_ephemeral_data_dry_run(self, mock_getmtime, mock_os_walk, mock_file_open):
        # Mock rationale: Simulates the content of the configuration file.
        # Mock rationale: Simulates the file system structure without actual disk access.
        # Mock rationale: Provides fixed modification times for files to control their age.

        # Simulate /test/logs directory
        mock_os_walk.return_value = [
            ('/test/logs', [], ['old.log', 'new.log', 'other.txt'])
        ]

        # Define modification times for files
        def getmtime_side_effect(path):
            if path == '/test/logs/old.log':
                # Older than 7 days
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            elif path == '/test/logs/new.log':
                # Newer than 7 days
                return (self.mock_now - datetime.timedelta(days=5)).timestamp()
            elif path == '/test/logs/other.txt':
                # Older than 7 days, but wrong pattern
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            return self.mock_now.timestamp() # Default for others

        mock_getmtime.side_effect = getmtime_side_effect

        # Run in dry-run mode
        sweep_ephemeral_data('fake_config.yaml', dry_run=True)

        # Assert that os.remove was NOT called
        self.mock_os_remove_instance.assert_not_called()

        # Assert that os.walk was called with the correct path
        mock_os_walk.assert_called_with('/test/logs')

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /test/logs\n    max_age_days: 7\n    patterns: ["*.log"]')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_sweep_ephemeral_data_actual_run(self, mock_getmtime, mock_os_walk, mock_file_open):
        # Mock rationale: Simulates the content of the configuration file.
        # Mock rationale: Simulates the file system structure without actual disk access.
        # Mock rationale: Provides fixed modification times for files to control their age.

        # Simulate /test/logs directory
        mock_os_walk.return_value = [
            ('/test/logs', [], ['old.log', 'new.log', 'other.txt'])
        ]

        # Define modification times for files
        def getmtime_side_effect(path):
            if path == '/test/logs/old.log':
                # Older than 7 days
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            elif path == '/test/logs/new.log':
                # Newer than 7 days
                return (self.mock_now - datetime.timedelta(days=5)).timestamp()
            elif path == '/test/logs/other.txt':
                # Older than 7 days, but wrong pattern
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            return self.mock_now.timestamp() # Default for others

        mock_getmtime.side_effect = getmtime_side_effect

        # Run in actual mode
        sweep_ephemeral_data('fake_config.yaml', dry_run=False)

        # Assert that os.remove was called for 'old.log'
        self.mock_os_remove_instance.assert_called_once_with('/test/logs/old.log')

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /nonexistent/path\n    max_age_days: 7\n    patterns: ["*.log"]')
    @patch('os.path.exists', return_value=False)
    @patch('os.walk')
    def test_sweep_ephemeral_data_nonexistent_path(self, mock_os_walk, mock_os_path_exists, mock_file_open):
        # Mock rationale: Simulates a configuration file with a non-existent path.
        # Mock rationale: Ensures os.path.exists returns False for the specified path.
        # Mock rationale: Ensures os.walk is not called for non-existent paths.

        sweep_ephemeral_data('fake_config.yaml', dry_run=True)

        # os.walk should not be called if path does not exist
        mock_os_walk.assert_not_called()
        self.mock_os_remove_instance.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /test/logs\n    max_age_days: 7\n    patterns: ["*.log"]\n  - path: /test/other\n    max_age_days: 1\n    patterns: ["*.tmp"]')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_sweep_multiple_paths_and_patterns(self, mock_getmtime, mock_os_walk, mock_file_open):
        # Mock rationale: Simulates a configuration with multiple paths and patterns.
        # Mock rationale: Simulates file system structure for multiple paths.
        # Mock rationale: Provides fixed modification times for files.

        mock_os_walk.side_effect = [
            # First path: /test/logs
            ('/test/logs', [], ['old.log', 'new.log', 'temp.tmp']),
            # Second path: /test/other
            ('/test/other', [], ['old.tmp', 'new.tmp', 'log.log'])
        ]

        def getmtime_side_effect(path):
            if path == '/test/logs/old.log': # Matches, old
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            elif path == '/test/logs/new.log': # Matches, new
                return (self.mock_now - datetime.timedelta(days=5)).timestamp()
            elif path == '/test/logs/temp.tmp': # No match, old
                return (self.mock_now - datetime.timedelta(days=10)).timestamp()
            elif path == '/test/other/old.tmp': # Matches, old
                return (self.mock_now - datetime.timedelta(days=2)).timestamp()
            elif path == '/test/other/new.tmp': # Matches, new
                return (self.mock_now - datetime.timedelta(days=0)).timestamp()
            elif path == '/test/other/log.log': # No match, old
                return (self.mock_now - datetime.timedelta(days=2)).timestamp()
            return self.mock_now.timestamp()

        mock_getmtime.side_effect = getmtime_side_effect

        sweep_ephemeral_data('fake_config.yaml', dry_run=False)

        # Expect old.log from /test/logs and old.tmp from /test/other to be removed
        self.mock_os_remove_instance.assert_any_call('/test/logs/old.log')
        self.mock_os_remove_instance.assert_any_call('/test/other/old.tmp')
        self.assertEqual(self.mock_os_remove_instance.call_count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data='invalid yaml content')
    def test_sweep_ephemeral_data_invalid_config(self, mock_file_open):
        # Mock rationale: Simulates an invalid YAML configuration file.
        # Mock rationale: Captures stdout to check error messages.
        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            sweep_ephemeral_data('invalid_config.yaml', dry_run=True)
            self.assertIn('Error parsing YAML configuration', mock_stdout.getvalue())
            self.mock_os_remove_instance.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths: []')
    def test_sweep_ephemeral_data_empty_paths(self, mock_file_open):
        # Mock rationale: Simulates a configuration file with an empty list of ephemeral paths.
        # Mock rationale: Captures stdout to check informational messages.
        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            sweep_ephemeral_data('empty_config.yaml', dry_run=True)
            self.assertIn('No ephemeral paths defined', mock_stdout.getvalue())
            self.mock_os_remove_instance.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /test/logs\n    patterns: ["*.log"]') # Missing max_age_days
    @patch('os.walk')
    def test_sweep_ephemeral_data_missing_age_in_entry(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulates a configuration file with a missing 'max_age_days' in an entry.
        # Mock rationale: Captures stdout to check warning messages.
        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            sweep_ephemeral_data('missing_age_config.yaml', dry_run=True)
            self.assertIn('Warning: Skipping entry due to missing \'path\' or \'max_age_days\'', mock_stdout.getvalue())
            mock_os_walk.assert_not_called()
            self.mock_os_remove_instance.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data='ephemeral_paths:\n  - path: /test/logs\n    max_age_days: 7\n    patterns: ["*.log"]')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_sweep_ephemeral_data_os_error_on_file(self, mock_getmtime, mock_os_walk, mock_file_open):
        # Mock rationale: Simulates an OSError when trying to get file modification time.
        # Mock rationale: Simulates file system structure.
        mock_os_walk.return_value = [
            ('/test/logs', [], ['problem.log'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied")

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            sweep_ephemeral_data('fake_config.yaml', dry_run=True)
            self.assertIn('Error processing file /test/logs/problem.log: Permission denied', mock_stdout.getvalue())
            self.mock_os_remove_instance.assert_not_called()
