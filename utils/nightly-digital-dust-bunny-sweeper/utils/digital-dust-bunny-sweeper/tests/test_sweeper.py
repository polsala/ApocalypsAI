import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the class to be tested
from src.sweeper import DigitalDustBunnySweeper

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Set a fixed current time for deterministic age calculations
        self.fixed_current_time = time.mktime((2024, 7, 15, 10, 0, 0, 0, 0, 0))
        self.mock_log_age_days = 30
        self.mock_log_age_seconds = self.mock_log_age_days * 24 * 60 * 60

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    def test_scan_empty_directories(self, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time
        
        # Mock os.walk to simulate a directory structure with empty dirs
        mock_walk_data = [
            ('/mock/path', ['dir1', 'empty_dir1'], ['file1.txt']),
            ('/mock/path/dir1', ['subdir1'], ['file2.log']),
            ('/mock/path/dir1/subdir1', [], []),
            ('/mock/path/empty_dir1', [], []),
            ('/mock/path/empty_dir2', [], []) # This one will be found as empty
        ]
        
        # os.walk yields (root, dirs, files). We need to simulate the bottom-up check.
        # For empty_dir2, it should be found when its root is processed and it has no files/dirs.
        # For subdir1, it should be found when its root is processed and it has no files/dirs.
        
        # Simulate os.walk yielding from deepest to shallowest for empty dir detection
        mock_os_walk_return = [
            ('/mock/path/dir1/subdir1', [], []),
            ('/mock/path/empty_dir1', [], []),
            ('/mock/path/empty_dir2', [], []),
            ('/mock/path/dir1', ['subdir1'], ['file2.log']),
            ('/mock/path', ['dir1', 'empty_dir1', 'empty_dir2'], ['file1.txt'])
        ]

        with patch('os.walk', return_value=mock_os_walk_return): # Mock rationale: Simulate filesystem traversal without actual I/O.
            sweeper = DigitalDustBunnySweeper('/mock/path')
            sweeper.scan()
            self.assertIn('/mock/path/dir1/subdir1', sweeper.empty_dirs)
            self.assertIn('/mock/path/empty_dir1', sweeper.empty_dirs)
            self.assertIn('/mock/path/empty_dir2', sweeper.empty_dirs)
            self.assertEqual(len(sweeper.empty_dirs), 3)

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    @patch('os.path.getmtime') # Mock rationale: Control file modification times for age-based filtering.
    def test_scan_old_log_files(self, mock_getmtime, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time

        # Define modification times: one old, one new
        old_mtime = self.fixed_current_time - (self.mock_log_age_seconds + 100) # Older than 30 days
        new_mtime = self.fixed_current_time - (self.mock_log_age_seconds - 100) # Newer than 30 days

        # Mock getmtime for specific files
        mock_getmtime.side_effect = lambda p: {
            '/mock/path/logs/old.log': old_mtime,
            '/mock/path/logs/new.log': new_mtime,
            '/mock/path/data/report.txt': old_mtime, # .txt can also be a log
            '/mock/path/docs/notes.md': new_mtime
        }.get(p, self.fixed_current_time) # Default to current time for others

        mock_os_walk_return = [
            ('/mock/path/logs', [], ['old.log', 'new.log']),
            ('/mock/path/data', [], ['report.txt']),
            ('/mock/path/docs', [], ['notes.md']),
            ('/mock/path', ['logs', 'data', 'docs'], [])
        ]

        with patch('os.walk', return_value=mock_os_walk_return): # Mock rationale: Simulate filesystem traversal without actual I/O.
            sweeper = DigitalDustBunnySweeper('/mock/path', log_age_days=self.mock_log_age_days)
            sweeper.scan()
            self.assertIn('/mock/path/logs/old.log', sweeper.old_log_files)
            self.assertIn('/mock/path/data/report.txt', sweeper.old_log_files)
            self.assertNotIn('/mock/path/logs/new.log', sweeper.old_log_files)
            self.assertNotIn('/mock/path/docs/notes.md', sweeper.old_log_files)
            self.assertEqual(len(sweeper.old_log_files), 2)

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    def test_scan_temporary_files(self, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time

        mock_os_walk_return = [
            ('/mock/path/temp', [], ['file.tmp', 'another.bak', 'config~', '.DS_Store', 'temp_data.csv']),
            ('/mock/path/src', [], ['main.py', 'test.pyc']),
            ('/mock/path', ['temp', 'src'], [])
        ]

        with patch('os.walk', return_value=mock_os_walk_return): # Mock rationale: Simulate filesystem traversal without actual I/O.
            sweeper = DigitalDustBunnySweeper('/mock/path')
            sweeper.scan()
            self.assertIn('/mock/path/temp/file.tmp', sweeper.temp_files)
            self.assertIn('/mock/path/temp/another.bak', sweeper.temp_files)
            self.assertIn('/mock/path/temp/config~', sweeper.temp_files)
            self.assertIn('/mock/path/temp/temp_data.csv', sweeper.temp_files)
            self.assertNotIn('/mock/path/temp/.DS_Store', sweeper.temp_files) # Not a temp file by our definition
            self.assertNotIn('/mock/path/src/main.py', sweeper.temp_files)
            self.assertEqual(len(sweeper.temp_files), 4)

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    @patch('os.walk') # Mock rationale: Simulate filesystem traversal without actual I/O.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion during tests.
    @patch('os.listdir', return_value=[]) # Mock rationale: Ensure directories are seen as empty for rmdir checks.
    def test_delete_dust_bunnies(self, mock_listdir, mock_rmdir, mock_remove, mock_walk, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time

        sweeper = DigitalDustBunnySweeper('/mock/path')
        sweeper.temp_files = ['/mock/path/temp/file.tmp']
        sweeper.old_log_files = ['/mock/path/logs/old.log']
        sweeper.empty_dirs = ['/mock/path/empty_dir']

        sweeper.delete_dust_bunnies()

        mock_remove.assert_any_call('/mock/path/temp/file.tmp')
        mock_remove.assert_any_call('/mock/path/logs/old.log')
        mock_rmdir.assert_called_once_with('/mock/path/empty_dir')
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_rmdir.call_count, 1)

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    @patch('os.walk') # Mock rationale: Simulate filesystem traversal without actual I/O.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion during tests.
    @patch('os.listdir', return_value=['file.txt']) # Mock rationale: Simulate a non-empty directory.
    def test_delete_dust_bunnies_non_empty_dir_skipped(self, mock_listdir, mock_rmdir, mock_remove, mock_walk, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time

        sweeper = DigitalDustBunnySweeper('/mock/path')
        sweeper.empty_dirs = ['/mock/path/non_empty_dir']

        sweeper.delete_dust_bunnies()

        mock_rmdir.assert_not_called() # Should not be called if listdir returns content

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base path is always a directory for testing.
    @patch('time.time') # Mock rationale: Control the 'current time' for deterministic age calculations.
    @patch('os.walk') # Mock rationale: Simulate filesystem traversal without actual I/O.
    @patch('os.path.getmtime') # Mock rationale: Control file modification times for age-based filtering.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_report_output(self, mock_print, mock_getmtime, mock_walk, mock_time, mock_isdir, mock_abspath):
        mock_time.return_value = self.fixed_current_time
        old_mtime = self.fixed_current_time - (self.mock_log_age_seconds + 100)
        mock_getmtime.return_value = old_mtime

        sweeper = DigitalDustBunnySweeper('/mock/path')
        sweeper.empty_dirs = ['/mock/path/empty_dir']
        sweeper.old_log_files = ['/mock/path/logs/old.log']
        sweeper.temp_files = ['/mock/path/temp/file.tmp']

        sweeper.report()

        mock_print.assert_any_call("\n--- Empty Directories Found ---")
        mock_print.assert_any_call("  - /mock/path/empty_dir")
        mock_print.assert_any_call(f"\n--- Old Log Files Found (older than {self.mock_log_age_days} days) ---")
        mock_print.assert_any_call(f"  - /mock/path/logs/old.log (last modified: {datetime.fromtimestamp(old_mtime).strftime('%Y-%m-%d')})")
        mock_print.assert_any_call("\n--- Temporary Files Found ---")
        mock_print.assert_any_call("  - /mock/path/temp/file.tmp")

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments for testing main function.
    @patch('src.sweeper.DigitalDustBunnySweeper') # Mock rationale: Isolate the main function logic from the class implementation.
    @patch('builtins.input', return_value='yes') # Mock rationale: Simulate user confirmation for deletion.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_delete_flow(self, mock_print, mock_input, MockSweeper, mock_parse_args):
        # Configure mock arguments for deletion
        mock_parse_args.return_value = MagicMock(path='/mock/path', delete=True, log_age=30)

        # Configure the mock sweeper instance
        mock_sweeper_instance = MockSweeper.return_value
        mock_sweeper_instance.empty_dirs = ['/mock/path/empty']
        mock_sweeper_instance.old_log_files = ['/mock/path/old.log']
        mock_sweeper_instance.temp_files = ['/mock/path/temp.tmp']

        from src.sweeper import main
        main()

        MockSweeper.assert_called_once_with('/mock/path', 30)
        mock_sweeper_instance.scan.assert_called_once()
        mock_sweeper_instance.report.assert_called_once()
        mock_input.assert_called_once_with("Are you sure you want to delete these files and directories? (yes/no): ")
        mock_sweeper_instance.delete_dust_bunnies.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments for testing main function.
    @patch('src.sweeper.DigitalDustBunnySweeper') # Mock rationale: Isolate the main function logic from the class implementation.
    @patch('builtins.input', return_value='no') # Mock rationale: Simulate user declining deletion.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_main_dry_run_flow(self, mock_print, mock_input, MockSweeper, mock_parse_args):
        # Configure mock arguments for dry run (default)
        mock_parse_args.return_value = MagicMock(path='/mock/path', delete=False, log_age=30)

        # Configure the mock sweeper instance
        mock_sweeper_instance = MockSweeper.return_value
        mock_sweeper_instance.empty_dirs = ['/mock/path/empty']
        mock_sweeper_instance.old_log_files = ['/mock/path/old.log']
        mock_sweeper_instance.temp_files = ['/mock/path/temp.tmp']

        from src.sweeper import main
        main()

        MockSweeper.assert_called_once_with('/mock/path', 30)
        mock_sweeper_instance.scan.assert_called_once()
        mock_sweeper_instance.report.assert_called_once()
        mock_input.assert_not_called() # No confirmation needed for dry run
        mock_sweeper_instance.delete_dust_bunnies.assert_not_called()
        mock_print.assert_any_call("\nDry run complete. No files or directories were deleted.")

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Avoid actual path resolution for testing.
    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate an invalid base path.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_scan_invalid_path(self, mock_print, mock_isdir, mock_abspath):
        sweeper = DigitalDustBunnySweeper('/invalid/path')
        sweeper.scan()
        mock_print.assert_any_call("Error: Path '/invalid/path' is not a valid directory.")
        self.assertEqual(len(sweeper.empty_dirs), 0)
        self.assertEqual(len(sweeper.old_log_files), 0)
        self.assertEqual(len(sweeper.temp_files), 0)

if __name__ == '__main__':
    unittest.main()
