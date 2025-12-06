import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta
import io
import sys

# Import the functions to be tested
from src.cleaner import scan_directory, get_file_info, main

class TestCataclysmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.stat')
    def test_get_file_info_success(self, mock_stat):
        # Mock rationale: Simulate a successful os.stat call for a file.
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = 1678886400.0 # March 15, 2023 12:00:00 PM UTC
        mock_stat_result.st_size = 1024 * 1024 # 1 MB
        mock_stat.return_value = mock_stat_result

        mtime, size = get_file_info("/mock/path/file.txt")
        self.assertEqual(mtime, 1678886400.0)
        self.assertEqual(size, 1024 * 1024)
        mock_stat.assert_called_once_with("/mock/path/file.txt")

    @patch('os.stat', side_effect=FileNotFoundError)
    def test_get_file_info_not_found(self, mock_stat):
        # Mock rationale: Simulate a FileNotFoundError when trying to stat a non-existent file.
        mtime, size = get_file_info("/mock/path/non_existent.txt")
        self.assertIsNone(mtime)
        self.assertIsNone(size)
        mock_stat.assert_called_once_with("/mock/path/non_existent.txt")

    @patch('src.cleaner.get_file_info')
    @patch('os.walk')
    def test_scan_directory_no_candidates(self, mock_os_walk, mock_get_file_info):
        # Mock rationale: Simulate a directory with files that do not meet the criteria.
        current_time = datetime(2023, 3, 20)
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'file2.log'])
        ]
        mock_get_file_info.side_effect = [
            # file1.txt: young, small
            (datetime(2023, 3, 19).timestamp(), 10 * 1024 * 1024), # 1 day old, 10 MB
            # file2.log: old, but small
            (datetime(2023, 1, 1).timestamp(), 5 * 1024 * 1024), # ~78 days old, 5 MB
        ]

        candidates = scan_directory('/mock/dir', min_age_days=30, min_size_mb=50, current_time=current_time)
        self.assertEqual(len(candidates), 0)

    @patch('src.cleaner.get_file_info')
    @patch('os.walk')
    def test_scan_directory_with_candidates(self, mock_os_walk, mock_get_file_info):
        # Mock rationale: Simulate a directory with files, some of which meet the criteria.
        current_time = datetime(2023, 3, 20)
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'file2.log', 'file3.bak'])
        ]
        mock_get_file_info.side_effect = [
            # file1.txt: young, small
            (datetime(2023, 3, 19).timestamp(), 10 * 1024 * 1024), # 1 day old, 10 MB
            # file2.log: old, large - CANDIDATE
            (datetime(2023, 1, 1).timestamp(), 70 * 1024 * 1024), # ~78 days old, 70 MB
            # file3.bak: old, but small
            (datetime(2022, 12, 1).timestamp(), 20 * 1024 * 1024), # ~109 days old, 20 MB
        ]

        candidates = scan_directory('/mock/dir', min_age_days=30, min_size_mb=50, current_time=current_time)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0][0], os.path.join('/mock/dir', 'file2.log'))
        self.assertEqual(candidates[0][1], 78) # Age in days
        self.assertAlmostEqual(candidates[0][2], 70.0, places=1) # Size in MB

    @patch('src.cleaner.get_file_info')
    @patch('os.walk')
    def test_scan_directory_multiple_paths_and_subdirs(self, mock_os_walk, mock_get_file_info):
        # Mock rationale: Simulate scanning multiple directories and subdirectories with various files.
        current_time = datetime(2023, 3, 20)
        mock_os_walk.side_effect = [
            # First path: /mock/dir1
            [
                ('/mock/dir1', ['subdir_a'], ['file_a.txt']),
                ('/mock/dir1/subdir_a', [], ['file_b.log'])
            ],
            # Second path: /mock/dir2
            [
                ('/mock/dir2', [], ['file_c.bak'])
            ]
        ]
        mock_get_file_info.side_effect = [
            # /mock/dir1/file_a.txt: old, large - CANDIDATE
            (datetime(2022, 10, 1).timestamp(), 150 * 1024 * 1024), # ~170 days old, 150 MB
            # /mock/dir1/subdir_a/file_b.log: young, small
            (datetime(2023, 3, 10).timestamp(), 5 * 1024 * 1024), # 10 days old, 5 MB
            # /mock/dir2/file_c.bak: old, large - CANDIDATE
            (datetime(2022, 11, 1).timestamp(), 80 * 1024 * 1024), # ~139 days old, 80 MB
        ]

        # Mock argparse for main function
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('os.path.isdir', return_value=True), \
             patch('src.cleaner.datetime') as mock_datetime:
            mock_parse_args.return_value = MagicMock(
                path=['/mock/dir1', '/mock/dir2'],
                min_age=30,
                min_size=50
            )
            mock_datetime.now.return_value = current_time
            mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp

            main()

            output = self.mock_stdout.getvalue()
            self.assertIn("Total Cataclysmic Candidates Found: 2", output)
            self.assertIn(f"  {os.path.join('/mock/dir1', 'file_a.txt')} (Age: 170 days, Size: 150.0 MB) - Candidate!", output)
            self.assertIn(f"  {os.path.join('/mock/dir2', 'file_c.bak')} (Age: 139 days, Size: 80.0 MB) - Candidate!", output)
            self.assertNotIn(f"  {os.path.join('/mock/dir1/subdir_a', 'file_b.log')}", output)

    @patch('src.cleaner.get_file_info')
    @patch('os.walk')
    def test_scan_directory_file_info_error(self, mock_os_walk, mock_get_file_info):
        # Mock rationale: Simulate a scenario where get_file_info returns None (e.g., file disappeared).
        current_time = datetime(2023, 3, 20)
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['valid_file.txt', 'invalid_file.txt'])
        ]
        mock_get_file_info.side_effect = [
            # valid_file.txt: old, large - CANDIDATE
            (datetime(2023, 1, 1).timestamp(), 70 * 1024 * 1024),
            # invalid_file.txt: returns None
            (None, None),
        ]

        candidates = scan_directory('/mock/dir', min_age_days=30, min_size_mb=50, current_time=current_time)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0][0], os.path.join('/mock/dir', 'valid_file.txt'))

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_isdir):
        # Mock rationale: Simulate an invalid directory path provided to the main function.
        mock_parse_args.return_value = MagicMock(
            path=['/non/existent/dir'],
            min_age=30,
            min_size=50
        )
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Warning: Path '/non/existent/dir' is not a valid directory. Skipping.", output)
        self.assertIn("Total Cataclysmic Candidates Found: 0", output)

    @patch('src.cleaner.get_file_info')
    @patch('os.walk')
    def test_main_no_candidates_output(self, mock_os_walk, mock_get_file_info):
        # Mock rationale: Simulate a scenario where no files meet the criteria, checking output.
        current_time = datetime(2023, 3, 20)
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file1.txt'])
        ]
        mock_get_file_info.return_value = (
            (current_time - timedelta(days=10)).timestamp(), # 10 days old
            10 * 1024 * 1024 # 10 MB
        )

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('os.path.isdir', return_value=True), \
             patch('src.cleaner.datetime') as mock_datetime:
            mock_parse_args.return_value = MagicMock(
                path=['/mock/dir'],
                min_age=30,
                min_size=50
            )
            mock_datetime.now.return_value = current_time
            mock_datetime.fromtimestamp = datetime.fromtimestamp

            main()
            output = self.mock_stdout.getvalue()
            self.assertIn("No candidates found in this path.", output)
            self.assertIn("Total Cataclysmic Candidates Found: 0", output)
            self.assertNotIn("Candidate!", output)
