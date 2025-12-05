import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.scavenger import find_old_files, delete_files

class TestScavenger(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_find_old_files_no_patterns(self, mock_datetime, mock_getmtime, mock_os_walk):
        # Mock rationale: datetime.datetime.now() is non-deterministic.
        # We mock it to control the "current" time for consistent testing of age.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        
        # Mock rationale: os.walk accesses the filesystem.
        # We mock it to simulate a directory structure without actual files.
        mock_os_walk.return_value = [
            ('/test_dir', ('subdir1',), ('file1.log', 'file2.tmp')),
            ('/test_dir/subdir1', (), ('file3.txt', 'file4.old')),
        ]

        # Mock rationale: os.path.getmtime accesses the filesystem.
        # We mock it to return specific modification times for our simulated files.
        # These timestamps are relative to the mocked datetime.now().
        # file1.log: 40 days old (should be found)
        # file2.tmp: 10 days old (should NOT be found)
        # file3.txt: 60 days old (should be found)
        # file4.old: 20 days old (should NOT be found)
        mock_getmtime.side_effect = [
            (datetime(2023, 9, 16, 10, 0, 0)).timestamp(), # file1.log (40 days old)
            (datetime(2023, 10, 16, 10, 0, 0)).timestamp(), # file2.tmp (10 days old)
            (datetime(2023, 8, 26, 10, 0, 0)).timestamp(), # file3.txt (60 days old)
            (datetime(2023, 10, 6, 10, 0, 0)).timestamp(), # file4.old (20 days old)
        ]

        # Test with 30 days old, no patterns
        found = find_old_files('/test_dir', 30)
        self.assertIn('/test_dir/file1.log', found)
        self.assertNotIn('/test_dir/file2.tmp', found)
        self.assertIn('/test_dir/subdir1/file3.txt', found)
        self.assertNotIn('/test_dir/subdir1/file4.old', found)
        self.assertEqual(len(found), 2)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_find_old_files_with_patterns(self, mock_datetime, mock_getmtime, mock_os_walk):
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_os_walk.return_value = [
            ('/test_dir', (), ('file1.log', 'temp_data.tmp', 'cache.dat')),
        ]
        # file1.log: 40 days old
        # temp_data.tmp: 40 days old
        # cache.dat: 10 days old
        mock_getmtime.side_effect = [
            (datetime(2023, 9, 16, 10, 0, 0)).timestamp(), # file1.log
            (datetime(2023, 9, 16, 10, 0, 0)).timestamp(), # temp_data.tmp
            (datetime(2023, 10, 16, 10, 0, 0)).timestamp(), # cache.dat
        ]

        # Test with 30 days old, patterns ['.tmp']
        found = find_old_files('/test_dir', 30, patterns=['.tmp'])
        self.assertNotIn('/test_dir/file1.log', found)
        self.assertIn('/test_dir/temp_data.tmp', found)
        self.assertNotIn('/test_dir/cache.dat', found) # Too new
        self.assertEqual(len(found), 1)

        # Test with 30 days old, patterns ['.log', '.tmp']
        mock_getmtime.reset_mock() # Reset mock to allow new side_effect
        mock_getmtime.side_effect = [
            (datetime(2023, 9, 16, 10, 0, 0)).timestamp(), # file1.log
            (datetime(2023, 9, 16, 10, 0, 0)).timestamp(), # temp_data.tmp
            (datetime(2023, 10, 16, 10, 0, 0)).timestamp(), # cache.dat
        ]
        found = find_old_files('/test_dir', 30, patterns=['.log', '.tmp'])
        self.assertIn('/test_dir/file1.log', found)
        self.assertIn('/test_dir/temp_data.tmp', found)
        self.assertNotIn('/test_dir/cache.dat', found)
        self.assertEqual(len(found), 2)

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_dry_run(self, mock_print, mock_os_remove):
        files_to_delete = ['/path/to/file1.log', '/path/to/file2.tmp']
        
        # Test dry run
        deleted_count = delete_files(files_to_delete, dry_run=True)
        mock_os_remove.assert_not_called() # No actual deletion
        mock_print.assert_any_call("DRY RUN: Processing 2 files...")
        mock_print.assert_any_call("  Would delete: /path/to/file1.log")
        mock_print.assert_any_call("  Would delete: /path/to/file2.tmp")
        self.assertEqual(deleted_count, 0) # Dry run doesn't count as deleted

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_actual_deletion(self, mock_print, mock_os_remove):
        files_to_delete = ['/path/to/file1.log', '/path/to/file2.tmp']
        
        # Test actual deletion
        deleted_count = delete_files(files_to_delete, dry_run=False)
        mock_os_remove.assert_any_call('/path/to/file1.log')
        mock_os_remove.assert_any_call('/path/to/file2.tmp')
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_print.assert_any_call("Processing 2 files...")
        mock_print.assert_any_call("  Deleted: /path/to/file1.log")
        mock_print.assert_any_call("  Deleted: /path/to/file2.tmp")
        self.assertEqual(deleted_count, 2)

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_with_error(self, mock_print, mock_os_remove):
        files_to_delete = ['/path/to/file1.log', '/path/to/non_existent.tmp']
        
        # Mock rationale: Simulate an OSError during file deletion.
        # This tests error handling without needing to create/delete actual files.
        mock_os_remove.side_effect = [None, OSError("Permission denied")]

        deleted_count = delete_files(files_to_delete, dry_run=False)
        mock_os_remove.assert_any_call('/path/to/file1.log')
        mock_os_remove.assert_any_call('/path/to/non_existent.tmp')
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_print.assert_any_call("  Deleted: /path/to/file1.log")
        mock_print.assert_any_call("  Error deleting /path/to/non_existent.tmp: Permission denied")
        self.assertEqual(deleted_count, 1) # Only one file successfully deleted

    @patch('builtins.print')
    def test_delete_files_no_files(self, mock_print):
        deleted_count = delete_files([], dry_run=False)
        mock_print.assert_any_call("No files to process.")
        self.assertEqual(deleted_count, 0)

if __name__ == '__main__':
    unittest.main()
