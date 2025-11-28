import unittest
import os
import shutil
import time
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Mock rationale: We need to simulate file system operations (os.walk, os.stat, os.remove, shutil.move, os.makedirs)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't leave artifacts.
# We also mock time.time() to control the 'current' time for age-based checks.

# Import the class to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import CosmicDustCollector

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        self.test_root = '/mock/repo'
        self.archive_path = os.path.join(self.test_root, '.cosmic_dust_archive')
        self.mock_time = time.time()

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_dust_empty_only(self, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time

        # Mock rationale: Simulate a directory structure with various files.
        # We control file sizes and modification times via mock_stat.
        mock_walk.return_value = [
            (self.test_root, ['dir1', 'dir2'], ['file_empty.txt', 'file_small_old.log', 'file_large_new.txt']),
            (os.path.join(self.test_root, 'dir1'), [], ['file_empty_dir1.tmp', 'file_small_new.txt'])
        ]

        # Mock rationale: Define stat results for each file.
        # st_size=0 for empty, st_size=50 for small, st_size=2000 for large.
        # st_mtime for old files is self.mock_time - 100 days, for new files is self.mock_time - 10 days.
        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'file_empty.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (100 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'file_small_old.log'): MagicMock(st_size=50, st_mtime=self.mock_time - (100 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'file_large_new.txt'): MagicMock(st_size=2000, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'dir1', 'file_empty_dir1.tmp'): MagicMock(st_size=0, st_mtime=self.mock_time - (5 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'dir1', 'file_small_new.txt'): MagicMock(st_size=50, st_mtime=self.mock_time - (5 * 24 * 60 * 60)),
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, max_size_bytes=100, max_age_days=90, empty_only=True)
        dust_files = collector.find_dust()

        expected_dust = [
            os.path.join(self.test_root, 'file_empty.txt'),
            os.path.join(self.test_root, 'dir1', 'file_empty_dir1.tmp')
        ]
        self.assertCountEqual(dust_files, expected_dust)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_dust_mixed_criteria(self, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time

        mock_walk.return_value = [
            (self.test_root, ['dir1'], ['empty.txt', 'small_old.log', 'large_old.txt', 'small_new.txt']),
            (os.path.join(self.test_root, 'dir1'), [], ['empty_dir1.tmp', 'small_old_dir1.txt'])
        ]

        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'empty.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'small_old.log'): MagicMock(st_size=50, st_mtime=self.mock_time - (100 * 24 * 60 * 60)), # Dust
            os.path.join(self.test_root, 'large_old.txt'): MagicMock(st_size=2000, st_mtime=self.mock_time - (100 * 24 * 60 * 60)), # Not dust (large)
            os.path.join(self.test_root, 'small_new.txt'): MagicMock(st_size=50, st_mtime=self.mock_time - (10 * 24 * 60 * 60)), # Not dust (new)
            os.path.join(self.test_root, 'dir1', 'empty_dir1.tmp'): MagicMock(st_size=0, st_mtime=self.mock_time - (5 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'dir1', 'small_old_dir1.txt'): MagicMock(st_size=70, st_mtime=self.mock_time - (120 * 24 * 60 * 60)), # Dust
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, max_size_bytes=100, max_age_days=90, empty_only=False)
        dust_files = collector.find_dust()

        expected_dust = [
            os.path.join(self.test_root, 'empty.txt'),
            os.path.join(self.test_root, 'small_old.log'),
            os.path.join(self.test_root, 'dir1', 'empty_dir1.tmp'),
            os.path.join(self.test_root, 'dir1', 'small_old_dir1.txt'),
        ]
        self.assertCountEqual(dust_files, expected_dust)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_dust(self, mock_stdout, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time
        mock_walk.return_value = [
            (self.test_root, [], ['empty.txt', 'small_old.log'])
        ]
        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'empty.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'small_old.log'): MagicMock(st_size=50, st_mtime=self.mock_time - (100 * 24 * 60 * 60)),
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, max_size_bytes=100, max_age_days=90)
        count = collector.list_dust()

        self.assertEqual(count, 2)
        output = mock_stdout.getvalue()
        self.assertIn("Found 2 cosmic dust files:", output)
        self.assertIn(os.path.join(self.test_root, 'empty.txt'), output)
        self.assertIn(os.path.join(self.test_root, 'small_old.log'), output)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('sys.stdout', new_callable=StringIO)
    def test_archive_dust(self, mock_stdout, mock_makedirs, mock_move, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time
        mock_walk.return_value = [
            (self.test_root, ['dir1'], ['empty.txt', 'small_old.log']),
            (os.path.join(self.test_root, 'dir1'), [], ['nested_empty.tmp'])
        ]
        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'empty.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'small_old.log'): MagicMock(st_size=50, st_mtime=self.mock_time - (100 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'dir1', 'nested_empty.tmp'): MagicMock(st_size=0, st_mtime=self.mock_time - (20 * 24 * 60 * 60)),
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, max_size_bytes=100, max_age_days=90)
        count = collector.archive_dust()

        self.assertEqual(count, 3)
        mock_makedirs.assert_any_call(self.archive_path, exist_ok=True)
        mock_move.assert_any_call(os.path.join(self.test_root, 'empty.txt'), os.path.join(self.archive_path, 'empty.txt'))
        mock_move.assert_any_call(os.path.join(self.test_root, 'small_old.log'), os.path.join(self.archive_path, 'small_old.log'))
        mock_move.assert_any_call(os.path.join(self.test_root, 'dir1', 'nested_empty.tmp'), os.path.join(self.archive_path, 'dir1', 'nested_empty.tmp'))
        output = mock_stdout.getvalue()
        self.assertIn("Successfully archived 3 cosmic dust files", output)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    @patch('os.remove')
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_dust(self, mock_stdout, mock_remove, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time
        mock_walk.return_value = [
            (self.test_root, [], ['empty.txt', 'small_old.log'])
        ]
        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'empty.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'small_old.log'): MagicMock(st_size=50, st_mtime=self.mock_time - (100 * 24 * 60 * 60)),
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, max_size_bytes=100, max_age_days=90)
        count = collector.delete_dust()

        self.assertEqual(count, 2)
        mock_remove.assert_any_call(os.path.join(self.test_root, 'empty.txt'))
        mock_remove.assert_any_call(os.path.join(self.test_root, 'small_old.log'))
        output = mock_stdout.getvalue()
        self.assertIn("Successfully deleted 2 cosmic dust files.", output)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_dust_excludes_archive_dir(self, mock_walk, mock_stat, mock_time_func, mock_abspath):
        mock_time_func.return_value = self.mock_time

        # Mock rationale: Simulate a directory structure including the archive directory.
        # The collector should not traverse or find dust within this directory.
        mock_walk.return_value = [
            (self.test_root, ['.cosmic_dust_archive', 'src'], ['file1.txt']),
            (os.path.join(self.test_root, '.cosmic_dust_archive'), [], ['archived_file.txt']),
            (os.path.join(self.test_root, 'src'), [], ['src_file.py'])
        ]

        mock_stat.side_effect = lambda path: {
            os.path.join(self.test_root, 'file1.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, '.cosmic_dust_archive', 'archived_file.txt'): MagicMock(st_size=0, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
            os.path.join(self.test_root, 'src', 'src_file.py'): MagicMock(st_size=1000, st_mtime=self.mock_time - (10 * 24 * 60 * 60)),
        }.get(path, MagicMock(st_size=100, st_mtime=self.mock_time))

        collector = CosmicDustCollector(self.test_root, empty_only=True)
        dust_files = collector.find_dust()

        expected_dust = [
            os.path.join(self.test_root, 'file1.txt'),
        ]
        self.assertCountEqual(dust_files, expected_dust)

if __name__ == '__main__':
    unittest.main()
