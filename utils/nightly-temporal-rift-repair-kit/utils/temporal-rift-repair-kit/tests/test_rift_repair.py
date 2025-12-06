import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the script
from src.rift_repair import (
    get_file_age_days,
    get_file_size_kb,
    scan_directory,
    report_files,
    delete_files,
    main
)

class TestRiftRepair(unittest.TestCase):

    def setUp(self):
        # Set a fixed "current time" for deterministic age calculations
        self.mock_current_time = datetime(2023, 10, 26, 12, 0, 0).timestamp()

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: getmtime is a system call that depends on file system state.
        # We need to control the modification time for deterministic age calculation.

        # File modified 10 days ago
        mock_getmtime.return_value = (datetime(2023, 10, 16, 12, 0, 0)).timestamp()
        with patch('time.time', return_value=self.mock_current_time):
            age = get_file_age_days("/fake/path/file1.txt")
            self.assertAlmostEqual(age, 10.0, places=5)

        # File modified 0 days ago (just now)
        mock_getmtime.return_value = self.mock_current_time
        with patch('time.time', return_value=self.mock_current_time):
            age = get_file_age_days("/fake/path/file2.txt")
            self.assertAlmostEqual(age, 0.0, places=5)

        # File not found
        mock_getmtime.side_effect = FileNotFoundError
        age = get_file_age_days("/nonexistent/file.txt")
        self.assertEqual(age, -1)

    @patch('os.path.getsize')
    def test_get_file_size_kb(self, mock_getsize):
        # Mock rationale: getsize is a system call that depends on file system state.
        # We need to control the size for deterministic size calculation.

        # 1024 bytes = 1 KB
        mock_getsize.return_value = 1024
        size = get_file_size_kb("/fake/path/file.txt")
        self.assertAlmostEqual(size, 1.0, places=5)

        # 5 MB = 5 * 1024 KB
        mock_getsize.return_value = 5 * 1024 * 1024
        size = get_file_size_kb("/fake/path/large_file.txt")
        self.assertAlmostEqual(size, 5 * 1024.0, places=5)

        # File not found
        mock_getsize.side_effect = FileNotFoundError
        size = get_file_size_kb("/nonexistent/file.txt")
        self.assertEqual(size, -1)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('time.time')
    def test_scan_directory(self, mock_time, mock_getsize, mock_getmtime, mock_walk):
        # Mock rationale: os.walk, getmtime, getsize are system calls.
        # We need to simulate a file system structure and file properties deterministically.
        # time.time is mocked to fix the "current" time for age calculations.

        mock_time.return_value = self.mock_current_time # Current time: Oct 26, 2023

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['old_small.txt', 'old_large.txt', 'new_small.txt', 'new_large.txt', 'very_old.txt']),
            ('/tmp/test_dir/subdir', [], ['old_subdir.txt'])
        ]

        # Define mock file properties
        file_properties = {
            '/tmp/test_dir/old_small.txt': {'mtime': (datetime(2023, 10, 10)).timestamp(), 'size': 500 * 1024}, # 16 days old, 500KB
            '/tmp/test_dir/old_large.txt': {'mtime': (datetime(2023, 10, 10)).timestamp(), 'size': 20 * 1024 * 1024}, # 16 days old, 20MB
            '/tmp/test_dir/new_small.txt': {'mtime': (datetime(2023, 10, 25)).timestamp(), 'size': 100 * 1024}, # 1 day old, 100KB
            '/tmp/test_dir/new_large.txt': {'mtime': (datetime(2023, 10, 25)).timestamp(), 'size': 15 * 1024 * 1024}, # 1 day old, 15MB
            '/tmp/test_dir/very_old.txt': {'mtime': (datetime(2023, 9, 1)).timestamp(), 'size': 10 * 1024}, # 55 days old, 10KB
            '/tmp/test_dir/subdir/old_subdir.txt': {'mtime': (datetime(2023, 10, 5)).timestamp(), 'size': 2 * 1024 * 1024}, # 21 days old, 2MB
        }

        def mock_getmtime_side_effect(path):
            return file_properties.get(path, {}).get('mtime', self.mock_current_time)

        def mock_getsize_side_effect(path):
            return file_properties.get(path, {}).get('size', 0)

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.side_effect = mock_getsize_side_effect

        # Test 1: max_age=15 days, min_size=1MB (1024KB)
        # Expected: old_large.txt, old_subdir.txt
        files = scan_directory('/tmp/test_dir', max_age_days=15, min_size_kb=1024)
        self.assertEqual(len(files), 2)
        self.assertIn(('/tmp/test_dir/old_large.txt', 16.0, 20480.0), files)
        self.assertIn(('/tmp/test_dir/subdir/old_subdir.txt', 21.0, 2048.0), files)

        # Test 2: max_age=50 days, min_size=0KB
        # Expected: very_old.txt
        files = scan_directory('/tmp/test_dir', max_age_days=50, min_size_kb=0)
        self.assertEqual(len(files), 1)
        self.assertIn(('/tmp/test_dir/very_old.txt', 55.0, 10.0), files)

        # Test 3: max_age=0 days, min_size=10MB (10240KB)
        # Expected: old_large.txt, new_large.txt
        files = scan_directory('/tmp/test_dir', max_age_days=0, min_size_kb=10240)
        self.assertEqual(len(files), 2)
        self.assertIn(('/tmp/test_dir/old_large.txt', 16.0, 20480.0), files)
        self.assertIn(('/tmp/test_dir/new_large.txt', 1.0, 15360.0), files)

        # Test 4: No files match
        files = scan_directory('/tmp/test_dir', max_age_days=100, min_size_kb=100000)
        self.assertEqual(len(files), 0)

    @patch('builtins.print')
    def test_report_files(self, mock_print):
        # Mock rationale: print is a side effect. We want to capture what's printed
        # to verify the reporting functionality without actual console output.

        files_data = [
            ("/path/to/file1.txt", 10.5, 500.25),
            ("/path/to/file2.log", 25.1, 1024.0),
        ]

        # Dry run
        report_files(files_data, dry_run=True)
        mock_print.assert_any_call("\n--- Files that would be deleted ---")
        mock_print.assert_any_call("- /path/to/file1.txt (Age: 10.5 days, Size: 500.25 KB)")
        mock_print.assert_any_call("- /path/to/file2.log (Age: 25.1 days, Size: 1024.00 KB)")
        mock_print.assert_any_call("Total files: 2")
        mock_print.assert_any_call("Total size: 1524.25 KB (1.49 MB)")
        mock_print.reset_mock()

        # Actual run
        report_files(files_data, dry_run=False)
        mock_print.assert_any_call("\n--- Files that will be deleted ---")
        mock_print.assert_any_call("Total files: 2")
        mock_print.reset_mock()

        # No files
        report_files([], dry_run=True)
        mock_print.assert_called_once_with("No files found matching the criteria.")

    @patch('os.remove')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_delete_files(self, mock_input, mock_print, mock_remove):
        # Mock rationale: os.remove is a system call that modifies the file system.
        # We must prevent actual deletion during tests.
        # print and input are side effects for user interaction, mocked for control.

        files_data = [
            ("/path/to/file1.txt", 10, 500),
            ("/path/to/file2.log", 25, 1024),
        ]

        # Test 1: Dry run - no deletion
        delete_files(files_data, dry_run=True, confirm=False)
        mock_remove.assert_not_called()
        mock_print.assert_any_call("Dry run complete. No files were deleted.")
        mock_print.reset_mock()

        # Test 2: Actual run, no confirmation (default behavior)
        delete_files(files_data, dry_run=False, confirm=False)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call("/path/to/file1.txt")
        mock_remove.assert_any_call("/path/to/file2.log")
        mock_print.assert_any_call("\nSuccessfully deleted 2 out of 2 files.")
        mock_remove.reset_mock()
        mock_print.reset_mock()

        # Test 3: Actual run, with confirmation (user says 'y')
        mock_input.return_value = 'y'
        delete_files(files_data, dry_run=False, confirm=True)
        mock_input.assert_called_once()
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("\nSuccessfully deleted 2 out of 2 files.")
        mock_input.reset_mock()
        mock_remove.reset_mock()
        mock_print.reset_mock()

        # Test 4: Actual run, with confirmation (user says 'N')
        mock_input.return_value = 'N'
        delete_files(files_data, dry_run=False, confirm=True)
        mock_input.assert_called_once()
        mock_remove.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled.")
        mock_input.reset_mock()
        mock_print.reset_mock()

        # Test 5: Error during deletion
        mock_remove.side_effect = [None, OSError("Permission denied")] # First file ok, second fails
        delete_files(files_data, dry_run=False, confirm=False)
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("Error deleting /path/to/file2.log: Permission denied")
        mock_print.assert_any_call("\nSuccessfully deleted 1 out of 2 files.")
        mock_remove.reset_mock()
        mock_print.reset_mock()

        # Test 6: No files to delete
        delete_files([], dry_run=False, confirm=False)
        mock_remove.assert_not_called()
        mock_print.assert_not_called() # No output if no files

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.rift_repair.scan_directory')
    @patch('src.rift_repair.report_files')
    @patch('src.rift_repair.delete_files')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_main(self, mock_print, mock_isdir, mock_delete_files, mock_report_files, mock_scan_directory, mock_parse_args):
        # Mock rationale: main orchestrates the utility. We mock its dependencies
        # (argparse, file system operations, reporting, deletion) to test its flow.

        # Mock argparse arguments
        mock_args = MagicMock()
        mock_args.path = ['/tmp/dir1', '/tmp/dir2']
        mock_args.max_age = 30
        mock_args.min_size = 1024
        mock_args.dry_run = False
        mock_args.confirm = False
        mock_parse_args.return_value = mock_args

        # Mock os.path.isdir to confirm paths exist
        mock_isdir.side_effect = lambda p: p in ['/tmp/dir1', '/tmp/dir2']

        # Mock scan_directory results
        mock_scan_directory.side_effect = [
            [('/tmp/dir1/fileA.txt', 40, 2048)], # From dir1
            [('/tmp/dir2/fileB.txt', 35, 3072)]  # From dir2
        ]

        # Mock report_files to return a count of files
        mock_report_files.return_value = 2

        # Run main
        main()

        # Assertions
        mock_isdir.assert_any_call('/tmp/dir1')
        mock_isdir.assert_any_call('/tmp/dir2')
        mock_scan_directory.assert_any_call('/tmp/dir1', 30, 1024)
        mock_scan_directory.assert_any_call('/tmp/dir2', 30, 1024)
        mock_report_files.assert_called_once_with(
            [('/tmp/dir1/fileA.txt', 40, 2048), ('/tmp/dir2/fileB.txt', 35, 3072)],
            False
        )
        mock_delete_files.assert_called_once_with(
            [('/tmp/dir1/fileA.txt', 40, 2048), ('/tmp/dir2/fileB.txt', 35, 3072)],
            False, False
        )
        mock_print.assert_any_call("Scanning '/tmp/dir1' for files older than 30 days and larger than 1024 KB...")
        mock_print.assert_any_call("Scanning '/tmp/dir2' for files older than 30 days and larger than 1024 KB...")

        # Test case: no files found
        mock_scan_directory.side_effect = [[], []]
        mock_report_files.return_value = 0
        mock_delete_files.reset_mock() # Clear previous calls
        mock_print.reset_mock()
        main()
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call("No files to delete based on the specified criteria.")

        # Test case: invalid path
        mock_isdir.side_effect = lambda p: p == '/tmp/dir1' # dir2 is invalid
        mock_scan_directory.side_effect = [[('/tmp/dir1/fileA.txt', 40, 2048)]]
        mock_report_files.return_value = 1
        mock_delete_files.reset_mock()
        mock_print.reset_mock()
        main()
        mock_print.assert_any_call("Warning: Path '/tmp/dir2' is not a valid directory. Skipping.")
        mock_scan_directory.assert_called_once_with('/tmp/dir1', 30, 1024) # Only dir1 scanned
        mock_delete_files.assert_called_once() # Only fileA.txt should be passed

if __name__ == '__main__':
    unittest.main()
