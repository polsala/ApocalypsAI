import unittest
import os
import shutil
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
# Assuming duster.py is in the same directory as test_duster.py for local import
# In a real scenario, you might adjust sys.path or use a package structure
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import get_file_age_in_days, find_debris_files, quarantine_file, main

class TestDataDebrisDuster(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_in_days(self, mock_datetime, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, datetime.datetime.now() returns current time.
        # We need to control these to ensure deterministic age calculation.
        mock_getmtime.return_value = datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_datetime.now.return_value = datetime(2023, 1, 31, 10, 0, 0) # 30 days later
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Allow real conversion

        age = get_file_age_in_days("/fake/path/file.txt")
        self.assertEqual(age, 30)

        mock_getmtime.return_value = datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_datetime.now.return_value = datetime(2023, 1, 1, 9, 0, 0) # File is in the future, age should be negative
        age = get_file_age_in_days("/fake/path/file.txt")
        self.assertEqual(age, -1) # Or 0, depending on how we want to handle future files. Current implementation returns -1 for age < 0.

        mock_getmtime.side_effect = OSError # Simulate file not found or permissions error
        age = get_file_age_in_days("/nonexistent/file.txt")
        self.assertEqual(age, -1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_find_debris_files(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir checks if a path is a directory. os.walk iterates through directory structure.
        # os.path.getmtime and datetime.datetime.now() are needed for age calculation.
        # We need to control the file system structure and file modification times for deterministic testing.

        mock_isdir.return_value = True
        mock_datetime.now.return_value = datetime(2024, 1, 31)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        # Scenario 1: Files found
        mock_walk.return_value = [
            ('/test_root', [], ['old_file.txt', 'new_file.txt']),
            ('/test_root/subdir', [], ['another_old.log'])
        ]
        # old_file.txt: 60 days old (older than 30)
        # new_file.txt: 10 days old (not older than 30)
        # another_old.log: 45 days old (older than 30)
        file_mtimes = {
            os.path.join('/test_root', 'old_file.txt'): (datetime(2024, 1, 31) - timedelta(days=60)).timestamp(),
            os.path.join('/test_root', 'new_file.txt'): (datetime(2024, 1, 31) - timedelta(days=10)).timestamp(),
            os.path.join('/test_root/subdir', 'another_old.log'): (datetime(2024, 1, 31) - timedelta(days=45)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, 0) # Return 0 for unknown files, though should not happen with this setup

        debris = find_debris_files('/test_root', 30)
        self.assertIn(os.path.join('/test_root', 'old_file.txt'), debris)
        self.assertIn(os.path.join('/test_root/subdir', 'another_old.log'), debris)
        self.assertNotIn(os.path.join('/test_root', 'new_file.txt'), debris)
        self.assertEqual(len(debris), 2)

        # Scenario 2: No files found
        mock_walk.return_value = [
            ('/test_root', [], ['new_file_1.txt', 'new_file_2.log'])
        ]
        file_mtimes = {
            os.path.join('/test_root', 'new_file_1.txt'): (datetime(2024, 1, 31) - timedelta(days=5)).timestamp(),
            os.path.join('/test_root', 'new_file_2.log'): (datetime(2024, 1, 31) - timedelta(days=15)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, 0)

        debris = find_debris_files('/test_root', 30)
        self.assertEqual(len(debris), 0)

        # Scenario 3: Root path is not a directory
        mock_isdir.return_value = False
        debris = find_debris_files('/non_existent_root', 30)
        self.assertEqual(len(debris), 0)
        mock_isdir.assert_called_with('/non_existent_root')


    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.dirname')
    @patch('os.path.basename')
    @patch('os.path.join')
    def test_quarantine_file(self, mock_join, mock_basename, mock_dirname, mock_move, mock_makedirs):
        # Mock rationale: os.makedirs creates directories, shutil.move moves files.
        # os.path.dirname, os.path.basename, os.path.join are used for path manipulation.
        # We need to control these to simulate file system operations without touching the actual disk.

        mock_dirname.return_value = '/parent/dir'
        mock_basename.return_value = 'file.txt'
        mock_join.side_effect = lambda *args: '/'.join(args) # Simple join for testing

        # Test successful quarantine
        result = quarantine_file('/parent/dir/file.txt', 'quarantine_zone')
        mock_makedirs.assert_called_with('/parent/dir/quarantine_zone', exist_ok=True)
        mock_move.assert_called_with('/parent/dir/file.txt', '/parent/dir/quarantine_zone/file.txt')
        self.assertTrue(result)

        # Test failed quarantine (e.g., permissions error)
        mock_move.side_effect = OSError("Permission denied")
        result = quarantine_file('/parent/dir/file.txt', 'quarantine_zone')
        self.assertFalse(result)
        mock_move.reset_mock() # Reset mock for next test
        mock_move.side_effect = None # Clear side effect

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_debris_files')
    @patch('duster.quarantine_file')
    @patch('duster.get_file_age_in_days')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print') # Mock print to capture output
    def test_main_list_mode(self, mock_print, mock_isdir, mock_exists, mock_get_file_age_in_days, mock_quarantine_file, mock_find_debris_files, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # find_debris_files, quarantine_file, get_file_age_in_days are core functions already tested,
        # so we mock them to control their return values and verify main's logic.
        # os.path.exists and os.path.isdir are for initial path validation.
        # builtins.print is mocked to capture output and assert messages.

        # Setup mock arguments for list mode
        mock_parse_args.return_value = argparse.Namespace(
            path='/test/path', age=30, mode='list', quarantine_dir_name='_quarantined_debris_'
        )
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_get_file_age_in_days.return_value = 45 # For printing age

        # Scenario 1: Debris found, list mode
        mock_find_debris_files.return_value = ['/test/path/old_file.txt', '/test/path/subdir/another_old.log']
        main()
        mock_find_debris_files.assert_called_with('/test/path', 30)
        mock_quarantine_file.assert_not_called() # Should not quarantine in list mode
        mock_print.assert_any_call("\n--- Found 2 pieces of data debris ---")
        mock_print.assert_any_call("🗑️  [DEBRIS] /test/path/old_file.txt (Age: 45 days)")
        mock_print.assert_any_call("💡 Tip: Run with `--mode quarantine` to move these files to a quarantine zone.")

        # Scenario 2: No debris found
        mock_find_debris_files.return_value = []
        main()
        mock_print.assert_any_call("✨ All clear! No data debris older than 30 days found in '/test/path'.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_debris_files')
    @patch('duster.quarantine_file')
    @patch('duster.get_file_age_in_days')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_main_quarantine_mode(self, mock_print, mock_isdir, mock_exists, mock_get_file_age_in_days, mock_quarantine_file, mock_find_debris_files, mock_parse_args):
        # Setup mock arguments for quarantine mode
        mock_parse_args.return_value = argparse.Namespace(
            path='/test/path', age=30, mode='quarantine', quarantine_dir_name='_quarantined_debris_'
        )
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_get_file_age_in_days.return_value = 45

        # Scenario 1: Debris found, quarantine mode, all successful
        mock_find_debris_files.return_value = ['/test/path/old_file_1.txt', '/test/path/old_file_2.txt']
        mock_quarantine_file.return_value = True # Simulate successful quarantine
        main()
        mock_find_debris_files.assert_called_with('/test/path', 30)
        self.assertEqual(mock_quarantine_file.call_count, 2) # Called for each file
        mock_quarantine_file.assert_any_call('/test/path/old_file_1.txt', '_quarantined_debris_')
        mock_quarantine_file.assert_any_call('/test/path/old_file_2.txt', '_quarantined_debris_')
        mock_print.assert_any_call("\n✅ Operation complete: 2 files quarantined.")

        # Scenario 2: Debris found, quarantine mode, some failures
        mock_find_debris_files.return_value = ['/test/path/old_file_1.txt', '/test/path/old_file_2.txt']
        mock_quarantine_file.side_effect = [True, False] # First succeeds, second fails
        main()
        self.assertEqual(mock_quarantine_file.call_count, 4) # Called 2 more times (total 4)
        mock_print.assert_any_call("\n✅ Operation complete: 1 files quarantined.") # Only 1 successful

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print')
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_path_validation(self, mock_exit, mock_print, mock_isdir, mock_exists, mock_parse_args):
        # Scenario 1: Path does not exist
        mock_parse_args.return_value = argparse.Namespace(
            path='/nonexistent', age=30, mode='list', quarantine_dir_name='_quarantined_debris_'
        )
        mock_exists.return_value = False
        main()
        mock_print.assert_any_call("🚫 Error: The specified path '/nonexistent' does not exist. Aborting duster operation.")
        mock_exit.assert_called_with(1)
        mock_exit.reset_mock() # Reset for next test

        # Scenario 2: Path is not a directory
        mock_parse_args.return_value = argparse.Namespace(
            path='/file.txt', age=30, mode='list', quarantine_dir_name='_quarantined_debris_'
        )
        mock_exists.return_value = True
        mock_isdir.return_value = False
        main()
        mock_print.assert_any_call("🚫 Error: The specified path '/file.txt' is not a directory. Aborting duster operation.")
        mock_exit.assert_called_with(1)
        mock_exit.reset_mock()

        # Scenario 3: Age is negative
        mock_parse_args.return_value = argparse.Namespace(
            path='/valid/path', age=-5, mode='list', quarantine_dir_name='_quarantined_debris_'
        )
        mock_exists.return_value = True
        mock_isdir.return_value = True
        main()
        mock_print.assert_any_call("🚫 Error: Age must be a non-negative integer. Got '-5'. Aborting duster operation.")
        mock_exit.assert_called_with(1)
        mock_exit.reset_mock()


if __name__ == '__main__':
    unittest.main()
