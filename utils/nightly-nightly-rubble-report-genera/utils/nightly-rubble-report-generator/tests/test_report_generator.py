import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Mock rationale: We need to simulate a file system without actually creating files
# or interacting with the real disk, ensuring tests are deterministic and fast.
# os.walk, os.path.exists, os.path.isdir, os.stat are key file system interactions.
# datetime.datetime.now is mocked to ensure consistent "age" calculations.

# Import the functions to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from report_generator import generate_report, format_bytes, format_timedelta

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        # Define a consistent "now" for testing file ages
        self.mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0)
        self.mock_now_timestamp = self.mock_now.timestamp()

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_generate_report_basic(self, mock_stat, mock_walk, mock_isdir, mock_exists, mock_datetime):
        # Mock rationale: datetime.datetime.now() needs to be fixed for consistent age calculation.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate existence and directory status for the root path.
        mock_exists.side_effect = lambda p: p in ['/test_root']
        mock_isdir.side_effect = lambda p: p == '/test_root'

        # Mock rationale: Simulate a file system structure with different file sizes and modification times.
        # Files:
        # - /test_root/dir1/large_old.txt (100MB, 300 days old)
        # - /test_root/dir1/medium_new.txt (20MB, 10 days old)
        # - /test_root/dir2/small_old.txt (5MB, 400 days old)
        # - /test_root/dir2/another_large_new.txt (60MB, 50 days old)
        # - /test_root/empty_file.txt (0MB, 100 days old)

        mock_walk.return_value = [
            ('/test_root', ['dir1', 'dir2'], ['empty_file.txt']),
            ('/test_root/dir1', [], ['large_old.txt', 'medium_new.txt']),
            ('/test_root/dir2', [], ['small_old.txt', 'another_large_new.txt']),
        ]

        # Mock rationale: os.stat needs to return specific size and mtime for each mocked file.
        # mtime calculation: self.mock_now_timestamp - (days * 24 * 60 * 60)
        file_stats = {
            '/test_root/dir1/large_old.txt': MagicMock(st_size=100 * 1024 * 1024, st_mtime=self.mock_now_timestamp - (300 * 24 * 60 * 60)),
            '/test_root/dir1/medium_new.txt': MagicMock(st_size=20 * 1024 * 1024, st_mtime=self.mock_now_timestamp - (10 * 24 * 60 * 60)),
            '/test_root/dir2/small_old.txt': MagicMock(st_size=5 * 1024 * 1024, st_mtime=self.mock_now_timestamp - (400 * 24 * 60 * 60)),
            '/test_root/dir2/another_large_new.txt': MagicMock(st_size=60 * 1024 * 1024, st_mtime=self.mock_now_timestamp - (50 * 24 * 60 * 60)),
            '/test_root/empty_file.txt': MagicMock(st_size=0, st_mtime=self.mock_now_timestamp - (100 * 24 * 60 * 60)),
        }
        mock_stat.side_effect = lambda p: file_stats.get(p, MagicMock(st_size=0, st_mtime=self.mock_now_timestamp))

        paths = ['/test_root']
        min_size_mb = 50
        min_age_days = 180
        top_n = 5

        report = generate_report(paths, min_size_mb, min_age_days, top_n)

        self.assertIn("# Rubble Report for /test_root", report)
        self.assertIn("Total Scanned Size: 185.0 MB", report) # 100+20+5+60+0 = 185MB
        self.assertIn("Total Files Scanned: 5", report)
        self.assertIn("Total Directories Scanned: 3", report) # /test_root, /test_root/dir1, /test_root/dir2

        # Check largest files (>= 50MB)
        self.assertIn("## Top 5 Largest Files (>= 50 MB)", report)
        self.assertIn("1. `100.0 MB` - `/test_root/dir1/large_old.txt`", report)
        self.assertIn("2. `60.0 MB` - `/test_root/dir2/another_large_new.txt`", report)
        self.assertNotIn("medium_new.txt", report) # 20MB < 50MB

        # Check oldest files (>= 180 days)
        self.assertIn("## Top 5 Oldest Files (>= 180 days)", report)
        self.assertIn("1. `1 year, 1 month ago` - `/test_root/dir2/small_old.txt`", report) # 400 days
        self.assertIn("2. `10 months ago` - `/test_root/dir1/large_old.txt`", report) # 300 days
        self.assertNotIn("medium_new.txt", report) # 10 days < 180 days
        self.assertNotIn("another_large_new.txt", report) # 50 days < 180 days

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_generate_report_empty_paths(self, mock_stat, mock_walk, mock_isdir, mock_exists, mock_datetime):
        # Mock rationale: datetime.datetime.now() needs to be fixed for consistent age calculation.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate non-existent paths.
        mock_exists.return_value = False
        mock_isdir.return_value = False
        mock_walk.return_value = [] # No files walked

        paths = ['/non_existent_path']
        min_size_mb = 1
        min_age_days = 1
        top_n = 1

        # Mock rationale: Capture stderr output to check warnings.
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            report = generate_report(paths, min_size_mb, min_age_days, top_n)
            self.assertIn("Warning: Path not found - /non_existent_path", fake_stderr.getvalue())

        self.assertIn("Total Scanned Size: 0.0 B", report)
        self.assertIn("Total Files Scanned: 0", report)
        self.assertIn("Total Directories Scanned: 0", report)
        self.assertIn("No large files found matching criteria.", report)
        self.assertIn("No old files found matching criteria.", report)

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_generate_report_no_matching_files(self, mock_stat, mock_walk, mock_isdir, mock_exists, mock_datetime):
        # Mock rationale: datetime.datetime.now() needs to be fixed for consistent age calculation.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        # Mock rationale: Simulate existence and directory status for the root path.
        mock_exists.side_effect = lambda p: p in ['/test_root']
        mock_isdir.side_effect = lambda p: p == '/test_root'

        # All files are small and new
        mock_walk.return_value = [
            ('/test_root', [], ['file1.txt', 'file2.txt']),
        ]
        file_stats = {
            '/test_root/file1.txt': MagicMock(st_size=100, st_mtime=self.mock_now_timestamp - (10 * 24 * 60 * 60)),
            '/test_root/file2.txt': MagicMock(st_size=200, st_mtime=self.mock_now_timestamp - (20 * 24 * 60 * 60)),
        }
        mock_stat.side_effect = lambda p: file_stats.get(p, MagicMock(st_size=0, st_mtime=self.mock_now_timestamp))

        paths = ['/test_root']
        min_size_mb = 50 # No files will meet this
        min_age_days = 180 # No files will meet this
        top_n = 5

        report = generate_report(paths, min_size_mb, min_age_days, top_n)

        self.assertIn("Total Scanned Size: 300.0 B", report)
        self.assertIn("Total Files Scanned: 2", report)
        self.assertIn("Total Directories Scanned: 1", report)
        self.assertIn("No large files found matching criteria.", report)
        self.assertIn("No old files found matching criteria.", report)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0.0 B")
        self.assertEqual(format_bytes(100), "100.0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.0 MB")
        self.assertEqual(format_bytes(1.5 * 1024 * 1024 * 1024), "1.5 GB")
        self.assertEqual(format_bytes(1024**5), "1.0 PB") # Beyond TB

    def test_format_timedelta(self):
        # Mock rationale: Ensure consistent 'now' for timedelta calculations.
        mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_now_ts = mock_now.timestamp()

        # Test 'today'
        self.assertEqual(format_timedelta(mock_now_ts), "today")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(hours=5).total_seconds()), "today")

        # Test days ago
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=1).total_seconds()), "1 day ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=29).total_seconds()), "29 days ago")

        # Test months ago
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=30).total_seconds()), "1 month ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=60).total_seconds()), "2 months ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=364).total_seconds()), "12 months ago")

        # Test years and months ago
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=365).total_seconds()), "1 year ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=365 + 30).total_seconds()), "1 year, 1 month ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=2 * 365 + 5 * 30).total_seconds()), "2 years, 5 months ago")
        self.assertEqual(format_timedelta(mock_now_ts - datetime.timedelta(days=2 * 365).total_seconds()), "2 years ago")

        # Test future (unlikely but robust)
        self.assertEqual(format_timedelta(mock_now_ts + datetime.timedelta(days=1).total_seconds()), "in the future")


if __name__ == '__main__':
    unittest.main()
