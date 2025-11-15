import unittest
from unittest.mock import patch, MagicMock
import time
from datetime import datetime, timedelta
import sys
import io

# Mock rationale: We need to test file system scanning logic without actually
# creating files on disk, which would make tests non-deterministic and slow.
# Mocking os.walk, os.stat, and os.path.isdir allows us to simulate various
# file system structures and file properties (size, modification time)
# in a controlled and fast manner.

# Import the functions to be tested
sys.path.insert(0, 'utils/digital-dust-bunny-sweeper/src')
from sweeper import scan_directory, format_size, main

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print output
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(500), "500 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024**2), "1.0 MB")
        self.assertEqual(format_size(1.5 * (1024**2)), "1.5 MB")
        self.assertEqual(format_size(1024**3), "1.0 GB")
        self.assertEqual(format_size(2.3 * (1024**3)), "2.3 GB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory_finds_large_files(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate a directory structure with files of various sizes.
        # We need to control the reported size for each file.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log', 'subdir/file3.bin'])
        ]

        # Mock rationale: Simulate file stats for each file.
        # file1.txt: small
        # file2.log: large
        # file3.bin: large (nested)
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'file1.txt' in path:
                mock_stat_obj.st_size = 50 * (1024**2) # 50 MB
                mock_stat_obj.st_mtime = time.time()
            elif 'file2.log' in path:
                mock_stat_obj.st_size = 150 * (1024**2) # 150 MB
                mock_stat_obj.st_mtime = time.time()
            elif 'file3.bin' in path:
                mock_stat_obj.st_size = 200 * (1024**2) # 200 MB
                mock_stat_obj.st_mtime = time.time()
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        large, old = scan_directory('/test_dir', min_size_mb=100, min_age_days=365)

        self.assertEqual(len(large), 2)
        self.assertTrue(any('file2.log' in f['path'] for f in large))
        self.assertTrue(any('file3.bin' in f['path'] for f in large))
        self.assertEqual(len(old), 0) # No old files in this test

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory_finds_old_files(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate a directory structure with files of various ages.
        # We need to control the reported modification time for each file.
        mock_walk.return_value = [
            ('/test_dir', [], ['recent.txt', 'old.log', 'ancient/very_old.py'])
        ]

        now = time.time()
        one_year_ago = now - (366 * 24 * 60 * 60) # More than 365 days ago
        six_months_ago = now - (180 * 24 * 60 * 60)

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_size = 100 # Small size, not relevant for age test
            if 'recent.txt' in path:
                mock_stat_obj.st_mtime = six_months_ago
            elif 'old.log' in path:
                mock_stat_obj.st_mtime = one_year_ago
            elif 'very_old.py' in path:
                mock_stat_obj.st_mtime = one_year_ago - (365 * 24 * 60 * 60) # Even older
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        large, old = scan_directory('/test_dir', min_size_mb=1000, min_age_days=365) # High size threshold

        self.assertEqual(len(large), 0)
        self.assertEqual(len(old), 2)
        self.assertTrue(any('old.log' in f['path'] for f in old))
        self.assertTrue(any('very_old.py' in f['path'] for f in old))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory_no_matches(self, mock_stat, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate a directory where no files meet the criteria.
        mock_walk.return_value = [
            ('/test_dir', [], ['small_recent.txt'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_size = 10 * (1024**2) # 10 MB
            mock_stat_obj.st_mtime = time.time() - (30 * 24 * 60 * 60) # 30 days ago
            return mock_stat_obj

        mock_stat.side_effect = mock_stat_side_effect

        large, old = scan_directory('/test_dir', min_size_mb=100, min_age_days=365)

        self.assertEqual(len(large), 0)
        self.assertEqual(len(old), 0)

    @patch('os.path.isdir')
    def test_scan_directory_invalid_path(self, mock_isdir):
        mock_isdir.return_value = False
        # Mock rationale: Test error handling for non-existent directories.
        large, old = scan_directory('/non_existent_dir')
        self.assertEqual(len(large), 0)
        self.assertEqual(len(old), 0)
        self.assertIn("Error: Directory not found", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.scan_directory') # Mock rationale: Isolate main function from file system ops
    def test_main_no_dust_bunnies(self, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and no findings.
        mock_parse_args.return_value = MagicMock(
            directory_path='/mock_dir',
            min_size_mb=100,
            min_age_days=365
        )
        mock_scan_directory.return_value = ([], []) # No large, no old files

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Scanning directory: /mock_dir", output)
        self.assertIn("No dust bunnies found matching criteria.", output)
        mock_scan_directory.assert_called_once_with('/mock_dir', 100, 365)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.scan_directory')
    def test_main_with_dust_bunnies(self, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and some findings.
        mock_parse_args.return_value = MagicMock(
            directory_path='/mock_dir',
            min_size_mb=10,
            min_age_days=30
        )

        now = time.time()
        old_time = now - (60 * 24 * 60 * 60) # 60 days ago

        mock_scan_directory.return_value = (
            [{'path': '/mock_dir/large.bin', 'size': 20 * (1024**2), 'mtime': now}],
            [{'path': '/mock_dir/old.log', 'size': 5 * (1024**2), 'mtime': old_time}]
        )

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Large Files (>= 10.0 MB):", output)
        self.assertIn("/mock_dir/large.bin (Size: 20.0 MB", output)
        self.assertIn("Ancient Files (Modified >= 30 days ago):", output)
        self.assertIn("/mock_dir/old.log (Size: 5.0 MB", output)
        self.assertNotIn("No dust bunnies found", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.scan_directory')
    def test_main_invalid_directory_path(self, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate an invalid directory path passed to main.
        mock_parse_args.return_value = MagicMock(
            directory_path='/non_existent_dir',
            min_size_mb=100,
            min_age_days=365
        )
        # The scan_directory function itself will print the error
        mock_scan_directory.return_value = ([], []) # It will return empty lists after printing error

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Directory not found at '/non_existent_dir'", output)
        # Ensure it still prints the "No dust bunnies found" if scan_directory returns empty lists
        self.assertIn("No dust bunnies found matching criteria.", output)


if __name__ == '__main__':
    unittest.main()
