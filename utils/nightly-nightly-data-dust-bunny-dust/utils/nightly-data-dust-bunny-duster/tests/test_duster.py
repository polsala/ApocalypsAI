import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path to allow importing duster
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import find_empty_directories, find_zero_byte_files, duster_main

class TestDuster(unittest.TestCase):

    @patch('os.walk')
    def test_find_empty_directories(self, mock_os_walk):
        # Mock rationale: os.walk is a file system traversal function.
        # We need to control its output to simulate different directory structures
        # without actually creating files/directories on disk.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir'], ['file1.txt']),
            ('/root/dir1', [], ['subfile1.txt']),
            ('/root/dir2', ['subdir_not_empty'], []),
            ('/root/dir2/subdir_not_empty', [], ['another_file.txt']),
            ('/root/empty_dir', [], []), # This is an empty directory
            ('/root/another_empty', [], []), # Another empty directory
        ]
        
        empty_dirs = find_empty_directories('/root')
        self.assertIn('/root/empty_dir', empty_dirs)
        self.assertIn('/root/another_empty', empty_dirs)
        self.assertEqual(len(empty_dirs), 2)
        self.assertNotIn('/root/dir1', empty_dirs)
        self.assertNotIn('/root/dir2', empty_dirs)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    def test_find_zero_byte_files(self, mock_os_getsize, mock_os_isfile, mock_os_walk):
        # Mock rationale: os.walk, os.path.isfile, and os.path.getsize are file system functions.
        # We need to simulate file existence and size without actual disk I/O.
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt', 'empty.log']),
            ('/root/dir1', [], ['subfile.txt', 'another_empty.dat']),
        ]
        
        # Configure getsize for specific files
        def getsize_side_effect(path):
            if path == '/root/file1.txt':
                return 100
            elif path == '/root/empty.log':
                return 0
            elif path == '/root/dir1/subfile.txt':
                return 50
            elif path == '/root/dir1/another_empty.dat':
                return 0
            return 1 # Default for other files if any
        
        mock_os_getsize.side_effect = getsize_side_effect

        zero_files = find_zero_byte_files('/root')
        self.assertIn('/root/empty.log', zero_files)
        self.assertIn('/root/dir1/another_empty.dat', zero_files)
        self.assertEqual(len(zero_files), 2)
        self.assertNotIn('/root/file1.txt', zero_files)
        self.assertNotIn('/root/dir1/subfile.txt', zero_files)

    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('duster.find_zero_byte_files', return_value=['/root/empty.log'])
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print') # Mock print to capture output
    def test_duster_main_report_mode(self, mock_print, mock_os_rmdir, mock_os_remove, 
                                     mock_find_zero_byte_files, mock_find_empty_directories, mock_os_isdir):
        # Mock rationale: We want to test the main logic of duster_main,
        # including its reporting and conditional deletion.
        # We mock its dependencies (find_empty_directories, find_zero_byte_files, os.remove, os.rmdir)
        # to control their behavior and ensure no actual file system changes.
        # We also mock print to verify the output messages.
        
        deleted_files, deleted_dirs = duster_main('/root', delete_mode=False)

        self.assertEqual(deleted_files, [])
        self.assertEqual(deleted_dirs, [])
        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()
        
        mock_print.assert_any_call("\n--- Zero-byte files found ---")
        mock_print.assert_any_call("- File: /root/empty.log")
        mock_print.assert_any_call("  (Run with --delete to remove these files)")
        mock_print.assert_any_call("\n--- Empty directories found ---")
        mock_print.assert_any_call("- Directory: /root/empty_dir")
        mock_print.assert_any_call("  (Run with --delete to remove these directories)")
        mock_print.assert_any_call("\nReport complete. No changes made. Use --delete to perform cleanup.")

    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_directories', return_value=['/root/empty_dir', '/root/another_empty'])
    @patch('duster.find_zero_byte_files', return_value=['/root/empty.log', '/root/sub/empty.txt'])
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_duster_main_delete_mode(self, mock_print, mock_os_rmdir, mock_os_remove, 
                                    mock_find_zero_byte_files, mock_find_empty_directories, mock_os_isdir):
        # Mock rationale: Same as above, but testing the deletion path.
        # We ensure os.remove and os.rmdir are called with the correct arguments.
        
        deleted_files, deleted_dirs = duster_main('/root', delete_mode=True)

        self.assertIn('/root/empty.log', deleted_files)
        self.assertIn('/root/sub/empty.txt', deleted_files)
        self.assertEqual(len(deleted_files), 2)
        
        self.assertIn('/root/empty_dir', deleted_dirs)
        self.assertIn('/root/another_empty', deleted_dirs)
        self.assertEqual(len(deleted_dirs), 2)

        mock_os_remove.assert_any_call('/root/empty.log')
        mock_os_remove.assert_any_call('/root/sub/empty.txt')
        self.assertEqual(mock_os_remove.call_count, 2)

        # rmdir should be called for both empty dirs
        mock_os_rmdir.assert_any_call('/root/empty_dir')
        mock_os_rmdir.assert_any_call('/root/another_empty')
        self.assertEqual(mock_os_rmdir.call_count, 2)
        
        mock_print.assert_any_call("[DELETED] /root/empty.log")
        mock_print.assert_any_call("[DELETED] /root/empty_dir")
        mock_print.assert_any_call("\nCleanup complete. Removed 2 files and 2 directories.")

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_duster_main_invalid_path(self, mock_print, mock_os_isdir):
        # Mock rationale: Test error handling for invalid input path without actual file system checks.
        deleted_files, deleted_dirs = duster_main('/nonexistent', delete_mode=False)
        self.assertEqual(deleted_files, [])
        self.assertEqual(deleted_dirs, [])
        mock_print.assert_any_call("Error: Path '/nonexistent' is not a valid directory.", file=sys.stderr)

    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_directories', return_value=[])
    @patch('duster.find_zero_byte_files', return_value=[])
    @patch('builtins.print')
    def test_duster_main_no_dust_bunnies(self, mock_print, mock_find_zero_byte_files, mock_find_empty_directories, mock_os_isdir):
        # Mock rationale: Test the scenario where no dust bunnies are found.
        duster_main('/root', delete_mode=False)
        mock_print.assert_any_call("\nNo zero-byte files found. Your digital pantry is clean!")
        mock_print.assert_any_call("\nNo empty directories found. Your digital shelves are full of purpose!")
        mock_print.assert_any_call("\nAll clear! No digital dust bunnies detected in this sector.")

    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_directories', return_value=['/root/empty_dir'])
    @patch('duster.find_zero_byte_files', return_value=['/root/empty.log'])
    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('os.rmdir', side_effect=OSError("Directory not empty"))
    @patch('builtins.print')
    def test_duster_main_deletion_errors(self, mock_print, mock_os_rmdir, mock_os_remove, 
                                        mock_find_zero_byte_files, mock_find_empty_directories, mock_os_isdir):
        # Mock rationale: Simulate OS errors during deletion to ensure error handling is robust.
        deleted_files, deleted_dirs = duster_main('/root', delete_mode=True)
        
        self.assertEqual(deleted_files, []) # Nothing was successfully deleted
        self.assertEqual(deleted_dirs, []) # Nothing was successfully deleted

        mock_print.assert_any_call("  [ERROR] Could not delete /root/empty.log: Permission denied", file=sys.stderr)
        mock_print.assert_any_call("  [ERROR] Could not delete /root/empty_dir: Directory not empty", file=sys.stderr)
        mock_os_remove.assert_called_once_with('/root/empty.log')
        mock_os_rmdir.assert_called_once_with('/root/empty_dir')


if __name__ == '__main__':
    unittest.main()
