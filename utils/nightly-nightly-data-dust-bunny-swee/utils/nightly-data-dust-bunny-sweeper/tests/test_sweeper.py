import unittest
import os
import time
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import find_dust_bunnies, main

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing of file ages
        self.now = datetime(2023, 10, 26, 10, 0, 0)
        # Mock datetime.now() to control the "current" time
        # Mock rationale: Ensures deterministic age calculations for files.
        self.mock_datetime_now = patch('src.sweeper.datetime')
        self.mock_dt = self.mock_datetime_now.start()
        self.mock_dt.now.return_value = self.now
        self.mock_dt.fromtimestamp = datetime.fromtimestamp # Keep original for conversion
        self.mock_dt.timedelta = timedelta # Keep original for timedelta
        self.mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime() constructor

    def tearDown(self):
        self.mock_datetime_now.stop()

    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.os.path.getmtime')
    def test_find_dust_bunnies_no_matches(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system structure and modification times without actual I/O.
        # This makes tests deterministic and fast.

        # Simulate a directory with files, none of which should match criteria
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'recent.log', 'important.bak'])
        ]
        # All files are recent (e.g., 10 days old)
        recent_timestamp = (self.now - timedelta(days=10)).timestamp()
        mock_getmtime.side_effect = [recent_timestamp, recent_timestamp, recent_timestamp]

        path = '/test_dir'
        age_days = 30
        patterns = ['*.tmp', '*.log']

        bunnies = find_dust_bunnies(path, age_days, patterns)
        self.assertEqual(len(bunnies), 0)

    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.os.path.getmtime')
    def test_find_dust_bunnies_with_matches(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system structure and modification times without actual I/O.
        # This makes tests deterministic and fast.

        # Simulate a directory with files, some matching criteria
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old.log', 'recent.txt', 'temp.tmp']),
            ('/test_dir/subdir', [], ['another_old.bak', 'new.log'])
        ]

        # Define timestamps:
        # old.log: 40 days old (matches age and pattern)
        # recent.txt: 10 days old (does not match age)
        # temp.tmp: 40 days old (matches age and pattern)
        # another_old.bak: 40 days old (matches age and pattern)
        # new.log: 10 days old (does not match age)
        old_timestamp = (self.now - timedelta(days=40)).timestamp()
        recent_timestamp = (self.now - timedelta(days=10)).timestamp()

        mock_getmtime.side_effect = [
            old_timestamp,      # /test_dir/old.log
            recent_timestamp,   # /test_dir/recent.txt
            old_timestamp,      # /test_dir/temp.tmp
            old_timestamp,      # /test_dir/subdir/another_old.bak
            recent_timestamp    # /test_dir/subdir/new.log
        ]

        path = '/test_dir'
        age_days = 30
        patterns = ['*.tmp', '*.log', '*.bak']

        bunnies = find_dust_bunnies(path, age_days, patterns)
        expected_bunnies = [
            '/test_dir/old.log',
            '/test_dir/temp.tmp',
            '/test_dir/subdir/another_old.bak'
        ]
        self.assertCountEqual(bunnies, expected_bunnies) # Use assertCountEqual for order-independent comparison

    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.os.path.getmtime')
    def test_find_dust_bunnies_os_error_handling(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system errors (e.g., permission denied) to ensure robust error handling.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.log', 'unreadable.tmp'])
        ]
        # file1.log is old and readable, unreadable.tmp raises OSError
        old_timestamp = (self.now - timedelta(days=40)).timestamp()
        mock_getmtime.side_effect = [old_timestamp, OSError("Permission denied")]

        path = '/test_dir'
        age_days = 30
        patterns = ['*.log', '*.tmp']

        bunnies = find_dust_bunnies(path, age_days, patterns)
        self.assertCountEqual(bunnies, ['/test_dir/file1.log'])
        # We could also check stderr output if we wanted to verify the warning message.

    @patch('src.sweeper.os.remove')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.argparse.ArgumentParser.parse_args')
    @patch('builtins.print') # Mock print to capture output
    def test_main_dry_run_default(self, mock_print, mock_parse_args, mock_find_dust_bunnies, mock_remove):
        # Mock rationale:
        # - mock_parse_args: Controls command-line arguments without actually running the CLI.
        # - mock_find_dust_bunnies: Isolates the main function from file system scanning logic.
        # - mock_remove: Ensures no actual file deletion occurs during tests.
        # - mock_print: Captures console output for verification.

        mock_parse_args.return_value = argparse.Namespace(
            path='.', age_days=30, patterns='*.tmp', clean=False, dry_run=False
        )
        mock_find_dust_bunnies.return_value = ['file1.tmp', 'file2.tmp']

        main()

        mock_find_dust_bunnies.assert_called_once_with('.', 30, ['*.tmp'])
        mock_remove.assert_not_called() # Should not delete in dry run (default)
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were deleted.")

    @patch('src.sweeper.os.remove')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_dry_run_explicit(self, mock_print, mock_parse_args, mock_find_dust_bunnies, mock_remove):
        # Mock rationale: Same as above, testing explicit dry-run behavior.
        mock_parse_args.return_value = argparse.Namespace(
            path='.', age_days=30, patterns='*.tmp', clean=True, dry_run=True # clean=True but dry_run=True
        )
        mock_find_dust_bunnies.return_value = ['file1.tmp', 'file2.tmp']

        main()

        mock_remove.assert_not_called()
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were deleted.")

    @patch('src.sweeper.os.remove')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_clean_mode(self, mock_print, mock_parse_args, mock_find_dust_bunnies, mock_remove):
        # Mock rationale: Same as above, testing actual cleanup behavior.
        mock_parse_args.return_value = argparse.Namespace(
            path='.', age_days=30, patterns='*.tmp', clean=True, dry_run=False
        )
        mock_find_dust_bunnies.return_value = ['file1.tmp', 'file2.tmp']

        main()

        mock_find_dust_bunnies.assert_called_once_with('.', 30, ['*.tmp'])
        self.assertEqual(mock_remove.call_count, 2) # Should call remove twice
        mock_remove.assert_any_call('file1.tmp')
        mock_remove.assert_any_call('file2.tmp')
        mock_print.assert_any_call("\nCleanup complete. Successfully deleted 2 files.")

    @patch('src.sweeper.os.remove')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_no_dust_bunnies(self, mock_print, mock_parse_args, mock_find_dust_bunnies, mock_remove):
        # Mock rationale: Test scenario where no files match the criteria.
        mock_parse_args.return_value = argparse.Namespace(
            path='.', age_days=30, patterns='*.tmp', clean=False, dry_run=False
        )
        mock_find_dust_bunnies.return_value = [] # No files found

        main()

        mock_find_dust_bunnies.assert_called_once()
        mock_remove.assert_not_called()
        mock_print.assert_any_call("No dust bunnies found! Your directory is sparkling clean.")

    @patch('src.sweeper.os.remove')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_clean_mode_with_deletion_error(self, mock_print, mock_parse_args, mock_find_dust_bunnies, mock_remove):
        # Mock rationale: Simulate a scenario where some files cannot be deleted.
        mock_parse_args.return_value = argparse.Namespace(
            path='.', age_days=30, patterns='*.tmp', clean=True, dry_run=False
        )
        mock_find_dust_bunnies.return_value = ['file1.tmp', 'file2.tmp']
        # Make one deletion succeed, one fail
        mock_remove.side_effect = [None, OSError("Permission denied")]

        main()

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('file1.tmp')
        mock_remove.assert_any_call('file2.tmp')
        mock_print.assert_any_call("  Error deleting file2.tmp: Permission denied")
        mock_print.assert_any_call("\nCleanup complete. Successfully deleted 1 files.")


if __name__ == '__main__':
    unittest.main()
