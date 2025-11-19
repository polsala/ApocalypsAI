import unittest
from unittest.mock import patch, MagicMock
import os
import time
import shutil
from datetime import datetime, timedelta

# Import the function to be tested
from src.sweeper import sweep_directory, get_file_age_days

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Mock current time to be consistent for tests
        self.mock_current_time = datetime(2023, 10, 26, 10, 0, 0).timestamp()
        self.patcher_time = patch('time.time', return_value=self.mock_current_time)
        self.patcher_time.start()

    def tearDown(self):
        self.patcher_time.stop()

    def _mock_os_walk(self, mock_structure):
        """
        Helper to mock os.walk.
        mock_structure is a list of (root, dirs, files) tuples.
        """
        mock_walk = MagicMock(side_effect=mock_structure)
        return mock_walk

    def _mock_getmtime(self, file_mtimes):
        """
        Helper to mock os.path.getmtime.
        file_mtimes is a dict mapping file_path -> timestamp.
        """
        mock_getmtime = MagicMock(side_effect=lambda path: file_mtimes.get(path, self.mock_current_time))
        return mock_getmtime
    
    def _mock_os_path_isdir(self, existing_dirs):
        """
        Helper to mock os.path.isdir.
        existing_dirs is a set of paths that exist as directories.
        """
        mock_isdir = MagicMock(side_effect=lambda path: path in existing_dirs)
        return mock_isdir

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_sweep_directory_dry_run(self, mock_walk, mock_isdir, mock_getmtime, mock_rmtree, mock_remove):
        # Mock rationale: Simulate file system traversal without actual disk access.
        # Mock rationale: Control which paths are considered directories.
        # Mock rationale: Control file modification times for age-based filtering.
        # Mock rationale: Ensure no actual deletion occurs during dry run.
        # Mock rationale: Ensure no actual deletion occurs during dry run.

        # Setup mock file system
        mock_walk.side_effect = [
            ('/tmp/test_dir', ['subdir1', '__pycache__'], ['old_file.tmp', 'new_file.log', 'keep_me.txt']),
            ('/tmp/test_dir/subdir1', [], ['another_old.tmp']),
            ('/tmp/test_dir/__pycache__', [], ['cache_file.pyc']),
        ]
        mock_isdir.side_effect = self._mock_os_path_isdir({'/tmp/test_dir', '/tmp/test_dir/subdir1', '/tmp/test_dir/__pycache__'}) 

        # Define file modification times (older than 7 days)
        eight_days_ago = self.mock_current_time - (8 * 24 * 60 * 60)
        six_days_ago = self.mock_current_time - (6 * 24 * 60 * 60)

        mock_getmtime.side_effect = self._mock_getmtime({
            '/tmp/test_dir/old_file.tmp': eight_days_ago,
            '/tmp/test_dir/new_file.log': six_days_ago, # Should not be reported
            '/tmp/test_dir/keep_me.txt': eight_days_ago, # Not matching pattern
            '/tmp/test_dir/subdir1/another_old.tmp': eight_days_ago,
            '/tmp/test_dir/__pycache__': eight_days_ago, # Directory
            '/tmp/test_dir/__pycache__/cache_file.pyc': eight_days_ago,
        })

        target_dirs = ['/tmp/test_dir']
        patterns = ['*.tmp', '__pycache__']
        age_days = 7
        dry_run = True

        results = sweep_directory(target_dirs, patterns, age_days, dry_run=dry_run)

        expected_reported = [
            '/tmp/test_dir/__pycache__',
            '/tmp/test_dir/old_file.tmp',
            '/tmp/test_dir/subdir1/another_old.tmp',
        ]
        # Sort for consistent comparison
        self.assertCountEqual(results['reported_files'], expected_reported)
        self.assertEqual(results['deleted_files'], [])
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_sweep_directory_actual_delete(self, mock_walk, mock_isdir, mock_getmtime, mock_rmtree, mock_remove):
        # Mock rationale: Simulate file system traversal without actual disk access.
        # Mock rationale: Control which paths are considered directories.
        # Mock rationale: Control file modification times for age-based filtering.
        # Mock rationale: Verify os.remove is called for files.
        # Mock rationale: Verify shutil.rmtree is called for directories.

        # Setup mock file system
        mock_walk.side_effect = [
            ('/tmp/test_dir', ['subdir1', '__pycache__'], ['old_file.tmp', 'new_file.log', 'keep_me.txt']),
            ('/tmp/test_dir/subdir1', [], ['another_old.tmp']),
            ('/tmp/test_dir/__pycache__', [], ['cache_file.pyc']),
        ]
        mock_isdir.side_effect = self._mock_os_path_isdir({'/tmp/test_dir', '/tmp/test_dir/subdir1', '/tmp/test_dir/__pycache__'}) 

        # Define file modification times (older than 7 days)
        eight_days_ago = self.mock_current_time - (8 * 24 * 60 * 60)
        six_days_ago = self.mock_current_time - (6 * 24 * 60 * 60)

        mock_getmtime.side_effect = self._mock_getmtime({
            '/tmp/test_dir/old_file.tmp': eight_days_ago,
            '/tmp/test_dir/new_file.log': six_days_ago,
            '/tmp/test_dir/keep_me.txt': eight_days_ago,
            '/tmp/test_dir/subdir1/another_old.tmp': eight_days_ago,
            '/tmp/test_dir/__pycache__': eight_days_ago,
            '/tmp/test_dir/__pycache__/cache_file.pyc': eight_days_ago,
        })

        target_dirs = ['/tmp/test_dir']
        patterns = ['*.tmp', '__pycache__']
        age_days = 7
        dry_run = False

        results = sweep_directory(target_dirs, patterns, age_days, dry_run=dry_run)

        expected_deleted = [
            '/tmp/test_dir/__pycache__',
            '/tmp/test_dir/old_file.tmp',
            '/tmp/test_dir/subdir1/another_old.tmp',
        ]
        self.assertCountEqual(results['reported_files'], expected_deleted)
        self.assertCountEqual(results['deleted_files'], expected_deleted)

        mock_rmtree.assert_any_call('/tmp/test_dir/__pycache__')
        mock_remove.assert_any_call('/tmp/test_dir/old_file.tmp')
        mock_remove.assert_any_call('/tmp/test_dir/subdir1/another_old.tmp')
        self.assertEqual(mock_rmtree.call_count, 1)
        self.assertEqual(mock_remove.call_count, 2)

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_sweep_directory_non_existent_target(self, mock_walk, mock_isdir, mock_getmtime, mock_rmtree, mock_remove):
        # Mock rationale: Simulate a target directory that does not exist.
        mock_isdir.side_effect = self._mock_os_path_isdir({'/existing/dir'}) 

        target_dirs = ['/non/existent/dir', '/existing/dir']
        patterns = ['*.tmp']
        age_days = 7
        dry_run = True

        mock_walk.side_effect = [
            ('/existing/dir', [], ['file.tmp'])
        ]
        mock_getmtime.return_value = self.mock_current_time - (8 * 24 * 60 * 60)

        results = sweep_directory(target_dirs, patterns, age_days, dry_run=dry_run, verbose=True)

        self.assertIn('/existing/dir/file.tmp', results['reported_files'])
        self.assertEqual(len(results['reported_files']), 1)
        self.assertEqual(results['deleted_files'], [])
        mock_walk.assert_called_once_with('/existing/dir') # Should not be called for non-existent dir

    @patch('os.path.getmtime')
    @patch('time.time')
    def test_get_file_age_days(self, mock_time_time, mock_getmtime):
        # Mock rationale: Control current time and file modification time for precise age calculation.
        mock_time_time.return_value = datetime(2023, 1, 8, 12, 0, 0).timestamp()
        
        # File modified 3 days ago
        three_days_ago = datetime(2023, 1, 5, 12, 0, 0).timestamp()
        mock_getmtime.return_value = three_days_ago
        self.assertAlmostEqual(get_file_age_days('/some/file'), 3.0)

        # File modified exactly 7 days ago
        seven_days_ago = datetime(2023, 1, 1, 12, 0, 0).timestamp()
        mock_getmtime.return_value = seven_days_ago
        self.assertAlmostEqual(get_file_age_days('/another/file'), 7.0)

    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('shutil.rmtree', side_effect=OSError("Permission denied"))
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_sweep_directory_deletion_error(self, mock_walk, mock_isdir, mock_getmtime, mock_rmtree, mock_remove):
        # Mock rationale: Simulate permission errors during deletion to ensure graceful handling.
        mock_walk.side_effect = [
            ('/tmp/test_dir', ['__pycache__'], ['old_file.tmp']),
        ]
        mock_isdir.side_effect = self._mock_os_path_isdir({'/tmp/test_dir', '/tmp/test_dir/__pycache__'}) 

        eight_days_ago = self.mock_current_time - (8 * 24 * 60 * 60)
        mock_getmtime.side_effect = self._mock_getmtime({
            '/tmp/test_dir/old_file.tmp': eight_days_ago,
            '/tmp/test_dir/__pycache__': eight_days_ago,
        })

        target_dirs = ['/tmp/test_dir']
        patterns = ['*.tmp', '__pycache__']
        age_days = 7
        dry_run = False

        results = sweep_directory(target_dirs, patterns, age_days, dry_run=dry_run, verbose=True)

        expected_reported = [
            '/tmp/test_dir/__pycache__',
            '/tmp/test_dir/old_file.tmp',
        ]
        self.assertCountEqual(results['reported_files'], expected_reported)
        self.assertEqual(results['deleted_files'], []) # Nothing should be marked as deleted if error occurred

        mock_rmtree.assert_any_call('/tmp/test_dir/__pycache__')
        mock_remove.assert_any_call('/tmp/test_dir/old_file.tmp')
        self.assertEqual(mock_rmtree.call_count, 1)
        self.assertEqual(mock_remove.call_count, 1)

    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_sweep_directory_no_match(self, mock_walk, mock_isdir, mock_getmtime):
        # Mock rationale: Test scenario where no files match the patterns or age criteria.
        mock_walk.side_effect = [
            ('/tmp/test_dir', ['subdir'], ['file1.txt', 'file2.log']),
        ]
        mock_isdir.side_effect = self._mock_os_path_isdir({'/tmp/test_dir', '/tmp/test_dir/subdir'}) 

        six_days_ago = self.mock_current_time - (6 * 24 * 60 * 60)
        mock_getmtime.side_effect = self._mock_getmtime({
            '/tmp/test_dir/file1.txt': six_days_ago,
            '/tmp/test_dir/file2.log': six_days_ago,
        })

        target_dirs = ['/tmp/test_dir']
        patterns = ['*.tmp', '__pycache__']
        age_days = 7
        dry_run = True

        results = sweep_directory(target_dirs, patterns, age_days, dry_run=dry_run)

        self.assertEqual(results['reported_files'], [])
        self.assertEqual(results['deleted_files'], [])

if __name__ == '__main__':
    unittest.main()
