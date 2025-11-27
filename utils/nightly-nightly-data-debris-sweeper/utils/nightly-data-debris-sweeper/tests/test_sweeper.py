import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from src.sweeper import sweep_debris, is_match

class TestDebrisSweeper(unittest.TestCase):

    def test_is_match(self):
        self.assertTrue(is_match("file.log", [".log"]))
        self.assertTrue(is_match("temp.tmp", [".tmp", ".bak"]))
        self.assertTrue(is_match("__pycache__", ["__pycache__"]))
        self.assertTrue(is_match("Thumbs.db", ["Thumbs.db"]))
        self.assertFalse(is_match("image.png", [".log", ".tmp"]))
        self.assertFalse(is_match("my_dir", ["__pycache__"]))
        self.assertTrue(is_match("my_file.log", [".log", "my_file.txt"]))
        self.assertTrue(is_match("my_file.txt", [".log", "my_file.txt"]))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print') # Mock print to capture output
    def test_sweep_debris_dry_run(self, mock_print, mock_rmtree, mock_remove, mock_os_walk, mock_isdir):
        # Mock rationale: Prevent actual file system operations and capture output.
        # os.path.isdir: Simulate that the root path exists.
        # os.walk: Simulate a directory structure with files and directories.
        # os.remove, shutil.rmtree: Ensure these are not called in dry-run mode.
        # builtins.print: Capture console output for verification.

        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', ['dir_to_clean', 'dir_to_keep'], ['file.log', 'file.txt']),
            ('/root/dir_to_clean', [], ['temp.tmp', 'important.md']),
            ('/root/dir_to_keep', [], ['another.log'])
        ]

        patterns = [".log", ".tmp", "dir_to_clean"]
        found = sweep_debris('/root', patterns, delete_mode=False)

        self.assertEqual(len(found), 4)
        self.assertIn('/root/dir_to_clean', found)
        self.assertIn('/root/file.log', found)
        self.assertIn('/root/dir_to_clean/temp.tmp', found)
        self.assertIn('/root/dir_to_keep/another.log', found)

        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_print.assert_any_call("Found directory: /root/dir_to_clean")
        mock_print.assert_any_call("Found file: /root/file.log")
        mock_print.assert_any_call("Found file: /root/dir_to_clean/temp.tmp")
        mock_print.assert_any_call("Found file: /root/dir_to_keep/another.log")
        mock_print.assert_any_call("Scan complete. 4 items identified.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    def test_sweep_debris_delete_mode(self, mock_print, mock_rmtree, mock_remove, mock_os_walk, mock_isdir):
        # Mock rationale: Prevent actual file system operations and capture output.
        # os.path.isdir: Simulate that the root path exists.
        # os.walk: Simulate a directory structure with files and directories.
        # os.remove, shutil.rmtree: Verify these are called correctly in delete mode.
        # builtins.print: Capture console output for verification.

        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', ['dir_to_clean', 'dir_to_keep'], ['file.log', 'file.txt']),
            ('/root/dir_to_clean', [], ['temp.tmp', 'important.md']),
            ('/root/dir_to_keep', [], ['another.log'])
        ]

        patterns = [".log", ".tmp", "dir_to_clean"]
        found = sweep_debris('/root', patterns, delete_mode=True)

        self.assertEqual(len(found), 4)
        self.assertIn('/root/dir_to_clean', found)
        self.assertIn('/root/file.log', found)
        self.assertIn('/root/dir_to_clean/temp.tmp', found)
        self.assertIn('/root/dir_to_keep/another.log', found)

        mock_rmtree.assert_called_once_with('/root/dir_to_clean')
        self.assertEqual(mock_remove.call_count, 3) # file.log, temp.tmp, another.log
        mock_remove.assert_any_call('/root/file.log')
        mock_remove.assert_any_call('/root/dir_to_clean/temp.tmp')
        mock_remove.assert_any_call('/root/dir_to_keep/another.log')

        mock_print.assert_any_call("Deleting directory: /root/dir_to_clean")
        mock_print.assert_any_call("Deleting file: /root/file.log")
        mock_print.assert_any_call("Deleting file: /root/dir_to_clean/temp.tmp")
        mock_print.assert_any_call("Deleting file: /root/dir_to_keep/another.log")
        mock_print.assert_any_call("Scan complete. 4 items deleted.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.print')
    def test_sweep_debris_invalid_path(self, mock_print, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate an invalid root path and ensure error handling.
        # os.path.isdir: Simulate that the root path does not exist.
        # os.walk: Ensure this is not called if the path is invalid.
        # builtins.print: Capture console output for verification.

        mock_isdir.return_value = False
        patterns = [".log"]
        found = sweep_debris('/nonexistent', patterns, delete_mode=False)

        self.assertEqual(len(found), 0)
        mock_os_walk.assert_not_called()
        mock_print.assert_any_call("Error: Root path '/nonexistent' is not a valid directory.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    def test_sweep_debris_error_handling(self, mock_print, mock_rmtree, mock_remove, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate errors during deletion and ensure they are caught and reported.
        # os.path.isdir: Simulate that the root path exists.
        # os.walk: Simulate a directory structure with items to delete.
        # os.remove, shutil.rmtree: Raise OSError to simulate deletion failures.
        # builtins.print: Capture console output for verification.

        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', ['bad_dir'], ['bad_file.log'])
        ]
        mock_rmtree.side_effect = OSError("Permission denied dir")
        mock_remove.side_effect = OSError("Permission denied file")

        patterns = [".log", "bad_dir"]
        found = sweep_debris('/root', patterns, delete_mode=True)

        self.assertEqual(len(found), 2)
        mock_print.assert_any_call("Error deleting directory /root/bad_dir: Permission denied dir")
        mock_print.assert_any_call("Error deleting file /root/bad_file.log: Permission denied file")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.print')
    def test_sweep_debris_no_patterns(self, mock_print, mock_os_walk, mock_isdir):
        # Mock rationale: Test the scenario where no patterns are provided.
        # os.path.isdir: Simulate that the root path exists.
        # os.walk: Ensure this is still called to scan, but no matches are found.
        # builtins.print: Capture console output for verification.

        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['file.txt'])
        ]

        found = sweep_debris('/root', [], delete_mode=False)

        self.assertEqual(len(found), 0)
        mock_os_walk.assert_called_once_with('/root', topdown=True)
        mock_print.assert_any_call("Scan complete. 0 items identified.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    def test_sweep_debris_dir_removal_prevents_file_scan_inside(self, mock_print, mock_rmtree, mock_remove, mock_os_walk, mock_isdir):
        # Mock rationale: Ensure that if a directory is marked for removal, its contents are not scanned or removed individually.
        # os.path.isdir: Simulate that the root path exists.
        # os.walk: Simulate a structure where a directory contains files that would also match patterns.
        # os.remove, shutil.rmtree: Verify calls.
        # builtins.print: Capture console output.

        mock_isdir.return_value = True
        # Simulate a structure where 'target_dir' contains 'nested.log'
        # and 'target_dir' itself is a pattern.
        mock_os_walk.return_value = [
            ('/root', ['target_dir', 'other_dir'], ['root_file.log']),
            ('/root/target_dir', [], ['nested.log', 'nested.txt'])
        ]

        patterns = ["target_dir", ".log"]
        found = sweep_debris('/root', patterns, delete_mode=True)

        self.assertEqual(len(found), 2) # target_dir and root_file.log
        self.assertIn('/root/target_dir', found)
        self.assertIn('/root/root_file.log', found)
        self.assertNotIn('/root/target_dir/nested.log', found) # Should not be found individually

        mock_rmtree.assert_called_once_with('/root/target_dir')
        mock_remove.assert_called_once_with('/root/root_file.log')
        
        mock_print.assert_any_call("Deleting directory: /root/target_dir")
        mock_print.assert_any_call("Deleting file: /root/root_file.log")
        mock_print.assert_any_call("Scan complete. 2 items deleted.")
