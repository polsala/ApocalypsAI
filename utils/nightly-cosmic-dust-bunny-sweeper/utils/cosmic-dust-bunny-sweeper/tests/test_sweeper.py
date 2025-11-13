import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from collections import namedtuple

# Mock rationale: We need to simulate file system operations (listing directories, checking emptiness, deleting files/dirs)
# without actually touching the real file system. This ensures tests are deterministic, fast, and don't leave artifacts.
# `os.walk`, `os.path.isdir`, `os.listdir`, `os.remove`, `shutil.rmtree`, `os.rmdir` are all mocked.

# Import the function to be tested
from src.sweeper import find_and_clean, DEFAULT_PATTERNS, is_empty_dir

# Define a mock structure for os.walk
# (root, dirnames, filenames)
MockWalkResult = namedtuple('MockWalkResult', ['root', 'dirnames', 'filenames'])

class TestCosmicDustBunnySweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_is_empty_dir(self, mock_listdir, mock_isdir):
        # Mock rationale: Test the helper function `is_empty_dir` in isolation.
        # `os.path.isdir` is mocked to control whether the path is considered a directory.
        # `os.listdir` is mocked to control the contents of the directory.

        mock_isdir.return_value = True

        # Test empty directory
        mock_listdir.return_value = []
        self.assertTrue(is_empty_dir('/mock/empty_dir'))

        # Test non-empty directory
        mock_listdir.return_value = ['file.txt']
        self.assertFalse(is_empty_dir('/mock/non_empty_dir'))

        # Test not a directory
        mock_isdir.return_value = False
        self.assertFalse(is_empty_dir('/mock/not_a_dir'))

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.rmdir')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.walk')
    def test_find_and_clean_dry_run_files(self, mock_walk, mock_listdir, mock_isdir, mock_rmdir, mock_rmtree, mock_remove):
        # Mock rationale: Simulate a file system with specific files and directories.
        # `os.walk` is mocked to provide a predefined directory structure.
        # `os.path.isdir` and `os.listdir` are mocked to support `is_empty_dir`.
        # `os.remove`, `shutil.rmtree`, `os.rmdir` are mocked to ensure no actual deletions occur during dry run.

        mock_walk.return_value = [
            MockWalkResult('/mock_root', ['dir1', 'dir2', '__pycache__'], ['file.txt', 'temp.tmp', 'log.log']),
            MockWalkResult('/mock_root/dir1', [], ['another.txt']),
            MockWalkResult('/mock_root/dir2', [], []),
            MockWalkResult('/mock_root/__pycache__', [], ['cache.pyc'])
        ]
        mock_isdir.side_effect = lambda p: p in ['/mock_root', '/mock_root/dir1', '/mock_root/dir2', '/mock_root/__pycache__']
        mock_listdir.side_effect = lambda p: [] if p == '/mock_root/dir2' else ['file.txt'] # Only dir2 is empty

        # Test with default patterns in dry run mode
        deleted_paths = find_and_clean('/mock_root', DEFAULT_PATTERNS, dry_run=True)

        expected_deleted = {
            '/mock_root/temp.tmp',
            '/mock_root/log.log',
            '/mock_root/__pycache__',
            '/mock_root/__pycache__/cache.pyc',
            '/mock_root/dir2' # Empty directory
        }

        self.assertEqual(deleted_paths, expected_deleted)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_rmdir.assert_not_called()

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.rmdir')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.walk')
    def test_find_and_clean_actual_run_files(self, mock_walk, mock_listdir, mock_isdir, mock_rmdir, mock_rmtree, mock_remove):
        # Mock rationale: Similar to dry run, but verify that deletion functions are called.
        # `os.remove`, `shutil.rmtree`, `os.rmdir` are mocked to track calls.

        mock_walk.return_value = [
            MockWalkResult('/mock_root', ['dir1', 'dir2', '__pycache__'], ['file.txt', 'temp.tmp', 'log.log']),
            MockWalkResult('/mock_root/dir1', [], ['another.txt']),
            MockWalkResult('/mock_root/dir2', [], []),
            MockWalkResult('/mock_root/__pycache__', [], ['cache.pyc'])
        ]
        mock_isdir.side_effect = lambda p: p in ['/mock_root', '/mock_root/dir1', '/mock_root/dir2', '/mock_root/__pycache__']
        mock_listdir.side_effect = lambda p: [] if p == '/mock_root/dir2' else ['file.txt'] # Only dir2 is empty

        # Test with default patterns in actual run mode
        deleted_paths = find_and_clean('/mock_root', DEFAULT_PATTERNS, dry_run=False)

        expected_deleted = {
            '/mock_root/temp.tmp',
            '/mock_root/log.log',
            '/mock_root/__pycache__',
            '/mock_root/__pycache__/cache.pyc',
            '/mock_root/dir2' # Empty directory
        }

        self.assertEqual(deleted_paths, expected_deleted)

        # Verify deletion calls
        mock_remove.assert_any_call('/mock_root/temp.tmp')
        mock_remove.assert_any_call('/mock_root/log.log')
        mock_remove.assert_any_call('/mock_root/__pycache__/cache.pyc')
        mock_rmtree.assert_any_call('/mock_root/__pycache__') # __pycache__ is deleted recursively
        mock_rmdir.assert_any_call('/mock_root/dir2') # Empty dir is deleted with rmdir

        self.assertEqual(mock_remove.call_count, 3)
        self.assertEqual(mock_rmtree.call_count, 1)
        self.assertEqual(mock_rmdir.call_count, 1)

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.rmdir')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.walk')
    def test_find_and_clean_custom_patterns(self, mock_walk, mock_listdir, mock_isdir, mock_rmdir, mock_rmtree, mock_remove):
        # Mock rationale: Test custom pattern matching logic.

        mock_walk.return_value = [
            MockWalkResult('/mock_root', ['build_dir'], ['config.ini', 'data.json', 'output.bin']),
            MockWalkResult('/mock_root/build_dir', [], ['temp_file.xyz', 'another_file.txt'])
        ]
        mock_isdir.side_effect = lambda p: p in ['/mock_root', '/mock_root/build_dir']
        mock_listdir.return_value = [] # Assume no empty dirs for this test

        custom_patterns = ['*.bin', 'build_dir', '*.xyz']
        deleted_paths = find_and_clean('/mock_root', custom_patterns, dry_run=True)

        expected_deleted = {
            '/mock_root/output.bin',
            '/mock_root/build_dir',
            '/mock_root/build_dir/temp_file.xyz'
        }

        self.assertEqual(deleted_paths, expected_deleted)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_rmdir.assert_not_called()

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.rmdir')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.walk')
    def test_find_and_clean_no_dust_bunnies(self, mock_walk, mock_listdir, mock_isdir, mock_rmdir, mock_rmtree, mock_remove):
        # Mock rationale: Test scenario where no files/directories match deletion criteria.

        mock_walk.return_value = [
            MockWalkResult('/mock_root', ['src'], ['main.py', 'README.md']),
            MockWalkResult('/mock_root/src', [], ['module.py'])
        ]
        mock_isdir.side_effect = lambda p: p in ['/mock_root', '/mock_root/src']
        mock_listdir.return_value = ['main.py'] # Not empty

        deleted_paths = find_and_clean('/mock_root', DEFAULT_PATTERNS, dry_run=True)

        self.assertEqual(deleted_paths, set())
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_rmdir.assert_not_called()

    @patch('os.path.isdir')
    def test_find_and_clean_invalid_directory(self, mock_isdir):
        # Mock rationale: Test error handling for an invalid target directory.

        mock_isdir.return_value = False

        deleted_paths = find_and_clean('/non_existent_dir', DEFAULT_PATTERNS, dry_run=True)
        self.assertEqual(deleted_paths, set())


if __name__ == '__main__':
    unittest.main()
