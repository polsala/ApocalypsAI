import unittest
import os
import shutil
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the function to test
from src.dust_collector import collect_cosmic_dust, main

class MockStat:
    def __init__(self, size, mtime):
        self.st_size = size
        self.st_mtime = mtime

class TestCosmicDustCollector(unittest.TestCase):

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('src.dust_collector.os.path.exists')
    def test_collect_cosmic_dust_list_mode(self, mock_exists, mock_move, mock_makedirs, mock_stat, mock_walk, mock_datetime):
        # Mock rationale: Ensure deterministic current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26)
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a file system structure.
        mock_walk.return_value = [
            ('/test_dir', ('subdir1',), ('file1.txt', 'file2.log', 'large_file.txt')),
            ('/test_dir/subdir1', (), ('empty.txt', 'old_small.tmp')),
        ]

        # Mock rationale: Control file properties (size, modification time) for testing dust criteria.
        def mock_os_stat(path):
            if path == '/test_dir/file1.txt':
                # Small, old file (dust)
                return MockStat(size=500, mtime=datetime.datetime(2023, 9, 1).timestamp())
            elif path == '/test_dir/file2.log':
                # Small, but recent file (not dust)
                return MockStat(size=800, mtime=datetime.datetime(2023, 10, 20).timestamp())
            elif path == '/test_dir/large_file.txt':
                # Large file (not dust)
                return MockStat(size=20000, mtime=datetime.datetime(2023, 8, 1).timestamp())
            elif path == '/test_dir/subdir1/empty.txt':
                # Empty file (dust)
                return MockStat(size=0, mtime=datetime.datetime(2023, 10, 1).timestamp())
            elif path == '/test_dir/subdir1/old_small.tmp':
                # Old and small file (dust)
                return MockStat(size=100, mtime=datetime.datetime(2023, 7, 1).timestamp())
            raise FileNotFoundError # Should not happen with mock_walk setup

        mock_stat.side_effect = mock_os_stat
        mock_exists.return_value = False # Mock rationale: Assume no duplicate names in dustbin initially.

        # Test with default parameters (max_size_kb=1, min_age_days=30)
        dust_files = collect_cosmic_dust('/test_dir')

        self.assertEqual(len(dust_files), 3)
        self.assertIn(('/test_dir/file1.txt', 'small (<1KB), old (>30 days)'), dust_files)
        self.assertIn(('/test_dir/subdir1/empty.txt', 'empty, small (<1KB)'), dust_files)
        self.assertIn(('/test_dir/subdir1/old_small.tmp', 'small (<1KB), old (>30 days)'), dust_files)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('src.dust_collector.os.path.exists')
    def test_collect_cosmic_dust_move_mode(self, mock_exists, mock_move, mock_makedirs, mock_stat, mock_walk, mock_datetime):
        # Mock rationale: Ensure deterministic current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26)
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a file system structure.
        mock_walk.return_value = [
            ('/test_dir', ('subdir1',), ('file1.txt', 'file2.log')),
            ('/test_dir/subdir1', (), ('empty.txt',)),
        ]

        # Mock rationale: Control file properties (size, modification time) for testing dust criteria.
        def mock_os_stat(path):
            if path == '/test_dir/file1.txt':
                return MockStat(size=500, mtime=datetime.datetime(2023, 9, 1).timestamp())
            elif path == '/test_dir/file2.log':
                return MockStat(size=800, mtime=datetime.datetime(2023, 10, 20).timestamp()) # Not dust
            elif path == '/test_dir/subdir1/empty.txt':
                return MockStat(size=0, mtime=datetime.datetime(2023, 10, 1).timestamp())
            raise FileNotFoundError

        mock_stat.side_effect = mock_os_stat
        mock_exists.return_value = False # Mock rationale: Assume no duplicate names in dustbin initially.

        dust_files = collect_cosmic_dust('/test_dir', action='move', dustbin_dir='my_dust')

        self.assertEqual(len(dust_files), 2)
        self.assertIn(('/test_dir/file1.txt', 'small (<1KB), old (>30 days)'), dust_files)
        self.assertIn(('/test_dir/subdir1/empty.txt', 'empty, small (<1KB)'), dust_files)

        mock_makedirs.assert_called_once_with('/test_dir/my_dust', exist_ok=True)
        mock_move.assert_any_call('/test_dir/file1.txt', '/test_dir/my_dust/file1.txt')
        mock_move.assert_any_call('/test_dir/subdir1/empty.txt', '/test_dir/my_dust/empty.txt')
        self.assertEqual(mock_move.call_count, 2)

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('src.dust_collector.os.path.exists')
    def test_collect_cosmic_dust_move_mode_with_existing_file_in_dustbin(self, mock_exists, mock_move, mock_makedirs, mock_stat, mock_walk, mock_datetime):
        # Mock rationale: Ensure deterministic current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26)
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a file system structure.
        mock_walk.return_value = [
            ('/test_dir', (), ('duplicate.txt',)),
        ]

        # Mock rationale: Control file properties (size, modification time) for testing dust criteria.
        def mock_os_stat(path):
            if path == '/test_dir/duplicate.txt':
                return MockStat(size=100, mtime=datetime.datetime(2023, 9, 1).timestamp())
            raise FileNotFoundError

        mock_stat.side_effect = mock_os_stat

        # Mock rationale: Simulate a file with the same name already existing in the dustbin.
        # First call for 'duplicate.txt' in dustbin returns True, second for 'duplicate_1.txt' returns False.
        mock_exists.side_effect = [True, False]

        dust_files = collect_cosmic_dust('/test_dir', action='move', dustbin_dir='my_dust')

        self.assertEqual(len(dust_files), 1)
        self.assertIn(('/test_dir/duplicate.txt', 'small (<1KB), old (>30 days)'), dust_files)

        mock_makedirs.assert_called_once_with('/test_dir/my_dust', exist_ok=True)
        mock_move.assert_called_once_with('/test_dir/duplicate.txt', '/test_dir/my_dust/duplicate_1.txt')
        self.assertEqual(mock_exists.call_count, 2) # Checks for original name, then for _1 name.

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('src.dust_collector.os.path.exists')
    def test_collect_cosmic_dust_no_dust(self, mock_exists, mock_move, mock_makedirs, mock_stat, mock_walk, mock_datetime):
        # Mock rationale: Ensure deterministic current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26)
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a file system with no dust files.
        mock_walk.return_value = [
            ('/test_dir', (), ('recent_large.txt',)),
        ]
        def mock_os_stat(path):
            if path == '/test_dir/recent_large.txt':
                return MockStat(size=50000, mtime=datetime.datetime(2023, 10, 25).timestamp())
            raise FileNotFoundError
        mock_stat.side_effect = mock_os_stat
        mock_exists.return_value = False

        dust_files = collect_cosmic_dust('/test_dir')

        self.assertEqual(len(dust_files), 0)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('src.dust_collector.os.path.isdir')
    @patch('src.dust_collector.collect_cosmic_dust')
    @patch('src.dust_collector.argparse.ArgumentParser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_list_output(self, mock_stdout, mock_argparse, mock_collect, mock_isdir):
        # Mock rationale: Simulate command-line arguments.
        mock_args = MagicMock()
        mock_args.directory = '/mock_dir'
        mock_args.max_size_kb = 1
        mock_args.min_age_days = 30
        mock_args.action = 'list'
        mock_args.dustbin_dir = 'cosmic_dustbin'
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate identified dust files.
        mock_collect.return_value = [
            ('/mock_dir/file1.txt', 'small, old'),
            ('/mock_dir/subdir/empty.txt', 'empty')
        ]

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning '/mock_dir' for cosmic dust", output)
        self.assertIn("- /mock_dir/file1.txt (Reason: small, old)", output)
        self.assertIn("- /mock_dir/subdir/empty.txt (Reason: empty)", output)
        self.assertIn("Total dust files identified: 2", output)
        mock_collect.assert_called_once_with('/mock_dir', 1, 30, 'list', 'cosmic_dustbin')

    @patch('src.dust_collector.os.path.isdir')
    @patch('src.dust_collector.collect_cosmic_dust')
    @patch('src.dust_collector.argparse.ArgumentParser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_dust_output(self, mock_stdout, mock_argparse, mock_collect, mock_isdir):
        # Mock rationale: Simulate command-line arguments.
        mock_args = MagicMock()
        mock_args.directory = '/mock_dir'
        mock_args.max_size_kb = 1
        mock_args.min_age_days = 30
        mock_args.action = 'list'
        mock_args.dustbin_dir = 'cosmic_dustbin'
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True

        # Mock rationale: Simulate no identified dust files.
        mock_collect.return_value = []

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning '/mock_dir' for cosmic dust", output)
        self.assertIn("No cosmic dust found. Your digital space is pristine!", output)
        mock_collect.assert_called_once_with('/mock_dir', 1, 30, 'list', 'cosmic_dustbin')

    @patch('src.dust_collector.os.path.isdir')
    @patch('src.dust_collector.collect_cosmic_dust')
    @patch('src.dust_collector.argparse.ArgumentParser')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_invalid_directory(self, mock_exit, mock_stdout, mock_argparse, mock_collect, mock_isdir):
        # Mock rationale: Simulate command-line arguments.
        mock_args = MagicMock()
        mock_args.directory = '/non_existent_dir'
        mock_args.max_size_kb = 1
        mock_args.min_age_days = 30
        mock_args.action = 'list'
        mock_args.dustbin_dir = 'cosmic_dustbin'
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock rationale: Simulate directory not existing.
        mock_isdir.return_value = False

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Error: Directory '/non_existent_dir' not found.", output)
        mock_exit.assert_called_once_with(1)
        mock_collect.assert_not_called()

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('src.dust_collector.os.path.exists')
    def test_collect_cosmic_dust_ignores_dustbin_in_move_mode(self, mock_exists, mock_move, mock_makedirs, mock_stat, mock_walk, mock_datetime):
        # Mock rationale: Ensure deterministic current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26)
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate a file system structure where the dustbin itself contains files.
        # The walk should not process files *inside* the dustbin when in move mode.
        mock_walk.return_value = [
            ('/test_dir', ('cosmic_dustbin',), ('file_to_move.txt',)),
            ('/test_dir/cosmic_dustbin', (), ('already_moved.txt',)), # This should be ignored
        ]

        def mock_os_stat(path):
            if path == '/test_dir/file_to_move.txt':
                return MockStat(size=100, mtime=datetime.datetime(2023, 9, 1).timestamp())
            elif path == '/test_dir/cosmic_dustbin/already_moved.txt':
                return MockStat(size=50, mtime=datetime.datetime(2023, 8, 1).timestamp())
            raise FileNotFoundError

        mock_stat.side_effect = mock_os_stat
        mock_exists.return_value = False

        dust_files = collect_cosmic_dust('/test_dir', action='move', dustbin_dir='cosmic_dustbin')

        self.assertEqual(len(dust_files), 1)
        self.assertIn(('/test_dir/file_to_move.txt', 'small (<1KB), old (>30 days)'), dust_files)
        mock_move.assert_called_once_with('/test_dir/file_to_move.txt', '/test_dir/cosmic_dustbin/file_to_move.txt')
        mock_makedirs.assert_called_once_with('/test_dir/cosmic_dustbin', exist_ok=True)

if __name__ == '__main__':
    unittest.main()
