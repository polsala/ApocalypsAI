import unittest
from unittest.mock import patch, MagicMock
import time
import os
from datetime import datetime

# Import the function to be tested
from src.collector import find_debris

class TestDataDebrisCollector(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age calculations
        self.mock_current_time = 1678886400.0 # March 15, 2023 00:00:00 UTC

    @patch('time.time')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.listdir')
    def test_find_old_files(self, mock_listdir, mock_stat, mock_walk, mock_isdir, mock_exists, mock_time):
        # Mock rationale: Simulate a file system with files of different access times.
        # We need to control the 'current time' and 'last access time' of files
        # to deterministically test the age-based filtering.
        mock_time.return_value = self.mock_current_time
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Simulate directory structure:
        # /root
        #   ├── old_file.txt (accessed 60 days ago)
        #   ├── recent_file.txt (accessed 10 days ago)
        #   └── subdir/
        #       └── another_old_file.log (accessed 40 days ago)
        mock_walk.return_value = [
            ('/root', ['subdir'], ['old_file.txt', 'recent_file.txt']),
            ('/root/subdir', [], ['another_old_file.log'])
        ]

        # Mock os.stat for files
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'old_file.txt' in path:
                mock_stat_obj.st_size = 100
                mock_stat_obj.st_atime = self.mock_current_time - (60 * 24 * 3600) # 60 days old
            elif 'recent_file.txt' in path:
                mock_stat_obj.st_size = 50
                mock_stat_obj.st_atime = self.mock_current_time - (10 * 24 * 3600) # 10 days old
            elif 'another_old_file.log' in path:
                mock_stat_obj.st_size = 200
                mock_stat_obj.st_atime = self.mock_current_time - (40 * 24 * 3600) # 40 days old
            else:
                raise FileNotFoundError # Should not happen with controlled walk
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect
        # Mock os.listdir to return non-empty for directories that contain files/subdirs
        mock_listdir.side_effect = lambda p: ['dummy'] if p in ['/root', '/root/subdir'] else []

        # Test with age filter: 30 days
        debris = find_debris('/root', max_age_days=30)

        self.assertEqual(len(debris), 2)
        self.assertIn('/root/old_file.txt', [d['path'] for d in debris])
        self.assertIn('/root/subdir/another_old_file.log', [d['path'] for d in debris])
        self.assertNotIn('/root/recent_file.txt', [d['path'] for d in debris])

    @patch('time.time')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.listdir')
    def test_find_empty_files_and_dirs(self, mock_listdir, mock_stat, mock_walk, mock_isdir, mock_exists, mock_time):
        # Mock rationale: Simulate a file system with empty files and directories.
        # We need to control file sizes and directory contents to test emptiness filtering.
        mock_time.return_value = self.mock_current_time
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Simulate directory structure:
        # /root
        #   ├── empty_file.txt (size 0)
        #   ├── non_empty_file.txt (size 100)
        #   ├── empty_dir/
        #   └── non_empty_dir/
        #       └── file_in_dir.txt
        mock_walk.return_value = [
            ('/root', ['empty_dir', 'non_empty_dir'], ['empty_file.txt', 'non_empty_file.txt']),
            ('/root/empty_dir', [], []),
            ('/root/non_empty_dir', [], ['file_in_dir.txt'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_atime = self.mock_current_time - (5 * 24 * 3600) # Not old for this test
            if 'empty_file.txt' in path:
                mock_stat_obj.st_size = 0
            elif 'non_empty_file.txt' in path or 'file_in_dir.txt' in path:
                mock_stat_obj.st_size = 100
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        # Mock os.listdir for directory emptiness check
        def mock_listdir_side_effect(path):
            if path == '/root':
                return ['empty_file.txt', 'non_empty_file.txt', 'empty_dir', 'non_empty_dir']
            elif path == '/root/empty_dir':
                return [] # This is an empty directory
            elif path == '/root/non_empty_dir':
                return ['file_in_dir.txt']
            return []

        mock_listdir.side_effect = mock_listdir_side_effect

        # Test with empty filter
        debris = find_debris('/root', include_empty=True)

        self.assertEqual(len(debris), 2)
        self.assertIn('/root/empty_file.txt', [d['path'] for d in debris])
        self.assertIn('/root/empty_dir', [d['path'] for d in debris])
        self.assertNotIn('/root/non_empty_file.txt', [d['path'] for d in debris])
        self.assertNotIn('/root/non_empty_dir', [d['path'] for d in debris])

    @patch('time.time')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.listdir')
    def test_find_files_by_min_size(self, mock_listdir, mock_stat, mock_walk, mock_isdir, mock_exists, mock_time):
        # Mock rationale: Simulate files of various sizes to test minimum size filtering.
        mock_time.return_value = self.mock_current_time
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Simulate directory structure:
        # /root
        #   ├── small_file.txt (size 50)
        #   ├── medium_file.txt (size 150)
        #   └── large_file.txt (size 250)
        mock_walk.return_value = [
            ('/root', [], ['small_file.txt', 'medium_file.txt', 'large_file.txt'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_atime = self.mock_current_time - (50 * 24 * 3600) # Old enough for default age
            if 'small_file.txt' in path:
                mock_stat_obj.st_size = 50
            elif 'medium_file.txt' in path:
                mock_stat_obj.st_size = 150
            elif 'large_file.txt' in path:
                mock_stat_obj.st_size = 250
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect
        mock_listdir.return_value = ['small_file.txt', 'medium_file.txt', 'large_file.txt']

        # Test with min_size filter: 100 bytes (and default age 30 days)
        debris = find_debris('/root', min_size_bytes=100)

        self.assertEqual(len(debris), 2)
        self.assertIn('/root/medium_file.txt', [d['path'] for d in debris])
        self.assertIn('/root/large_file.txt', [d['path'] for d in debris])
        self.assertNotIn('/root/small_file.txt', [d['path'] for d in debris])

    @patch('time.time')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.listdir')
    def test_combined_filters(self, mock_listdir, mock_stat, mock_walk, mock_isdir, mock_exists, mock_time):
        # Mock rationale: Test the interaction of age, empty, and min_size filters.
        mock_time.return_value = self.mock_current_time
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Simulate directory structure:
        # /root
        #   ├── old_small_file.txt (60 days old, size 50)
        #   ├── old_large_file.txt (60 days old, size 150)
        #   ├── recent_large_file.txt (10 days old, size 150)
        #   ├── empty_file.txt (5 days old, size 0)
        #   └── empty_dir/
        mock_walk.return_value = [
            ('/root', ['empty_dir'], ['old_small_file.txt', 'old_large_file.txt', 'recent_large_file.txt', 'empty_file.txt']),
            ('/root/empty_dir', [], [])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'old_small_file.txt' in path:
                mock_stat_obj.st_size = 50
                mock_stat_obj.st_atime = self.mock_current_time - (60 * 24 * 3600)
            elif 'old_large_file.txt' in path:
                mock_stat_obj.st_size = 150
                mock_stat_obj.st_atime = self.mock_current_time - (60 * 24 * 3600)
            elif 'recent_large_file.txt' in path:
                mock_stat_obj.st_size = 150
                mock_stat_obj.st_atime = self.mock_current_time - (10 * 24 * 3600)
            elif 'empty_file.txt' in path:
                mock_stat_obj.st_size = 0
                mock_stat_obj.st_atime = self.mock_current_time - (5 * 24 * 3600)
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        def mock_listdir_side_effect(path):
            if path == '/root':
                return ['old_small_file.txt', 'old_large_file.txt', 'recent_large_file.txt', 'empty_file.txt', 'empty_dir']
            elif path == '/root/empty_dir':
                return []
            return []

        mock_listdir.side_effect = mock_listdir_side_effect

        # Test: age > 30 days, min_size >= 100 bytes, include_empty=False
        debris = find_debris('/root', max_age_days=30, include_empty=False, min_size_bytes=100)

        self.assertEqual(len(debris), 1)
        self.assertIn('/root/old_large_file.txt', [d['path'] for d in debris])

        # Test: include_empty=True, no age, no min_size
        debris = find_debris('/root', include_empty=True)
        self.assertEqual(len(debris), 2) # empty_file.txt, empty_dir
        self.assertIn('/root/empty_file.txt', [d['path'] for d in debris])
        self.assertIn('/root/empty_dir', [d['path'] for d in debris])

        # Test: no filters (should default to age 30)
        debris = find_debris('/root')
        self.assertEqual(len(debris), 2) # old_small_file.txt, old_large_file.txt
        self.assertIn('/root/old_small_file.txt', [d['path'] for d in debris])
        self.assertIn('/root/old_large_file.txt', [d['path'] for d in debris])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_invalid_path(self, mock_isdir, mock_exists):
        # Mock rationale: Test how the utility handles non-existent or non-directory paths.
        mock_exists.return_value = False
        debris = find_debris('/nonexistent_path')
        self.assertEqual(len(debris), 0)

        mock_exists.return_value = True
        mock_isdir.return_value = False # It exists but is a file, not a directory
        debris = find_debris('/a_file.txt')
        self.assertEqual(len(debris), 0)

if __name__ == '__main__':
    unittest.main()
