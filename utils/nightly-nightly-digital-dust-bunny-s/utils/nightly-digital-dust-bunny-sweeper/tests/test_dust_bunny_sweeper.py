import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing dust_bunny_sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_bunny_sweeper

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Mock datetime.now() for consistent age calculations
        self.mock_now = datetime(2023, 10, 27, 10, 0, 0)
        self.patcher_datetime_now = patch('dust_bunny_sweeper.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original
        self.mock_datetime.timedelta = timedelta # Keep original

        # Mock os.path.getmtime for consistent file modification times
        self.mock_mtime_map = {
            '/mock/project/file_old.txt': (self.mock_now - timedelta(days=31)).timestamp(),
            '/mock/project/file_recent.txt': (self.mock_now - timedelta(days=5)).timestamp(),
            '/mock/project/sub/file_old_sub.txt': (self.mock_now - timedelta(days=40)).timestamp(),
            '/mock/project/sub/file_recent_sub.txt': (self.mock_now - timedelta(days=10)).timestamp(),
            '/mock/project/__pycache__/cache_file.pyc': (self.mock_now - timedelta(days=1)).timestamp(),
            '/mock/project/.DS_Store': (self.mock_now - timedelta(days=2)).timestamp(),
            '/mock/project/empty_dir': (self.mock_now - timedelta(days=1)).timestamp(), # mtime for empty dir itself
            '/mock/project/another_empty_dir': (self.mock_now - timedelta(days=1)).timestamp(),
            '/mock/project/logs/app.log': (self.mock_now - timedelta(days=8)).timestamp(),
            '/mock/project/logs/debug.log': (self.mock_now - timedelta(days=2)).timestamp(),
            '/mock/project/logs/old_error.log': (self.mock_now - timedelta(days=100)).timestamp(),
        }
        self.patcher_getmtime = patch('os.path.getmtime', side_effect=lambda p: self.mock_mtime_map.get(p, time.time()))
        self.mock_getmtime = self.patcher_getmtime.start()

        # Mock os.path.isdir and os.path.isfile
        self.mock_fs_structure = {
            '/mock/project': True,
            '/mock/project/file_old.txt': False,
            '/mock/project/file_recent.txt': False,
            '/mock/project/__pycache__': True,
            '/mock/project/__pycache__/cache_file.pyc': False,
            '/mock/project/.DS_Store': False,
            '/mock/project/sub': True,
            '/mock/project/sub/file_old_sub.txt': False,
            '/mock/project/sub/file_recent_sub.txt': False,
            '/mock/project/empty_dir': True,
            '/mock/project/another_empty_dir': True,
            '/mock/project/logs': True,
            '/mock/project/logs/app.log': False,
            '/mock/project/logs/debug.log': False,
            '/mock/project/logs/old_error.log': False,
        }
        self.patcher_isdir = patch('os.path.isdir', side_effect=lambda p: self.mock_fs_structure.get(p, False))
        self.mock_isdir = self.patcher_isdir.start()
        self.patcher_isfile = patch('os.path.isfile', side_effect=lambda p: not self.mock_fs_structure.get(p, True))
        self.mock_isfile = self.patcher_isfile.start()
        self.patcher_islink = patch('os.path.islink', return_value=False)
        self.mock_islink = self.patcher_islink.start()

        # Mock os.listdir for empty directory checks
        self.mock_listdir_map = {
            '/mock/project': ['file_old.txt', 'file_recent.txt', '__pycache__', '.DS_Store', 'sub', 'empty_dir', 'another_empty_dir', 'logs'],
            '/mock/project/__pycache__': ['cache_file.pyc'],
            '/mock/project/sub': ['file_old_sub.txt', 'file_recent_sub.txt'],
            '/mock/project/empty_dir': [],
            '/mock/project/another_empty_dir': [],
            '/mock/project/logs': ['app.log', 'debug.log', 'old_error.log'],
        }
        self.patcher_listdir = patch('os.listdir', side_effect=lambda p: self.mock_listdir_map.get(p, []))
        self.mock_listdir = self.patcher_listdir.start()

        # Mock os.walk to simulate directory traversal
        self.mock_walk_data = [
            ('/mock/project', ['__pycache__', 'sub', 'empty_dir', 'another_empty_dir', 'logs'], ['file_old.txt', 'file_recent.txt', '.DS_Store']),
            ('/mock/project/__pycache__', [], ['cache_file.pyc']),
            ('/mock/project/sub', [], ['file_old_sub.txt', 'file_recent_sub.txt']),
            ('/mock/project/empty_dir', [], []),
            ('/mock/project/another_empty_dir', [], []),
            ('/mock/project/logs', [], ['app.log', 'debug.log', 'old_error.log']),
        ]
        self.patcher_walk = patch('os.walk', return_value=self.mock_walk_data)
        self.mock_walk = self.patcher_walk.start()

        # Mock deletion functions
        self.patcher_remove = patch('os.remove')
        self.mock_remove = self.patcher_remove.start()
        self.patcher_rmtree = patch('shutil.rmtree')
        self.mock_rmtree = self.patcher_rmtree.start()

        # Capture print output
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.patcher_getmtime.stop()
        self.patcher_isdir.stop()
        self.patcher_isfile.stop()
        self.patcher_islink.stop()
        self.patcher_listdir.stop()
        self.patcher_walk.stop()
        self.patcher_remove.stop()
        self.patcher_rmtree.stop()
        self.patcher_print.stop()
        sys.path.pop(0)

    def test_find_dust_bunnies_patterns_only(self):
        # Mock rationale: Simulate a file system with __pycache__ and .DS_Store files.
        # datetime.now, os.path.getmtime, os.path.isdir, os.path.isfile, os.listdir, os.walk are mocked
        # to provide a consistent virtual file system state for deterministic testing.
        root = '/mock/project'
        patterns = ['__pycache__', '.DS_Store']
        max_age_days = 0

        found = dust_bunny_sweeper.find_dust_bunnies(root, patterns, max_age_days)
        expected = [
            '/mock/project/.DS_Store',
            '/mock/project/__pycache__'
        ]
        self.assertListEqual(found, expected)

    def test_find_dust_bunnies_max_age_only(self):
        # Mock rationale: Simulate files with different modification times.
        # datetime.now, os.path.getmtime, os.path.isdir, os.path.isfile, os.listdir, os.walk are mocked
        # to provide a consistent virtual file system state and time for deterministic age-based testing.
        root = '/mock/project'
        patterns = []
        max_age_days = 30

        found = dust_bunny_sweeper.find_dust_bunnies(root, patterns, max_age_days)
        expected = [
            '/mock/project/file_old.txt',
            '/mock/project/logs/old_error.log',
            '/mock/project/sub/file_old_sub.txt'
        ]
        self.assertListEqual(found, expected)

    def test_find_dust_bunnies_patterns_and_max_age(self):
        # Mock rationale: Combine pattern matching and age-based filtering.
        # datetime.now, os.path.getmtime, os.path.isdir, os.path.isfile, os.listdir, os.walk are mocked
        # to provide a consistent virtual file system state and time for deterministic testing.
        root = '/mock/project'
        patterns = ['__pycache__', '.DS_Store', '*.log']
        max_age_days = 7

        found = dust_bunny_sweeper.find_dust_bunnies(root, patterns, max_age_days)
        expected = [
            '/mock/project/.DS_Store',
            '/mock/project/__pycache__',
            '/mock/project/file_old.txt',
            '/mock/project/logs/app.log', # Matches *.log and is older than 7 days
            '/mock/project/logs/old_error.log', # Matches *.log and is older than 7 days
            '/mock/project/sub/file_old_sub.txt'
        ]
        self.assertListEqual(found, expected)

    def test_find_dust_bunnies_empty_dirs(self):
        # Mock rationale: Simulate directories that are empty.
        # os.listdir is mocked to return empty lists for specific directories.
        # os.walk is mocked to traverse these directories.
        root = '/mock/project'
        patterns = []
        max_age_days = 0

        found = dust_bunny_sweeper.find_dust_bunnies(root, patterns, max_age_days)
        expected = [
            '/mock/project/another_empty_dir',
            '/mock/project/empty_dir'
        ]
        self.assertListEqual(found, expected)

    def test_find_dust_bunnies_non_existent_path(self):
        # Mock rationale: Test error handling for invalid root paths.
        # os.path.isdir is mocked to return False for the non-existent path.
        root = '/non/existent/path'
        patterns = []
        max_age_days = 0

        self.mock_isdir.side_effect = lambda p: p == '/mock/project'

        found = dust_bunny_sweeper.find_dust_bunnies(root, patterns, max_age_days)
        self.assertListEqual(found, [])
        self.mock_print.assert_called_with(f"Error: Path '{root}' is not a valid directory.")

    def test_clean_dust_bunnies_dry_run(self):
        # Mock rationale: Verify that deletion functions are NOT called in dry-run mode.
        # os.remove and shutil.rmtree are mocked to track calls without actual file system changes.
        dust_bunnies = [
            '/mock/project/.DS_Store',
            '/mock/project/__pycache__',
            '/mock/project/file_old.txt'
        ]
        self.mock_isdir.side_effect = lambda p: p == '/mock/project/__pycache__'

        dust_bunny_sweeper.clean_dust_bunnies(dust_bunnies, dry_run=True)

        self.mock_remove.assert_not_called()
        self.mock_rmtree.assert_not_called()
        self.mock_print.assert_any_call("\nWould delete (dry run) 3 items:")
        self.mock_print.assert_any_call("  [DRY RUN] /mock/project/.DS_Store")
        self.mock_print.assert_any_call("  [DRY RUN] /mock/project/__pycache__")
        self.mock_print.assert_any_call("  [DRY RUN] /mock/project/file_old.txt")
        self.mock_print.assert_any_call("\nDry run complete. Use --delete to perform actual deletion.")

    def test_clean_dust_bunnies_actual_delete(self):
        # Mock rationale: Verify that deletion functions ARE called in actual delete mode.
        # os.remove and shutil.rmtree are mocked to track calls without actual file system changes.
        dust_bunnies = [
            '/mock/project/.DS_Store',
            '/mock/project/__pycache__',
            '/mock/project/file_old.txt'
        ]
        # Configure mock_isdir to return True for the directory and False for files
        self.mock_isdir.side_effect = lambda p: p == '/mock/project/__pycache__'

        dust_bunny_sweeper.clean_dust_bunnies(dust_bunnies, dry_run=False)

        self.mock_remove.assert_called_once_with('/mock/project/.DS_Store')
        self.mock_remove.assert_called_once_with('/mock/project/file_old.txt')
        self.mock_rmtree.assert_called_once_with('/mock/project/__pycache__')
        self.mock_print.assert_any_call("\nDeleting 3 items:")
        self.mock_print.assert_any_call("\nCleanup complete.")

    def test_clean_dust_bunnies_no_items(self):
        # Mock rationale: Verify behavior when no items are found for deletion.
        # No deletion functions should be called, and a specific message should be printed.
        dust_bunny_sweeper.clean_dust_bunnies([], dry_run=True)
        self.mock_print.assert_called_once_with("No dust bunnies found to clean.")
        self.mock_remove.assert_not_called()
        self.mock_rmtree.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_dry_run_default_patterns(self, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and capture output.
        # argparse.ArgumentParser.parse_args is mocked to control CLI input.
        # sys.stdout is mocked to capture printed output for verification.
        # find_dust_bunnies and clean_dust_bunnies are called internally, and their mocks handle the logic.
        mock_parse_args.return_value = MagicMock(
            path='/mock/project',
            delete=False,
            patterns=['__pycache__', '.DS_Store'],
            max_age_days=0,
            verbose=False
        )

        # Re-mock os.walk for main test to ensure it's fresh after other tests
        with patch('os.walk', return_value=self.mock_walk_data):
            dust_bunny_sweeper.main()

        self.mock_print.assert_any_call("Scanning '/mock/project' for dust bunnies...")
        self.mock_print.assert_any_call("\nWould delete (dry run) 2 items:")
        self.mock_print.assert_any_call("  [DRY RUN] /mock/project/.DS_Store")
        self.mock_print.assert_any_call("  [DRY RUN] /mock/project/__pycache__")
        self.mock_print.assert_any_call("\nDry run complete. Use --delete to perform actual deletion.")
        self.mock_remove.assert_not_called()
        self.mock_rmtree.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_delete_old_files(self, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments for deleting old files.
        # argparse.ArgumentParser.parse_args is mocked to control CLI input.
        # sys.stdout is mocked to capture printed output for verification.
        # find_dust_bunnies and clean_dust_bunnies are called internally, and their mocks handle the logic.
        mock_parse_args.return_value = MagicMock(
            path='/mock/project',
            delete=True,
            patterns=[], # No patterns, only age-based
            max_age_days=30,
            verbose=False
        )

        # Re-mock os.walk for main test to ensure it's fresh after other tests
        with patch('os.walk', return_value=self.mock_walk_data):
            dust_bunny_sweeper.main()

        self.mock_print.assert_any_call("Scanning '/mock/project' for dust bunnies...")
        self.mock_print.assert_any_call("\nDeleting 3 items:")
        self.mock_remove.assert_any_call('/mock/project/file_old.txt')
        self.mock_remove.assert_any_call('/mock/project/logs/old_error.log')
        self.mock_remove.assert_any_call('/mock/project/sub/file_old_sub.txt')
        self.mock_rmtree.assert_not_called() # No directories should be deleted with this config
        self.mock_print.assert_any_call("\nCleanup complete.")

if __name__ == '__main__':
    unittest.main()
