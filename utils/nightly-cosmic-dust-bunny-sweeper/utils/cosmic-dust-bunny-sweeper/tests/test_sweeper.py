import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestCosmicDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: datetime.now() is used to determine the current time for age calculations.
        # By mocking it to a fixed point, we ensure deterministic results for file age.
        self.mock_now = datetime(2023, 10, 26, 12, 0, 0) # Fixed date for testing
        self.patcher_datetime_now = patch('sweeper.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp
        self.mock_datetime.timedelta = timedelta # Keep original timedelta

        # Mock rationale: os.path.exists is used to check if a path exists.
        # We mock it to control the existence of paths for testing error handling and valid inputs.
        self.patcher_os_path_exists = patch('os.path.exists', return_value=True)
        self.mock_os_path_exists = self.patcher_os_path_exists.start()

        # Mock rationale: os.path.isdir and os.path.isfile are used to determine path types.
        # We mock them to simulate file system structure without actual disk I/O.
        self.patcher_os_path_isdir = patch('os.path.isdir', side_effect=lambda p: p.endswith('/') or 'dir' in p)
        self.mock_os_path_isdir = self.patcher_os_path_isdir.start()
        self.patcher_os_path_isfile = patch('os.path.isfile', side_effect=lambda p: not (p.endswith('/') or 'dir' in p))
        self.mock_os_path_isfile = self.patcher_os_path_isfile.start()

    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.patcher_os_path_exists.stop()
        self.patcher_os_path_isdir.stop()
        self.patcher_os_path_isfile.stop()

    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the modification time of a file.
        # We need to control this value to deterministically test file age calculation.
        # By setting it to a specific timestamp, we can ensure the age calculation is correct.
        
        # File modified 40 days ago
        forty_days_ago_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        mock_getmtime.return_value = forty_days_ago_timestamp
        self.assertEqual(sweeper.get_file_age_days('/path/to/old_file.txt'), 40)

        # File modified 10 days ago
        ten_days_ago_timestamp = (self.mock_now - timedelta(days=10)).timestamp()
        mock_getmtime.return_value = ten_days_ago_timestamp
        self.assertEqual(sweeper.get_file_age_days('/path/to/recent_file.txt'), 10)

        # Test non-existent file
        self.mock_os_path_exists.return_value = False # Temporarily mock exists for this specific test
        self.assertEqual(sweeper.get_file_age_days('/path/to/non_existent.txt'), -1)
        self.mock_os_path_exists.return_value = True # Reset for other tests

    @patch('os.listdir')
    def test_is_empty_dir(self, mock_listdir):
        # Mock rationale: os.listdir returns a list of entries in a directory.
        # We need to control this to simulate empty or non-empty directories for testing.
        
        # Empty directory
        mock_listdir.return_value = []
        self.assertTrue(sweeper.is_empty_dir('/path/to/empty_dir'))

        # Non-empty directory
        mock_listdir.return_value = ['file.txt']
        self.assertFalse(sweeper.is_empty_dir('/path/to/non_empty_dir'))

        # Not a directory (mocked by self.mock_os_path_isdir)
        self.mock_os_path_isdir.side_effect = lambda p: p == '/path/to/actual_dir'
        self.assertFalse(sweeper.is_empty_dir('/path/to/file.txt'))
        self.mock_os_path_isdir.side_effect = lambda p: p.endswith('/') or 'dir' in p # Reset

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    def test_find_dust_bunnies(self, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: os.walk simulates traversing a directory tree.
        # os.path.getmtime controls file ages. os.listdir controls directory emptiness.
        # These mocks allow us to create a virtual filesystem for testing without actual disk I/O.

        # Setup mock file modification times
        old_file_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        recent_file_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        def getmtime_side_effect(path):
            if 'old_file' in path: return old_file_timestamp
            if 'recent_file' in path: return recent_file_timestamp
            return recent_file_timestamp # Default for other files
        mock_getmtime.side_effect = getmtime_side_effect

        # Setup mock os.listdir for empty_dir check
        def listdir_side_effect(path):
            if 'empty_dir' in path: return []
            return ['some_file.txt'] # Default for non-empty
        mock_listdir.side_effect = listdir_side_effect

        # Setup mock os.walk to simulate a directory structure
        # /root_path/old_file.txt (40 days old)
        # /root_path/recent_file.txt (10 days old)
        # /root_path/subdir1/empty_dir/ (empty)
        # /root_path/subdir2/file.txt
        mock_walk.return_value = [
            ('/root_path', ['subdir1', 'subdir2'], ['old_file.txt', 'recent_file.txt']),
            ('/root_path/subdir1', ['empty_dir'], []),
            ('/root_path/subdir1/empty_dir', [], []),
            ('/root_path/subdir2', [], ['file.txt'])
        ]

        # Mock os.path.isdir and os.path.isfile for the walk process
        self.mock_os_path_isdir.side_effect = lambda p: 'dir' in p or p.endswith('/')
        self.mock_os_path_isfile.side_effect = lambda p: 'file' in p or '.txt' in p

        old_files, empty_dirs = sweeper.find_dust_bunnies('/root_path', 30)

        self.assertIn('/root_path/old_file.txt', old_files)
        self.assertNotIn('/root_path/recent_file.txt', old_files)
        self.assertIn('/root_path/subdir1/empty_dir', empty_dirs)
        self.assertNotIn('/root_path', empty_dirs) # Root should not be considered empty
        self.assertEqual(len(old_files), 1)
        self.assertEqual(len(empty_dirs), 1)

        # Test non-existent root path
        self.mock_os_path_exists.return_value = False
        old_files, empty_dirs = sweeper.find_dust_bunnies('/non_existent_path', 30)
        self.assertEqual(old_files, [])
        self.assertEqual(empty_dirs, [])
        self.mock_os_path_exists.return_value = True # Reset

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    @patch('sweeper.is_empty_dir', return_value=True) # Ensure rmdir re-check passes for all dirs
    def test_sweep_bunnies_dry_run(self, mock_is_empty_dir, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: os.remove and os.rmdir perform actual file system modifications.
        # builtins.print captures output. is_empty_dir ensures rmdir check passes.
        # These mocks prevent actual deletions and allow us to verify logging behavior.

        old_files = ['/path/to/old_file1.txt', '/path/to/old_file2.log']
        empty_dirs = ['/path/to/empty_dir1', '/path/to/empty_dir2']

        sweeper.sweep_bunnies(old_files, empty_dirs, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()
        mock_print.assert_any_call("\n--- DRY RUN MODE --- No changes will be made ---")
        mock_print.assert_any_call("  - /path/to/old_file1.txt")
        mock_print.assert_any_call("  - /path/to/empty_dir1")

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    @patch('sweeper.is_empty_dir', side_effect=[True, False, True]) # For rmdir re-check: dir3, then dir2, then dir1
    def test_sweep_bunnies_actual_run(self, mock_is_empty_dir, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: os.remove and os.rmdir perform actual file system modifications.
        # builtins.print captures output. is_empty_dir simulates directory state changes.
        # These mocks prevent actual deletions and allow us to verify deletion calls and error handling.

        old_files = ['/path/to/old_file1.txt', '/path/to/old_file2.log']
        empty_dirs = ['/path/to/empty_dir1', '/path/to/empty_dir2', '/path/to/empty_dir3']

        sweeper.sweep_bunnies(old_files, empty_dirs, dry_run=False)

        mock_remove.assert_called_with('/path/to/old_file1.txt')
        mock_remove.assert_called_with('/path/to/old_file2.log')
        self.assertEqual(mock_remove.call_count, 2)

        # empty_dir1 and empty_dir3 should be removed (as is_empty_dir returns True for them)
        # empty_dir2 should be skipped (as is_empty_dir returns False for it)
        # Due to sorting, deepest paths are processed first. Assuming /path/to/empty_dir3 is deepest.
        mock_rmdir.assert_any_call('/path/to/empty_dir3') 
        mock_rmdir.assert_any_call('/path/to/empty_dir1')
        self.assertEqual(mock_rmdir.call_count, 2)
        mock_print.assert_any_call("    Skipping /path/to/empty_dir2: no longer empty.")

    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('os.rmdir', side_effect=OSError("Directory not empty"))
    @patch('builtins.print')
    @patch('sweeper.is_empty_dir', return_value=True)
    def test_sweep_bunnies_error_handling(self, mock_is_empty_dir, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: os.remove and os.rmdir can raise OSErrors (e.g., permission denied).
        # We need to simulate these errors to ensure the utility handles them gracefully and logs appropriately.

        old_files = ['/path/to/unremovable_file.txt']
        empty_dirs = ['/path/to/unremovable_dir']

        sweeper.sweep_bunnies(old_files, empty_dirs, dry_run=False)

        mock_remove.assert_called_once_with('/path/to/unremovable_file.txt')
        mock_rmdir.assert_called_once_with('/path/to/unremovable_dir')
        mock_print.assert_any_call("    Error deleting file /path/to/unremovable_file.txt: Permission denied")
        mock_print.assert_any_call("    Error deleting directory /path/to/unremovable_dir: Directory not empty")

if __name__ == '__main__':
    unittest.main()
