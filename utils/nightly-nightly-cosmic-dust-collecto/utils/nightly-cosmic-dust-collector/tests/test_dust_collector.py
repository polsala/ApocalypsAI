import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.dust_collector.datetime') # Mock datetime within the module
    def test_finds_old_small_files(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate the current time for age calculation.
        # We need to mock datetime.now() and ensure datetime.fromtimestamp() works.
        real_datetime = datetime # Keep a reference to the real datetime
        mock_datetime.now.return_value = real_datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = real_datetime.fromtimestamp # Use real fromtimestamp

        # Mock rationale: Simulate a valid target directory.
        mock_isdir.return_value = True

        # Mock rationale: Simulate directory structure and files.
        # File 1: Old, small -> should be found
        # File 2: Recent, small -> should be ignored (age)
        # File 3: Old, large -> should be ignored (size)
        # File 4: Old, small, wrong extension -> should be ignored (include_ext)
        # File 5: Old, small, excluded extension -> should be ignored (exclude_ext)
        # File 6: Old, small, correct extension -> should be found
        mock_walk.return_value = [
            ('/mock/path', ('subdir',), ('file1.txt', 'file2.log', 'file3.json', 'file4.py', 'file5.tmp', 'file6.data')),
            ('/mock/path/subdir', (), ('subfile1.txt',))
        ]

        # Mock rationale: Simulate os.stat results for each file.
        # file_path -> (size_bytes, mtime_timestamp)
        mock_stat_map = {
            '/mock/path/file1.txt': (5 * 1024, (real_datetime(2023, 9, 1) - timedelta(seconds=1)).timestamp()), # Old, 5KB
            '/mock/path/file2.log': (2 * 1024, (real_datetime(2023, 10, 20) - timedelta(seconds=1)).timestamp()), # Recent, 2KB
            '/mock/path/file3.json': (15 * 1024, (real_datetime(2023, 9, 1) - timedelta(seconds=1)).timestamp()), # Old, 15KB
            '/mock/path/file4.py': (3 * 1024, (real_datetime(2023, 9, 1) - timedelta(seconds=1)).timestamp()), # Old, 3KB
            '/mock/path/file5.tmp': (4 * 1024, (real_datetime(2023, 9, 1) - timedelta(seconds=1)).timestamp()), # Old, 4KB
            '/mock/path/file6.data': (6 * 1024, (real_datetime(2023, 9, 1) - timedelta(seconds=1)).timestamp()), # Old, 6KB
            '/mock/path/subdir/subfile1.txt': (1 * 1024, (real_datetime(2023, 8, 15) - timedelta(seconds=1)).timestamp()), # Old, 1KB
        }

        def mock_os_stat(path):
            mock_stat_obj = MagicMock()
            size, mtime = mock_stat_map.get(path, (0, 0))
            mock_stat_obj.st_size = size
            mock_stat_obj.st_mtime = mtime
            return mock_stat_obj

        mock_stat.side_effect = mock_os_stat

        # Test with default parameters
        dust_found = collect_dust(target_dir='/mock/path', min_age_days=30, max_size_kb=10)
        self.assertEqual(len(dust_found), 3)
        self.assertIn({'path': '/mock/path/file1.txt', 'size_bytes': 5120, 'last_modified': '2023-08-31T23:59:59'}, dust_found)
        self.assertIn({'path': '/mock/path/file6.data', 'size_bytes': 6144, 'last_modified': '2023-08-31T23:59:59'}, dust_found)
        self.assertIn({'path': '/mock/path/subdir/subfile1.txt', 'size_bytes': 1024, 'last_modified': '2023-08-14T23:59:59'}, dust_found)

        # Test with include_extensions
        dust_found_inc = collect_dust(target_dir='/mock/path', min_age_days=30, max_size_kb=10, include_extensions=['.txt'])
        self.assertEqual(len(dust_found_inc), 2)
        self.assertIn({'path': '/mock/path/file1.txt', 'size_bytes': 5120, 'last_modified': '2023-08-31T23:59:59'}, dust_found_inc)
        self.assertIn({'path': '/mock/path/subdir/subfile1.txt', 'size_bytes': 1024, 'last_modified': '2023-08-14T23:59:59'}, dust_found_inc)

        # Test with exclude_extensions
        dust_found_exc = collect_dust(target_dir='/mock/path', min_age_days=30, max_size_kb=10, exclude_extensions=['.data'])
        self.assertEqual(len(dust_found_exc), 2)
        self.assertIn({'path': '/mock/path/file1.txt', 'size_bytes': 5120, 'last_modified': '2023-08-31T23:59:59'}, dust_found_exc)
        self.assertIn({'path': '/mock/path/subdir/subfile1.txt', 'size_bytes': 1024, 'last_modified': '2023-08-14T23:59:59'}, dust_found_exc)

        # Test with both include and exclude
        dust_found_both = collect_dust(target_dir='/mock/path', min_age_days=30, max_size_kb=10, include_extensions=['.txt', '.data'], exclude_extensions=['.data'])
        self.assertEqual(len(dust_found_both), 2)
        self.assertIn({'path': '/mock/path/file1.txt', 'size_bytes': 5120, 'last_modified': '2023-08-31T23:59:59'}, dust_found_both)
        self.assertIn({'path': '/mock/path/subdir/subfile1.txt', 'size_bytes': 1024, 'last_modified': '2023-08-14T23:59:59'}, dust_found_both)


    @patch('os.path.isdir')
    def test_non_existent_directory(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        dust_found = collect_dust(target_dir='/non/existent/path')
        self.assertEqual(len(dust_found), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.dust_collector.datetime')
    def test_empty_directory(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        real_datetime = datetime
        mock_datetime.now.return_value = real_datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = real_datetime.fromtimestamp
        mock_isdir.return_value = True
        mock_walk.return_value = [('/mock/empty', (), ())] # No files
        dust_found = collect_dust(target_dir='/mock/empty')
        self.assertEqual(len(dust_found), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.dust_collector.datetime')
    def test_file_disappears_during_scan(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file being deleted between os.walk and os.stat.
        real_datetime = datetime
        mock_datetime.now.return_value = real_datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = real_datetime.fromtimestamp
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', (), ('ghost_file.txt',))
        ]
        mock_stat.side_effect = FileNotFoundError # Simulate file not found

        dust_found = collect_dust(target_dir='/mock/path')
        self.assertEqual(len(dust_found), 0) # Should not raise error, just skip
