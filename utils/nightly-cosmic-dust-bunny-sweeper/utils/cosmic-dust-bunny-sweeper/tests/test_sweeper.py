import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Mock rationale: We need to simulate file system operations (os.walk, os.path.getmtime, os.remove, os.rmdir)
# and user input (input) without actually touching the real file system or requiring user interaction.
# This ensures tests are deterministic, fast, and safe.

# Add the src directory to sys.path for importing the sweeper module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper
sys.path.pop(0)

class TestCosmicDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing print statements
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.mock_stdout = StringIO()
        self.mock_stderr = StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout/stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.walk')
    def test_find_empty_directories(self, mock_walk):
        # Mock rationale: Simulate different directory structures without creating actual files.
        # os.walk yields (dirpath, dirnames, filenames)
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir', 'dir_with_empty_subdir'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], ['file3.txt']),
            ('/root/empty_dir', [], []),
            ('/root/dir_with_empty_subdir', ['nested_empty'], ['file_in_parent.txt']),
            ('/root/dir_with_empty_subdir/nested_empty', [], [])
        ]

        empty_dirs = sweeper.find_empty_directories('/root')
        expected_empty_dirs = [
            '/root/empty_dir',
            '/root/dir_with_empty_subdir/nested_empty'
        ]
        self.assertCountEqual(empty_dirs, expected_empty_dirs)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_files(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate files with different modification times without creating actual files.
        # os.walk yields (dirpath, dirnames, filenames)
        mock_walk.return_value = [
            ('/root', [], ['old_file.txt', 'new_file.txt', 'ancient_file.log'])
        ]

        now = datetime.datetime.now()
        # Mock rationale: Provide specific modification times for mocked files.
        mock_getmtime.side_effect = {
            '/root/old_file.txt': (now - datetime.timedelta(days=31)).timestamp(), # Older than 30 days
            '/root/new_file.txt': (now - datetime.timedelta(days=10)).timestamp(), # Newer than 30 days
            '/root/ancient_file.log': (now - datetime.timedelta(days=100)).timestamp() # Older than 30 days
        }.get

        old_files = sweeper.find_old_files('/root', 30)
        expected_old_files = [
            '/root/old_file.txt',
            '/root/ancient_file.log'
        ]
        self.assertCountEqual(old_files, expected_old_files)

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/root/old_file.txt'])
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('os.listdir', return_value=[]) # Mock rationale: Ensure os.listdir returns empty for rmdir check
    def test_main_deletion_confirmed(self, mock_listdir, mock_sys_exit, mock_rmdir, mock_remove, mock_input, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        # Simulate command line arguments
        with patch('sys.argv', ['sweeper.py', '/root']):
            sweeper.main()

            mock_find_empty_directories.assert_called_once_with('/root')
            mock_find_old_files.assert_called_once_with('/root', 30)
            mock_input.assert_called_once() # Should ask for confirmation
            mock_remove.assert_called_once_with('/root/old_file.txt')
            mock_rmdir.assert_called_once_with('/root/empty_dir')
            mock_sys_exit.assert_called_once_with(0)
            self.assertIn("Cosmic cleansing complete! 2 items purged.", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/root/old_file.txt'])
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user denying deletion.
    @patch('os.remove') # Mock rationale: Prevent actual file deletion.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_deletion_denied(self, mock_sys_exit, mock_rmdir, mock_remove, mock_input, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        with patch('sys.argv', ['sweeper.py', '/root']):
            sweeper.main()

            mock_find_empty_directories.assert_called_once_with('/root')
            mock_find_old_files.assert_called_once_with('/root', 30)
            mock_input.assert_called_once() # Should ask for confirmation
            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called()
            mock_sys_exit.assert_called_once_with(0)
            self.assertIn("Deletion cancelled.", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/root/old_file.txt'])
    @patch('os.remove') # Mock rationale: Prevent actual file deletion.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_dry_run(self, mock_sys_exit, mock_rmdir, mock_remove, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        with patch('sys.argv', ['sweeper.py', '/root', '--dry-run']):
            sweeper.main()

            mock_find_empty_directories.assert_called_once_with('/root')
            mock_find_old_files.assert_called_once_with('/root', 30)
            mock_remove.assert_not_called()
            mock_rmdir.assert_not_called()
            mock_sys_exit.assert_called_once_with(0)
            self.assertIn("Dry run complete. 2 items would be cleaned.", self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_invalid_path(self, mock_sys_exit, mock_isdir):
        with patch('sys.argv', ['sweeper.py', '/nonexistent/path']):
            sweeper.main()
            mock_isdir.assert_called_once_with('/nonexistent/path')
            mock_sys_exit.assert_called_once_with(1)
            self.assertIn("Error: Path '/nonexistent/path' is not a valid directory.", self.mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_empty_directories', return_value=[])
    @patch('sweeper.find_old_files', return_value=[])
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_no_items_to_clean(self, mock_sys_exit, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        with patch('sys.argv', ['sweeper.py', '/root']):
            sweeper.main()
            mock_find_empty_directories.assert_called_once_with('/root')
            mock_find_old_files.assert_called_once_with('/root', 30)
            mock_sys_exit.assert_called_once_with(0)
            self.assertIn("No cosmic dust bunnies or empty voids found. Your system is pristine!", self.mock_stdout.getvalue())

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_files_os_error(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate an OSError when trying to access file mtime.
        mock_walk.return_value = [
            ('/root', [], ['inaccessible_file.txt'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied")

        old_files = sweeper.find_old_files('/root', 30)
        self.assertEqual(old_files, []) # No files should be added if error occurs
        self.assertIn("Warning: Could not access file /root/inaccessible_file.txt: Permission denied", self.mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/root/old_file.txt'])
    @patch('builtins.input', return_value='y')
    @patch('os.remove', side_effect=OSError("File in use")) # Mock rationale: Simulate failure to delete a file.
    @patch('os.rmdir', side_effect=OSError("Dir not empty")) # Mock rationale: Simulate failure to delete a directory.
    @patch('sys.exit')
    @patch('os.listdir', return_value=[]) # Mock rationale: Ensure os.listdir returns empty for rmdir check
    def test_main_deletion_errors(self, mock_listdir, mock_sys_exit, mock_rmdir, mock_remove, mock_input, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        with patch('sys.argv', ['sweeper.py', '/root']):
            sweeper.main()
            mock_remove.assert_called_once_with('/root/old_file.txt')
            mock_rmdir.assert_called_once_with('/root/empty_dir')
            self.assertIn("Could not delete file /root/old_file.txt: File in use", self.mock_stderr.getvalue())
            self.assertIn("Could not delete directory /root/empty_dir: Dir not empty", self.mock_stderr.getvalue())
            mock_sys_exit.assert_called_once_with(0) # Still exits 0 if some items are deleted/attempted
