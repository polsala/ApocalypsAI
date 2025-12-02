import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import shutil
from io import StringIO
import sys

# Import the function to be tested
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

        # Define a base time for consistent age calculations
        self.base_time = datetime.datetime(2023, 10, 26, 10, 0, 0)

        # Mock file system structure and modification times
        # Mock rationale: Simulate file system structure and modification times without actual disk I/O.
        # This allows deterministic testing of file identification and archiving logic.
        self.mock_files = {
            '/test_dir/old_log.log': (self.base_time - datetime.timedelta(days=40)).timestamp(),
            '/test_dir/recent_file.txt': (self.base_time - datetime.timedelta(days=5)).timestamp(),
            '/test_dir/temp_data.tmp': (self.base_time - datetime.timedelta(days=20)).timestamp(),
            '/test_dir/important.md': (self.base_time - datetime.timedelta(days=10)).timestamp(),
            '/test_dir/subdir/another_old.log': (self.base_time - datetime.timedelta(days=45)).timestamp(),
            '/test_dir/subdir/new_config.json': (self.base_time - datetime.timedelta(days=1)).timestamp(),
            '/test_dir/archive/already_archived.log': (self.base_time - datetime.timedelta(days=100)).timestamp(), # Should be ignored
        }

        # Mock os.walk to simulate directory traversal
        # Mock rationale: Control the directory structure and files encountered during traversal.
        self.mock_os_walk_return_value = [
            ('/test_dir', ['subdir', 'archive'], ['old_log.log', 'recent_file.txt', 'temp_data.tmp', 'important.md']),
            ('/test_dir/subdir', [], ['another_old.log', 'new_config.json']),
            ('/test_dir/archive', [], ['already_archived.log']) # Ensure archive dir is skipped
        ]

    def tearDown(self):
        sys.stdout = self.held_stdout # Restore stdout

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_collect_dust_dry_run_age_only(self, mock_datetime, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        # Mock rationale: Fix the current time for consistent age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: Simulate directory existence.
        mock_os_isdir.return_value = True
        mock_os_exists.side_effect = lambda p: p in ['/test_dir', '/test_dir/subdir', '/test_dir/archive']

        # Mock rationale: Simulate file existence.
        mock_os_isfile.side_effect = lambda p: p in self.mock_files

        # Mock rationale: Provide specific modification times for files.
        mock_os_getmtime.side_effect = lambda p: self.mock_files.get(p, 0)

        # Mock rationale: Control the directory structure and files encountered.
        mock_os_walk.return_value = self.mock_os_walk_return_value

        # Test with age_days = 30 (old_log.log, temp_data.tmp, another_old.log should be found)
        dust_files = collect_dust(target_dir='/test_dir', age_days=30, archive_mode=False, verbose=False)

        expected_files = [
            '/test_dir/old_log.log',
            '/test_dir/temp_data.tmp',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(dust_files, expected_files)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_collect_dust_dry_run_with_patterns(self, mock_datetime, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_os_isdir.return_value = True
        mock_os_exists.side_effect = lambda p: p in ['/test_dir', '/test_dir/subdir', '/test_dir/archive']
        mock_os_isfile.side_effect = lambda p: p in self.mock_files
        mock_os_getmtime.side_effect = lambda p: self.mock_files.get(p, 0)
        mock_os_walk.return_value = self.mock_os_walk_return_value

        # Test with age_days = 30 and patterns = ['*.log']
        dust_files = collect_dust(target_dir='/test_dir', age_days=30, patterns=['*.log'], archive_mode=False, verbose=False)

        expected_files = [
            '/test_dir/old_log.log',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(dust_files, expected_files)

        # Test with age_days = 15 and patterns = ['*.tmp']
        dust_files = collect_dust(target_dir='/test_dir', age_days=15, patterns=['*.tmp'], archive_mode=False, verbose=False)
        expected_files = [
            '/test_dir/temp_data.tmp'
        ]
        self.assertCountEqual(dust_files, expected_files)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('datetime.datetime')
    def test_collect_dust_archive_mode(self, mock_datetime, mock_shutil_move, mock_os_makedirs, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_os_isdir.return_value = True
        mock_os_exists.side_effect = lambda p: p in ['/test_dir', '/test_dir/subdir'] or p == '/test_dir/archive' # archive dir might not exist initially
        mock_os_isfile.side_effect = lambda p: p in self.mock_files
        mock_os_getmtime.side_effect = lambda p: self.mock_files.get(p, 0)
        mock_os_walk.return_value = self.mock_os_walk_return_value

        # Mock rationale: Prevent actual file system changes during archiving.
        mock_shutil_move.return_value = None
        mock_os_makedirs.return_value = None

        # Test with age_days = 30 and archive_mode = True
        dust_files = collect_dust(target_dir='/test_dir', age_days=30, archive_mode=True, verbose=False)

        expected_files = [
            '/test_dir/old_log.log',
            '/test_dir/temp_data.tmp',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(dust_files, expected_files)

        # Verify that shutil.move was called for each identified file
        self.assertEqual(mock_shutil_move.call_count, len(expected_files))
        mock_shutil_move.assert_any_call('/test_dir/old_log.log', '/test_dir/archive')
        mock_shutil_move.assert_any_call('/test_dir/temp_data.tmp', '/test_dir/archive')
        mock_shutil_move.assert_any_call('/test_dir/subdir/another_old.log', '/test_dir/archive')

        # Verify that os.makedirs was called for the archive directory
        mock_os_makedirs.assert_called_once_with('/test_dir/archive', exist_ok=True)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_collect_dust_no_dust_found(self, mock_datetime, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_os_isdir.return_value = True
        mock_os_exists.side_effect = lambda p: p in ['/test_dir', '/test_dir/subdir', '/test_dir/archive']
        mock_os_isfile.side_effect = lambda p: p in self.mock_files
        mock_os_getmtime.side_effect = lambda p: self.mock_files.get(p, 0)
        mock_os_walk.return_value = self.mock_os_walk_return_value

        # Set age_days very low so no files are considered old
        dust_files = collect_dust(target_dir='/test_dir', age_days=1, archive_mode=False, verbose=True)
        self.assertEqual(dust_files, [])
        self.assertIn("No cosmic dust found.", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_collect_dust_non_existent_directory(self, mock_datetime, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: Simulate a non-existent target directory.
        mock_os_isdir.return_value = False
        mock_os_exists.return_value = False

        dust_files = collect_dust(target_dir='/non_existent_dir', age_days=30, archive_mode=False, verbose=True)
        self.assertEqual(dust_files, [])
        self.assertIn("Error: Target directory '/non_existent_dir' does not exist or is not a directory.", self.mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_collect_dust_archive_dir_is_skipped(self, mock_datetime, mock_os_walk, mock_os_isfile, mock_os_getmtime, mock_os_exists, mock_os_isdir):
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_os_isdir.return_value = True
        mock_os_exists.side_effect = lambda p: p in ['/test_dir', '/test_dir/subdir', '/test_dir/archive']
        mock_os_isfile.side_effect = lambda p: p in self.mock_files
        mock_os_getmtime.side_effect = lambda p: self.mock_files.get(p, 0)
        mock_os_walk.return_value = self.mock_os_walk_return_value

        # Ensure that the file inside the mock archive directory is not processed
        dust_files = collect_dust(target_dir='/test_dir', age_days=30, archive_mode=False, verbose=False)

        # The already_archived.log should NOT be in the results, even if it's old
        self.assertNotIn('/test_dir/archive/already_archived.log', dust_files)
        expected_files = [
            '/test_dir/old_log.log',
            '/test_dir/temp_data.tmp',
            '/test_dir/subdir/another_old.log'
        ]
        self.assertCountEqual(dust_files, expected_files)

if __name__ == '__main__':
    unittest.main()
