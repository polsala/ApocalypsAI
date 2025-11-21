import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from datetime import datetime, timedelta

# Import the function to be tested
from src.cleaner import find_and_delete_old_debris

class TestDigitalDebrisDestroyer(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing of age
        self.base_time = datetime(2023, 1, 15, 12, 0, 0)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime') # Mock datetime to control 'now'
    def test_dry_run_finds_old_files_and_dirs(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original for conversion

        # Mock rationale: Simulate file system structure and modification times.
        # Files: old_log.log (31 days old), new_log.log (1 day old), temp_file.tmp (31 days old)
        # Dirs: old_cache/ (31 days old), new_build/ (1 day old)
        mock_walk.return_value = [
            ('/root', ['old_cache', 'new_build'], ['old_log.log', 'new_log.log']),
            ('/root/old_cache', [], ['nested_old.tmp']),
            ('/root/new_build', [], ['nested_new.tmp'])
        ]

        # Mock rationale: Provide specific modification times for files/dirs.
        # Use a dictionary to map paths to timestamps
        file_mtimes = {
            '/root/old_log.log': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_log.log': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/old_cache': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_build': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/old_cache/nested_old.tmp': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_build/nested_new.tmp': (self.base_time - timedelta(days=1)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        # Test with dry_run=True
        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['*.log', '__pycache__', 'old_cache', '*.tmp'],
            age_days=30,
            dry_run=True
        )

        # Assertions for dry run
        self.assertEqual(len(deleted), 0) # Nothing should be deleted in dry run
        self.assertEqual(len(skipped), 0)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()

        # Check if the correct items were identified
        expected_found_items = [
            '/root/old_log.log',
            '/root/old_cache/nested_old.tmp',
            '/root/old_cache'
        ]
        # The order might vary due to os.walk topdown=False and dictionary iteration
        # So we check for set equality
        mock_stdout = MagicMock()
        with patch('builtins.print', mock_stdout):
            find_and_delete_old_debris(
                root_path='/root',
                patterns=['*.log', '__pycache__', 'old_cache', '*.tmp'],
                age_days=30,
                dry_run=True
            )
            output_lines = [call.args[0] for call in mock_stdout.call_args_list if '[DRY RUN]' in call.args[0]]
            self.assertEqual(len(output_lines), len(expected_found_items))
            for item in expected_found_items:
                self.assertTrue(any(item in line for line in output_lines))

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime')
    def test_delete_mode_removes_old_files_and_dirs(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Mock rationale: Simulate file system structure and modification times.
        mock_walk.return_value = [
            ('/root', ['old_cache', 'new_build'], ['old_log.log', 'new_log.log']),
            ('/root/old_cache', [], ['nested_old.tmp']),
            ('/root/new_build', [], ['nested_new.tmp'])
        ]

        file_mtimes = {
            '/root/old_log.log': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_log.log': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/old_cache': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_build': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/old_cache/nested_old.tmp': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/new_build/nested_new.tmp': (self.base_time - timedelta(days=1)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        # Test with dry_run=False
        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['*.log', 'old_cache', '*.tmp'],
            age_days=30,
            dry_run=False
        )

        # Assertions for actual deletion
        expected_deleted_items = [
            '/root/old_log.log',
            '/root/old_cache/nested_old.tmp',
            '/root/old_cache'
        ]
        self.assertEqual(len(deleted), len(expected_deleted_items))
        self.assertEqual(len(skipped), 0)

        # Check if os.remove and shutil.rmtree were called for the correct items
        mock_remove.assert_any_call('/root/old_log.log')
        mock_remove.assert_any_call('/root/old_cache/nested_old.tmp')
        mock_rmtree.assert_any_call('/root/old_cache')

        # Ensure new files/dirs were not touched
        mock_remove.assert_called_once_with('/root/old_log.log') # Only old_log.log and nested_old.tmp should be removed directly
        mock_remove.assert_any_call('/root/old_cache/nested_old.tmp')
        mock_rmtree.assert_called_once_with('/root/old_cache') # Only old_cache should be rmtree'd

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime')
    def test_no_match_no_deletion(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Mock rationale: Simulate file system structure and modification times.
        mock_walk.return_value = [
            ('/root', [], ['file.txt', 'another.doc'])
        ]
        file_mtimes = {
            '/root/file.txt': (self.base_time - timedelta(days=10)).timestamp(),
            '/root/another.doc': (self.base_time - timedelta(days=10)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['*.log', '__pycache__'], # Patterns that won't match
            age_days=5,
            dry_run=False
        )

        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(skipped), 0)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime')
    def test_files_too_new_no_deletion(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Mock rationale: Simulate file system structure and modification times.
        mock_walk.return_value = [
            ('/root', [], ['recent.log', 'recent_cache'])
        ]
        file_mtimes = {
            '/root/recent.log': (self.base_time - timedelta(days=5)).timestamp(),
            '/root/recent_cache': (self.base_time - timedelta(days=5)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['*.log', 'recent_cache'],
            age_days=10, # Require 10 days, but files are only 5 days old
            dry_run=False
        )

        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(skipped), 0)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime')
    def test_deletion_error_handling(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Mock rationale: Simulate file system structure and modification times.
        mock_walk.return_value = [
            ('/root', [], ['error.log'])
        ]
        file_mtimes = {
            '/root/error.log': (self.base_time - timedelta(days=31)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        # Mock rationale: Simulate an OSError during deletion
        mock_remove.side_effect = OSError("Permission denied")

        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['*.log'],
            age_days=30,
            dry_run=False
        )

        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(skipped), 1)
        self.assertIn('/root/error.log', skipped)
        mock_remove.assert_called_once_with('/root/error.log')
        mock_rmtree.assert_not_called()

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('src.cleaner.datetime')
    def test_directory_pattern_matching(self, mock_datetime, mock_rmtree, mock_remove, mock_walk, mock_getmtime, mock_exists):
        # Mock rationale: Control the current time for age calculations.
        mock_datetime.now.return_value = self.base_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Mock rationale: Simulate file system structure and modification times.
        mock_walk.return_value = [
            ('/root', ['dist', 'build', 'src'], []),
            ('/root/dist', [], ['bundle.js']),
            ('/root/build', [], ['app.exe']),
            ('/root/src', [], ['main.py'])
        ]
        file_mtimes = {
            '/root/dist': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/build': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/src': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/dist/bundle.js': (self.base_time - timedelta(days=31)).timestamp(),
            '/root/build/app.exe': (self.base_time - timedelta(days=1)).timestamp(),
            '/root/src/main.py': (self.base_time - timedelta(days=1)).timestamp(),
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, self.base_time.timestamp())

        # Mock rationale: Ensure os.path.exists always returns True for our mocked paths
        mock_exists.return_value = True

        deleted, skipped = find_and_delete_old_debris(
            root_path='/root',
            patterns=['dist', 'build/'], # Test both 'dir' and 'dir/' patterns
            age_days=30,
            dry_run=False
        )

        self.assertEqual(len(deleted), 1)
        self.assertIn('/root/dist', deleted)
        mock_rmtree.assert_called_once_with('/root/dist')
        mock_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()
