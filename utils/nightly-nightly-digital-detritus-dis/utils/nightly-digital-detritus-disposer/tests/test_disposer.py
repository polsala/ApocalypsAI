import unittest
import os
import time
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.disposer import get_old_files, main

class TestDigitalDetritusDisposer(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing
        self.base_time = datetime(2023, 1, 1, 12, 0, 0)
        # Mock time.time() to return a fixed timestamp for deterministic age calculation
        # Mock rationale: Ensures that file age calculations are consistent across test runs,
        #                 regardless of when the tests are executed.
        self.mock_time_patcher = patch('time.time', return_value=self.base_time.timestamp())
        self.mock_time = self.mock_time_patcher.start()

    def tearDown(self):
        self.mock_time_patcher.stop()

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_finds_old_files(self, mock_getmtime, mock_walk):
        # Mock rationale: os.walk is a file system operation. Mocking it allows us to simulate
        #                 a directory structure without actually creating files on disk.
        mock_walk.return_value = [
            ('/mock_dir', [], ['file_old.txt', 'file_new.txt']),
            ('/mock_dir/subdir', [], ['another_old.log'])
        ]

        # Mock rationale: os.path.getmtime is a file system operation. Mocking it allows us to
        #                 control the modification times of simulated files, making tests deterministic.
        #                 We can precisely define which files are 'old' and which are 'new'.
        def mock_mtime_side_effect(path):
            if 'file_old.txt' in path:
                # Older than 30 days from base_time
                return (self.base_time - timedelta(days=31)).timestamp()
            elif 'another_old.log' in path:
                # Older than 30 days from base_time
                return (self.base_time - timedelta(days=45)).timestamp()
            elif 'file_new.txt' in path:
                # Newer than 30 days from base_time
                return (self.base_time - timedelta(days=10)).timestamp()
            return self.base_time.timestamp() # Default for others

        mock_getmtime.side_effect = mock_mtime_side_effect

        old_files = get_old_files('/mock_dir', 30)
        expected_files = [
            os.path.join('/mock_dir', 'file_old.txt'),
            os.path.join('/mock_dir/subdir', 'another_old.log')
        ]
        self.assertCountEqual(old_files, expected_files)
        self.assertEqual(mock_getmtime.call_count, 3) # Called for file_old, file_new, another_old

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_no_old_files(self, mock_getmtime, mock_walk):
        # Mock rationale: Same as above, simulating a directory with only new files.
        mock_walk.return_value = [
            ('/mock_dir', [], ['file_new1.txt', 'file_new2.txt'])
        ]
        mock_getmtime.return_value = (self.base_time - timedelta(days=10)).timestamp()

        old_files = get_old_files('/mock_dir', 30)
        self.assertEqual(old_files, [])

    @patch('os.walk')
    @patch('os.path.getmtime', side_effect=OSError("Permission denied"))
    def test_get_old_files_handles_os_error(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulates a scenario where file access fails (e.g., permissions).
        #                 Ensures the utility gracefully handles such errors without crashing.
        mock_walk.return_value = [
            ('/mock_dir', [], ['unreadable.txt'])
        ]

        with patch('builtins.print') as mock_print:
            old_files = get_old_files('/mock_dir', 30)
            self.assertEqual(old_files, [])
            mock_print.assert_called_with(unittest.mock.ANY) # Check if warning was printed
            self.assertIn("Warning: Could not access file", mock_print.call_args[0][0])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('src.disposer.get_old_files', return_value=[os.path.join('/mock_dir', 'old.txt')])
    @patch('builtins.print')
    @patch('os.remove')
    def test_main_dry_run(self, mock_remove, mock_print, mock_get_old_files, mock_isdir, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to provide command-line arguments
        #                 programmatically, avoiding actual CLI interaction during tests.
        mock_parse_args.return_value = argparse.Namespace(
            path='/mock_dir', age=30, dry_run=True, delete=False
        )
        # Mock rationale: os.path.isdir is a file system check. Mocking it ensures the test doesn't
        #                 depend on the existence of a real directory.
        # Mock rationale: src.disposer.get_old_files is the core logic for finding files. Mocking it
        #                 isolates the 'main' function's behavior from the file scanning logic,
        #                 allowing us to test argument parsing and output independently.
        # Mock rationale: builtins.print is mocked to capture stdout and verify that the correct
        #                 messages are displayed to the user without polluting the test runner's console.
        # Mock rationale: os.remove is a file system modification. Mocking it prevents actual file
        #                 deletion during tests, ensuring test safety and determinism.

        main()

        mock_print.assert_any_call("\nScanning '/mock_dir' for files older than 30 days...")
        mock_print.assert_any_call("\nFound 1 pieces of digital detritus:")
        mock_print.assert_any_call(f"  - {os.path.join('/mock_dir', 'old.txt')}")
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were deleted.")
        mock_remove.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('src.disposer.get_old_files', return_value=[os.path.join('/mock_dir', 'old.txt'), os.path.join('/mock_dir', 'another_old.log')])
    @patch('builtins.print')
    @patch('os.remove')
    def test_main_delete_mode(self, mock_remove, mock_print, mock_get_old_files, mock_isdir, mock_parse_args):
        # Mock rationale: Same as above, but for the delete mode.
        mock_parse_args.return_value = argparse.Namespace(
            path='/mock_dir', age=30, dry_run=False, delete=True
        )

        main()

        mock_print.assert_any_call("\nInitiating detritus disposal... (This cannot be undone!)")
        mock_remove.assert_any_call(os.path.join('/mock_dir', 'old.txt'))
        mock_remove.assert_any_call(os.path.join('/mock_dir', 'another_old.log'))
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("\nDetritus disposal complete. Your filesystem thanks you! 💖")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('src.disposer.get_old_files', return_value=[])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_detritus_found(self, mock_exit, mock_print, mock_get_old_files, mock_isdir, mock_parse_args):
        # Mock rationale: Simulates a clean directory. sys.exit is mocked to prevent the test runner
        #                 from exiting prematurely when the utility reports no detritus.
        mock_parse_args.return_value = argparse.Namespace(
            path='/mock_dir', age=30, dry_run=True, delete=False
        )

        main()

        mock_print.assert_any_call("No digital detritus found! Your filesystem is sparkling clean. ✨")
        mock_exit.assert_called_with(0) # Expect exit code 0 for no-op

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Simulates an invalid path provided by the user.
        mock_parse_args.return_value = argparse.Namespace(
            path='/non_existent_dir', age=30, dry_run=True, delete=False
        )

        main()

        mock_print.assert_any_call("Error: Directory '/non_existent_dir' does not exist or is not a directory.")
        mock_exit.assert_called_with(1) # Expect exit code 1 for failure

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_dry_run_and_delete_error(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Tests the argument validation for mutually exclusive flags.
        mock_parse_args.return_value = argparse.Namespace(
            path='/mock_dir', age=30, dry_run=True, delete=True
        )

        main()

        mock_print.assert_any_call("Error: Cannot use --dry-run and --delete together. Choose one.")
        mock_exit.assert_called_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('src.disposer.get_old_files', return_value=[os.path.join('/mock_dir', 'unremovable.txt')])
    @patch('builtins.print')
    @patch('os.remove', side_effect=OSError("Permission denied"))
    def test_main_delete_error_handling(self, mock_remove, mock_print, mock_get_old_files, mock_isdir, mock_parse_args):
        # Mock rationale: Simulates a scenario where a file cannot be deleted (e.g., permissions).
        #                 Ensures the utility reports the error gracefully and continues.
        mock_parse_args.return_value = argparse.Namespace(
            path='/mock_dir', age=30, dry_run=False, delete=True
        )

        main()

        mock_remove.assert_called_once_with(os.path.join('/mock_dir', 'unremovable.txt'))
        mock_print.assert_any_call(unittest.mock.ANY) # Check if error was printed
        self.assertIn("Error deleting", mock_print.call_args_list[-2][0][0]) # Check the second to last print call
        mock_print.assert_any_call("\nDetritus disposal complete. Your filesystem thanks you! 💖")


if __name__ == '__main__':
    unittest.main()
