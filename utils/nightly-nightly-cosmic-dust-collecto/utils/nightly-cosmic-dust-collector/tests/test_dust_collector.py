import unittest
import os
import time
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Assume dust_collector.py is in the parent directory of tests/
# To run tests, you might need to adjust sys.path or run from the project root
# For self-contained utility, we'll assume it's run from its own directory or path is set.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import find_dust_files, is_dust_file, main

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age calculations
        self.mock_current_time = time.mktime((datetime(2023, 10, 26, 10, 0, 0)).timetuple())
        # Mock os.stat to return consistent values
        self.mock_stat_results = {}

    def mock_os_stat(self, path):
        # Mock rationale: os.stat interacts with the file system, which is non-deterministic
        # and slow. We mock it to control file properties (size, mtime) for tests.
        if path in self.mock_stat_results:
            mock_stat = MagicMock()
            mock_stat.st_size = self.mock_stat_results[path]['size']
            mock_stat.st_mtime = self.mock_stat_results[path]['mtime']
            return mock_stat
        raise FileNotFoundError(f"Mock stat for {path} not found.")

    @patch('time.time')
    @patch('os.stat')
    def test_is_dust_file_empty(self, mock_stat, mock_time):
        # Mock rationale: time.time() returns current time, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        filepath = "/mock/path/empty.txt"
        self.mock_stat_results[filepath] = {'size': 0, 'mtime': self.mock_current_time}
        is_dust, reason = is_dust_file(filepath, 30, 1, self.mock_current_time)
        self.assertTrue(is_dust)
        self.assertEqual(reason, "empty")

    @patch('time.time')
    @patch('os.stat')
    def test_is_dust_file_small(self, mock_stat, mock_time):
        # Mock rationale: time.time() returns current time, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        filepath = "/mock/path/small.txt"
        # 0.5 KB = 512 bytes
        self.mock_stat_results[filepath] = {'size': 512, 'mtime': self.mock_current_time}
        is_dust, reason = is_dust_file(filepath, 30, 1, self.mock_current_time) # max_size_kb=1 (1024 bytes)
        self.assertTrue(is_dust)
        self.assertEqual(reason, "smaller than 1KB")

    @patch('time.time')
    @patch('os.stat')
    def test_is_dust_file_old(self, mock_stat, mock_time):
        # Mock rationale: time.time() returns current time, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        filepath = "/mock/path/old.txt"
        # File modified 31 days ago
        old_mtime = time.mktime((datetime(2023, 9, 25, 10, 0, 0)).timetuple())
        self.mock_stat_results[filepath] = {'size': 2048, 'mtime': old_mtime} # 2KB
        is_dust, reason = is_dust_file(filepath, 30, 1, self.mock_current_time) # min_age_days=30, max_size_kb=1
        self.assertTrue(is_dust)
        self.assertEqual(reason, "older than 30 days")

    @patch('time.time')
    @patch('os.stat')
    def test_is_dust_file_not_dust(self, mock_stat, mock_time):
        # Mock rationale: time.time() returns current time, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        filepath = "/mock/path/clean.txt"
        # File modified recently, large enough
        recent_mtime = time.mktime((datetime(2023, 10, 20, 10, 0, 0)).timetuple())
        self.mock_stat_results[filepath] = {'size': 2048, 'mtime': recent_mtime} # 2KB
        is_dust, reason = is_dust_file(filepath, 30, 1, self.mock_current_time)
        self.assertFalse(is_dust)
        self.assertEqual(reason, "")

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_dust_files_basic(self, mock_walk, mock_stat, mock_time):
        # Mock rationale: os.walk() traverses the file system, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        # time.time() returns current time, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/mock/root', ['subdir'], ['empty.txt', 'small.txt', 'old.txt', 'clean.txt']),
            ('/mock/root/subdir', [], ['another_old.log'])
        ]

        # Define mock stat results for files
        old_mtime = time.mktime((datetime(2023, 9, 25, 10, 0, 0)).timetuple()) # 31 days old
        recent_mtime = time.mktime((datetime(2023, 10, 20, 10, 0, 0)).timetuple()) # 6 days old

        self.mock_stat_results = {
            '/mock/root/empty.txt': {'size': 0, 'mtime': recent_mtime},
            '/mock/root/small.txt': {'size': 512, 'mtime': recent_mtime}, # 0.5KB
            '/mock/root/old.txt': {'size': 2048, 'mtime': old_mtime}, # 2KB
            '/mock/root/clean.txt': {'size': 2048, 'mtime': recent_mtime}, # 2KB
            '/mock/root/subdir/another_old.log': {'size': 100, 'mtime': old_mtime} # 0.1KB
        }

        dust_files = find_dust_files('/mock/root', min_age_days=30, max_size_kb=1, exclude_patterns="")
        
        expected_dust = [
            ('/mock/root/empty.txt', 'empty'),
            ('/mock/root/small.txt', 'smaller than 1KB'),
            ('/mock/root/old.txt', 'older than 30 days'),
            ('/mock/root/subdir/another_old.log', 'smaller than 1KB') # Also old, but small takes precedence in is_dust_file
        ]
        
        # Sort for consistent comparison
        self.assertEqual(sorted(dust_files), sorted(expected_dust))

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_dust_files_with_exclude(self, mock_walk, mock_stat, mock_time):
        # Mock rationale: os.walk() traverses the file system, non-deterministic.
        # os.stat() accesses file system, non-deterministic.
        # time.time() returns current time, non-deterministic.
        mock_time.return_value = self.mock_current_time
        mock_stat.side_effect = self.mock_os_stat

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/mock/root', ['excluded_dir', 'subdir'], ['empty.txt', 'temp.log']),
            ('/mock/root/excluded_dir', [], ['should_be_ignored.txt']),
            ('/mock/root/subdir', [], ['another_old.log'])
        ]

        old_mtime = time.mktime((datetime(2023, 9, 25, 10, 0, 0)).timetuple()) # 31 days old
        recent_mtime = time.mktime((datetime(2023, 10, 20, 10, 0, 0)).timetuple()) # 6 days old

        self.mock_stat_results = {
            '/mock/root/empty.txt': {'size': 0, 'mtime': recent_mtime},
            '/mock/root/temp.log': {'size': 100, 'mtime': recent_mtime}, # 0.1KB
            '/mock/root/excluded_dir/should_be_ignored.txt': {'size': 0, 'mtime': recent_mtime},
            '/mock/root/subdir/another_old.log': {'size': 100, 'mtime': old_mtime} # 0.1KB
        }

        # Exclude 'excluded_dir' and all '*.log' files
        dust_files = find_dust_files('/mock/root', min_age_days=30, max_size_kb=1, exclude_patterns="excluded_dir/*,*.log")
        
        expected_dust = [
            ('/mock/root/empty.txt', 'empty')
            # '/mock/root/temp.log' is excluded by *.log
            # '/mock/root/excluded_dir/should_be_ignored.txt' is excluded by excluded_dir/*
            # '/mock/root/subdir/another_old.log' is excluded by *.log
        ]
        
        self.assertEqual(sorted(dust_files), sorted(expected_dust))

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('os.remove')
    @patch('dust_collector.find_dust_files') # Mock rationale: Avoid actual file system interaction
    @patch('os.path.isdir') # Mock rationale: Avoid actual file system interaction
    def test_main_delete_files(self, mock_isdir, mock_find_dust_files, mock_remove, mock_stdout):
        # Mock rationale: os.path.isdir checks file system. find_dust_files is already tested
        # and interacts with os.walk/os.stat. os.remove performs file deletion.
        # We mock these to isolate the main function's logic and prevent actual file changes.
        mock_isdir.return_value = True
        mock_find_dust_files.return_value = [
            ("/mock/path/dust1.txt", "empty"),
            ("/mock/path/dust2.txt", "old")
        ]

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/mock/path", min_age_days=30, max_size_kb=1, delete=True, exclude=""
        )):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Expect successful exit

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call("/mock/path/dust1.txt")
        mock_remove.assert_any_call("/mock/path/dust2.txt")
        self.assertIn("Successfully deleted 2 files.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('dust_collector.find_dust_files') # Mock rationale: Avoid actual file system interaction
    @patch('os.path.isdir') # Mock rationale: Avoid actual file system interaction
    def test_main_list_files(self, mock_isdir, mock_find_dust_files, mock_stdout):
        # Mock rationale: os.path.isdir checks file system. find_dust_files is already tested
        # and interacts with os.walk/os.stat.
        mock_isdir.return_value = True
        mock_find_dust_files.return_value = [
            ("/mock/path/dust1.txt", "empty"),
            ("/mock/path/dust2.txt", "old")
        ]

        # Simulate command line arguments without --delete
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/mock/path", min_age_days=30, max_size_kb=1, delete=False, exclude=""
        )):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Expect successful exit

        self.assertIn("Found 2 cosmic dust files:", mock_stdout.getvalue())
        self.assertIn("- /mock/path/dust1.txt (Reason: empty)", mock_stdout.getvalue())
        self.assertIn("- /mock/path/dust2.txt (Reason: old)", mock_stdout.getvalue())
        self.assertIn("To delete these files, run the command again with the '--delete' flag.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('dust_collector.find_dust_files') # Mock rationale: Avoid actual file system interaction
    @patch('os.path.isdir') # Mock rationale: Avoid actual file system interaction
    def test_main_no_dust_found(self, mock_isdir, mock_find_dust_files, mock_stdout):
        # Mock rationale: os.path.isdir checks file system. find_dust_files is already tested
        # and interacts with os.walk/os.stat.
        mock_isdir.return_value = True
        mock_find_dust_files.return_value = []

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/mock/path", min_age_days=30, max_size_kb=1, delete=False, exclude=""
        )):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Expect successful exit

        self.assertIn("No cosmic dust found. Your repository is sparkling clean!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('os.path.isdir') # Mock rationale: Avoid actual file system interaction
    def test_main_invalid_path(self, mock_isdir, mock_stdout):
        # Mock rationale: os.path.isdir checks file system.
        mock_isdir.return_value = False

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/invalid/path", min_age_days=30, max_size_kb=1, delete=False, exclude=""
        )):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1) # Expect error exit

        self.assertIn("Error: Path '/invalid/path' is not a valid directory.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
