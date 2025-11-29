import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.dust_collector import get_file_age_days, find_old_files, delete_files

class TestDustCollector(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_days_old_file(self, mock_datetime, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, datetime.datetime.now() returns current time.
        # We need to control these to simulate file ages deterministically without actual file system interaction.
        test_filepath = "/test/path/old_file.log"
        
        # Simulate current time as 2023-01-31
        mock_datetime.now.return_value = datetime(2023, 1, 31)
        # Simulate file modification time as 2023-01-01 (30 days old)
        mock_getmtime.return_value = datetime(2023, 1, 1).timestamp()
        
        age = get_file_age_days(test_filepath)
        self.assertEqual(age, 30)

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_days_recent_file(self, mock_datetime, mock_getmtime):
        # Mock rationale: Same as above, to simulate a file that is not old enough.
        test_filepath = "/test/path/recent_file.log"
        
        # Simulate current time as 2023-01-05
        mock_datetime.now.return_value = datetime(2023, 1, 5)
        # Simulate file modification time as 2023-01-01 (4 days old)
        mock_getmtime.return_value = datetime(2023, 1, 1).timestamp()
        
        age = get_file_age_days(test_filepath)
        self.assertEqual(age, 4)

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_days_non_existent_file(self, mock_datetime, mock_getmtime):
        # Mock rationale: Simulate a FileNotFoundError from os.path.getmtime.
        test_filepath = "/test/path/non_existent.log"
        mock_getmtime.side_effect = FileNotFoundError
        
        age = get_file_age_days(test_filepath)
        self.assertEqual(age, -1)

    @patch('src.dust_collector.get_file_age_days')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_old_files_no_recursion(self, mock_walk, mock_isfile, mock_get_file_age_days):
        # Mock rationale: os.walk simulates directory traversal, os.path.isfile checks if an entry is a file,
        # get_file_age_days provides the age. We control these to simulate a file system structure and ages.
        
        # Simulate directory structure:
        # /test_dir/
        #   old_file.log (age 10)
        #   recent_file.txt (age 2)
        #   subdir/
        #     another_old.log (age 15)
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_file.log', 'recent_file.txt']),
            ('/test_dir/subdir', [], ['another_old.log']) # This should not be walked if not recursive
        ]
        
        # Mock os.path.isfile for all files
        mock_isfile.side_effect = lambda x: x in [
            '/test_dir/old_file.log',
            '/test_dir/recent_file.txt',
            '/test_dir/subdir/another_old.log'
        ]

        # Mock file ages
        mock_get_file_age_days.side_effect = lambda filepath: {
            '/test_dir/old_file.log': 10,
            '/test_dir/recent_file.txt': 2,
            '/test_dir/subdir/another_old.log': 15 # This age should not be queried if not recursive
        }.get(filepath, -1)

        # Test with threshold 5 days, no recursion
        old_files = find_old_files('/test_dir', 5, recursive=False)
        self.assertEqual(len(old_files), 1)
        self.assertIn('/test_dir/old_file.log', old_files)
        
        # Ensure os.walk was called correctly (only for the top directory)
        mock_walk.assert_called_once_with('/test_dir')

    @patch('src.dust_collector.get_file_age_days')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_old_files_with_recursion(self, mock_walk, mock_isfile, mock_get_file_age_days):
        # Mock rationale: Same as above, but testing recursive behavior.
        
        # Simulate directory structure:
        # /test_dir/
        #   old_file.log (age 10)
        #   recent_file.txt (age 2)
        #   subdir/
        #     another_old.log (age 15)
        #     new_file.doc (age 1)
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_file.log', 'recent_file.txt']),
            ('/test_dir/subdir', [], ['another_old.log', 'new_file.doc'])
        ]
        
        mock_isfile.side_effect = lambda x: x in [
            '/test_dir/old_file.log',
            '/test_dir/recent_file.txt',
            '/test_dir/subdir/another_old.log',
            '/test_dir/subdir/new_file.doc'
        ]

        mock_get_file_age_days.side_effect = lambda filepath: {
            '/test_dir/old_file.log': 10,
            '/test_dir/recent_file.txt': 2,
            '/test_dir/subdir/another_old.log': 15,
            '/test_dir/subdir/new_file.doc': 1
        }.get(filepath, -1)

        # Test with threshold 5 days, with recursion
        old_files = find_old_files('/test_dir', 5, recursive=True)
        self.assertEqual(len(old_files), 2)
        self.assertIn('/test_dir/old_file.log', old_files)
        self.assertIn('/test_dir/subdir/another_old.log', old_files)

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_dry_run(self, mock_print, mock_remove):
        # Mock rationale: os.remove performs file deletion, builtins.print captures output.
        # We need to ensure os.remove is NOT called in dry-run mode and correct messages are printed.
        
        files_to_delete = ["/path/to/file1.log", "/path/to/file2.txt"]
        
        delete_files(files_to_delete, dry_run=True)
        
        mock_remove.assert_not_called()
        mock_print.assert_any_call("\n--- [DRY RUN] Would delete 2 file(s) ---")
        mock_print.assert_any_call("[DRY RUN] Would delete: /path/to/file1.log")
        mock_print.assert_any_call("[DRY RUN] Would delete: /path/to/file2.txt")

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_actual_delete(self, mock_print, mock_remove):
        # Mock rationale: Same as above, but ensuring os.remove IS called in actual deletion mode.
        
        files_to_delete = ["/path/to/file1.log", "/path/to/file2.txt"]
        
        delete_files(files_to_delete, dry_run=False)
        
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call("/path/to/file1.log")
        mock_remove.assert_any_call("/path/to/file2.txt")
        mock_print.assert_any_call("\n--- Deleting 2 file(s) ---")
        mock_print.assert_any_call("Deleting: /path/to/file1.log")
        mock_print.assert_any_call("Deleting: /path/to/file2.txt")

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_with_error(self, mock_print, mock_remove):
        # Mock rationale: Simulate an OSError during file deletion to test error handling.
        
        files_to_delete = ["/path/to/file1.log", "/path/to/file2.txt"]
        mock_remove.side_effect = [None, OSError("Permission denied")] # First succeeds, second fails
        
        delete_files(files_to_delete, dry_run=False)
        
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call("/path/to/file1.log")
        mock_remove.assert_any_call("/path/to/file2.txt")
        mock_print.assert_any_call("Deleting: /path/to/file1.log")
        mock_print.assert_any_call("Error deleting /path/to/file2.txt: Permission denied")

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_no_files(self, mock_print, mock_remove):
        # Mock rationale: Test the scenario where no files are passed for deletion.
        
        files_to_delete = []
        
        delete_files(files_to_delete, dry_run=False)
        
        mock_remove.assert_not_called()
        mock_print.assert_any_call("No old files found to process.")

if __name__ == '__main__':
    unittest.main()
