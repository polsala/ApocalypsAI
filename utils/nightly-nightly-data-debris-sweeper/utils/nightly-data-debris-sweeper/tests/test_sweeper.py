import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions directly for easier mocking
from src.sweeper import clean_directory, get_modification_time, remove_file, remove_dir, list_dir, is_dir

class TestNightlyDataDebrisSweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Fix current time for deterministic age calculations across tests.
        self.mock_current_time = datetime(2023, 10, 26, 10, 0, 0)
        self.mock_timestamp = self.mock_current_time.timestamp()

    @patch('src.sweeper.time.time')
    @patch('src.sweeper.get_modification_time')
    @patch('src.sweeper.remove_file')
    @patch('src.sweeper.remove_dir')
    @patch('src.sweeper.list_dir')
    @patch('src.sweeper.is_dir')
    @patch('src.sweeper.os.walk')
    def test_dry_run_identifies_old_files_and_dirs(self, mock_os_walk, mock_is_dir, mock_list_dir, mock_remove_dir, mock_remove_file, mock_get_modification_time, mock_time_time):
        # Mock rationale: Simulate file system traversal without actual disk I/O.
        # Mock rationale: Prevent actual file deletion during dry run.
        # Mock rationale: Fix current time for deterministic age calculations.
        # Mock rationale: Control file modification times for age-based deletion logic.
        # Mock rationale: Control directory emptiness for deletion logic.

        mock_time_time.return_value = self.mock_timestamp

        root_path = '/mock/path'

        # Define modification times
        old_time = (self.mock_current_time - timedelta(days=10)).timestamp()
        new_time = (self.mock_current_time - timedelta(days=1)).timestamp()

        # Mock os.walk to simulate directory structure
        mock_os_walk.return_value = [
            (root_path, ['old_dir', 'new_dir'], ['another_old_file.tmp']),
            (os.path.join(root_path, 'old_dir'), ['empty_old_subdir'], ['old_file.log']),
            (os.path.join(root_path, 'old_dir', 'empty_old_subdir'), [], []),
            (os.path.join(root_path, 'new_dir'), [], ['new_file.txt'])
        ]

        # Mock get_modification_time for specific paths
        def mock_getmtime_side_effect(path):
            if 'old_file.log' in path or 'another_old_file.tmp' in path or 'old_dir' in path or 'empty_old_subdir' in path:
                return old_time
            elif 'new_file.txt' in path or 'new_dir' in path:
                return new_time
            return self.mock_timestamp # Default for root_path

        mock_get_modification_time.side_effect = mock_getmtime_side_effect

        # Mock list_dir for checking empty directories
        def mock_list_dir_side_effect(path):
            if os.path.join(root_path, 'old_dir', 'empty_old_subdir') == path:
                return [] # Simulate empty after file deletion
            return ['some_file'] # Default for non-empty

        mock_list_dir.side_effect = mock_list_dir_side_effect

        # Mock is_dir
        mock_is_dir.return_value = True # Assume all paths are directories for simplicity

        # Run in dry-run mode
        clean_directory(root_path, age_days=7, patterns=['*.log', '*.tmp'], dry_run=True)

        # Assertions for dry-run mode
        mock_remove_file.assert_not_called() # No actual deletion should occur in dry-run
        mock_remove_dir.assert_not_called()  # No actual deletion should occur in dry-run

        # Ensure the correct paths were checked for modification time and emptiness
        self.assertIn(os.path.join(root_path, 'old_dir', 'old_file.log'), [call.args[0] for call in mock_get_modification_time.call_args_list])
        self.assertIn(os.path.join(root_path, 'another_old_file.tmp'), [call.args[0] for call in mock_get_modification_time.call_args_list])
        self.assertNotIn(os.path.join(root_path, 'new_dir', 'new_file.txt'), [call.args[0] for call in mock_get_modification_time.call_args_list])

        self.assertIn(os.path.join(root_path, 'old_dir', 'empty_old_subdir'), [call.args[0] for call in mock_list_dir.call_args_list])
        self.assertIn(os.path.join(root_path, 'old_dir', 'empty_old_subdir'), [call.args[0] for call in mock_get_modification_time.call_args_list])


    @patch('src.sweeper.time.time')
    @patch('src.sweeper.get_modification_time')
    @patch('src.sweeper.remove_file')
    @patch('src.sweeper.remove_dir')
    @patch('src.sweeper.list_dir')
    @patch('src.sweeper.is_dir')
    @patch('src.sweeper.os.walk')
    def test_execute_mode_deletes_correct_files_and_dirs(self, mock_os_walk, mock_is_dir, mock_list_dir, mock_remove_dir, mock_remove_file, mock_get_modification_time, mock_time_time):
        # Mock rationale: Simulate file system traversal without actual disk I/O.
        # Mock rationale: Verify `remove_file` and `remove_dir` are called with correct paths.
        # Mock rationale: Fix current time for deterministic age calculations.
        # Mock rationale: Control file modification times for age-based deletion logic.
        # Mock rationale: Control directory emptiness for deletion logic.

        mock_time_time.return_value = self.mock_timestamp

        root_path = '/mock/path'

        old_time = (self.mock_current_time - timedelta(days=10)).timestamp()
        new_time = (self.mock_current_time - timedelta(days=1)).timestamp()

        mock_os_walk.return_value = [
            (root_path, ['old_dir', 'new_dir'], ['another_old_file.tmp']),
            (os.path.join(root_path, 'old_dir'), ['empty_old_subdir'], ['old_file.log']),
            (os.path.join(root_path, 'old_dir', 'empty_old_subdir'), [], []),
            (os.path.join(root_path, 'new_dir'), [], ['new_file.txt'])
        ]

        def mock_getmtime_side_effect(path):
            if 'old_file.log' in path or 'another_old_file.tmp' in path or 'old_dir' in path or 'empty_old_subdir' in path:
                return old_time
            elif 'new_file.txt' in path or 'new_dir' in path:
                return new_time
            return self.mock_timestamp

        mock_get_modification_time.side_effect = mock_getmtime_side_effect

        def mock_list_dir_side_effect(path):
            if os.path.join(root_path, 'old_dir', 'empty_old_subdir') == path:
                return []
            return ['some_file']

        mock_list_dir.side_effect = mock_list_dir_side_effect
        mock_is_dir.return_value = True

        # Run in execute mode
        clean_directory(root_path, age_days=7, patterns=['*.log', '*.tmp'], dry_run=False)

        # Assertions for execute mode
        expected_file_to_delete_1 = os.path.join(root_path, 'old_dir', 'old_file.log')
        expected_file_to_delete_2 = os.path.join(root_path, 'another_old_file.tmp')
        expected_dir_to_delete = os.path.join(root_path, 'old_dir', 'empty_old_subdir')

        mock_remove_file.assert_any_call(expected_file_to_delete_1)
        mock_remove_file.assert_any_call(expected_file_to_delete_2)
        self.assertEqual(mock_remove_file.call_count, 2)

        mock_remove_dir.assert_any_call(expected_dir_to_delete)
        self.assertEqual(mock_remove_dir.call_count, 1)

        # Ensure new files/dirs are not touched
        self.assertNotIn(os.path.join(root_path, 'new_dir', 'new_file.txt'), [call.args[0] for call in mock_remove_file.call_args_list])
        self.assertNotIn(os.path.join(root_path, 'new_dir'), [call.args[0] for call in mock_remove_dir.call_args_list])

    @patch('src.sweeper.time.time')
    @patch('src.sweeper.get_modification_time')
    @patch('src.sweeper.remove_file')
    @patch('src.sweeper.remove_dir')
    @patch('src.sweeper.list_dir')
    @patch('src.sweeper.is_dir')
    @patch('src.sweeper.os.walk')
    def test_no_patterns_deletes_all_old_files(self, mock_os_walk, mock_is_dir, mock_list_dir, mock_remove_dir, mock_remove_file, mock_get_modification_time, mock_time_time):
        # Mock rationale: Simulate file system traversal and modification times without actual disk I/O.
        # Mock rationale: Verify `remove_file` is called for all old files when no patterns are specified.
        # Mock rationale: Fix current time for deterministic age calculations.

        mock_time_time.return_value = self.mock_timestamp

        root_path = '/mock/path'
        old_time = (self.mock_current_time - timedelta(days=10)).timestamp()
        new_time = (self.mock_current_time - timedelta(days=1)).timestamp()

        mock_os_walk.return_value = [
            (root_path, [], ['old_file.log', 'old_file.txt', 'new_file.doc'])
        ]

        def mock_getmtime_side_effect(path):
            if 'old_file.log' in path or 'old_file.txt' in path:
                return old_time
            elif 'new_file.doc' in path:
                return new_time
            return self.mock_timestamp

        mock_get_modification_time.side_effect = mock_getmtime_side_effect
        mock_is_dir.return_value = True
        mock_list_dir.return_value = ['some_file'] # Not relevant for this test

        clean_directory(root_path, age_days=7, patterns=[], dry_run=False)

        expected_file_1 = os.path.join(root_path, 'old_file.log')
        expected_file_2 = os.path.join(root_path, 'old_file.txt')

        mock_remove_file.assert_any_call(expected_file_1)
        mock_remove_file.assert_any_call(expected_file_2)
        self.assertEqual(mock_remove_file.call_count, 2)
        self.assertNotIn(os.path.join(root_path, 'new_file.doc'), [call.args[0] for call in mock_remove_file.call_args_list])

    @patch('src.sweeper.time.time')
    @patch('src.sweeper.get_modification_time')
    @patch('src.sweeper.remove_file')
    @patch('src.sweeper.remove_dir')
    @patch('src.sweeper.list_dir')
    @patch('src.sweeper.is_dir')
    @patch('src.sweeper.os.walk')
    def test_non_existent_path_handled(self, mock_os_walk, mock_is_dir, mock_list_dir, mock_remove_dir, mock_remove_file, mock_get_modification_time, mock_time_time):
        # Mock rationale: Simulate a non-existent root path to test error handling and ensure no file operations occur.

        mock_is_dir.return_value = False # Simulate root_path not being a directory

        # We expect a print statement for error, but no file operations
        clean_directory('/non/existent/path', age_days=7, patterns=[], dry_run=False)

        mock_os_walk.assert_not_called()
        mock_remove_file.assert_not_called()
        mock_remove_dir.assert_not_called()

    @patch('src.sweeper.time.time')
    @patch('src.sweeper.get_modification_time')
    @patch('src.sweeper.remove_file')
    @patch('src.sweeper.remove_dir')
    @patch('src.sweeper.list_dir')
    @patch('src.sweeper.is_dir')
    @patch('src.sweeper.os.walk')
    def test_os_error_on_file_access_handled(self, mock_os_walk, mock_is_dir, mock_list_dir, mock_remove_dir, mock_remove_file, mock_get_modification_time, mock_time_time):
        # Mock rationale: Simulate an OSError during file access (e.g., permissions) to test error handling.
        # Mock rationale: Ensure other deletable files are still processed despite an error on one file.

        mock_time_time.return_value = self.mock_timestamp
        root_path = '/mock/path'
        old_time = (self.mock_current_time - timedelta(days=10)).timestamp()

        mock_os_walk.return_value = [
            (root_path, [], ['unreadable_file.log', 'deletable_file.tmp'])
        ]

        def mock_getmtime_side_effect(path):
            if 'unreadable_file.log' in path:
                raise OSError("Permission denied")
            return old_time

        mock_get_modification_time.side_effect = mock_getmtime_side_effect
        mock_is_dir.return_value = True
        mock_list_dir.return_value = ['some_file']

        clean_directory(root_path, age_days=7, patterns=['*.log', '*.tmp'], dry_run=False)

        # Ensure deletable_file.tmp was still attempted to be removed
        mock_remove_file.assert_any_call(os.path.join(root_path, 'deletable_file.tmp'))
        self.assertEqual(mock_remove_file.call_count, 1) # Only one file should be attempted for deletion

if __name__ == '__main__':
    unittest.main()
