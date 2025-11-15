import unittest
import os
import time
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Mock rationale: We need to simulate a file system without actually creating files
# or directories, and control file modification times for deterministic testing.
# os.walk, os.path.getmtime, os.path.isdir, os.path.isfile, os.remove, os.rmdir
# are patched to achieve this isolation.

# Add src directory to sys.path for importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, get_file_age_days, delete_items
sys.path.pop(0)

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: Control the modification time of a file for age calculation.
        current_time = time.time()
        mock_getmtime.return_value = current_time - (35 * 24 * 60 * 60) # 35 days ago
        self.assertAlmostEqual(get_file_age_days('/fake/path/file.log'), 35.0, places=5)

        mock_getmtime.return_value = current_time - (10 * 24 * 60 * 60) # 10 days ago
        self.assertAlmostEqual(get_file_age_days('/fake/path/file.log'), 10.0, places=5)

        mock_getmtime.side_effect = OSError # Simulate file not found
        self.assertEqual(get_file_age_days('/nonexistent/file.log'), -1)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a file system structure and control file modification times
        # without touching the actual disk. os.walk is the primary interface for scanning.

        current_time = time.time()
        # Simulate files: 2 old logs, 1 recent log, 2 temp files, 1 normal file
        # Simulate directories: 1 empty, 1 non-empty
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'empty_dir'], ['normal_file.txt']),
            ('/root/dir1', [], ['old_log.log', 'recent_log.log', 'temp_file.tmp', 'tmp_another.txt']),
            ('/root/empty_dir', [], [])
        ]

        # Set specific mtimes for files
        def mock_getmtime_side_effect(path):
            if 'old_log.log' in path:
                return current_time - (40 * 24 * 60 * 60) # 40 days old
            elif 'recent_log.log' in path:
                return current_time - (5 * 24 * 60 * 60) # 5 days old
            else:
                return current_time # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        empty_dirs, old_logs, temp_files = find_dust_bunnies('/root', old_days=30)

        self.assertEqual(len(empty_dirs), 1)
        self.assertIn('/root/empty_dir', empty_dirs)

        self.assertEqual(len(old_logs), 1)
        self.assertIn('/root/dir1/old_log.log', old_logs)

        self.assertEqual(len(temp_files), 2)
        self.assertIn('/root/dir1/temp_file.tmp', temp_files)
        self.assertIn('/root/dir1/tmp_another.txt', temp_files)

        # Test with a non-existent path
        mock_isdir.return_value = False
        empty_dirs, old_logs, temp_files = find_dust_bunnies('/nonexistent', old_days=30)
        self.assertEqual(empty_dirs, [])
        self.assertEqual(old_logs, [])
        self.assertEqual(temp_files, [])
        self.assertIn("Error: Path '/nonexistent' is not a valid directory.", self.mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['y', 'n', 'y'])
    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.isdir')
    def test_delete_items(self, mock_isdir, mock_os_remove, mock_os_rmdir, mock_input):
        # Mock rationale: Simulate user input for confirmation, and prevent actual file/directory
        # deletion by patching os.remove and os.rmdir. os.path.isdir is needed to distinguish
        # between files and directories for deletion.

        # Test deleting empty directories
        mock_isdir.return_value = True # For directories
        empty_dirs = ['/path/to/empty_dir1', '/path/to/empty_dir2']
        delete_items(empty_dirs, "empty directories")
        self.assertEqual(mock_os_rmdir.call_count, 2)
        mock_os_rmdir.assert_any_call('/path/to/empty_dir1')
        mock_os_rmdir.assert_any_call('/path/to/empty_dir2')
        self.assertIn("Deleted empty directory: /path/to/empty_dir1", self.mock_stdout.getvalue())

        # Test skipping deletion of old log files
        mock_os_remove.reset_mock()
        mock_os_rmdir.reset_mock()
        mock_isdir.return_value = False # For files
        old_logs = ['/path/to/old.log']
        delete_items(old_logs, "old log files")
        self.assertEqual(mock_os_remove.call_count, 0)
        self.assertIn("Skipping deletion of old log files.", self.mock_stdout.getvalue())

        # Test deleting temporary files with an error
        mock_os_remove.reset_mock()
        mock_os_rmdir.reset_mock()
        mock_isdir.return_value = False
        mock_os_remove.side_effect = [None, OSError("Permission denied")] # First success, second fail
        temp_files = ['/path/to/temp1.tmp', '/path/to/temp2.tmp']
        delete_items(temp_files, "temporary files")
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_os_remove.assert_any_call('/path/to/temp1.tmp')
        mock_os_remove.assert_any_call('/path/to/temp2.tmp')
        self.assertIn("Deleted file: /path/to/temp1.tmp", self.mock_stdout.getvalue())
        self.assertIn("Error deleting /path/to/temp2.tmp: Permission denied", self.mock_stdout.getvalue())

        # Test with empty list
        mock_os_remove.reset_mock()
        mock_os_rmdir.reset_mock()
        delete_items([], "nothing")
        self.assertEqual(mock_os_remove.call_count, 0)
        self.assertEqual(mock_os_rmdir.call_count, 0)

if __name__ == '__main__':
    unittest.main()
