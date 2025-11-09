import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Import the functions to be tested
# Assuming the script is in src/ and tests are in tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_bunny_collector

class TestCosmicDustBunnyCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_directory_basic(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file modification times
        # without actual file system interaction.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file1.txt', 'file2.log']),
            ('/mock/path/subdir', [], ['subfile.tmp'])
        ]
        mock_getmtime.side_effect = [1672531200.0, 1672617600.0, 1672704000.0] # Jan 1, Jan 2, Jan 3 2023

        expected = [
            ('/mock/path/file1.txt', 1672531200.0),
            ('/mock/path/file2.log', 1672617600.0),
            ('/mock/path/subdir/subfile.tmp', 1672704000.0)
        ]
        result = list(dust_bunny_collector.scan_directory('/mock/path'))
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_directory_empty(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test scanning an empty directory.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/empty', [], [])
        ]
        result = list(dust_bunny_collector.scan_directory('/mock/empty'))
        self.assertEqual(result, [])

    @patch('os.path.isdir')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_scan_directory_invalid_path(self, mock_stderr, mock_isdir):
        # Mock rationale: Test error handling for an invalid directory path.
        mock_isdir.return_value = False
        result = list(dust_bunny_collector.scan_directory('/invalid/path'))
        self.assertEqual(result, [])
        mock_stderr.write.assert_called_with("Error: Path '/invalid/path' is not a valid directory.\n")

    @patch('datetime.datetime')
    def test_filter_old_files(self, mock_datetime):
        # Mock rationale: Fix the 'current time' to ensure deterministic age calculation.
        # This allows testing files older/newer than a specific threshold.
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 31, 12, 0, 0) # Jan 31, 2023
        mock_datetime.datetime.timestamp.return_value = mock_datetime.now.return_value.timestamp()

        # Files: (filepath, mtime_timestamp)
        # Jan 1, 2023 (30 days old)
        # Jan 2, 2023 (29 days old)
        # Dec 1, 2022 (61 days old)
        # Jan 30, 2023 (1 day old)
        files_data = [
            ('/path/to/old_file_1.txt', datetime.datetime(2023, 1, 1, 12, 0, 0).timestamp()),
            ('/path/to/recent_file.log', datetime.datetime(2023, 1, 2, 12, 0, 0).timestamp()),
            ('/path/to/very_old_file.tmp', datetime.datetime(2022, 12, 1, 12, 0, 0).timestamp()),
            ('/path/to/new_file.doc', datetime.datetime(2023, 1, 30, 12, 0, 0).timestamp())
        ]

        # Test with 30 days old threshold
        old_files_30_days = dust_bunny_collector.filter_old_files(files_data, 30)
        self.assertIn('/path/to/old_file_1.txt', old_files_30_days)
        self.assertIn('/path/to/very_old_file.tmp', old_files_30_days)
        self.assertNotIn('/path/to/recent_file.log', old_files_30_days)
        self.assertNotIn('/path/to/new_file.doc', old_files_30_days)
        self.assertEqual(len(old_files_30_days), 2)

        # Test with 60 days old threshold
        old_files_60_days = dust_bunny_collector.filter_old_files(files_data, 60)
        self.assertNotIn('/path/to/old_file_1.txt', old_files_60_days)
        self.assertIn('/path/to/very_old_file.tmp', old_files_60_days)
        self.assertEqual(len(old_files_60_days), 1)

        # Test with 1 day old threshold (should include almost all)
        old_files_1_day = dust_bunny_collector.filter_old_files(files_data, 1)
        self.assertIn('/path/to/old_file_1.txt', old_files_1_day)
        self.assertIn('/path/to/recent_file.log', old_files_1_day)
        self.assertIn('/path/to/very_old_file.tmp', old_files_1_day)
        self.assertNotIn('/path/to/new_file.doc', old_files_1_day)
        self.assertEqual(len(old_files_1_day), 3)

    @patch('builtins.print')
    def test_report_files_found(self, mock_print):
        # Mock rationale: Capture print output to verify correct reporting.
        files = ['/path/file1.txt', '/path/file2.log']
        dust_bunny_collector.report_files(files)
        mock_print.assert_any_call(f"Found {len(files)} cosmic dust bunnies (files older than specified days):")
        mock_print.assert_any_call("  - /path/file1.txt")
        mock_print.assert_any_call("  - /path/file2.log")

    @patch('builtins.print')
    def test_report_files_not_found(self, mock_print):
        # Mock rationale: Capture print output to verify correct reporting when no files are found.
        files = []
        dust_bunny_collector.report_files(files)
        mock_print.assert_called_once_with("No cosmic dust bunnies found! Your space is sparkling clean.")

    @patch('os.remove')
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_delete_files_success(self, mock_stderr, mock_print, mock_remove):
        # Mock rationale: Prevent actual file deletion and verify os.remove is called correctly.
        files = ['/path/file1.txt', '/path/file2.log']
        dust_bunny_collector.delete_files(files)
        mock_remove.assert_any_call('/path/file1.txt')
        mock_remove.assert_any_call('/path/file2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("  Deleted: /path/file1.txt")
        mock_print.assert_any_call("  Deleted: /path/file2.log")
        mock_print.assert_any_call("Successfully removed 2 cosmic dust bunnies.")
        self.assertFalse(mock_stderr.called)

    @patch('os.remove')
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_delete_files_with_error(self, mock_stderr, mock_print, mock_remove):
        # Mock rationale: Simulate an OSError during deletion and verify error reporting.
        files = ['/path/file1.txt', '/path/file2.log']
        mock_remove.side_effect = [None, OSError("Permission denied")]
        dust_bunny_collector.delete_files(files)
        mock_remove.assert_any_call('/path/file1.txt')
        mock_remove.assert_any_call('/path/file2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("  Deleted: /path/file1.txt")
        mock_stderr.write.assert_any_call("  Error deleting '/path/file2.log': Permission denied\n")
        mock_print.assert_any_call("Successfully removed 1 cosmic dust bunnies.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_collector.scan_directory')
    @patch('dust_bunny_collector.filter_old_files')
    @patch('dust_bunny_collector.report_files')
    @patch('dust_bunny_collector.delete_files')
    @patch('builtins.print')
    @patch('builtins.input', return_value='yes')
    @patch('sys.exit')
    def test_main_dry_run(self, mock_sys_exit, mock_input, mock_print, mock_delete_files, mock_report_files, mock_filter_old_files, mock_scan_directory, mock_parse_args):
        # Mock rationale: Test the main execution flow for dry-run mode.
        # Mocking argparse, scan, filter, report, delete functions to isolate main logic.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=30, dry_run=True, delete=False)
        mock_scan_directory.return_value = [('/mock/path/file1.txt', 123)]
        mock_filter_old_files.return_value = ['/mock/path/file1.txt']

        dust_bunny_collector.main()

        mock_scan_directory.assert_called_once_with('/mock/path')
        mock_filter_old_files.assert_called_once_with([('/mock/path/file1.txt', 123)], 30)
        mock_report_files.assert_called_once_with(['/mock/path/file1.txt'])
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call("\n--- DRY RUN MODE ---")
        mock_print.assert_any_call("--- END DRY RUN ---\n")
        mock_print.assert_any_call("No files were deleted. To delete, run again without --dry-run and with --delete.")
        mock_sys_exit.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_collector.scan_directory')
    @patch('dust_bunny_collector.filter_old_files')
    @patch('dust_bunny_collector.report_files')
    @patch('dust_bunny_collector.delete_files')
    @patch('builtins.print')
    @patch('builtins.input', return_value='yes')
    @patch('sys.exit')
    def test_main_delete_confirmed(self, mock_sys_exit, mock_input, mock_print, mock_delete_files, mock_report_files, mock_filter_old_files, mock_scan_directory, mock_parse_args):
        # Mock rationale: Test the main execution flow for deletion mode with user confirmation.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=30, dry_run=False, delete=True)
        mock_scan_directory.return_value = [('/mock/path/file1.txt', 123)]
        mock_filter_old_files.return_value = ['/mock/path/file1.txt']

        dust_bunny_collector.main()

        mock_scan_directory.assert_called_once_with('/mock/path')
        mock_filter_old_files.assert_called_once_with([('/mock/path/file1.txt', 123)], 30)
        mock_report_files.assert_called_once_with(['/mock/path/file1.txt'])
        mock_input.assert_called_once_with("Are you sure you want to delete these files? (yes/no): ")
        mock_delete_files.assert_called_once_with(['/mock/path/file1.txt'])
        mock_sys_exit.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_collector.scan_directory')
    @patch('dust_bunny_collector.filter_old_files')
    @patch('dust_bunny_collector.report_files')
    @patch('dust_bunny_collector.delete_files')
    @patch('builtins.print')
    @patch('builtins.input', return_value='no')
    @patch('sys.exit')
    def test_main_delete_cancelled(self, mock_sys_exit, mock_input, mock_print, mock_delete_files, mock_report_files, mock_filter_old_files, mock_scan_directory, mock_parse_args):
        # Mock rationale: Test the main execution flow for deletion mode with user cancellation.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=30, dry_run=False, delete=True)
        mock_scan_directory.return_value = [('/mock/path/file1.txt', 123)]
        mock_filter_old_files.return_value = ['/mock/path/file1.txt']

        dust_bunny_collector.main()

        mock_scan_directory.assert_called_once_with('/mock/path')
        mock_filter_old_files.assert_called_once_with([('/mock/path/file1.txt', 123)], 30)
        mock_report_files.assert_called_once_with(['/mock/path/file1.txt'])
        mock_input.assert_called_once_with("Are you sure you want to delete these files? (yes/no): ")
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled.")
        mock_sys_exit.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_collector.scan_directory')
    @patch('dust_bunny_collector.filter_old_files')
    @patch('dust_bunny_collector.report_files')
    @patch('dust_bunny_collector.delete_files')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_default_report(self, mock_sys_exit, mock_print, mock_delete_files, mock_report_files, mock_filter_old_files, mock_scan_directory, mock_parse_args):
        # Mock rationale: Test the default behavior (just reporting) when no dry-run or delete flags are set.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=30, dry_run=False, delete=False)
        mock_scan_directory.return_value = [('/mock/path/file1.txt', 123)]
        mock_filter_old_files.return_value = ['/mock/path/file1.txt']

        dust_bunny_collector.main()

        mock_scan_directory.assert_called_once_with('/mock/path')
        mock_filter_old_files.assert_called_once_with([('/mock/path/file1.txt', 123)], 30)
        mock_report_files.assert_called_once_with(['/mock/path/file1.txt'])
        mock_delete_files.assert_not_called()
        mock_print.assert_any_call("\nTo delete these files, run again with the --delete flag.")
        mock_sys_exit.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_collector.scan_directory')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_files_found(self, mock_sys_exit, mock_print, mock_scan_directory, mock_parse_args):
        # Mock rationale: Test scenario where scan_directory finds no files.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=30, dry_run=False, delete=False)
        mock_scan_directory.return_value = []
        
        dust_bunny_collector.main()
        
        mock_print.assert_any_call("No files found in the specified directory.")
        mock_sys_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_negative_days_old(self, mock_sys_exit, mock_print, mock_parse_args):
        # Mock rationale: Test input validation for --days-old argument.
        mock_parse_args.return_value = MagicMock(path='/mock/path', days_old=-5, dry_run=False, delete=False)
        
        dust_bunny_collector.main()
        
        mock_print.assert_any_call("Error: --days-old cannot be negative.")
        mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
