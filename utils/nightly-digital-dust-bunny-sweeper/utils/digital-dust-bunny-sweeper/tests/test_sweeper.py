import unittest
from unittest.mock import patch, MagicMock
import os
import time
import sys
from io import StringIO

# Add the src directory to the Python path for importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actually creating files.
        # This allows deterministic testing of directory traversal logic and empty directory identification.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir_top'], ['file1.txt']),
            ('/root/dir1', ['subdir1'], []),
            ('/root/dir1/subdir1', [], []), # This should be found as empty
            ('/root/dir2', [], ['file2.log']),
            ('/root/empty_dir_top', [], []), # This should be found as empty
            ('/root/dir1/subdir2', [], []) # Another empty dir
        ]
        # Expected order: deeper empty dirs first, then shallower ones.
        expected_empty_dirs = ['/root/dir1/subdir2', '/root/dir1/subdir1', '/root/empty_dir_top']
        found_dirs = sweeper.find_empty_dirs('/root')
        self.assertEqual(found_dirs, expected_empty_dirs)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_old_logs(self, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate file modification times and directory structure.
        # This allows testing age-based filtering without relying on actual file timestamps or creating files.
        current_time = time.time()
        one_day_ago = current_time - (1 * 24 * 60 * 60)
        ten_days_ago = current_time - (10 * 24 * 60 * 60)
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)

        mock_os_walk.return_value = [
            ('/root', [], ['recent.log', 'old.txt', 'very_old.log', 'not_log.md']),
            ('/root/logs', [], ['app.log', 'debug.txt'])
        ]

        # Mock rationale: Provide specific modification times for mocked files.
        # This ensures deterministic results for age-based filtering logic.
        mock_getmtime.side_effect = lambda path: {
            '/root/recent.log': one_day_ago,
            '/root/old.txt': thirty_days_ago,
            '/root/very_old.log': thirty_days_ago + 1, # Just under 30 days old
            '/root/not_log.md': ten_days_ago,
            '/root/logs/app.log': thirty_days_ago,
            '/root/logs/debug.txt': one_day_ago
        }.get(path, current_time) # Default to current_time for unexpected paths

        # Test with 29 days old cutoff (should find 'old.txt' and 'app.log')
        old_logs = sweeper.find_old_logs('/root', 29, ['.log', '.txt'])
        self.assertIn('/root/old.txt', old_logs)
        self.assertIn('/root/logs/app.log', old_logs)
        self.assertNotIn('/root/recent.log', old_logs)
        self.assertNotIn('/root/very_old.log', old_logs)
        self.assertNotIn('/root/not_log.md', old_logs)
        self.assertNotIn('/root/logs/debug.txt', old_logs)
        self.assertEqual(len(old_logs), 2)

        # Test with 31 days old cutoff (should find nothing older than 31 days)
        old_logs_31_days = sweeper.find_old_logs('/root', 31, ['.log', '.txt'])
        self.assertEqual(len(old_logs_31_days), 0)

        # Test with custom extensions
        old_logs_custom_ext = sweeper.find_old_logs('/root', 29, ['.md'])
        self.assertIn('/root/not_log.md', old_logs_custom_ext)
        self.assertEqual(len(old_logs_custom_ext), 1)

    @patch('os.walk')
    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.getmtime')
    def test_perform_cleanup_dry_run(self, mock_getmtime, mock_os_remove, mock_os_rmdir, mock_os_walk):
        # Mock rationale: Simulate file system operations and modification times.
        # This allows testing the dry-run output and ensuring no actual deletions occur.
        current_time = time.time()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)

        mock_os_walk.return_value = [
            ('/root', ['empty_dir', 'logs'], ['old.txt']),
            ('/root/empty_dir', [], []),
            ('/root/logs', [], ['app.log'])
        ]
        mock_getmtime.side_effect = lambda path: {
            '/root/old.txt': thirty_days_ago,
            '/root/logs/app.log': thirty_days_ago
        }.get(path, current_time)

        sweeper.perform_cleanup(
            '/root',
            dry_run=True,
            delete_empty_dirs_flag=True,
            delete_old_logs_days=29,
            log_extensions=['.log', '.txt']
        )

        output = self.mock_stdout.getvalue()
        self.assertIn('*** DRY RUN MODE: No files or directories will be deleted. ***', output)
        self.assertIn('[DRY RUN] Found empty directory: /root/empty_dir', output)
        self.assertIn('[DRY RUN] Found old log file: /root/old.txt', output)
        self.assertIn('[DRY RUN] Found old log file: /root/logs/app.log', output)
        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()

    @patch('os.walk')
    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.getmtime')
    def test_perform_cleanup_actual_deletion(self, mock_getmtime, mock_os_remove, mock_os_rmdir, mock_os_walk):
        # Mock rationale: Simulate file system operations and modification times.
        # This allows testing that deletion functions are called correctly when not in dry-run mode.
        current_time = time.time()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)

        mock_os_walk.return_value = [
            ('/root', ['empty_dir', 'logs'], ['old.txt']),
            ('/root/empty_dir', [], []),
            ('/root/logs', [], ['app.log'])
        ]
        mock_getmtime.side_effect = lambda path: {
            '/root/old.txt': thirty_days_ago,
            '/root/logs/app.log': thirty_days_ago
        }.get(path, current_time)

        sweeper.perform_cleanup(
            '/root',
            dry_run=False,
            delete_empty_dirs_flag=True,
            delete_old_logs_days=29,
            log_extensions=['.log', '.txt']
        )

        output = self.mock_stdout.getvalue()
        self.assertIn('Found empty directory: /root/empty_dir', output)
        self.assertIn('Deleted: /root/empty_dir', output)
        self.assertIn('Found old log file: /root/old.txt', output)
        self.assertIn('Deleted: /root/old.txt', output)
        self.assertIn('Found old log file: /root/logs/app.log', output)
        self.assertIn('Deleted: /root/logs/app.log', output)

        mock_os_rmdir.assert_called_once_with('/root/empty_dir')
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_os_remove.assert_any_call('/root/old.txt')
        mock_os_remove.assert_any_call('/root/logs/app.log')

    @patch('os.path.isdir')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.perform_cleanup')
    def test_main_invalid_path(self, mock_perform_cleanup, mock_parse_args, mock_isdir):
        # Mock rationale: Simulate command-line arguments and an invalid directory path.
        # This tests the argument parsing and error handling for invalid paths without actual file system checks.
        mock_parse_args.return_value = MagicMock(
            path_to_scan='/nonexistent',
            dry_run=False,
            delete_empty_dirs=False,
            delete_old_logs=None,
            log_extensions=['.log', '.txt']
        )
        mock_isdir.return_value = False # Simulate invalid path

        with self.assertRaises(SystemExit) as cm:
            sweeper.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: '/nonexistent' is not a valid directory.", self.mock_stdout.getvalue())
        mock_perform_cleanup.assert_not_called()

    @patch('os.path.isdir')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.perform_cleanup')
    def test_main_valid_path(self, mock_perform_cleanup, mock_parse_args, mock_isdir):
        # Mock rationale: Simulate command-line arguments and a valid directory path.
        # This tests that `main` correctly calls `perform_cleanup` with parsed arguments.
        mock_parse_args.return_value = MagicMock(
            path_to_scan='/valid/path',
            dry_run=True,
            delete_empty_dirs=True,
            delete_old_logs=7,
            log_extensions=['.log']
        )
        mock_isdir.return_value = True # Simulate valid path

        sweeper.main()

        mock_perform_cleanup.assert_called_once_with(
            '/valid/path',
            True,
            True,
            7,
            ['.log']
        )

if __name__ == '__main__':
    unittest.main()
