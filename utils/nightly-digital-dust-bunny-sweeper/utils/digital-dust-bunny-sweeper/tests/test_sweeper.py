import unittest
import os
import sys
import time
from unittest.mock import patch, MagicMock
from io import StringIO
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        self.mock_stdout = StringIO()
        self.mock_stderr = StringIO()
        self.patcher_stdout = patch('sys.stdout', new=self.mock_stdout)
        self.patcher_stderr = patch('sys.stderr', new=self.mock_stderr)
        self.patcher_stdout.start()
        self.patcher_stderr.start()

    def tearDown(self):
        self.patcher_stdout.stop()
        self.patcher_stderr.stop()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir', side_effect=lambda x: [] if 'empty' in x else ['file'])
    def test_find_dust_bunnies_no_bunnies(self, mock_listdir, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a clean directory structure without actual file system interaction.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo', ['dir1', 'dir2'], ['file.txt']),
            ('/repo/dir1', [], ['another.py']),
            ('/repo/dir2', [], ['data.json']),
        ]
        # Mock rationale: Ensure no files are considered 'old' by returning a very recent modification time.
        mock_getmtime.return_value = time.time() - (5 * 24 * 60 * 60) # 5 days old

        empty_dirs, old_files = sweeper.find_dust_bunnies('/repo', min_age_days=10)
        self.assertEqual(empty_dirs, [])
        self.assertEqual(old_files, [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir', side_effect=lambda x: [] if 'empty_dir' in x else ['file'])
    def test_find_dust_bunnies_empty_dirs(self, mock_listdir, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directories that are truly empty.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo/empty_dir1', [], []), # This will be detected as empty
            ('/repo/empty_dir2', [], []), # This will be detected as empty
            ('/repo', ['empty_dir1', 'empty_dir2', 'full_dir'], ['file.txt']),
            ('/repo/full_dir', [], ['important.log']), # Not empty, but has a log file
        ]
        # Mock rationale: Ensure no files are considered 'old' for this specific test.
        mock_getmtime.return_value = time.time() - (5 * 24 * 60 * 60)

        empty_dirs, old_files = sweeper.find_dust_bunnies('/repo', min_age_days=10)
        self.assertIn('/repo/empty_dir1', empty_dirs)
        self.assertIn('/repo/empty_dir2', empty_dirs)
        self.assertEqual(len(empty_dirs), 2)
        self.assertEqual(old_files, [])

    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.listdir', return_value=['file'])
    def test_find_dust_bunnies_old_files(self, mock_listdir, mock_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a directory with old log/temp files.
        mock_isdir.return_value = True
        # Simulate current time for age calculation
        current_time = time.time()
        # Old file (older than 30 days)
        old_mtime = current_time - (35 * 24 * 60 * 60) 
        # Recent file (younger than 30 days)
        recent_mtime = current_time - (10 * 24 * 60 * 60)

        def mock_getmtime_side_effect(path):
            if 'old_error.log' in path: return old_mtime
            if 'recent.log' in path: return recent_mtime
            if 'temp.tmp' in path: return old_mtime
            if 'backup.bak' in path: return old_mtime
            if 'ignored.txt' in path: return old_mtime # Should be ignored due to extension
            return recent_mtime # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            ('/repo', [], ['old_error.log', 'recent.log', 'ignored.txt']),
            ('/repo/sub', [], ['temp.tmp', 'backup.bak']),
        ]

        empty_dirs, old_files = sweeper.find_dust_bunnies('/repo', min_age_days=30)
        self.assertEqual(empty_dirs, [])
        self.assertIn('/repo/old_error.log', old_files)
        self.assertIn('/repo/sub/temp.tmp', old_files)
        self.assertIn('/repo/sub/backup.bak', old_files)
        self.assertNotIn('/repo/recent.log', old_files) # Should not be in list
        self.assertNotIn('/repo/ignored.txt', old_files) # Should not be in list
        self.assertEqual(len(old_files), 3)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir', return_value=['file'])
    def test_find_dust_bunnies_invalid_path(self, mock_listdir, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an invalid root path.
        mock_isdir.return_value = False

        empty_dirs, old_files = sweeper.find_dust_bunnies('/nonexistent', min_age_days=30)
        self.assertEqual(empty_dirs, [])
        self.assertEqual(old_files, [])
        self.assertIn("Error: Path '/nonexistent' is not a valid directory.", self.mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', side_effect=lambda x: [] if 'empty_dir' in x else ['file'])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_mode(self, mock_parse_args, mock_listdir, mock_rmdir, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate the main execution path with deletion enabled.
        # Configure argparse to simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(path='/repo', age=30, delete=True)

        # Simulate current time for age calculation
        current_time = time.time()
        old_mtime = current_time - (35 * 24 * 60 * 60) # 35 days old

        def mock_getmtime_side_effect(path):
            if 'old_error.log' in path: return old_mtime
            if 'temp.tmp' in path: return old_mtime
            return current_time # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            ('/repo/empty_dir', [], []), # Empty directory
            ('/repo/sub_dir', [], ['temp.tmp']),
            ('/repo', ['empty_dir', 'sub_dir'], ['old_error.log', 'keep.txt']),
        ]

        sweeper.main()

        # Assertions for deletion calls
        mock_remove.assert_any_call('/repo/old_error.log')
        mock_remove.assert_any_call('/repo/sub_dir/temp.tmp')
        self.assertEqual(mock_remove.call_count, 2)

        mock_rmdir.assert_called_once_with('/repo/empty_dir')

        output = self.mock_stdout.getvalue()
        self.assertIn("Deleting identified dust bunnies...", output)
        self.assertIn("Removed file: /repo/old_error.log", output)
        self.assertIn("Removed file: /repo/sub_dir/temp.tmp", output)
        self.assertIn("Removed empty directory: /repo/empty_dir", output)
        self.assertIn("Sweep complete! 3 dust bunnies banished.", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', side_effect=lambda x: [] if 'empty_dir' in x else ['file'])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run_mode(self, mock_parse_args, mock_listdir, mock_rmdir, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate the main execution path with dry-run (default) enabled.
        mock_parse_args.return_value = MagicMock(path='/repo', age=30, delete=False)

        current_time = time.time()
        old_mtime = current_time - (35 * 24 * 60 * 60)

        def mock_getmtime_side_effect(path):
            if 'old_error.log' in path: return old_mtime
            if 'temp.tmp' in path: return old_mtime
            return current_time

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            ('/repo/empty_dir', [], []),
            ('/repo/sub_dir', [], ['temp.tmp']),
            ('/repo', ['empty_dir', 'sub_dir'], ['old_error.log', 'keep.txt']),
        ]

        sweeper.main()

        # Assertions for no deletion calls
        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()

        output = self.mock_stdout.getvalue()
        self.assertIn("Identified Digital Dust Bunnies", output)
        self.assertIn("Empty Directories:", output)
        self.assertIn("  - /repo/empty_dir", output)
        self.assertIn("Old Temporary/Log Files:", output)
        self.assertIn("  - /repo/old_error.log", output)
        self.assertIn("  - /repo/sub_dir/temp.tmp", output)
        self.assertIn("(Dry run complete. To delete these items, run with the '--delete' flag.)", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir', return_value=['file'])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_bunnies_found(self, mock_parse_args, mock_listdir, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a scenario where no dust bunnies are found.
        mock_parse_args.return_value = MagicMock(path='/repo', age=30, delete=False)

        mock_walk.return_value = [
            ('/repo', ['dir1'], ['file.txt']),
            ('/repo/dir1', [], ['another.py']),
        ]
        mock_getmtime.return_value = time.time() - (5 * 24 * 60 * 60) # 5 days old

        sweeper.main()

        output = self.mock_stdout.getvalue()
        self.assertIn("Your digital space is sparkling clean! No dust bunnies found.", output)
        self.assertNotIn("Identified Digital Dust Bunnies", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir', side_effect=lambda x: ['file'] if 'no_longer_empty' in x else [])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dir_no_longer_empty_during_deletion(self, mock_parse_args, mock_listdir, mock_rmdir, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory that was initially empty but has files after other deletions,
        # or was found empty but became non-empty before rmdir could be called.
        mock_parse_args.return_value = MagicMock(path='/repo', age=30, delete=True)

        current_time = time.time()
        old_mtime = current_time - (35 * 24 * 60 * 60)

        def mock_getmtime_side_effect(path):
            if 'old_file.log' in path: return old_mtime
            return current_time

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            ('/repo/no_longer_empty', [], []), # Initially empty
            ('/repo', ['no_longer_empty'], ['old_file.log']),
        ]

        # mock_listdir is configured to make '/repo/no_longer_empty' appear non-empty when rmdir is called.

        sweeper.main()

        mock_remove.assert_called_once_with('/repo/old_file.log')
        mock_rmdir.assert_not_called() # Should not be called because listdir will return ['file']

        output = self.mock_stdout.getvalue()
        self.assertIn("Removed file: /repo/old_file.log", output)
        self.assertIn("Directory /repo/no_longer_empty is no longer empty, skipping removal.", output)
        self.assertIn("Sweep complete! 1 dust bunnies banished.", output)
