import unittest
import os
import time
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import tempfile

# Import the functions to be tested
from src.sweeper import (
    get_file_age_in_days,
    find_old_files,
    find_empty_dirs,
    delete_files,
    delete_empty_directories,
    main
)

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing filesystem operations
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir) # Change CWD to simplify paths in tests

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def create_test_file(self, path, age_days=0):
        """Helper to create a file with a specific modification time."""
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write("test content")
        
        # Set modification time
        if age_days > 0:
            old_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()
            os.utime(full_path, (old_timestamp, old_timestamp))
        return full_path

    def create_test_dir(self, path):
        """Helper to create a directory."""
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the modification time of a file.
        # We need to control this value to test age calculation deterministically
        # without relying on actual file system changes or current time.
        
        # Simulate a file modified 10 days ago
        mock_getmtime.return_value = (datetime.now() - timedelta(days=10)).timestamp()
        
        # Mock rationale: time.time() returns the current time. We need to fix this
        # to ensure the age calculation is consistent regardless of when the test runs.
        with patch('time.time', return_value=datetime.now().timestamp()):
            age = get_file_age_in_days("dummy_file.txt")
            self.assertAlmostEqual(age, 10.0, places=2)

        # Test error case
        mock_getmtime.side_effect = OSError
        age = get_file_age_in_days("non_existent_file.txt")
        self.assertEqual(age, -1)

    def test_find_old_files(self):
        # Create files with different ages
        self.create_test_file("old_file_1.txt", age_days=35)
        self.create_test_file("subdir/old_file_2.txt", age_days=40)
        self.create_test_file("new_file.txt", age_days=5)
        self.create_test_file("subdir/new_file_2.txt", age_days=10)
        self.create_test_file("another_subdir/old_file_3.log", age_days=60)

        # Find files older than 30 days
        old_files = find_old_files(self.test_dir, 30)
        self.assertEqual(len(old_files), 3)
        self.assertIn(os.path.join(self.test_dir, "old_file_1.txt"), old_files)
        self.assertIn(os.path.join(self.test_dir, "subdir", "old_file_2.txt"), old_files)
        self.assertIn(os.path.join(self.test_dir, "another_subdir", "old_file_3.log"), old_files)

        # Find files older than 50 days
        old_files_50 = find_old_files(self.test_dir, 50)
        self.assertEqual(len(old_files_50), 1)
        self.assertIn(os.path.join(self.test_dir, "another_subdir", "old_file_3.log"), old_files_50)

        # No files older than 100 days
        old_files_100 = find_old_files(self.test_dir, 100)
        self.assertEqual(len(old_files_100), 0)

    def test_find_empty_dirs(self):
        # Create directories
        self.create_test_dir("empty_dir_1")
        self.create_test_dir("parent/empty_dir_2")
        self.create_test_dir("parent/non_empty_dir")
        self.create_test_file("parent/non_empty_dir/file.txt")
        self.create_test_dir("nested/empty_1/empty_2")
        self.create_test_dir("nested/non_empty_parent/empty_child")
        self.create_test_file("nested/non_empty_parent/file.txt")

        empty_dirs = find_empty_dirs(self.test_dir)
        # The order might vary, so check for presence and count
        self.assertEqual(len(empty_dirs), 3)
        self.assertIn(os.path.join(self.test_dir, "empty_dir_1"), empty_dirs)
        self.assertIn(os.path.join(self.test_dir, "parent", "empty_dir_2"), empty_dirs)
        self.assertIn(os.path.join(self.test_dir, "nested", "empty_1", "empty_2"), empty_dirs)
        # Note: 'nested/empty_1' is not empty because it contains 'empty_2' until 'empty_2' is removed.
        # The `find_empty_dirs` function with `topdown=False` correctly identifies the deepest empty ones first.

    @patch('builtins.print')
    @patch('os.remove')
    def test_delete_files_dry_run(self, mock_remove, mock_print):
        # Mock rationale: os.remove performs actual file deletion.
        # We need to mock it to prevent actual filesystem changes during tests
        # and to verify that it *would* have been called.
        # Mock rationale: builtins.print captures console output for verification.
        
        file1 = self.create_test_file("file_to_delete_1.txt")
        file2 = self.create_test_file("file_to_delete_2.txt")
        
        deleted_count = delete_files([file1, file2], dry_run=True)
        self.assertEqual(deleted_count, 0) # No actual deletions in dry run
        mock_remove.assert_not_called()
        mock_print.assert_any_call(f"[DRY RUN] Would delete: {file1}")
        mock_print.assert_any_call(f"[DRY RUN] Would delete: {file2}")

    @patch('builtins.print')
    @patch('os.remove')
    def test_delete_files_actual_run(self, mock_remove, mock_print):
        # Mock rationale: os.remove for preventing actual deletion and verifying calls.
        # Mock rationale: builtins.print for capturing output.

        file1 = self.create_test_file("file_to_delete_1.txt")
        file2 = self.create_test_file("file_to_delete_2.txt")
        
        deleted_count = delete_files([file1, file2], dry_run=False)
        self.assertEqual(deleted_count, 2)
        mock_remove.assert_any_call(file1)
        mock_remove.assert_any_call(file2)
        mock_print.assert_any_call(f"Deleted: {file1}")
        mock_print.assert_any_call(f"Deleted: {file2}")

    @patch('builtins.print')
    @patch('os.rmdir')
    @patch('os.listdir', return_value=[]) # Mock rationale: os.listdir checks if a dir is empty.
                                        # We need to control this to simulate empty directories.
    def test_delete_empty_directories_dry_run(self, mock_listdir, mock_rmdir, mock_print):
        # Mock rationale: os.rmdir for preventing actual deletion and verifying calls.
        # Mock rationale: os.listdir for simulating empty directories.
        # Mock rationale: builtins.print for capturing output.

        dir1 = self.create_test_dir("empty_dir_a")
        dir2 = self.create_test_dir("parent_b/empty_dir_c")
        
        deleted_count = delete_empty_directories([dir1, dir2], dry_run=True)
        self.assertEqual(deleted_count, 0)
        mock_rmdir.assert_not_called()
        mock_print.assert_any_call(f"[DRY RUN] Would delete empty directory: {dir1}")
        mock_print.assert_any_call(f"[DRY RUN] Would delete empty directory: {dir2}")

    @patch('builtins.print')
    @patch('os.rmdir')
    @patch('os.listdir', return_value=[])
    def test_delete_empty_directories_actual_run(self, mock_listdir, mock_rmdir, mock_print):
        # Mock rationale: os.rmdir for preventing actual deletion and verifying calls.
        # Mock rationale: os.listdir for simulating empty directories.
        # Mock rationale: builtins.print for capturing output.

        dir1 = self.create_test_dir("empty_dir_a")
        dir2 = self.create_test_dir("parent_b/empty_dir_c")
        
        deleted_count = delete_empty_directories([dir1, dir2], dry_run=False)
        self.assertEqual(deleted_count, 2)
        mock_rmdir.assert_any_call(dir1)
        mock_rmdir.assert_any_call(dir2)
        mock_print.assert_any_call(f"Deleted empty directory: {dir1}")
        mock_print.assert_any_call(f"Deleted empty directory: {dir2}")

    @patch('builtins.print')
    @patch('os.listdir', return_value=['file.txt']) # Simulate non-empty dir
    @patch('os.rmdir')
    def test_delete_empty_directories_skips_non_empty(self, mock_rmdir, mock_listdir, mock_print):
        # Mock rationale: os.rmdir for preventing actual deletion and verifying calls.
        # Mock rationale: os.listdir for simulating non-empty directories.
        # Mock rationale: builtins.print for capturing output.

        dir_path = self.create_test_dir("non_empty_dir")
        
        deleted_count = delete_empty_directories([dir_path], dry_run=False)
        self.assertEqual(deleted_count, 0)
        mock_rmdir.assert_not_called()
        mock_print.assert_any_call(f"Skipped non-empty directory: {dir_path}")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_old_files', return_value=['/path/to/old_file.txt'])
    @patch('src.sweeper.delete_files', return_value=1)
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    def test_main_delete_old_files(self, mock_isdir, mock_print, mock_delete_files, mock_find_old_files, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args to control CLI arguments.
        # Mock rationale: find_old_files to control the list of files found without actual scanning.
        # Mock rationale: delete_files to control the deletion process without actual file ops.
        # Mock rationale: builtins.print for capturing output.
        # Mock rationale: os.path.isdir to simulate a valid path without creating it.

        mock_parse_args.return_value = MagicMock(
            path="/test/path", age=30, mode="delete", confirm=True
        )
        
        main()
        mock_find_old_files.assert_called_once_with("/test/path", 30)
        mock_delete_files.assert_called_once_with(['/path/to/old_file.txt'], dry_run=False)
        mock_print.assert_any_call("\nOperation complete. 1 files were deleted.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('src.sweeper.delete_empty_directories', return_value=1)
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    def test_main_delete_empty_dirs(self, mock_isdir, mock_print, mock_delete_empty_directories, mock_find_empty_dirs, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args to control CLI arguments.
        # Mock rationale: find_empty_dirs to control the list of directories found.
        # Mock rationale: delete_empty_directories to control the deletion process.
        # Mock rationale: builtins.print for capturing output.
        # Mock rationale: os.path.isdir to simulate a valid path.

        mock_parse_args.return_value = MagicMock(
            path="/test/path", mode="delete-empty-dirs", confirm=True
        )
        
        main()
        mock_find_empty_dirs.assert_called_once_with("/test/path")
        mock_delete_empty_directories.assert_called_once_with(['/path/to/empty_dir'], dry_run=False)
        mock_print.assert_any_call("\nOperation complete. 1 empty directories were deleted.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=False)
    def test_main_invalid_path_exit(self, mock_isdir, mock_exit, mock_print, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args to control CLI arguments.
        # Mock rationale: builtins.print for capturing output.
        # Mock rationale: sys.exit to prevent actual program termination during test.
        # Mock rationale: os.path.isdir to simulate an invalid path.

        mock_parse_args.return_value = MagicMock(
            path="/non/existent/path", mode="list", confirm=False
        )
        
        main()
        mock_print.assert_any_call("Error: Path '/non/existent/path' is not a valid directory.")
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    def test_main_delete_no_confirm_exit(self, mock_isdir, mock_exit, mock_print, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args to control CLI arguments.
        # Mock rationale: builtins.print for capturing output.
        # Mock rationale: sys.exit to prevent actual program termination during test.
        # Mock rationale: os.path.isdir to simulate a valid path.

        mock_parse_args.return_value = MagicMock(
            path="/test/path", age=30, mode="delete", confirm=False
        )
        
        main()
        mock_print.assert_any_call("Error: '--confirm' is required for 'delete' mode.")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
