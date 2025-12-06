import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.scavenger import scan_directory, get_file_age_days, get_file_size_mb

class TestResourceScavenger(unittest.TestCase):

    def setUp(self):
        # Set a fixed current time for deterministic age calculations
        self.fixed_current_time = datetime(2023, 10, 26, 10, 0, 0).timestamp()

    @patch('time.time')
    @patch('os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime, mock_time):
        # Mock rationale: Ensure deterministic age calculation by fixing current time and file modification time.
        mock_time.return_value = self.fixed_current_time # 2023-10-26
        
        # File modified 100 days ago
        mtime_100_days_ago = (datetime(2023, 10, 26) - timedelta(days=100)).timestamp()
        mock_getmtime.return_value = mtime_100_days_ago
        self.assertAlmostEqual(get_file_age_days('dummy.txt'), 100.0, places=5)

        # File modified 500 days ago
        mtime_500_days_ago = (datetime(2023, 10, 26) - timedelta(days=500)).timestamp()
        mock_getmtime.return_value = mtime_500_days_ago
        self.assertAlmostEqual(get_file_age_days('another_dummy.txt'), 500.0, places=5)

        # Mock os.path.getmtime for a non-existent file
        mock_getmtime.side_effect = FileNotFoundError
        self.assertEqual(get_file_age_days('non_existent.txt'), -1.0)

    @patch('os.path.getsize')
    def test_get_file_size_mb(self, mock_getsize):
        # Mock rationale: Ensure deterministic size calculation without actual file system access.
        
        # 10 MB file
        mock_getsize.return_value = 10 * 1024 * 1024
        self.assertAlmostEqual(get_file_size_mb('file_10mb.txt'), 10.0, places=5)

        # 100 KB file (should be ~0.097 MB)
        mock_getsize.return_value = 100 * 1024
        self.assertAlmostEqual(get_file_size_mb('file_100kb.txt'), 0.09765625, places=5)

        # Mock os.path.getsize for a non-existent file
        mock_getsize.side_effect = FileNotFoundError
        self.assertEqual(get_file_size_mb('non_existent.txt'), 0.0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_basic_functionality(self, mock_time, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system structure and file properties for deterministic testing.
        # Mock rationale: Fix current time for consistent age calculations.
        mock_time.return_value = self.fixed_current_time # 2023-10-26
        mock_isdir.return_value = True

        # Simulate a directory structure
        # root: /test_repo
        #   - large_file.bin (100MB, modified 2023-01-01 -> old)
        #   - small_file.txt (1MB, modified 2023-10-20 -> recent)
        #   - old_doc.pdf (5MB, modified 2022-01-01 -> very old)
        #   - empty_dir/
        #   - sub_dir/
        #     - another_large.log (60MB, modified 2023-09-01 -> recent enough)
        #     - sub_empty_dir/

        mock_walk.return_value = [
            ('/test_repo', ['empty_dir', 'sub_dir'], ['large_file.bin', 'small_file.txt', 'old_doc.pdf']),
            ('/test_repo/empty_dir', [], []),
            ('/test_repo/sub_dir', ['sub_empty_dir'], ['another_large.log']),
            ('/test_repo/sub_dir/sub_empty_dir', [], []),
        ]

        # Mock file sizes
        def mock_getsize_side_effect(path):
            if 'large_file.bin' in path: return 100 * 1024 * 1024 # 100 MB
            if 'small_file.txt' in path: return 1 * 1024 * 1024   # 1 MB
            if 'old_doc.pdf' in path: return 5 * 1024 * 1024    # 5 MB
            if 'another_large.log' in path: return 60 * 1024 * 1024 # 60 MB
            return 0
        mock_getsize.side_effect = mock_getsize_side_effect

        # Mock modification times
        def mock_getmtime_side_effect(path):
            if 'large_file.bin' in path: return datetime(2023, 1, 1).timestamp() # ~300 days old
            if 'small_file.txt' in path: return datetime(2023, 10, 20).timestamp() # ~6 days old
            if 'old_doc.pdf' in path: return datetime(2022, 1, 1).timestamp() # ~660 days old
            if 'another_large.log' in path: return datetime(2023, 9, 1).timestamp() # ~55 days old
            return self.fixed_current_time # Default to recent
        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Run with default thresholds: size_threshold_mb=50, age_threshold_days=365
        findings = scan_directory('/test_repo')

        expected_findings = [
            '[VOID ZONE] /test_repo/empty_dir/',
            '[VOID ZONE] /test_repo/sub_dir/sub_empty_dir/',
            '[OVERSIZED FILE] /test_repo/large_file.bin (100.0 MB)',
            '[ANCIENT ARTIFACT] /test_repo/old_doc.pdf (Last modified: 2022-01-01)',
            '[OVERSIZED FILE] /test_repo/sub_dir/another_large.log (60.0 MB)'
        ]
        self.assertCountEqual(findings, expected_findings)

    @patch('os.path.isdir', return_value=False)
    def test_scan_directory_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        findings = scan_directory('/non_existent_path')
        self.assertEqual(findings, ["Error: Path '/non_existent_path' is not a valid directory."])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/test_repo', [], [])])
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_no_findings(self, mock_time, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a clean directory with no issues.
        mock_time.return_value = self.fixed_current_time
        mock_getsize.return_value = 1 * 1024 * 1024 # 1 MB
        mock_getmtime.return_value = self.fixed_current_time - timedelta(days=10).total_seconds() # 10 days old

        findings = scan_directory('/test_repo', size_threshold_mb=10, age_threshold_days=30)
        self.assertEqual(findings, [])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_custom_thresholds(self, mock_time, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test with custom size and age thresholds.
        mock_time.return_value = self.fixed_current_time # 2023-10-26

        mock_walk.return_value = [
            ('/test_repo', [], ['medium_file.data', 'very_old_log.txt']),
        ]

        # Mock file sizes
        def mock_getsize_side_effect(path):
            if 'medium_file.data' in path: return 20 * 1024 * 1024 # 20 MB
            if 'very_old_log.txt' in path: return 1 * 1024 * 1024 # 1 MB
            return 0
        mock_getsize.side_effect = mock_getsize_side_effect

        # Mock modification times
        def mock_getmtime_side_effect(path):
            if 'medium_file.data' in path: return datetime(2023, 5, 1).timestamp() # ~178 days old
            if 'very_old_log.txt' in path: return datetime(2020, 1, 1).timestamp() # ~1394 days old
            return self.fixed_current_time
        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Run with custom thresholds: size_threshold_mb=15, age_threshold_days=180
        findings = scan_directory('/test_repo', size_threshold_mb=15, age_threshold_days=180)

        expected_findings = [
            '[OVERSIZED FILE] /test_repo/medium_file.data (20.0 MB)',
            '[ANCIENT ARTIFACT] /test_repo/very_old_log.txt (Last modified: 2020-01-01)'
        ]
        self.assertCountEqual(findings, expected_findings)

if __name__ == '__main__':
    unittest.main()
