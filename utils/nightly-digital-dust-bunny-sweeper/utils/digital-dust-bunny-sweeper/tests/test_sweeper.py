import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import find_old_files, delete_files

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_files_basic(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual disk access.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with files and their modification times.
        # We need to control the timestamps precisely for age-based filtering.
        # File 1: Old enough
        # File 2: Not old enough
        # File 3: Old enough, in a subdirectory
        # File 4: Error accessing

        # Define current time for consistent testing
        now = datetime(2023, 10, 26, 10, 0, 0) # Fixed current time
        # Calculate cutoff time for 30 days ago
        # cutoff_time = now - timedelta(days=30) # Not directly used in mock, but for conceptual clarity

        # Mock os.walk to return a specific directory structure
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt', 'unreadable.txt']),
            ('/test_dir/subdir', [], ['file3.log'])
        ]

        # Mock os.path.getmtime to return specific timestamps
        # Mock rationale: Control file modification times for deterministic age calculation.
        def mock_getmtime_side_effect(path):
            if path == '/test_dir/file1.txt':
                # Older than 30 days
                return (now - timedelta(days=45)).timestamp()
            elif path == '/test_dir/file2.txt':
                # Newer than 30 days
                return (now - timedelta(days=15)).timestamp()
            elif path == '/test_dir/subdir/file3.log':
                # Older than 30 days
                return (now - timedelta(days=60)).timestamp()
            elif path == '/test_dir/unreadable.txt':
                # Simulate an OSError for this file
                raise OSError("Permission denied")
            return now.timestamp() # Default for any other unexpected path

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Patch datetime.now() to return our fixed 'now' for consistent age calculation
        # Mock rationale: Ensure datetime.now() is deterministic for age calculations.
        with patch('src.sweeper.datetime') as mock_datetime:
            mock_datetime.now.return_value = now
            mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original behavior for fromtimestamp
            mock_datetime.timedelta = timedelta # Keep original behavior for timedelta

            old_files = find_old_files('/test_dir', 30)

            # Expected files: file1.txt (45 days old), file3.log (60 days old)
            expected_files = [
                ('/test_dir/file1.txt', 45),
                ('/test_dir/subdir/file3.log', 60)
            ]
            self.assertCountEqual(old_files, expected_files)

    @patch('os.path.isdir')
    def test_find_old_files_non_existent_directory(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory without actual disk access.
        mock_isdir.return_value = False
        old_files = find_old_files('/non_existent_dir', 30)
        self.assertEqual(old_files, [])

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    def test_delete_files_dry_run(self, mock_remove, mock_print):
        file_list = [
            ('/path/to/old_file1.txt', 45),
            ('/path/to/old_file2.log', 60)
        ]
        delete_files(file_list, dry_run=True)
        mock_remove.assert_not_called() # No files should be removed in dry run
        mock_print.assert_any_call("\n--- Dry Run Mode --- (No files will be deleted) ---")
        mock_print.assert_any_call("[DRY RUN] Would delete: /path/to/old_file1.txt (Age: 45 days)")
        mock_print.assert_any_call("[DRY RUN] Would delete: /path/to/old_file2.log (Age: 60 days)")

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    def test_delete_files_confirm_delete_all_yes(self, mock_input, mock_remove, mock_print):
        file_list = [
            ('/path/to/old_file1.txt', 45),
            ('/path/to/old_file2.log', 60)
        ]
        delete_files(file_list, dry_run=False, confirm_delete=True)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/old_file1.txt')
        mock_remove.assert_any_call('/path/to/old_file2.log')
        mock_print.assert_any_call("Deleted: /path/to/old_file1.txt")
        mock_print.assert_any_call("Deleted: /path/to/old_file2.log")

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    @patch('builtins.input', side_effect=['y', 'n']) # Mock rationale: Simulate user confirming some, skipping others.
    def test_delete_files_confirm_delete_some_yes(self, mock_input, mock_remove, mock_print):
        file_list = [
            ('/path/to/old_file1.txt', 45),
            ('/path/to/old_file2.log', 60)
        ]
        delete_files(file_list, dry_run=False, confirm_delete=True)
        self.assertEqual(mock_remove.call_count, 1)
        mock_remove.assert_any_call('/path/to/old_file1.txt')
        mock_print.assert_any_call("Deleted: /path/to/old_file1.txt")
        mock_print.assert_any_call("Skipped: /path/to/old_file2.log")

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    def test_delete_files_force_delete(self, mock_remove, mock_print):
        file_list = [
            ('/path/to/old_file1.txt', 45),
            ('/path/to/old_file2.log', 60)
        ]
        delete_files(file_list, dry_run=False, force_delete=True)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/old_file1.txt')
        mock_remove.assert_any_call('/path/to/old_file2.log')
        mock_print.assert_any_call("Deleted: /path/to/old_file1.txt")
        mock_print.assert_any_call("Deleted: /path/to/old_file2.log")

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    @patch('os.remove', side_effect=OSError("Test Error")) # Mock rationale: Simulate an error during deletion.
    def test_delete_files_force_delete_with_error(self, mock_remove, mock_print):
        file_list = [
            ('/path/to/old_file1.txt', 45)
        ]
        delete_files(file_list, dry_run=False, force_delete=True)
        mock_remove.assert_called_once_with('/path/to/old_file1.txt')
        mock_print.assert_any_call("Error deleting /path/to/old_file1.txt: Test Error")

    @patch('builtins.print') # Mock rationale: Capture print statements for verification.
    def test_delete_files_no_files(self, mock_print):
        file_list = []
        delete_files(file_list, dry_run=True)
        mock_print.assert_any_call("No digital dust bunnies found. Your digital space is pristine!")

    # Test main function argument parsing and flow
    @patch('src.sweeper.find_old_files', return_value=[('/mock/file.txt', 100)])
    @patch('src.sweeper.delete_files')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run_default(self, mock_parse_args, mock_delete_files, mock_find_old_files):
        # Mock rationale: Simulate command-line arguments without actually running the CLI.
        mock_parse_args.return_value = MagicMock(directory='/test', age=90, dry_run=False, confirm_delete=False, force_delete=False)
        from src.sweeper import main
        main()
        mock_find_old_files.assert_called_once_with('/test', 90)
        mock_delete_files.assert_called_once_with([('/mock/file.txt', 100)], dry_run=True, confirm_delete=False, force_delete=False)

    @patch('src.sweeper.find_old_files', return_value=[('/mock/file.txt', 100)])
    @patch('src.sweeper.delete_files')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_confirm_delete(self, mock_parse_args, mock_delete_files, mock_find_old_files):
        mock_parse_args.return_value = MagicMock(directory='/test', age=90, dry_run=False, confirm_delete=True, force_delete=False)
        from src.sweeper import main
        main()
        mock_find_old_files.assert_called_once_with('/test', 90)
        mock_delete_files.assert_called_once_with([('/mock/file.txt', 100)], dry_run=False, confirm_delete=True, force_delete=False)

    @patch('src.sweeper.find_old_files', return_value=[('/mock/file.txt', 100)])
    @patch('src.sweeper.delete_files')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_force_delete(self, mock_parse_args, mock_delete_files, mock_find_old_files):
        mock_parse_args.return_value = MagicMock(directory='/test', age=90, dry_run=False, confirm_delete=False, force_delete=True)
        from src.sweeper import main
        main()
        mock_find_old_files.assert_called_once_with('/test', 90)
        mock_delete_files.assert_called_once_with([('/mock/file.txt', 100)], dry_run=False, confirm_delete=False, force_delete=True)

    @patch('src.sweeper.find_old_files', return_value=[('/mock/file.txt', 100)])
    @patch('src.sweeper.delete_files')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_explicit_dry_run(self, mock_parse_args, mock_delete_files, mock_find_old_files):
        mock_parse_args.return_value = MagicMock(directory='/test', age=90, dry_run=True, confirm_delete=False, force_delete=False)
        from src.sweeper import main
        main()
        mock_find_old_files.assert_called_once_with('/test', 90)
        mock_delete_files.assert_called_once_with([('/mock/file.txt', 100)], dry_run=True, confirm_delete=False, force_delete=False)
