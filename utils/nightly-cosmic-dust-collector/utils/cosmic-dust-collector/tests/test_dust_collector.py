import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta
import re

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import find_dust_files, main
sys.path.pop(0)

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing of file ages
        self.base_time = datetime(2023, 1, 1, 12, 0, 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print') # Mock print to capture output
    def test_find_dust_files_dry_run_no_patterns(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: os.walk simulates the file system traversal.
        # os.path.getmtime provides deterministic modification times for age filtering.
        # os.remove is mocked to prevent actual file deletion during tests.
        # builtins.print is mocked to capture console output for verification.

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['old_file.txt', 'new_file.txt']),
            ('/test_dir/subdir1', [], ['temp.log']),
            ('/test_dir/subdir2', [], ['another_old.dat'])
        ]

        # Define modification times for files
        file_mtimes = {
            '/test_dir/old_file.txt': (self.base_time - timedelta(days=40)).timestamp(),
            '/test_dir/new_file.txt': (self.base_time - timedelta(days=10)).timestamp(),
            '/test_dir/subdir1/temp.log': (self.base_time - timedelta(days=50)).timestamp(),
            '/test_dir/subdir2/another_old.dat': (self.base_time - timedelta(days=35)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        # Run the collector with default age (30 days) and no patterns (dry run)
        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=None, dry_run=True)

        # Assertions
        self.assertIn('/test_dir/old_file.txt', found_files)
        self.assertNotIn('/test_dir/new_file.txt', found_files)
        self.assertIn('/test_dir/subdir1/temp.log', found_files)
        self.assertIn('/test_dir/subdir2/another_old.dat', found_files)
        self.assertEqual(len(found_files), 3)
        mock_remove.assert_not_called() # Ensure no deletion in dry run
        # Check that the last print call indicates a dry run
        self.assertTrue(any("This was a dry run" in call.args[0] for call in mock_print.call_args_list))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_with_patterns(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Same as above, ensuring deterministic file system and preventing actual deletion.

        mock_walk.return_value = [
            ('/test_dir', [], ['report.log', 'data.csv', 'temp_file.txt']),
            ('/test_dir/cache', [], ['cache.tmp', 'important.txt'])
        ]

        file_mtimes = {
            '/test_dir/report.log': (self.base_time - timedelta(days=40)).timestamp(),
            '/test_dir/data.csv': (self.base_time - timedelta(days=10)).timestamp(),
            '/test_dir/temp_file.txt': (self.base_time - timedelta(days=50)).timestamp(),
            '/test_dir/cache/cache.tmp': (self.base_time - timedelta(days=60)).timestamp(),
            '/test_dir/cache/important.txt': (self.base_time - timedelta(days=70)).timestamp(), # Old but not matching pattern
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        # Look for .log and .tmp files older than 30 days
        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=['*.log', '*.tmp', 'temp_*'], dry_run=True)

        self.assertIn('/test_dir/report.log', found_files)
        self.assertIn('/test_dir/temp_file.txt', found_files)
        self.assertIn('/test_dir/cache/cache.tmp', found_files)
        self.assertNotIn('/test_dir/data.csv', found_files) # Not old enough
        self.assertNotIn('/test_dir/cache/important.txt', found_files) # Not matching pattern
        self.assertEqual(len(found_files), 3)
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_delete_mode(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Same as above, ensuring deterministic file system and preventing actual deletion.

        mock_walk.return_value = [
            ('/test_dir', [], ['to_delete.txt', 'keep.txt'])
        ]

        file_mtimes = {
            '/test_dir/to_delete.txt': (self.base_time - timedelta(days=40)).timestamp(),
            '/test_dir/keep.txt': (self.base_time - timedelta(days=10)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=None, dry_run=False)

        self.assertIn('/test_dir/to_delete.txt', found_files)
        self.assertEqual(len(found_files), 1)
        mock_remove.assert_called_once_with('/test_dir/to_delete.txt') # Ensure deletion is called
        self.assertTrue(any("Initiating cosmic dust removal..." in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("Cosmic dust removal complete." in call.args[0] for call in mock_print.call_args_list))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_no_dust_found(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Same as above, ensuring deterministic file system and preventing actual deletion.

        mock_walk.return_value = [
            ('/test_dir', [], ['recent.txt', 'other.csv'])
        ]

        file_mtimes = {
            '/test_dir/recent.txt': (self.base_time - timedelta(days=5)).timestamp(),
            '/test_dir/other.csv': (self.base_time - timedelta(days=15)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=None, dry_run=True)

        self.assertEqual(len(found_files), 0)
        mock_remove.assert_not_called()
        self.assertTrue(any("No cosmic dust found. Your repository is sparkling clean!" in call.args[0] for call in mock_print.call_args_list))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_os_error_on_getmtime(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Simulates a file system error when trying to access file metadata.

        mock_walk.return_value = [
            ('/test_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]

        file_mtimes = {
            '/test_dir/accessible.txt': (self.base_time - timedelta(days=40)).timestamp(),
        }
        # Simulate OSError for 'inaccessible.txt'
        def getmtime_side_effect(path):
            if path == '/test_dir/inaccessible.txt':
                raise OSError("Permission denied")
            return file_mtimes.get(path, self.base_time.timestamp())

        mock_getmtime.side_effect = getmtime_side_effect

        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=None, dry_run=True)

        self.assertIn('/test_dir/accessible.txt', found_files)
        self.assertEqual(len(found_files), 1)
        self.assertTrue(any(re.search(r"Warning: Could not access '/test_dir/inaccessible.txt'", call.args[0]) for call in mock_print.call_args_list))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_dry_run(self, mock_parse_args, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # Other mocks are for file system operations as before.

        mock_parse_args.return_value = MagicMock(
            path='/mock_repo',
            age=10,
            patterns=['*.log'],
            delete=False
        )

        mock_walk.return_value = [
            ('/mock_repo', [], ['old.log', 'new.txt'])
        ]
        file_mtimes = {
            '/mock_repo/old.log': (self.base_time - timedelta(days=15)).timestamp(),
            '/mock_repo/new.txt': (self.base_time - timedelta(days=5)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        main()

        self.assertTrue(any("This was a dry run" in call.args[0] for call in mock_print.call_args_list))
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_delete_mode(self, mock_parse_args, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Same as above, controlling CLI arguments and file system operations.

        mock_parse_args.return_value = MagicMock(
            path='/mock_repo',
            age=10,
            patterns=['*.tmp'],
            delete=True
        )

        mock_walk.return_value = [
            ('/mock_repo', [], ['temp.tmp', 'keep.txt'])
        ]
        file_mtimes = {
            '/mock_repo/temp.tmp': (self.base_time - timedelta(days=15)).timestamp(),
            '/mock_repo/keep.txt': (self.base_time - timedelta(days=5)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        main()

        mock_remove.assert_called_once_with('/mock_repo/temp.tmp')
        self.assertTrue(any("Initiating cosmic dust removal..." in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("Cosmic dust removal complete." in call.args[0] for call in mock_print.call_args_list))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_pattern_match_dir_name(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Test if directory names matching patterns are also considered.

        mock_walk.return_value = [
            ('/test_dir', ['__pycache__'], ['file_in_root.txt']),
            ('/test_dir/__pycache__', [], ['compiled.pyc', 'another.tmp'])
        ]

        file_mtimes = {
            '/test_dir/file_in_root.txt': (self.base_time - timedelta(days=10)).timestamp(),
            '/test_dir/__pycache__/compiled.pyc': (self.base_time - timedelta(days=40)).timestamp(),
            '/test_dir/__pycache__/another.tmp': (self.base_time - timedelta(days=50)).timestamp(),
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        # Look for '__pycache__' directories and their contents, older than 30 days
        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=['__pycache__'], dry_run=True)

        self.assertIn('/test_dir/__pycache__/compiled.pyc', found_files)
        self.assertIn('/test_dir/__pycache__/another.tmp', found_files)
        self.assertEqual(len(found_files), 2)
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_find_dust_files_pattern_match_dir_name_and_file_name(self, mock_print, mock_remove, mock_getmtime, mock_walk):
        # Mock rationale: Test if both directory and file name patterns work together.

        mock_walk.return_value = [
            ('/test_dir', ['temp_data'], ['old_log.log']),
            ('/test_dir/temp_data', [], ['data.csv', 'temp_file.txt'])
        ]

        file_mtimes = {
            '/test_dir/old_log.log': (self.base_time - timedelta(days=40)).timestamp(),
            '/test_dir/temp_data/data.csv': (self.base_time - timedelta(days=50)).timestamp(),
            '/test_dir/temp_data/temp_file.txt': (self.base_time - timedelta(days=10)).timestamp(), # Not old enough
        }
        mock_getmtime.side_effect = lambda f: file_mtimes.get(f, self.base_time.timestamp())

        # Look for '*.log' files OR files in 'temp_*' directories, older than 30 days
        found_files = find_dust_files(root_dir='/test_dir', min_age_days=30, patterns=['*.log', 'temp_*'], dry_run=True)

        self.assertIn('/test_dir/old_log.log', found_files)
        self.assertIn('/test_dir/temp_data/data.csv', found_files)
        self.assertNotIn('/test_dir/temp_data/temp_file.txt', found_files) # Directory matches, but file not old enough
        self.assertEqual(len(found_files), 2)
        mock_remove.assert_not_called()


if __name__ == '__main__':
    unittest.main()
