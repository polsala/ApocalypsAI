import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the sweeper module
from src.sweeper import get_file_age_in_days, is_empty_dir, find_dust_bunnies, clean_dust_bunnies, main

class TestSweeper(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the modification time of a file.
        # We need to control this value to simulate files of different ages for testing.
        # We also mock time.time() to ensure a consistent 'current' time.
        with patch('time.time', return_value=datetime(2023, 1, 31).timestamp()):
            # File modified 10 days ago
            mock_getmtime.return_value = datetime(2023, 1, 21).timestamp()
            self.assertAlmostEqual(get_file_age_in_days("dummy_file"), 10.0, places=5)

            # File modified 0 days ago (current time)
            mock_getmtime.return_value = datetime(2023, 1, 31).timestamp()
            self.assertAlmostEqual(get_file_age_in_days("dummy_file"), 0.0, places=5)

            # Test OSError
            mock_getmtime.side_effect = OSError
            self.assertEqual(get_file_age_in_days("non_existent_file"), -1)

    @patch('os.listdir')
    def test_is_empty_dir(self, mock_listdir):
        # Mock rationale: os.listdir returns a list of entries in a directory.
        # We need to control this list to simulate empty and non-empty directories.
        mock_listdir.return_value = []
        self.assertTrue(is_empty_dir("empty_dir"))

        mock_listdir.return_value = ["file.txt"]
        self.assertFalse(is_empty_dir("non_empty_dir"))

        mock_listdir.return_value = ["subdir"]
        self.assertFalse(is_empty_dir("non_empty_dir_with_subdir"))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_find_dust_bunnies_age_threshold(self, mock_time, mock_getmtime, mock_walk):
        # Mock rationale: os.walk simulates the directory tree traversal.
        # os.path.getmtime and time.time are mocked to control file ages.
        # This allows us to create a deterministic file system state for testing.

        mock_time.return_value = datetime(2023, 1, 31).timestamp() # Current time

        # Simulate a directory structure:
        # root/
        #   old_file.txt (modified 35 days ago)
        #   new_file.txt (modified 5 days ago)
        #   subdir/
        #     another_old_file.log (modified 40 days ago)
        #     empty_dir/
        mock_walk.return_value = [
            ("root", ["subdir"], ["old_file.txt", "new_file.txt"]),
            ("root/subdir", ["empty_dir"], ["another_old_file.log"]),
            ("root/subdir/empty_dir", [], [])
        ]

        # Mock modification times
        def mock_mtime_side_effect(path):
            if "old_file.txt" in path:
                return datetime(2022, 12, 27).timestamp() # 35 days old
            elif "new_file.txt" in path:
                return datetime(2023, 1, 26).timestamp() # 5 days old
            elif "another_old_file.log" in path:
                return datetime(2022, 12, 22).timestamp() # 40 days old
            return mock_time.return_value # Default to current for others

        mock_getmtime.side_effect = mock_mtime_side_effect

        # Test with age threshold 30 days
        files, dirs = find_dust_bunnies("root", age_threshold_days=30)
        self.assertIn(os.path.join("root", "old_file.txt"), files)
        self.assertIn(os.path.join("root", "subdir", "another_old_file.log"), files)
        self.assertNotIn(os.path.join("root", "new_file.txt"), files)
        self.assertIn(os.path.join("root", "subdir", "empty_dir"), dirs) # empty_dir is found
        self.assertEqual(len(files), 2)
        self.assertEqual(len(dirs), 1)

        # Test with no age threshold, but patterns
        files, dirs = find_dust_bunnies("root", patterns=["*.log"])
        self.assertIn(os.path.join("root", "subdir", "another_old_file.log"), files)
        self.assertNotIn(os.path.join("root", "old_file.txt"), files)
        self.assertNotIn(os.path.join("root", "new_file.txt"), files)
        self.assertIn(os.path.join("root", "subdir", "empty_dir"), dirs)
        self.assertEqual(len(files), 1)
        self.assertEqual(len(dirs), 1)

        # Test with both age and patterns
        files, dirs = find_dust_bunnies("root", age_threshold_days=30, patterns=["*.txt"])
        self.assertIn(os.path.join("root", "old_file.txt"), files) # Old AND .txt
        self.assertNotIn(os.path.join("root", "new_file.txt"), files) # .txt but not old enough
        self.assertNotIn(os.path.join("root", "subdir", "another_old_file.log"), files) # Old but not .txt
        self.assertIn(os.path.join("root", "subdir", "empty_dir"), dirs)
        self.assertEqual(len(files), 1)
        self.assertEqual(len(dirs), 1)

        # Test empty_dirs_only
        files, dirs = find_dust_bunnies("root", empty_dirs_only=True)
        self.assertEqual(len(files), 0)
        self.assertIn(os.path.join("root", "subdir", "empty_dir"), dirs)
        self.assertEqual(len(dirs), 1)

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('src.sweeper.is_empty_dir', return_value=True) # Mock rationale: Ensure rmdir check passes
    def test_clean_dust_bunnies_dry_run(self, mock_is_empty_dir, mock_rmdir, mock_remove):
        # Mock rationale: os.remove and os.rmdir are file system operations.
        # We mock them to prevent actual file deletion during tests and verify calls.
        # is_empty_dir is mocked to control the condition for directory deletion.
        files = ["path/to/old_file.txt", "path/to/temp.log"]
        dirs = ["path/to/empty_dir"]

        with patch('builtins.print') as mock_print:
            clean_dust_bunnies(files, dirs, dry_run=True)
            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called()
            mock_print.assert_any_call("\n--- DRY RUN RESULTS ---")
            mock_print.assert_any_call("  File: path/to/old_file.txt")
            mock_print.assert_any_call("  Directory: path/to/empty_dir")

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('src.sweeper.is_empty_dir', return_value=True)
    def test_clean_dust_bunnies_cleanup(self, mock_is_empty_dir, mock_rmdir, mock_remove):
        # Mock rationale: Same as dry-run, but verify actual calls to remove/rmdir.
        files = ["path/to/old_file.txt", "path/to/temp.log"]
        dirs = ["path/to/empty_dir", "path/to/another_empty_dir"]

        with patch('builtins.print') as mock_print:
            clean_dust_bunnies(files, dirs, dry_run=False)
            self.assertEqual(mock_remove.call_count, len(files))
            mock_remove.assert_any_call("path/to/old_file.txt")
            mock_remove.assert_any_call("path/to/temp.log")

            self.assertEqual(mock_rmdir.call_count, len(dirs))
            mock_rmdir.assert_any_call("path/to/empty_dir")
            mock_rmdir.assert_any_call("path/to/another_empty_dir")

            mock_print.assert_any_call("\n--- CLEANUP RESULTS ---")
            mock_print.assert_any_call("    DELETED: path/to/old_file.txt")
            mock_print.assert_any_call("    DELETED: path/to/empty_dir")

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('src.sweeper.is_empty_dir')
    def test_clean_dust_bunnies_cleanup_non_empty_dir_skipped(self, mock_is_empty_dir, mock_rmdir, mock_remove):
        # Mock rationale: Test that non-empty directories are skipped during cleanup.
        files = []
        dirs = ["path/to/non_empty_dir"]
        mock_is_empty_dir.return_value = False # Simulate a non-empty directory

        with patch('builtins.print') as mock_print:
            clean_dust_bunnies(files, dirs, dry_run=False)
            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called() # Should not be called for non-empty dir
            mock_print.assert_any_call("  Skipping non-empty directory: path/to/non_empty_dir")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.clean_dust_bunnies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_dry_run(self, mock_print, mock_isdir, mock_clean_bunnies, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # find_dust_bunnies and clean_dust_bunnies are mocked to isolate main's logic.
        # os.path.isdir is mocked to simulate a valid path without actual file system checks.
        # builtins.print is mocked to capture output.

        mock_parse_args.return_value = MagicMock(
            path="test_path",
            age=10,
            patterns="*.log",
            empty_dirs_only=False,
            dry_run=True,
            clean=False
        )
        mock_find_bunnies.return_value = (["file1.log"], ["dir1"])

        main()

        mock_find_bunnies.assert_called_once_with(
            root_path="test_path",
            age_threshold_days=10,
            patterns=["*.log"],
            empty_dirs_only=False
        )
        mock_clean_bunnies.assert_called_once_with(["file1.log"], ["dir1"], dry_run=True)
        mock_print.assert_any_call("Scanning 'test_path' for digital dust bunnies...")
        mock_print.assert_any_call("\nDigital dust bunny sweeping complete!")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_dust_bunnies')
    @patch('src.sweeper.clean_dust_bunnies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_cleanup(self, mock_print, mock_isdir, mock_clean_bunnies, mock_find_bunnies, mock_parse_args):
        # Mock rationale: Same as dry-run, but for cleanup mode.
        mock_parse_args.return_value = MagicMock(
            path="test_path",
            age=None,
            patterns=None,
            empty_dirs_only=True,
            dry_run=False,
            clean=True
        )
        mock_find_bunnies.return_value = ([], ["dir2"])

        main()

        mock_find_bunnies.assert_called_once_with(
            root_path="test_path",
            age_threshold_days=None,
            patterns=None,
            empty_dirs_only=True
        )
        mock_clean_bunnies.assert_called_once_with([], ["dir2"], dry_run=False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Test error handling for invalid path.
        mock_parse_args.return_value = MagicMock(
            path="invalid_path",
            dry_run=True,
            clean=False
        )
        main()
        mock_print.assert_any_call("Error: Path 'invalid_path' is not a valid directory.")
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_mode_specified(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Test error handling when neither dry-run nor clean is specified.
        mock_parse_args.return_value = MagicMock(
            path="test_path",
            dry_run=False,
            clean=False
        )
        main()
        mock_print.assert_any_call("Error: You must specify either --dry-run or --clean.")
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_both_modes_specified(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Test error handling when both dry-run and clean are specified.
        mock_parse_args.return_value = MagicMock(
            path="test_path",
            dry_run=True,
            clean=True
        )
        main()
        mock_print.assert_any_call("Error: Cannot specify both --dry-run and --clean.")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
