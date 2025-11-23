import unittest
from unittest.mock import patch, MagicMock
import os
import time
import datetime
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Mock rationale: time.time() is mocked to provide a fixed 'current time' for deterministic
        # age calculations across test runs, preventing tests from failing due to real-time changes.
        self.mock_current_time = 1678886400.0  # March 15, 2023 00:00:00 UTC
        self.patcher_time = patch('time.time', return_value=self.mock_current_time)
        self.mock_time = self.patcher_time.start()

    def tearDown(self):
        self.patcher_time.stop()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_basic(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate the existence of the root directory
        # without requiring actual file system interaction.
        mock_isdir.return_value = True

        # Mock rationale: os.walk is mocked to simulate directory traversal and file discovery.
        # It returns (root, dirs, files) tuples, allowing control over the file system structure.
        mock_walk.return_value = [
            ('/test_root', ['subdir'], ['file1.txt', 'file2.log']),
            ('/test_root/subdir', [], ['subfile.tmp'])
        ]

        # Mock rationale: os.stat is mocked to provide file metadata (size, mtime) deterministically.
        # The side_effect ensures different stat results for different files as they are accessed.
        # file_mtime values are calculated relative to self.mock_current_time to ensure they are older than min_age_days.
        # min_age_days = 30, so files must be older than (self.mock_current_time - 30*24*60*60)
        # Let's make files older than 30 days (e.g., 31 days ago) or newer (e.g., 10 days ago).
        # 31 days ago: self.mock_current_time - (31 * 24 * 60 * 60) = 1676294400.0
        # 10 days ago: self.mock_current_time - (10 * 24 * 60 * 60) = 1678022400.0

        # File 1: Old (31 days), small (100 bytes) -> DUST
        # File 2: Old (31 days), large (2MB) -> TOO LARGE
        # File 3: New (10 days), small (50 bytes) -> TOO NEW
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=1676294400.0), # file1.txt
            MagicMock(st_size=2000000, st_mtime=1676294400.0), # file2.log
            MagicMock(st_size=50, st_mtime=1678022400.0) # subfile.tmp
        ]

        # Default parameters: max_size_bytes=1MB, min_age_days=30, include_empty=True
        dust = collect_dust('/test_root')

        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test_root', 'file1.txt'))
        self.assertEqual(dust[0]['size_bytes'], 100)
        self.assertAlmostEqual(dust[0]['age_days'], 31.0, places=2)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_empty_files(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['empty.txt', 'small.txt'])
        ]

        # File 1: Empty, old (31 days) -> DUST (if include_empty=True)
        # File 2: Small, old (31 days) -> DUST
        mock_stat.side_effect = [
            MagicMock(st_size=0, st_mtime=1676294400.0), # empty.txt
            MagicMock(st_size=500, st_mtime=1676294400.0), # small.txt
        ]

        # Test with include_empty=True (default)
        dust_with_empty = collect_dust('/test_root', min_age_days=30)
        self.assertEqual(len(dust_with_empty), 2)
        self.assertIn(os.path.join('/test_root', 'empty.txt'), [d['path'] for d in dust_with_empty])
        self.assertIn(os.path.join('/test_root', 'small.txt'), [d['path'] for d in dust_with_empty])

        # Reset mocks for next test to ensure clean state
        mock_stat.reset_mock()
        mock_walk.reset_mock()
        mock_isdir.reset_mock()
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['empty.txt', 'small.txt'])
        ]
        mock_stat.side_effect = [
            MagicMock(st_size=0, st_mtime=1676294400.0), # empty.txt
            MagicMock(st_size=500, st_mtime=1676294400.0), # small.txt
        ]

        # Test with include_empty=False
        dust_without_empty = collect_dust('/test_root', min_age_days=30, include_empty=False)
        self.assertEqual(len(dust_without_empty), 1)
        self.assertNotIn(os.path.join('/test_root', 'empty.txt'), [d['path'] for d in dust_without_empty])
        self.assertIn(os.path.join('/test_root', 'small.txt'), [d['path'] for d in dust_without_empty])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_size_and_age_filters(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['old_small.txt', 'old_large.txt', 'new_small.txt'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=1676294400.0), # old_small.txt (31 days old, 100 bytes) -> DUST
            MagicMock(st_size=2000000, st_mtime=1676294400.0), # old_large.txt (31 days old, 2MB) -> TOO LARGE
            MagicMock(st_size=100, st_mtime=1678022400.0) # new_small.txt (10 days old, 100 bytes) -> TOO NEW
        ]

        # max_size_bytes=1MB (1024*1024), min_age_days=30
        dust = collect_dust('/test_root', max_size_bytes=1024*1024, min_age_days=30)
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test_root', 'old_small.txt'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_non_existent_path(self, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to return False, simulating a path that does not exist.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            collect_dust('/non_existent_path')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_os_error_during_stat(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['file1.txt', 'file2.txt'])
        ]
        # Mock rationale: os.stat is mocked to raise an OSError for one file, simulating a file
        # being deleted or becoming inaccessible after os.walk has listed it.
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=1676294400.0), # file1.txt is fine (DUST)
            OSError("Permission denied") # file2.txt causes an error, should be skipped
        ]

        dust = collect_dust('/test_root')
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], os.path.join('/test_root', 'file1.txt'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_collect_dust_exclude_dirs(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: os.walk is mocked to simulate directory traversal, including directories
        # that should be excluded. The `dirs` list is modified in-place by the utility.
        mock_walk.return_value = [
            ('/test_root', ['.git', 'node_modules', 'src'], ['root_file.txt']),
            ('/test_root/.git', [], ['config']), # Should be excluded
            ('/test_root/node_modules', [], ['package.json']), # Should be excluded
            ('/test_root/src', [], ['source.py']) # Should be included
        ]

        # All files are old and small enough to be dust if not excluded
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=1676294400.0), # root_file.txt
            MagicMock(st_size=50, st_mtime=1676294400.0), # config (will not be stat'd due to exclusion)
            MagicMock(st_size=200, st_mtime=1676294400.0), # package.json (will not be stat'd due to exclusion)
            MagicMock(st_size=150, st_mtime=1676294400.0), # source.py
        ]

        dust = collect_dust('/test_root', exclude_dirs=['.git', 'node_modules'])
        self.assertEqual(len(dust), 2)
        self.assertIn(os.path.join('/test_root', 'root_file.txt'), [d['path'] for d in dust])
        self.assertIn(os.path.join('/test_root', 'src', 'source.py'), [d['path'] for d in dust])
        self.assertNotIn(os.path.join('/test_root', '.git', 'config'), [d['path'] for d in dust])
        self.assertNotIn(os.path.join('/test_root', 'node_modules', 'package.json'), [d['path'] for d in dust])

if __name__ == '__main__':
    unittest.main()
