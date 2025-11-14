import unittest
from unittest.mock import patch, MagicMock
import os
import time
import shutil
from datetime import datetime, timedelta

# Import the function to be tested
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic testing
        self.fixed_current_time = datetime(2023, 10, 26, 12, 0, 0).timestamp()
        self.age_days = 30
        self.age_seconds = self.age_days * 24 * 60 * 60

        # Mock time.time() globally for all tests in this class
        self.patcher_time = patch('time.time', return_value=self.fixed_current_time)
        self.mock_time = self.patcher_time.start()

    def tearDown(self):
        self.patcher_time.stop()

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_invalid_target_path(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate non-existent or non-directory target paths.
        mock_exists.return_value = False
        result = collect_dust("/nonexistent/path")
        self.assertEqual(result["status"], "error")
        self.assertIn("does not exist", result["message"])

        mock_exists.return_value = True
        mock_isdir.return_value = False
        result = collect_dust("/file/not/dir")
        self.assertEqual(result["status"], "error")
        self.assertIn("is not a directory", result["message"])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    def test_dry_run_identifies_stale_files_and_empty_dirs(self, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory structure and file modification times
        # to test identification logic without actual filesystem interaction.
        # os.walk: Provides the directory structure.
        # os.path.getmtime: Returns specific timestamps for files.
        # os.listdir: Returns empty list for designated empty directories.

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/test_repo', ['sub1', 'sub2', '.cosmic-dust-bin'], ['old_file.txt', 'new_file.txt']),
            ('/test_repo/sub1', [], ['another_old.log']),
            ('/test_repo/sub2', [], []),
            ('/test_repo/.cosmic-dust-bin', [], ['moved_file.txt'])
        ]

        # Simulate file modification times
        # old_file.txt: 60 days old (stale)
        # new_file.txt: 10 days old (fresh)
        # another_old.log: 40 days old (stale)
        mock_getmtime.side_effect = lambda p: {
            '/test_repo/old_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=60)).timestamp(),
            '/test_repo/new_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=10)).timestamp(),
            '/test_repo/sub1/another_old.log': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=40)).timestamp(),
            '/test_repo/.cosmic-dust-bin/moved_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=5)).timestamp(),
        }.get(p, self.fixed_current_time) # Default to current time if not specified

        # Simulate empty directories
        mock_listdir.side_effect = lambda p: [] if p == '/test_repo/sub2' else ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=True)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["stale_files_found"], 2)
        self.assertIn('/test_repo/old_file.txt', result["stale_files_list"])
        self.assertIn('/test_repo/sub1/another_old.log', result["stale_files_list"])

        self.assertEqual(result["empty_dirs_found"], 1)
        self.assertIn('/test_repo/sub2', result["empty_dirs_list"])

        self.assertTrue(result["dry_run"])
        self.assertEqual(len(result["files_moved"]), 0)
        self.assertEqual(len(result["dirs_removed"]), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.rmdir')
    def test_live_run_moves_files_and_removes_dirs(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory structure and file modification times
        # to test the actual move/remove logic. Track calls to os.makedirs, shutil.move, os.rmdir.

        mock_walk.return_value = [
            ('/test_repo', ['sub1', 'sub2'], ['old_file.txt', 'new_file.txt']),
            ('/test_repo/sub1', [], ['another_old.log']),
            ('/test_repo/sub2', [], []),
        ]

        mock_getmtime.side_effect = lambda p: {
            '/test_repo/old_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=60)).timestamp(),
            '/test_repo/new_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=10)).timestamp(),
            '/test_repo/sub1/another_old.log': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=40)).timestamp(),
        }.get(p, self.fixed_current_time)

        # Simulate empty directories
        mock_listdir.side_effect = lambda p: [] if p == '/test_repo/sub2' else ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["stale_files_found"], 2)
        self.assertEqual(result["empty_dirs_found"], 1)

        self.assertFalse(result["dry_run"])

        # Assert that os.makedirs was called for the dust bin
        mock_makedirs.assert_called_once_with(os.path.join("/test_repo", ".cosmic-dust-bin"), exist_ok=True)

        # Assert that shutil.move was called for stale files
        mock_move.assert_any_call('/test_repo/old_file.txt', os.path.join("/test_repo", ".cosmic-dust-bin", 'old_file.txt'))
        mock_move.assert_any_call('/test_repo/sub1/another_old.log', os.path.join("/test_repo", ".cosmic-dust-bin", 'another_old.log'))
        self.assertEqual(mock_move.call_count, 2)
        self.assertEqual(len(result["files_moved"]), 2)

        # Assert that os.rmdir was called for empty directories
        mock_rmdir.assert_called_once_with('/test_repo/sub2')
        self.assertEqual(len(result["dirs_removed"]), 1)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.rmdir')
    def test_no_stale_files_or_empty_dirs(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a scenario where no files are stale and no directories are empty.

        mock_walk.return_value = [
            ('/test_repo', ['sub1'], ['new_file.txt']),
            ('/test_repo/sub1', [], ['another_new.log']),
        ]

        mock_getmtime.side_effect = lambda p: {
            '/test_repo/new_file.txt': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=5)).timestamp(),
            '/test_repo/sub1/another_new.log': (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=15)).timestamp(),
        }.get(p, self.fixed_current_time)

        mock_listdir.return_value = ['some_file'] # All directories are non-empty

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["stale_files_found"], 0)
        self.assertEqual(result["empty_dirs_found"], 0)

        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()
        mock_rmdir.assert_not_called()

        self.assertEqual(len(result["files_moved"]), 0)
        self.assertEqual(len(result["dirs_removed"]), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move', side_effect=OSError("Permission denied"))
    @patch('os.rmdir')
    def test_error_handling_move(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a permission error during file movement.

        mock_walk.return_value = [
            ('/test_repo', [], ['old_file.txt']),
        ]
        mock_getmtime.return_value = (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=60)).timestamp()
        mock_listdir.return_value = ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False)

        self.assertEqual(result["status"], "success") # The overall operation might still be successful in reporting
        self.assertEqual(result["stale_files_found"], 1)
        self.assertEqual(len(result["files_moved"]), 0)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Error moving /test_repo/old_file.txt: Permission denied", result["errors"][0])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.rmdir', side_effect=OSError("Directory not empty"))
    def test_error_handling_rmdir(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Simulate an error during directory removal (e.g., directory became non-empty).

        mock_walk.return_value = [
            ('/test_repo', ['sub1'], []),
            ('/test_repo/sub1', [], []),
        ]
        mock_getmtime.return_value = self.fixed_current_time # No stale files
        mock_listdir.side_effect = lambda p: [] if p == '/test_repo/sub1' else ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["empty_dirs_found"], 1)
        self.assertEqual(len(result["dirs_removed"]), 0)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Error removing /test_repo/sub1: Directory not empty", result["errors"][0])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.rmdir')
    def test_custom_dust_bin_name(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Verify that a custom dust bin name is used correctly.

        custom_bin = ".archive"
        mock_walk.return_value = [
            ('/test_repo', [], ['old_file.txt']),
        ]
        mock_getmtime.return_value = (datetime.fromtimestamp(self.fixed_current_time) - timedelta(days=60)).timestamp()
        mock_listdir.return_value = ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False, dust_bin_name=custom_bin)

        mock_makedirs.assert_called_once_with(os.path.join("/test_repo", custom_bin), exist_ok=True)
        mock_move.assert_called_once_with('/test_repo/old_file.txt', os.path.join("/test_repo", custom_bin, 'old_file.txt'))
        self.assertEqual(result["dust_bin_name"], custom_bin)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.rmdir')
    def test_dust_bin_not_removed_if_empty(self, mock_rmdir, mock_move, mock_makedirs, mock_isdir, mock_exists, mock_listdir, mock_getmtime, mock_walk):
        # Mock rationale: Ensure the dust bin itself is not considered an empty directory for removal.

        mock_walk.return_value = [
            ('/test_repo', ['sub1', '.cosmic-dust-bin'], []),
            ('/test_repo/sub1', [], []),
            ('/test_repo/.cosmic-dust-bin', [], []),
        ]
        mock_getmtime.return_value = self.fixed_current_time # No stale files
        mock_listdir.side_effect = lambda p: [] if p == '/test_repo/sub1' or p == '/test_repo/.cosmic-dust-bin' else ['some_file']

        result = collect_dust("/test_repo", age_days=self.age_days, dry_run=False)

        self.assertEqual(result["empty_dirs_found"], 1) # Only sub1 should be found as empty
        self.assertIn('/test_repo/sub1', result["empty_dirs_list"])
        self.assertNotIn('/test_repo/.cosmic-dust-bin', result["empty_dirs_list"])
        mock_rmdir.assert_called_once_with('/test_repo/sub1')


if __name__ == '__main__':
    unittest.main()
