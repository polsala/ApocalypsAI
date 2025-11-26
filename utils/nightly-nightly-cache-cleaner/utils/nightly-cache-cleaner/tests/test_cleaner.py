import unittest
import os
import sys
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing cleaner.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cleaner

class TestCleaner(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_files_to_clean_pattern_and_age(self, mock_datetime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate file system structure and modification times for deterministic testing.
        # Mock datetime.datetime.now to control the "current" time for age calculations.
        # Mock os.walk to provide a predefined directory structure.
        # Mock os.path.getmtime to return specific modification times for files.

        # Set a fixed "current" time for testing age
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        root_path = "/test_root"
        patterns = ["*.tmp", "*.log"]
        min_age_days = 7

        # Simulate files:
        # - file1.tmp: old, matches pattern -> should be deleted
        # - file2.log: new, matches pattern -> should NOT be deleted
        # - file3.txt: old, no pattern match -> should NOT be deleted
        # - file4.tmp: new, matches pattern -> should NOT be deleted
        # - sub/file5.log: old, matches pattern -> should be deleted
        
        # Mock os.walk to return a specific directory structure
        mock_walk.return_value = [
            (root_path, ['sub'], ['file1.tmp', 'file2.log', 'file3.txt']),
            (os.path.join(root_path, 'sub'), [], ['file5.log', 'file4.tmp'])
        ]

        # Mock os.path.getmtime for each file
        # Old files (older than 7 days from mock_now)
        old_timestamp = (mock_now - timedelta(days=10)).timestamp()
        # New files (newer than 7 days from mock_now)
        new_timestamp = (mock_now - timedelta(days=3)).timestamp()

        mock_getmtime.side_effect = lambda path: {
            os.path.join(root_path, 'file1.tmp'): old_timestamp,
            os.path.join(root_path, 'file2.log'): new_timestamp,
            os.path.join(root_path, 'file3.txt'): old_timestamp,
            os.path.join(root_path, 'sub', 'file5.log'): old_timestamp,
            os.path.join(root_path, 'sub', 'file4.tmp'): new_timestamp,
        }.get(path, new_timestamp) # Default to new if path not explicitly set

        expected_files = [
            os.path.join(root_path, 'file1.tmp'),
            os.path.join(root_path, 'sub', 'file5.log')
        ]

        result = cleaner.get_files_to_clean(root_path, patterns, min_age_days)
        self.assertCountEqual(result, expected_files)
        
        # Ensure getmtime was called for relevant files
        mock_getmtime.assert_any_call(os.path.join(root_path, 'file1.tmp'))
        mock_getmtime.assert_any_call(os.path.join(root_path, 'file2.log'))
        mock_getmtime.assert_any_call(os.path.join(root_path, 'file3.txt'))
        mock_getmtime.assert_any_call(os.path.join(root_path, 'sub', 'file5.log'))
        mock_getmtime.assert_any_call(os.path.join(root_path, 'sub', 'file4.tmp'))


    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_files_to_clean_no_match(self, mock_datetime, mock_getmtime, mock_walk):
        # Mock rationale: Test scenario where no files match the criteria.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_path = "/test_root"
        patterns = ["*.xyz"] # No files will match this pattern
        min_age_days = 1

        mock_walk.return_value = [
            (root_path, [], ['file1.tmp', 'file2.log'])
        ]
        mock_getmtime.return_value = (mock_now - timedelta(days=10)).timestamp()

        result = cleaner.get_files_to_clean(root_path, patterns, min_age_days)
        self.assertEqual(result, [])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_files_to_clean_empty_directory(self, mock_datetime, mock_getmtime, mock_walk):
        # Mock rationale: Test scenario with an empty directory.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_path = "/test_root"
        patterns = ["*.tmp"]
        min_age_days = 1

        mock_walk.return_value = [] # Empty directory
        mock_getmtime.return_value = (mock_now - timedelta(days=10)).timestamp()

        result = cleaner.get_files_to_clean(root_path, patterns, min_age_days)
        self.assertEqual(result, [])

    @patch('os.path.isdir', return_value=True)
    @patch('cleaner.get_files_to_clean', return_value=['/test_root/file1.tmp', '/test_root/file2.log'])
    @patch('builtins.input', return_value='yes')
    @patch('os.remove')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_delete_success(self, mock_print, mock_parse_args, mock_remove, mock_input, mock_get_files, mock_isdir):
        # Mock rationale: Test the main execution path for successful deletion.
        # Mock argparse to control command-line arguments.
        # Mock os.path.isdir to simulate a valid directory.
        # Mock cleaner.get_files_to_clean to provide a list of files to be deleted.
        # Mock builtins.input to simulate user confirmation.
        # Mock os.remove to verify deletion calls.
        # Mock builtins.print to capture output.

        mock_parse_args.return_value = argparse.Namespace(
            path="/test_root",
            patterns="*.tmp,*.log",
            age=7,
            dry_run=False,
            force=False
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 0) # Expect exit code 0 for success
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/test_root/file1.tmp')
        mock_remove.assert_any_call('/test_root/file2.log')
        mock_input.assert_called_once()
        mock_print.assert_any_call("Deleted: /test_root/file1.tmp")
        mock_print.assert_any_call("Deleted: /test_root/file2.log")
        mock_print.assert_any_call("\nClean-up complete. Successfully deleted 2 files.")

    @patch('os.path.isdir', return_value=True)
    @patch('cleaner.get_files_to_clean', return_value=['/test_root/file1.tmp'])
    @patch('builtins.input', return_value='no')
    @patch('os.remove')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_delete_cancelled(self, mock_print, mock_parse_args, mock_remove, mock_input, mock_get_files, mock_isdir):
        # Mock rationale: Test the main execution path when user cancels deletion.
        mock_parse_args.return_value = argparse.Namespace(
            path="/test_root",
            patterns="*.tmp",
            age=7,
            dry_run=False,
            force=False
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 2) # Expect exit code 2 for no-op
        mock_remove.assert_not_called()
        mock_input.assert_called_once()
        mock_print.assert_any_call("Deletion cancelled.")

    @patch('os.path.isdir', return_value=True)
    @patch('cleaner.get_files_to_clean', return_value=['/test_root/file1.tmp'])
    @patch('os.remove')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_dry_run(self, mock_print, mock_parse_args, mock_remove, mock_get_files, mock_isdir):
        # Mock rationale: Test the main execution path for dry-run mode.
        mock_parse_args.return_value = argparse.Namespace(
            path="/test_root",
            patterns="*.tmp",
            age=7,
            dry_run=True,
            force=False
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 0) # Dry run is a successful operation
        mock_remove.assert_not_called()
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were deleted.")

    @patch('os.path.isdir', return_value=True)
    @patch('cleaner.get_files_to_clean', return_value=['/test_root/file1.tmp'])
    @patch('os.remove')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_force_delete(self, mock_print, mock_parse_args, mock_remove, mock_get_files, mock_isdir):
        # Mock rationale: Test the main execution path for forced deletion (no confirmation).
        mock_parse_args.return_value = argparse.Namespace(
            path="/test_root",
            patterns="*.tmp",
            age=7,
            dry_run=False,
            force=True
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 0)
        mock_remove.assert_called_once_with('/test_root/file1.tmp')
        # Ensure input() was NOT called because --force was used
        with patch('builtins.input') as mock_input:
            cleaner.main()
            mock_input.assert_not_called()

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_parse_args, mock_isdir):
        # Mock rationale: Test the main execution path with an invalid directory path.
        mock_parse_args.return_value = argparse.Namespace(
            path="/non_existent_path",
            patterns="*.tmp",
            age=7,
            dry_run=False,
            force=False
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for error
        mock_print.assert_any_call("Error: The specified path '/non_existent_path' is not a valid directory.")

    @patch('os.path.isdir', return_value=True)
    @patch('cleaner.get_files_to_clean', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_no_files_found(self, mock_print, mock_parse_args, mock_get_files, mock_isdir):
        # Mock rationale: Test the main execution path when no files are found to clean.
        mock_parse_args.return_value = argparse.Namespace(
            path="/test_root",
            patterns="*.tmp",
            age=7,
            dry_run=False,
            force=False
        )

        with self.assertRaises(SystemExit) as cm:
            cleaner.main()
        
        self.assertEqual(cm.exception.code, 0) # No files found is a successful no-op
        mock_print.assert_any_call("No forgotten files found matching the criteria. Your digital space is pristine!")


if __name__ == '__main__':
    unittest.main()
