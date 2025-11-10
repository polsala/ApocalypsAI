import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing collector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import collector

class TestDigitalDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'now' for deterministic age calculations
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0)

    @patch('collector.datetime')
    def test_get_file_age_days(self, mock_dt):
        # Mock rationale: `datetime.now()` needs to be fixed for deterministic age calculation.
        mock_dt.now.return_value = self.mock_now
        mock_dt.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime() constructor

        # Simulate a file modified 100 days ago
        mtime_100_days_ago = (self.mock_now - timedelta(days=100)).timestamp()
        with patch('os.path.getmtime', return_value=mtime_100_days_ago):
            self.assertEqual(collector.get_file_age_days('/fake/path/file.txt'), 100)

        # Simulate a file modified 500 days ago
        mtime_500_days_ago = (self.mock_now - timedelta(days=500)).timestamp()
        with patch('os.path.getmtime', return_value=mtime_500_days_ago):
            self.assertEqual(collector.get_file_age_days('/fake/path/another.txt'), 500)

        # Simulate OSError (file not found/permissions)
        with patch('os.path.getmtime', side_effect=OSError):
            self.assertEqual(collector.get_file_age_days('/nonexistent/file.txt'), -1)

    def test_format_size(self):
        self.assertEqual(collector.format_size(100), "100 Bytes")
        self.assertEqual(collector.format_size(1024), "1.0 KB")
        self.assertEqual(collector.format_size(1536), "1.5 KB")
        self.assertEqual(collector.format_size(1024**2), "1.0 MB")
        self.assertEqual(collector.format_size(1.5 * (1024**2)), "1.5 MB")
        self.assertEqual(collector.format_size(1024**3), "1.0 GB")

    @patch('collector.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies(self, mock_walk, mock_isdir, mock_getsize, mock_getmtime, mock_dt):
        # Mock rationale: `datetime.now()` needs to be fixed for deterministic age calculation.
        # Mock rationale: `os.path.getmtime`, `os.path.getsize`, `os.path.isdir`, `os.walk`
        #                 are mocked to simulate file system state without actual disk I/O.
        mock_dt.now.return_value = self.mock_now
        mock_dt.fromtimestamp = datetime.fromtimestamp
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_isdir.return_value = True

        # Define modification times for various files/dirs
        # Old (older than 365 days)
        old_mtime_ts = (self.mock_now - timedelta(days=400)).timestamp()
        # New (younger than 365 days)
        new_mtime_ts = (self.mock_now - timedelta(days=100)).timestamp()

        # Mock os.walk to simulate a directory structure
        mock_walk.return_value = [
            ('/root', ['dir_old', 'dir_new'], ['file_old.txt', 'file_new.txt']),
            ('/root/dir_old', [], ['nested_old.log']),
            ('/root/dir_new', [], ['nested_new.json'])
        ]

        # Mock getmtime for specific paths
        def mock_getmtime_side_effect(path):
            if 'file_old.txt' in path or 'dir_old' in path or 'nested_old.log' in path:
                return old_mtime_ts
            elif 'file_new.txt' in path or 'dir_new' in path or 'nested_new.json' in path:
                return new_mtime_ts
            raise OSError # Should not happen with mocked paths
        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Mock getsize for specific files
        def mock_getsize_side_effect(path):
            if 'file_old.txt' in path: return 1024
            if 'nested_old.log' in path: return 2048
            if 'file_new.txt' in path: return 512
            if 'nested_new.json' in path: return 256
            raise OSError
        mock_getsize.side_effect = mock_getsize_side_effect

        # Test with default max_age_days (365)
        old_files, old_dirs, total_size = collector.find_dust_bunnies('/root')

        self.assertEqual(len(old_files), 2)
        self.assertEqual(len(old_dirs), 1)
        self.assertEqual(total_size, 1024 + 2048) # file_old.txt + nested_old.log

        # Check specific file details
        old_file_paths = {f['path'] for f in old_files}
        self.assertIn('/root/file_old.txt', old_file_paths)
        self.assertIn('/root/dir_old/nested_old.log', old_file_paths)

        old_dir_paths = {d['path'] for d in old_dirs}
        self.assertIn('/root/dir_old', old_dir_paths)

        # Test with a smaller max_age_days (e.g., 50 days) - everything should be old
        mock_walk.return_value = [
            ('/root', ['dir_old', 'dir_new'], ['file_old.txt', 'file_new.txt']),
            ('/root/dir_old', [], ['nested_old.log']),
            ('/root/dir_new', [], ['nested_new.json'])
        ]
        old_files_50, old_dirs_50, total_size_50 = collector.find_dust_bunnies('/root', max_age_days=50)
        self.assertEqual(len(old_files_50), 4) # All files are older than 50 days
        self.assertEqual(len(old_dirs_50), 2)  # All dirs are older than 50 days
        self.assertEqual(total_size_50, 1024 + 2048 + 512 + 256)

        # Test with an invalid path
        mock_isdir.return_value = False
        old_files_invalid, old_dirs_invalid, total_size_invalid = collector.find_dust_bunnies('/invalid/path')
        self.assertEqual(len(old_files_invalid), 0)
        self.assertEqual(len(old_dirs_invalid), 0)
        self.assertEqual(total_size_invalid, 0)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('collector.find_dust_bunnies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_bunnies(self, mock_parse_args, mock_find_dust_bunnies, mock_stdout):
        # Mock rationale: `argparse` is mocked to control CLI arguments.
        # Mock rationale: `find_dust_bunnies` is mocked to control the scan result.
        # Mock rationale: `sys.stdout` is mocked to capture printed output for assertion.
        mock_parse_args.return_value = MagicMock(path='/test/path', max_age_days=365)
        mock_find_dust_bunnies.return_value = ([], [], 0)

        collector.main()

        mock_stdout.assert_any_call('Scanning /test/path for digital dust bunnies older than 365 days...\n')
        mock_stdout.assert_any_call('No digital dust bunnies found! Your digital space is sparkling clean ✨.\n')

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('collector.find_dust_bunnies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_bunnies(self, mock_parse_args, mock_find_dust_bunnies, mock_stdout):
        # Mock rationale: `argparse` is mocked to control CLI arguments.
        # Mock rationale: `find_dust_bunnies` is mocked to control the scan result.
        # Mock rationale: `sys.stdout` is mocked to capture printed output for assertion.
        mock_parse_args.return_value = MagicMock(path='/test/path', max_age_days=365)
        mock_find_dust_bunnies.return_value = (
            [
                {'path': '/test/path/old_file.txt', 'size': 1024, 'mtime': '2022-01-01'}
            ],
            [
                {'path': '/test/path/old_dir', 'mtime': '2022-02-01'}
            ],
            1024
        )

        collector.main()

        mock_stdout.assert_any_call('Scanning /test/path for digital dust bunnies older than 365 days...\n')
        mock_stdout.assert_any_call('Found 🧹 Digital Dust Bunnies 🧹:\n')
        mock_stdout.assert_any_call('- File: /test/path/old_file.txt (Size: 1.0 KB, Last Modified: 2022-01-01)\n')
        mock_stdout.assert_any_call('- Dir:  /test/path/old_dir (Last Modified: 2022-02-01)\n')
        mock_stdout.assert_any_call('\n--- Summary ---\n')
        mock_stdout.assert_any_call('Total Digital Dust Bunnies Found: 2\n')
        mock_stdout.assert_any_call('Total Size of Files: 1.0 KB\n')

if __name__ == '__main__':
    unittest.main()
