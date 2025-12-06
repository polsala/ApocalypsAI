import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the Python path to import duster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import find_empty_dirs, find_old_small_files, run_duster

class TestDuster(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age checks across tests
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0)

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: os.walk is a file system traversal function. We need to control its
        # output to simulate various directory structures without actually creating files on disk,
        # ensuring deterministic and isolated tests.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir'], ['file1.txt']), # /root is not empty
            ('/root/dir1', [], ['file2.txt']), # /root/dir1 is not empty
            ('/root/dir2', ['subdir'], []), # /root/dir2 is not empty (has subdir)
            ('/root/dir2/subdir', [], []), # This is an empty dir
            ('/root/empty_dir', [], []), # This is an empty dir
        ]
        expected_empty_dirs = [
            '/root/dir2/subdir',
            '/root/empty_dir'
        ]
        result = find_empty_dirs('/root')
        self.assertCountEqual(result, expected_empty_dirs)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.stat')
    def test_find_old_small_files(self, mock_os_stat, mock_os_path_isfile, mock_os_walk):
        # Mock rationale: os.walk, os.path.isfile, and os.stat are file system interaction functions.
        # We need to control their behavior to simulate files with specific properties (age, size, name)
        # without relying on actual file system state, ensuring deterministic and isolated tests.

        # Simulate current time for age calculation
        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Allow real timestamp conversion
            mock_dt.timedelta = timedelta # Ensure timedelta works as expected

            mock_os_walk.return_value = [
                ('/root', [], [
                    'old_small.log',    # Matches criteria
                    'new_small.log',    # Too new
                    'old_large.log',    # Too large
                    'old_small.txt',    # Wrong pattern
                    'old_small.bak',    # Matches criteria
                    'inaccessible.log'  # Will raise OSError
                ]),
            ]
            # All paths are files except the inaccessible one
            mock_os_path_isfile.side_effect = lambda x: x != '/root/inaccessible.log'

            # Mock os.stat for each file
            def mock_stat_side_effect(path):
                stat_mock = MagicMock()
                if path == '/root/old_small.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp() # Old
                    stat_mock.st_size = 500 # Small (<1KB)
                elif path == '/root/new_small.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=10)).timestamp() # New
                    stat_mock.st_size = 500 # Small
                elif path == '/root/old_large.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp() # Old
                    stat_mock.st_size = 2000 * 1024 # Large (>1KB)
                elif path == '/root/old_small.txt':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp() # Old
                    stat_mock.st_size = 500 # Small
                elif path == '/root/old_small.bak':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp() # Old
                    stat_mock.st_size = 500 # Small
                elif path == '/root/inaccessible.log':
                    raise OSError("Permission denied") # Simulate inaccessible file
                else:
                    raise FileNotFoundError # Should not happen with current mock_os_walk
                return stat_mock

            mock_os_stat.side_effect = mock_stat_side_effect

            expected_files = [
                '/root/old_small.log',
                '/root/old_small.bak'
            ]
            result = find_old_small_files('/root', age_days=30, max_size_kb=1, patterns=['log', 'bak'])
            self.assertCountEqual(result, expected_files)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.stat')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir') # For checking if directory is empty before rmdir
    @patch('builtins.print') # Mock print to capture output
    def test_run_duster_dry_run(self, mock_print, mock_os_listdir, mock_os_rmdir, mock_os_remove, mock_os_stat, mock_os_path_isfile, mock_os_walk):
        # Mock rationale: We need to simulate the entire file system interaction and output
        # without actually touching the disk. This includes file listing, stat calls,
        # and verifying that deletion operations DO NOT occur in dry run. print is mocked to verify output messages.

        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
            mock_dt.timedelta = timedelta

            mock_os_walk.return_value = [
                ('/root', ['empty_dir', 'non_empty_dir'], ['old_small.log']),
                ('/root/empty_dir', [], []),
                ('/root/non_empty_dir', [], ['another_file.txt']),
            ]
            mock_os_path_isfile.side_effect = lambda x: x == '/root/old_small.log'

            def mock_stat_side_effect(path):
                stat_mock = MagicMock()
                if path == '/root/old_small.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp()
                    stat_mock.st_size = 500
                else:
                    raise FileNotFoundError
                return stat_mock
            mock_os_stat.side_effect = mock_stat_side_effect

            # Mock os.listdir for empty_dir check (it's empty)
            mock_os_listdir.side_effect = lambda p: [] if p == '/root/empty_dir' else ['file']

            exit_code = run_duster('/root', dry_run=True, age_days=30, max_size_kb=1, patterns=['log'])

            self.assertEqual(exit_code, 0) # Should be 0 if items found, even in dry run
            mock_os_remove.assert_not_called()
            mock_os_rmdir.assert_not_called()
            mock_print.assert_any_call("Found 1 empty directories.")
            mock_print.assert_any_call("  [DIR] /root/empty_dir")
            mock_print.assert_any_call("Found 1 old, small files matching patterns.")
            mock_print.assert_any_call("  [FILE] /root/old_small.log")
            mock_print.assert_any_call("\nDry run complete. No items were deleted.")

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.stat')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('builtins.print')
    def test_run_duster_delete(self, mock_print, mock_os_listdir, mock_os_rmdir, mock_os_remove, mock_os_stat, mock_os_path_isfile, mock_os_walk):
        # Mock rationale: Similar to dry run, but now we expect os.remove and os.rmdir to be called.
        # We verify these calls and the corresponding print messages, simulating successful deletion.

        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
            mock_dt.timedelta = timedelta

            mock_os_walk.return_value = [
                ('/root', ['empty_dir', 'non_empty_dir'], ['old_small.log']),
                ('/root/empty_dir', [], []),
                ('/root/non_empty_dir', [], ['another_file.txt']),
            ]
            mock_os_path_isfile.side_effect = lambda x: x == '/root/old_small.log'

            def mock_stat_side_effect(path):
                stat_mock = MagicMock()
                if path == '/root/old_small.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp()
                    stat_mock.st_size = 500
                else:
                    raise FileNotFoundError
                return stat_mock
            mock_os_stat.side_effect = mock_stat_side_effect

            # Mock os.listdir for empty_dir check (it's empty)
            mock_os_listdir.side_effect = lambda p: [] if p == '/root/empty_dir' else ['file']

            exit_code = run_duster('/root', dry_run=False, age_days=30, max_size_kb=1, patterns=['log'])

            self.assertEqual(exit_code, 0)
            mock_os_remove.assert_called_once_with('/root/old_small.log')
            mock_os_rmdir.assert_called_once_with('/root/empty_dir')
            mock_print.assert_any_call("  Deleted file: /root/old_small.log")
            mock_print.assert_any_call("  Deleted empty directory: /root/empty_dir")
            mock_print.assert_any_call("\nDeletion complete. Total items deleted: 2")

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.stat')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('builtins.print')
    def test_run_duster_no_dust_bunnies(self, mock_print, mock_os_listdir, mock_os_rmdir, mock_os_remove, mock_os_stat, mock_os_path_isfile, mock_os_walk):
        # Mock rationale: Test the scenario where no files or directories meet the criteria.
        # Verify that no deletions occur and the correct "no-op" message and exit code are returned.

        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
            mock_dt.timedelta = timedelta

            mock_os_walk.return_value = [
                ('/root', ['non_empty_dir'], ['important.py']), # /root is not empty
                ('/root/non_empty_dir', [], ['another_file.txt']), # /root/non_empty_dir is not empty
            ]
            # All paths are files, but none match criteria
            mock_os_path_isfile.side_effect = lambda x: x == '/root/important.py' or x == '/root/non_empty_dir/another_file.txt'

            def mock_stat_side_effect(path):
                stat_mock = MagicMock()
                if path == '/root/important.py':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=10)).timestamp() # Too new
                    stat_mock.st_size = 10000 # Too large
                elif path == '/root/non_empty_dir/another_file.txt':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=10)).timestamp() # Too new
                    stat_mock.st_size = 10000 # Too large
                else:
                    raise FileNotFoundError
                return stat_mock
            mock_os_stat.side_effect = mock_stat_side_effect

            # All dirs are non-empty
            mock_os_listdir.return_value = ['file']

            exit_code = run_duster('/root', dry_run=False, age_days=30, max_size_kb=1, patterns=['log'])

            self.assertEqual(exit_code, 2) # No-op exit code
            mock_os_remove.assert_not_called()
            mock_os_rmdir.assert_not_called()
            mock_print.assert_any_call("No digital dust bunnies found. Your space is pristine!")

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.stat')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('builtins.print')
    def test_run_duster_deletion_errors(self, mock_print, mock_os_listdir, mock_os_rmdir, mock_os_remove, mock_os_stat, mock_os_path_isfile, mock_os_walk):
        # Mock rationale: Test how the duster handles errors during deletion. Verify that errors
        # are printed to stderr but the process continues for other items, and the exit code is still 0 (success).

        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
            mock_dt.timedelta = timedelta

            mock_os_walk.return_value = [
                ('/root', ['empty_dir'], ['old_small.log']),
                ('/root/empty_dir', [], []),
            ]
            mock_os_path_isfile.side_effect = lambda x: x == '/root/old_small.log'

            def mock_stat_side_effect(path):
                stat_mock = MagicMock()
                if path == '/root/old_small.log':
                    stat_mock.st_mtime = (self.mock_now - timedelta(days=40)).timestamp()
                    stat_mock.st_size = 500
                else:
                    raise FileNotFoundError
                return stat_mock
            mock_os_stat.side_effect = mock_stat_side_effect

            mock_os_listdir.return_value = [] # empty_dir is truly empty

            # Make deletion fail for the file, but succeed for the directory
            mock_os_remove.side_effect = OSError("Permission denied for file")
            mock_os_rmdir.return_value = None # Succeeds for directory

            exit_code = run_duster('/root', dry_run=False, age_days=30, max_size_kb=1, patterns=['log'])

            self.assertEqual(exit_code, 0) # Still 0 as some items were processed/attempted
            mock_os_remove.assert_called_once_with('/root/old_small.log')
            mock_os_rmdir.assert_called_once_with('/root/empty_dir')
            mock_print.assert_any_call("  Error deleting file /root/old_small.log: Permission denied for file", file=sys.stderr)
            mock_print.assert_any_call("  Deleted empty directory: /root/empty_dir")
            mock_print.assert_any_call("\nDeletion complete. Total items deleted: 1") # Only directory was deleted successfully


if __name__ == '__main__':
    unittest.main()
