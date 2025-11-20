import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the Python path to import sweeper.py
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_empty_directories, find_stale_files

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Define a base path for our mock filesystem
        self.base_path = '/mock/root'
        # Define a current time for consistent testing of file age
        self.current_time = time.time()

    @patch('os.walk')
    def test_find_empty_directories(self, mock_os_walk):
        # Mock rationale: os.walk is a generator that traverses the filesystem.
        # We need to control its output to simulate various directory structures
        # without actually creating files on disk. This ensures deterministic and offline testing.

        # Scenario 1: A simple empty directory
        mock_os_walk.return_value = [
            (self.base_path, ['empty_dir'], []), # root has one subdir
            (os.path.join(self.base_path, 'empty_dir'), [], []) # empty_dir is empty
        ]
        empty_dirs = find_empty_directories(self.base_path)
        self.assertEqual(len(empty_dirs), 1)
        self.assertIn(os.path.join(self.base_path, 'empty_dir'), empty_dirs)

        # Scenario 2: Nested empty directories (only the deepest should be reported by current logic)
        mock_os_walk.return_value = [
            (self.base_path, ['parent_empty'], []), # root has one subdir
            (os.path.join(self.base_path, 'parent_empty'), ['child_empty'], []), # parent_empty has one subdir
            (os.path.join(self.base_path, 'parent_empty', 'child_empty'), [], []) # child_empty is empty
        ]
        empty_dirs = find_empty_directories(self.base_path)
        self.assertEqual(len(empty_dirs), 1)
        self.assertIn(os.path.join(self.base_path, 'parent_empty', 'child_empty'), empty_dirs)

        # Scenario 3: Directory with files, not empty
        mock_os_walk.return_value = [
            (self.base_path, ['not_empty'], []), # root has one subdir
            (os.path.join(self.base_path, 'not_empty'), [], ['file.txt']) # not_empty has a file
        ]
        empty_dirs = find_empty_directories(self.base_path)
        self.assertEqual(len(empty_dirs), 0)

        # Scenario 4: Root itself is empty (no subdirs, no files)
        mock_os_walk.return_value = [
            (self.base_path, [], [])
        ]
        empty_dirs = find_empty_directories(self.base_path)
        self.assertEqual(len(empty_dirs), 1)
        self.assertIn(self.base_path, empty_dirs)

        # Scenario 5: Mixed content, one empty subdir
        mock_os_walk.return_value = [
            (self.base_path, ['dir1', 'dir2'], ['root_file.txt']), # root has files and subdirs
            (os.path.join(self.base_path, 'dir1'), [], ['file1.txt']), # dir1 has files
            (os.path.join(self.base_path, 'dir2'), ['empty_subdir'], []), # dir2 has subdir
            (os.path.join(self.base_path, 'dir2', 'empty_subdir'), [], []) # empty_subdir is empty
        ]
        empty_dirs = find_empty_directories(self.base_path)
        self.assertEqual(len(empty_dirs), 1)
        self.assertIn(os.path.join(self.base_path, 'dir2', 'empty_subdir'), empty_dirs)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    def test_find_stale_files(self, mock_os_getsize, mock_os_getmtime, mock_os_isfile, mock_os_walk):
        # Mock rationale:
        # - os.walk: To simulate directory traversal without touching the filesystem.
        # - os.path.isfile: To ensure we only process actual files and not directories or broken links.
        # - os.path.getmtime: To control the modification time of simulated files for age checks.
        # - os.path.getsize: To control the size of simulated files for size checks.
        # These mocks ensure deterministic and offline testing by providing predefined values.

        # Simulate a file that is old and small (stale)
        stale_file_path = os.path.join(self.base_path, 'old_small.log')
        new_large_file_path = os.path.join(self.base_path, 'new_large.txt')
        old_large_file_path = os.path.join(self.base_path, 'old_large.bak')
        new_small_file_path = os.path.join(self.base_path, 'new_small.tmp')

        mock_os_walk.return_value = [
            (self.base_path, [], [
                os.path.basename(stale_file_path),
                os.path.basename(new_large_file_path),
                os.path.basename(old_large_file_path),
                os.path.basename(new_small_file_path)
            ])
        ]
        # All paths are considered files for this test, unless explicitly set otherwise
        mock_os_isfile.side_effect = lambda p: p in [
            stale_file_path,
            new_large_file_path,
            old_large_file_path,
            new_small_file_path
        ]

        # Define mock return values for getmtime and getsize
        def getmtime_side_effect(path):
            if path == stale_file_path:
                return self.current_time - timedelta(days=40).total_seconds() # 40 days old
            elif path == new_large_file_path:
                return self.current_time - timedelta(days=10).total_seconds() # 10 days old
            elif path == old_large_file_path:
                return self.current_time - timedelta(days=40).total_seconds() # 40 days old
            elif path == new_small_file_path:
                return self.current_time - timedelta(days=10).total_seconds() # 10 days old
            return self.current_time # Default for others

        def getsize_side_effect(path):
            if path == stale_file_path:
                return int(0.5 * 1024 * 1024) # 0.5 MB
            elif path == new_large_file_path:
                return int(2 * 1024 * 1024) # 2 MB
            elif path == old_large_file_path:
                return int(2 * 1024 * 1024) # 2 MB
            elif path == new_small_file_path:
                return int(0.5 * 1024 * 1024) # 0.5 MB
            return 100 # Default small size

        mock_os_getmtime.side_effect = getmtime_side_effect
        mock_os_getsize.side_effect = getsize_side_effect

        # Test with default age (30 days) and size (1MB)
        stale_files = find_stale_files(self.base_path, age_days=30, max_size_mb=1)
        self.assertEqual(len(stale_files), 1)
        self.assertEqual(stale_files[0]['path'], stale_file_path)
        self.assertAlmostEqual(stale_files[0]['size_mb'], 0.5, places=1)

        # Test with different age and size criteria
        # Now, old_large.bak should also be considered stale if max_size_mb is increased
        stale_files_2 = find_stale_files(self.base_path, age_days=30, max_size_mb=3)
        self.assertEqual(len(stale_files_2), 2)
        self.assertIn(stale_file_path, [f['path'] for f in stale_files_2])
        self.assertIn(old_large_file_path, [f['path'] for f in stale_files_2])

        # Test with no stale files (all are new or large based on criteria)
        mock_os_getmtime.side_effect = lambda p: self.current_time - timedelta(days=10).total_seconds() # All files are new
        mock_os_getsize.side_effect = lambda p: int(0.5 * 1024 * 1024) # All files are small
        stale_files_3 = find_stale_files(self.base_path, age_days=30, max_size_mb=1)
        self.assertEqual(len(stale_files_3), 0)

        # Test with a non-file path (e.g., a broken symlink or directory) being passed to os.path.isfile
        mock_os_walk.return_value = [
            (self.base_path, [], ['not_a_file'])
        ]
        mock_os_isfile.side_effect = lambda p: False # Simulate it's not a file
        stale_files_4 = find_stale_files(self.base_path, age_days=30, max_size_mb=1)
        self.assertEqual(len(stale_files_4), 0)

if __name__ == '__main__':
    unittest.main()
