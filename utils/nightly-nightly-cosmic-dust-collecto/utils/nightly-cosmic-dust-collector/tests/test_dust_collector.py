import unittest
from unittest.mock import patch, MagicMock
import os
import time
import datetime
from src.dust_collector import collect_dust

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        self.base_path = "/mock/repo"
        self.archive_path = "/mock/archive"
        self.current_time = time.time() # Mock current time
        self.old_file_time = self.current_time - (30 * 24 * 3600) # 30 days ago
        self.new_file_time = self.current_time - (5 * 24 * 3600)  # 5 days ago

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join) # Use real join for path construction
    def test_report_mode_identifies_old_files(self, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory structure with files of different ages
        # to test if the utility correctly identifies "dust" based on the age threshold.
        mock_walk.return_value = [
            (self.base_path, [], ['old_log.log', 'new_report.txt', 'temp_file.tmp']),
            (os.path.join(self.base_path, 'sub'), [], ['another_old.bak'])
        ]
        
        # Mock rationale: Provide specific modification times for each file to control
        # which files are considered old or new.
        mock_getmtime.side_effect = lambda p: {
            os.path.join(self.base_path, 'old_log.log'): self.old_file_time,
            os.path.join(self.base_path, 'new_report.txt'): self.new_file_time,
            os.path.join(self.base_path, 'temp_file.tmp'): self.old_file_time,
            os.path.join(self.base_path, 'sub', 'another_old.bak'): self.old_file_time,
        }.get(p, self.new_file_time) # Default to new if not specified

        dust_files = collect_dust(self.base_path, 10, 'report') # Threshold 10 days
        
        expected_dust = [
            os.path.join(self.base_path, 'old_log.log'),
            os.path.join(self.base_path, 'temp_file.tmp'),
            os.path.join(self.base_path, 'sub', 'another_old.bak'),
        ]
        self.assertCountEqual(dust_files, expected_dust)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.remove')
    def test_delete_mode_removes_old_files(self, mock_remove, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system operations for deletion without
        # actually modifying the file system. This verifies that `os.remove` is called
        # for the correct files.
        mock_walk.return_value = [
            (self.base_path, [], ['old_log.log', 'new_report.txt'])
        ]
        mock_getmtime.side_effect = lambda p: {
            os.path.join(self.base_path, 'old_log.log'): self.old_file_time,
            os.path.join(self.base_path, 'new_report.txt'): self.new_file_time,
        }.get(p, self.new_file_time)

        collect_dust(self.base_path, 10, 'delete')

        mock_remove.assert_called_once_with(os.path.join(self.base_path, 'old_log.log'))
        self.assertNotIn(os.path.join(self.base_path, 'new_report.txt'), [call.args[0] for call in mock_remove.call_args_list])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('shutil.move')
    @patch('os.makedirs') # Mock rationale: Ensure the destination directory is "created" if it doesn't exist.
    def test_move_mode_moves_old_files(self, mock_makedirs, mock_move, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system operations for moving files without
        # actually modifying the file system. This verifies that `shutil.move` is called
        # for the correct files and that the destination directory is handled.
        mock_walk.return_value = [
            (self.base_path, [], ['old_log.log', 'new_report.txt'])
        ]
        mock_getmtime.side_effect = lambda p: {
            os.path.join(self.base_path, 'old_log.log'): self.old_file_time,
            os.path.join(self.base_path, 'new_report.txt'): self.new_file_time,
        }.get(p, self.new_file_time)

        collect_dust(self.base_path, 10, 'move', destination=self.archive_path)

        mock_makedirs.assert_called_once_with(self.archive_path, exist_ok=True)
        mock_move.assert_called_once_with(
            os.path.join(self.base_path, 'old_log.log'),
            os.path.join(self.archive_path, 'old_log.log')
        )
        self.assertNotIn(os.path.join(self.base_path, 'new_report.txt'), [call.args[0] for call in mock_move.call_args_list])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join)
    def test_file_patterns_filter_files(self, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Test the filtering mechanism based on file patterns.
        # This ensures only files matching the specified patterns are considered for "dust" collection.
        mock_walk.return_value = [
            (self.base_path, [], ['old_log.log', 'new_report.txt', 'temp_file.tmp', 'data.csv'])
        ]
        mock_getmtime.side_effect = lambda p: {
            os.path.join(self.base_path, 'old_log.log'): self.old_file_time,
            os.path.join(self.base_path, 'new_report.txt'): self.old_file_time, # Also old
            os.path.join(self.base_path, 'temp_file.tmp'): self.old_file_time,
            os.path.join(self.base_path, 'data.csv'): self.old_file_time,
        }.get(p, self.new_file_time)

        dust_files = collect_dust(self.base_path, 10, 'report', file_patterns=['*.log', '*.tmp'])
        
        expected_dust = [
            os.path.join(self.base_path, 'old_log.log'),
            os.path.join(self.base_path, 'temp_file.tmp'),
        ]
        self.assertCountEqual(dust_files, expected_dust)
        self.assertNotIn(os.path.join(self.base_path, 'new_report.txt'), dust_files)
        self.assertNotIn(os.path.join(self.base_path, 'data.csv'), dust_files)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join)
    def test_no_old_files(self, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Verify that if no files meet the age criteria, the utility
        # correctly reports an empty list and performs no actions.
        mock_walk.return_value = [
            (self.base_path, [], ['file1.txt', 'file2.txt'])
        ]
        mock_getmtime.return_value = self.new_file_time # All files are new

        dust_files = collect_dust(self.base_path, 10, 'report')
        self.assertEqual(dust_files, [])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join)
    def test_empty_directory(self, mock_join, mock_getmtime, mock_walk):
        # Mock rationale: Ensure the utility handles empty directories gracefully
        # without errors and reports no dust.
        mock_walk.return_value = [] # Empty directory
        
        dust_files = collect_dust(self.base_path, 10, 'report')
        self.assertEqual(dust_files, [])

    def test_invalid_action_raises_error(self):
        # Mock rationale: Test input validation for the 'action' parameter.
        # This ensures the utility fails gracefully with invalid inputs.
        with self.assertRaisesRegex(ValueError, "Invalid action"):
            collect_dust(self.base_path, 10, 'invalid_action')

    def test_move_action_without_destination_raises_error(self):
        # Mock rationale: Test input validation for the 'move' action requiring a destination.
        # This ensures the utility fails gracefully when required parameters are missing.
        with self.assertRaisesRegex(ValueError, "Destination path is required for 'move' action"):
            collect_dust(self.base_path, 10, 'move')
