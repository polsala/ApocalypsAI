import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import sys

# Mock rationale: We need to simulate file system operations without actually touching the disk.
# os.walk, os.path.isdir, os.path.getmtime, os.remove, and shutil.rmtree are critical for this.
# By mocking them, we ensure tests are deterministic, fast, and don't leave artifacts.

# Import the functions to be tested
# Assuming sweeper.py is in src/ and tests are in tests/
# Adjust import path if necessary, or run tests from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sweeper import find_empty_dirs, find_old_temp_files, delete_items, main
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = MagicMock()
        # Capture stderr for testing error messages
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = MagicMock()

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.walk')
    def test_find_empty_dirs_no_empty(self, mock_walk):
        # Mock rationale: Simulate a directory structure with no empty directories.
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], ['file3.txt'])
        ]
        result = find_empty_dirs('/root')
        self.assertEqual(result, [])

    @patch('os.walk')
    def test_find_empty_dirs_with_empty(self, mock_walk):
        # Mock rationale: Simulate a directory structure containing empty directories.
        mock_walk.return_value = [
            ('/root', ['dir1', 'empty_dir1'], ['file1.txt']),
            ('/root/dir1', ['empty_subdir'], ['file2.txt']),
            ('/root/dir1/empty_subdir', [], []),
            ('/root/empty_dir1', [], []),
            ('/root/non_empty', [], ['file3.txt'])
        ]
        result = find_empty_dirs('/root')
        # os.walk yields directories from top-down, so empty_subdir might be found before empty_dir1
        # The order depends on the mock_walk return value, so we sort for consistent comparison.
        self.assertCountEqual(result, ['/root/dir1/empty_subdir', '/root/empty_dir1'])

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_temp_files(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate files with different modification times and extensions.
        # We need to control what os.path.getmtime returns for specific file paths.
        # We also need to control the directory structure via os.walk.

        # Define a cutoff time (e.g., 30 days ago)
        now = datetime.datetime.now()
        old_time = (now - datetime.timedelta(days=40)).timestamp()
        new_time = (now - datetime.timedelta(days=10)).timestamp()

        mock_walk.return_value = [
            ('/root', [], ['old.tmp', 'new.log', 'old.bak', 'not_temp.txt'])
        ]

        # Map file paths to their mock modification times
        def mock_getmtime_side_effect(path):
            if path == '/root/old.tmp': return old_time
            if path == '/root/new.log': return new_time
            if path == '/root/old.bak': return old_time
            if path == '/root/not_temp.txt': return old_time # Should be ignored by extension
            raise FileNotFoundError

        mock_getmtime.side_effect = mock_getmtime_side_effect

        result = find_old_temp_files('/root', 30, ['.tmp', '.log', '.bak'])
        self.assertCountEqual(result, ['/root/old.tmp', '/root/old.bak'])

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_temp_files_no_old(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate files that are all newer than the cutoff.
        now = datetime.datetime.now()
        new_time = (now - datetime.timedelta(days=10)).timestamp()

        mock_walk.return_value = [
            ('/root', [], ['new1.tmp', 'new2.log'])
        ]
        mock_getmtime.return_value = new_time

        result = find_old_temp_files('/root', 30, ['.tmp', '.log'])
        self.assertEqual(result, [])

    @patch('os.path.isdir')
    @patch('os.remove')
    @patch('shutil.rmtree')
    def test_delete_items_dry_run(self, mock_rmtree, mock_remove, mock_isdir):
        # Mock rationale: Test the dry-run behavior without actual deletion.
        # os.path.isdir is needed to distinguish between files and directories for printing.
        mock_isdir.side_effect = lambda x: x == '/root/empty_dir'
        items_to_delete = ['/root/old.tmp', '/root/empty_dir']
        delete_items(items_to_delete, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        self.assertIn("Would delete: /root/old.tmp", self.mock_stdout.getvalue())
        self.assertIn("Would delete: /root/empty_dir", self.mock_stdout.getvalue())
        self.assertIn("[DRY RUN] Attempting to identify 2 items...", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.remove')
    @patch('shutil.rmtree')
    def test_delete_items_actual_deletion(self, mock_rmtree, mock_remove, mock_isdir):
        # Mock rationale: Test actual deletion calls for files and directories.
        # os.path.isdir is needed to ensure the correct deletion function (os.remove vs shutil.rmtree) is called.
        mock_isdir.side_effect = lambda x: x == '/root/empty_dir'
        items_to_delete = ['/root/old.tmp', '/root/empty_dir']
        delete_items(items_to_delete, dry_run=False)

        mock_remove.assert_called_once_with('/root/old.tmp')
        mock_rmtree.assert_called_once_with('/root/empty_dir')
        self.assertIn("Deleted file: /root/old.tmp", self.mock_stdout.getvalue())
        self.assertIn("Deleted directory: /root/empty_dir", self.mock_stdout.getvalue())
        self.assertIn("Attempting to delete 2 items...", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('sweeper.find_old_temp_files', return_value=['/path/to/old.tmp'])
    @patch('sweeper.delete_items')
    def test_main_flow(self, mock_delete_items, mock_find_old_temp_files, mock_find_empty_dirs, mock_parse_args, mock_exit, mock_isdir):
        # Mock rationale: Test the main function's orchestration of other functions and argument parsing.
        # We mock argparse to control CLI inputs, os.path.isdir for path validation, and the core logic functions
        # (find_empty_dirs, find_old_temp_files, delete_items) to ensure they are called correctly.
        # sys.exit is mocked to prevent the test runner from exiting.

        mock_parse_args.return_value = MagicMock(
            path='/test/path',
            age=60,
            extensions=['.test'],
            dry_run=True
        )

        main()

        mock_isdir.assert_called_once_with('/test/path')
        mock_find_empty_dirs.assert_called_once_with('/test/path')
        mock_find_old_temp_files.assert_called_once_with('/test/path', 60, ['.test'])
        self.assertEqual(mock_delete_items.call_count, 2)
        mock_delete_items.assert_any_call(['/path/to/empty_dir'], True)
        mock_delete_items.assert_any_call(['/path/to/old.tmp'], True)
        self.assertIn("Scanning '/test/path' for digital dust bunnies...", self.mock_stdout.getvalue())
        self.assertIn("Found 1 empty directories:", self.mock_stdout.getvalue())
        self.assertIn("Found 1 old temporary files (older than 60 days, extensions: .test):", self.mock_stdout.getvalue())
        self.assertIn("Digital Dust Bunny Sweeper finished.", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_exit, mock_isdir):
        # Mock rationale: Test error handling for an invalid path.
        mock_parse_args.return_value = MagicMock(
            path='/non/existent/path',
            age=30,
            extensions=['.tmp'],
            dry_run=False
        )

        main()

        mock_isdir.assert_called_once_with('/non/existent/path')
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Path '/non/existent/path' is not a valid directory.", self.mock_stderr.getvalue())

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_temp_files_os_error(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate an OSError when accessing file modification time.
        mock_walk.return_value = [
            ('/root', [], ['unreadable.tmp'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied")

        result = find_old_temp_files('/root', 30, ['.tmp'])
        self.assertEqual(result, []) # No files should be added if error occurs
        self.assertIn("Warning: Could not access file /root/unreadable.tmp: Permission denied", self.mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=False)
    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('shutil.rmtree')
    def test_delete_items_os_error_file(self, mock_rmtree, mock_remove, mock_isdir):
        # Mock rationale: Simulate an OSError during file deletion.
        items_to_delete = ['/root/unremovable.tmp']
        delete_items(items_to_delete, dry_run=False)

        mock_remove.assert_called_once_with('/root/unremovable.tmp')
        mock_rmtree.assert_not_called()
        self.assertIn("Error deleting /root/unremovable.tmp: Permission denied", self.mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.remove')
    @patch('shutil.rmtree', side_effect=OSError("Directory not empty"))
    def test_delete_items_os_error_dir(self, mock_rmtree, mock_remove, mock_isdir):
        # Mock rationale: Simulate an OSError during directory deletion.
        items_to_delete = ['/root/unremovable_dir']
        delete_items(items_to_delete, dry_run=False)

        mock_rmtree.assert_called_once_with('/root/unremovable_dir')
        mock_remove.assert_not_called()
        self.assertIn("Error deleting /root/unremovable_dir: Directory not empty", self.mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
