import unittest
from unittest.mock import patch, MagicMock
import os
import time
import sys

# Mock rationale: We need to simulate file system interactions (walking directories, checking modification times, deleting files/dirs)
# without actually touching the real file system. This ensures tests are deterministic, fast, and safe.

# Add src directory to sys.path for importing sweeper module during testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import sweeper
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a base time for mocking file modification times
        self.now = time.time()
        self.one_day_ago = self.now - (24 * 60 * 60)
        self.sixty_days_ago = self.now - (60 * 24 * 60 * 60)

    @patch('os.walk')
    def test_find_empty_dirs_no_empty(self, mock_os_walk):
        # Mock rationale: Simulate a directory structure with no empty directories.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], ['file3.txt']),
        ]
        empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertEqual(len(empty_dirs), 0)

    @patch('os.walk')
    def test_find_empty_dirs_with_empty(self, mock_os_walk):
        # Mock rationale: Simulate a directory structure containing empty directories.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'empty_dir1'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/empty_dir1', [], []),
            ('/root/dir1/empty_subdir', [], []),
        ]
        empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertIn(os.path.join('/root', 'empty_dir1'), empty_dirs)
        self.assertIn(os.path.join('/root', 'dir1', 'empty_subdir'), empty_dirs)
        self.assertEqual(len(empty_dirs), 2)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_files_no_old_files(self, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate files that are not old enough or don't match extensions.
        mock_os_walk.return_value = [
            ('/root', [], ['recent.log', 'recent.tmp', 'new.txt']),
        ]
        # All files are recent (e.g., 1 day old)
        mock_getmtime.side_effect = lambda x: self.one_day_ago

        old_files = sweeper.find_old_files('/root', 30, ['.log', '.tmp'])
        self.assertEqual(len(old_files), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_files_with_old_files(self, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate files that are old and match extensions.
        mock_os_walk.return_value = [
            ('/root', [], ['old.log', 'old.tmp', 'recent.log', 'old.bak', 'new.txt']),
        ]
        # Define specific modification times for files
        def getmtime_side_effect(path):
            if 'old.log' in path or 'old.tmp' in path or 'old.bak' in path:
                return self.sixty_days_ago # Older than 30 days
            elif 'recent.log' in path:
                return self.one_day_ago # Newer than 30 days
            return self.now # Default for others

        mock_getmtime.side_effect = getmtime_side_effect

        old_files = sweeper.find_old_files('/root', 30, ['.log', '.tmp', '.bak'])
        self.assertEqual(len(old_files), 3)
        self.assertIn(os.path.join('/root', 'old.log'), old_files)
        self.assertIn(os.path.join('/root', 'old.tmp'), old_files)
        self.assertIn(os.path.join('/root', 'old.bak'), old_files)
        self.assertNotIn(os.path.join('/root', 'recent.log'), old_files)
        self.assertNotIn(os.path.join('/root', 'new.txt'), old_files)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print') # Mock print to prevent console output during tests
    @patch('os.path.isdir', return_value=True) # Mock rationale: Ensure paths are considered valid for scanning
    def test_main_delete_mode(self, mock_isdir, mock_print, mock_parse_args, mock_rmdir, mock_remove, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate a full run of the main function with deletion enabled.
        # We need to mock argparse to control CLI arguments, os.remove/rmdir to verify deletions,
        # and os.walk/getmtime for file system simulation.

        # Simulate CLI arguments for deletion
        mock_parse_args.return_value = MagicMock(
            paths=['/test_root'],
            age=30,
            extensions=['.log', '.tmp'],
            delete=True
        )

        # Simulate directory structure and files
        mock_os_walk.return_value = [
            ('/test_root', ['empty_dir'], ['old.log', 'recent.tmp', 'keep.txt']),
            ('/test_root/empty_dir', [], []),
        ]

        # Simulate file modification times
        def getmtime_side_effect(path):
            if 'old.log' in path:
                return self.sixty_days_ago
            elif 'recent.tmp' in path:
                return self.one_day_ago
            return self.now

        mock_getmtime.side_effect = getmtime_side_effect

        sweeper.main()

        # Verify os.remove was called for 'old.log'
        mock_remove.assert_called_once_with(os.path.join('/test_root', 'old.log'))

        # Verify os.rmdir was called for 'empty_dir'
        mock_rmdir.assert_called_once_with(os.path.join('/test_root', 'empty_dir'))

        # Verify print calls for deletion confirmation
        mock_print.assert_any_call(f"  Deleted old file: {os.path.join('/test_root', 'old.log')}")
        mock_print.assert_any_call(f"  Deleted empty directory: {os.path.join('/test_root', 'empty_dir')}")

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True) # Mock rationale: Ensure paths are considered valid for scanning
    def test_main_dry_run_mode(self, mock_isdir, mock_print, mock_parse_args, mock_rmdir, mock_remove, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate a full run of the main function with deletion disabled (dry run).
        # Verify that os.remove and os.rmdir are NOT called.

        # Simulate CLI arguments for dry run
        mock_parse_args.return_value = MagicMock(
            paths=['/test_root'],
            age=30,
            extensions=['.log'],
            delete=False
        )

        # Simulate directory structure and files
        mock_os_walk.return_value = [
            ('/test_root', ['empty_dir'], ['old.log', 'recent.log']),
            ('/test_root/empty_dir', [], []),
        ]

        # Simulate file modification times
        def getmtime_side_effect(path):
            if 'old.log' in path:
                return self.sixty_days_ago
            elif 'recent.log' in path:
                return self.one_day_ago
            return self.now

        mock_getmtime.side_effect = getmtime_side_effect

        sweeper.main()

        # Verify that os.remove and os.rmdir were NOT called
        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()

        # Verify print calls indicate a dry run
        mock_print.assert_any_call("\nFound Empty Directories (potential dust bunnies):")
        mock_print.assert_any_call(f"  - {os.path.join('/test_root', 'empty_dir')}")
        mock_print.assert_any_call("\nFound Old Files (stale digital detritus older than 30 days):")
        mock_print.assert_any_call(f"  - {os.path.join('/test_root', 'old.log')}")
        mock_print.assert_any_call("\n--- Dry Run Complete. Use --delete to perform actual cleanup. ---")

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_isdir, mock_getmtime, mock_os_walk):
        # Mock rationale: Test how the utility handles an invalid path provided by the user.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = MagicMock(
                paths=['/non_existent_path'],
                age=30,
                extensions=['.log'],
                delete=False
            )
            sweeper.main()

            # Check if the warning for invalid path was printed to stderr
            mock_print.assert_any_call("Warning: Path '/non_existent_path' is not a valid directory. Skipping.", file=sys.stderr)
            mock_os_walk.assert_not_called() # os.walk should not be called for invalid paths


if __name__ == '__main__':
    unittest.main()
