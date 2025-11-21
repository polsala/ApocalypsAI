import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import shutil

# Import the function to be tested
from src.dust_collector import collect_dust

class TestDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_no_directory(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Simulate a non-existent directory to test error handling.
        mock_isdir.return_value = False
        mock_exists.return_value = False # For archive_dir check, though isdir will short-circuit
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        result = collect_dust("/nonexistent/path", 30, ["log"])
        self.assertEqual(result, [])
        mock_isdir.assert_called_once_with("/nonexistent/path")
        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_no_files_to_collect(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Simulate a directory with files, but none match criteria (extension or age).
        mock_isdir.return_value = True
        mock_exists.side_effect = lambda path: path == "/test_dir" # /test_dir/archive should not exist initially
        mock_makedirs.return_value = None
        mock_move.return_value = None

        # Simulate current time
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        # Simulate os.walk returning files, but none matching extensions or being old enough
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['file1.txt', 'recent.log']),
            ('/test_dir/subdir', [], ['another.csv'])
        ]

        # Simulate modification times (all recent or wrong extension)
        mock_getmtime.side_effect = {
            '/test_dir/file1.txt': datetime.datetime(2022, 12, 25, 10, 0, 0).timestamp(), # Not .log
            '/test_dir/recent.log': datetime.datetime(2022, 12, 30, 10, 0, 0).timestamp(), # Not old enough (age=30 days)
            '/test_dir/subdir/another.csv': datetime.datetime(2022, 12, 20, 10, 0, 0).timestamp() # Not .log
        }.get

        result = collect_dust("/test_dir", 30, ["log"])
        self.assertEqual(result, [])
        mock_makedirs.assert_called_once_with("/test_dir/archive") # Archive dir is created even if no files moved
        mock_move.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_files_are_collected(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Simulate a directory with old files matching criteria to test successful archiving.
        mock_isdir.return_value = True
        # Simulate only /test_dir existing initially, so archive_dir and its subdirs are created.
        mock_exists.side_effect = lambda path: path == "/test_dir"
        mock_makedirs.return_value = None
        mock_move.return_value = None

        # Simulate current time: Jan 1, 2023
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        # Simulate os.walk returning files
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old.log', 'recent.txt']),
            ('/test_dir/subdir', [], ['another_old.log', 'current.tmp'])
        ]

        # Simulate modification times
        # old.log: modified Nov 15, 2022 (older than 30 days from Jan 1, 2023)
        # recent.txt: modified Dec 20, 2022 (not .log, not old enough for 30 days)
        # another_old.log: modified Oct 1, 2022 (older than 30 days)
        # current.tmp: modified Dec 25, 2022 (not old enough for 30 days)
        mock_getmtime.side_effect = {
            '/test_dir/old.log': datetime.datetime(2022, 11, 15, 10, 0, 0).timestamp(),
            '/test_dir/recent.txt': datetime.datetime(2022, 12, 20, 10, 0, 0).timestamp(),
            '/test_dir/subdir/another_old.log': datetime.datetime(2022, 10, 1, 10, 0, 0).timestamp(),
            '/test_dir/subdir/current.tmp': datetime.datetime(2022, 12, 25, 10, 0, 0).timestamp()
        }.get

        result = collect_dust("/test_dir", 30, ["log"])

        expected_moved = [
            '/test_dir/old.log',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(result, expected_moved)

        # Check calls to shutil.move
        mock_move.assert_any_call('/test_dir/old.log', '/test_dir/archive/old.log')
        mock_move.assert_any_call('/test_dir/subdir/another_old.log', '/test_dir/archive/subdir/another_old.log')
        self.assertEqual(mock_move.call_count, 2)

        # Check calls to os.makedirs for archive subdirectories
        mock_makedirs.assert_any_call('/test_dir/archive')
        mock_makedirs.assert_any_call('/test_dir/archive/subdir')
        self.assertEqual(mock_makedirs.call_count, 2)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_dry_run_mode(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Test that in dry-run mode, files are identified but not actually moved or directories created.
        mock_isdir.return_value = True
        mock_exists.side_effect = lambda path: path == "/test_dir" # archive_dir and archive_subdir should not exist initially
        mock_makedirs.return_value = None
        mock_move.return_value = None

        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old.log']),
            ('/test_dir/subdir', [], ['another_old.log'])
        ]

        mock_getmtime.side_effect = {
            '/test_dir/old.log': datetime.datetime(2022, 11, 15, 10, 0, 0).timestamp(),
            '/test_dir/subdir/another_old.log': datetime.datetime(2022, 10, 1, 10, 0, 0).timestamp()
        }.get

        result = collect_dust("/test_dir", 30, ["log"], dry_run=True)

        expected_moved = [
            '/test_dir/old.log',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(result, expected_moved)

        mock_makedirs.assert_not_called() # Should not create directories in dry-run
        mock_move.assert_not_called() # Should not move files in dry-run

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_archive_dir_already_exists(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Test scenario where the archive directory already exists, ensuring no redundant creation.
        mock_isdir.return_value = True
        # Simulate /test_dir and /test_dir/archive existing, but /test_dir/archive/subdir does not initially
        mock_exists.side_effect = lambda path: path in ["/test_dir", "/test_dir/archive"]
        mock_makedirs.return_value = None
        mock_move.return_value = None

        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old.log']),
            ('/test_dir/subdir', [], ['another_old.log'])
        ]

        mock_getmtime.side_effect = {
            '/test_dir/old.log': datetime.datetime(2022, 11, 15, 10, 0, 0).timestamp(),
            '/test_dir/subdir/another_old.log': datetime.datetime(2022, 10, 1, 10, 0, 0).timestamp()
        }.get

        result = collect_dust("/test_dir", 30, ["log"])

        expected_moved = [
            '/test_dir/old.log',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(result, expected_moved)

        # os.makedirs should be called only for '/test_dir/archive/subdir', not for '/test_dir/archive'
        mock_makedirs.assert_called_once_with('/test_dir/archive/subdir')
        mock_move.assert_called()

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_skip_archive_directory_itself(self, mock_datetime, mock_getmtime, mock_walk, mock_move, mock_makedirs, mock_exists, mock_isdir):
        # Mock rationale: Ensure the collector does not attempt to archive files already within the archive directory.
        mock_isdir.return_value = True
        mock_exists.side_effect = lambda path: path in ["/test_dir", "/test_dir/archive"]
        mock_makedirs.return_value = None
        mock_move.return_value = None

        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)

        mock_walk.return_value = [
            ('/test_dir', ['archive'], ['old.log']),
            ('/test_dir/archive', [], ['already_archived.log']) # This file should be skipped
        ]

        mock_getmtime.side_effect = {
            '/test_dir/old.log': datetime.datetime(2022, 11, 15, 10, 0, 0).timestamp(),
            '/test_dir/archive/already_archived.log': datetime.datetime(2022, 10, 1, 10, 0, 0).timestamp()
        }.get

        result = collect_dust("/test_dir", 30, ["log"])

        expected_moved = [
            '/test_dir/old.log'
        ]
        self.assertCountEqual(result, expected_moved)

        mock_move.assert_called_once_with('/test_dir/old.log', '/test_dir/archive/old.log')
        mock_makedirs.assert_not_called() # archive dir already exists, no subdirs needed for this test
