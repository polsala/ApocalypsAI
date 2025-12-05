import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from datetime import datetime, timedelta

# Import the function to be tested
from src.finder import find_and_manage_forgotten_files

class TestForgottenFileFinder(unittest.TestCase):

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_finds_and_reports_old_files(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: We need to control the current time to determine file age.
        # We also need to simulate file system traversal and file modification times
        # without actually touching the disk.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now

        # Simulate directory structure and files
        target_dir = "/test_project"
        old_file_path = os.path.join(target_dir, "old_file.txt")
        new_file_path = os.path.join(target_dir, "new_file.txt")
        nested_old_file_path = os.path.join(target_dir, "sub", "nested_old.log")

        # Mock os.walk to return our simulated files
        mock_walk.return_value = [
            (target_dir, ["sub"], ["old_file.txt", "new_file.txt"]),
            (os.path.join(target_dir, "sub"), [], ["nested_old.log"])
        ]

        # Mock os.path.getmtime for each file
        # Old file (modified 31 days ago)
        mock_getmtime.side_effect = lambda p: {
            old_file_path: (mock_now - timedelta(days=31)).timestamp(),
            new_file_path: (mock_now - timedelta(days=5)).timestamp(),
            nested_old_file_path: (mock_now - timedelta(days=45)).timestamp(),
        }.get(p, mock_now.timestamp()) # Default to now if path not explicitly mocked

        # Mock os.path.isdir to confirm target_dir exists
        mock_isdir.return_value = True # For target_dir

        # Run the function in report-only mode
        results = find_and_manage_forgotten_files(
            target_dir=target_dir,
            age_days=30,
            report_only=True
        )

        # Assertions
        self.assertEqual(len(results['found_files']), 2)
        self.assertIn(old_file_path, results['found_files'])
        self.assertIn(nested_old_file_path, results['found_files'])
        self.assertNotIn(new_file_path, results['found_files'])
        self.assertEqual(len(results['quarantined_files']), 0)
        self.assertEqual(len(results['errors']), 0)
        mock_move.assert_not_called() # Should not move in report-only mode

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_moves_old_files_to_quarantine(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Similar to above, but specifically testing the move operation.
        # We need to ensure shutil.move is called with the correct source and destination paths.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now

        target_dir = "/test_project"
        quarantine_dir = "/quarantine_zone"
        old_file_path = os.path.join(target_dir, "old_file.txt")
        nested_old_file_path = os.path.join(target_dir, "sub", "nested_old.log")

        mock_walk.return_value = [
            (target_dir, ["sub"], ["old_file.txt"]),
            (os.path.join(target_dir, "sub"), [], ["nested_old.log"])
        ]

        mock_getmtime.side_effect = lambda p: {
            old_file_path: (mock_now - timedelta(days=31)).timestamp(),
            nested_old_file_path: (mock_now - timedelta(days=45)).timestamp(),
        }.get(p, mock_now.timestamp())

        mock_isdir.side_effect = lambda p: p == target_dir or p == quarantine_dir # target_dir exists, quarantine_dir might be created

        results = find_and_manage_forgotten_files(
            target_dir=target_dir,
            age_days=30,
            quarantine_dir=quarantine_dir,
            report_only=False
        )

        self.assertEqual(len(results['found_files']), 2)
        self.assertEqual(len(results['quarantined_files']), 2)
        self.assertIn(old_file_path, results['quarantined_files'])
        self.assertIn(nested_old_file_path, results['quarantined_files'])
        self.assertEqual(len(results['errors']), 0)

        # Assert that quarantine directory was attempted to be created
        mock_makedirs.assert_any_call(quarantine_dir, exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(quarantine_dir, "sub"), exist_ok=True)

        # Assert shutil.move was called for each old file
        mock_move.assert_any_call(old_file_path, os.path.join(quarantine_dir, "old_file.txt"))
        mock_move.assert_any_call(nested_old_file_path, os.path.join(quarantine_dir, "sub", "nested_old.log"))
        self.assertEqual(mock_move.call_count, 2)

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_handles_non_existent_target_directory(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Test error handling for invalid input.
        mock_isdir.return_value = False # Simulate target_dir not existing

        results = find_and_manage_forgotten_files(
            target_dir="/non_existent",
            age_days=10,
            report_only=True
        )

        self.assertEqual(len(results['found_files']), 0)
        self.assertEqual(len(results['quarantined_files']), 0)
        self.assertEqual(len(results['errors']), 1)
        self.assertIn("Target directory '/non_existent' not found.", results['errors'])
        mock_walk.assert_not_called()
        mock_move.assert_not_called()

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_handles_empty_target_directory(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Ensure the utility behaves correctly when no files are found.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now

        target_dir = "/empty_project"
        mock_walk.return_value = [(target_dir, [], [])] # No files
        mock_isdir.return_value = True

        results = find_and_manage_forgotten_files(
            target_dir=target_dir,
            age_days=30,
            report_only=True
        )

        self.assertEqual(len(results['found_files']), 0)
        self.assertEqual(len(results['quarantined_files']), 0)
        self.assertEqual(len(results['errors']), 0)
        mock_move.assert_not_called()

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_move_failure_is_reported(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Test error handling during the move operation.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now

        target_dir = "/test_project"
        quarantine_dir = "/quarantine_zone"
        old_file_path = os.path.join(target_dir, "old_file.txt")

        mock_walk.return_value = [(target_dir, [], ["old_file.txt"])]
        mock_getmtime.return_value = (mock_now - timedelta(days=31)).timestamp()
        mock_isdir.return_value = True
        mock_move.side_effect = Exception("Permission denied") # Simulate a move error

        results = find_and_manage_forgotten_files(
            target_dir=target_dir,
            age_days=30,
            quarantine_dir=quarantine_dir,
            report_only=False
        )

        self.assertEqual(len(results['found_files']), 1)
        self.assertEqual(len(results['quarantined_files']), 0) # Should not be quarantined if move failed
        self.assertEqual(len(results['errors']), 1)
        self.assertIn("Failed to move", results['errors'][0])
        mock_move.assert_called_once()

    @patch('src.finder.datetime')
    @patch('src.finder.os.walk')
    @patch('src.finder.os.path.getmtime')
    @patch('src.finder.os.path.isdir')
    @patch('src.finder.os.makedirs')
    @patch('src.finder.shutil.move')
    def test_quarantine_dir_creation(self, mock_move, mock_makedirs, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Ensure the quarantine directory is created if it doesn't exist.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now

        target_dir = "/test_project"
        quarantine_dir = "/new_quarantine_zone"
        old_file_path = os.path.join(target_dir, "old_file.txt")

        mock_walk.return_value = [(target_dir, [], ["old_file.txt"])]
        mock_getmtime.return_value = (mock_now - timedelta(days=31)).timestamp()
        mock_isdir.side_effect = lambda p: p == target_dir # target_dir exists, quarantine_dir does not initially

        results = find_and_manage_forgotten_files(
            target_dir=target_dir,
            age_days=30,
            quarantine_dir=quarantine_dir,
            report_only=False
        )

        self.assertEqual(len(results['found_files']), 1)
        self.assertEqual(len(results['quarantined_files']), 1)
        self.assertEqual(len(results['errors']), 0)
        mock_makedirs.assert_any_call(quarantine_dir, exist_ok=True)
        mock_move.assert_called_once_with(old_file_path, os.path.join(quarantine_dir, "old_file.txt"))

    @patch('src.finder.argparse.ArgumentParser')
    @patch('src.finder.find_and_manage_forgotten_files')
    def test_main_function_calls_finder_with_correct_args(self, mock_finder, mock_argparse):
        # Mock rationale: Test the main function's argument parsing and how it calls the core logic.
        # We don't need to mock file system operations here, just the argparse and the core function call.
        mock_args = MagicMock()
        mock_args.path = "/mock/path"
        mock_args.age = 60
        mock_args.quarantine = "/mock/quarantine"
        mock_args.report_only = True

        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = mock_args
        mock_argparse.return_value = mock_parser

        # Call main directly
        from src.finder import main
        main()

        mock_finder.assert_called_once_with(
            target_dir="/mock/path",
            age_days=60,
            quarantine_dir="/mock/quarantine",
            report_only=True
        )

if __name__ == '__main__':
    unittest.main()
