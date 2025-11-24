import unittest
import os
import sys
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.collector import collect_dust_bunnies, generate_report, get_file_age_days, is_empty_dir, main

class TestCosmicDustBunnyCollector(unittest.TestCase):

    # Mock rationale: os.path.getmtime returns a timestamp, which depends on the current time.
    # Mocking datetime.now() allows deterministic testing of age-based filtering.
    @patch('src.collector.datetime')
    def test_get_file_age_days(self, mock_datetime):
        # Set a fixed "now" for testing
        fixed_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.timedelta

        # Mock os.path.getmtime to return a specific timestamp
        with patch('src.collector.os.path.getmtime') as mock_getmtime:
            # File modified 35 days ago
            mock_getmtime.return_value = (fixed_now - timedelta(days=35)).timestamp()
            self.assertEqual(get_file_age_days('/path/to/old_file.txt'), 35)

            # File modified 10 days ago
            mock_getmtime.return_value = (fixed_now - timedelta(days=10)).timestamp()
            self.assertEqual(get_file_age_days('/path/to/recent_file.txt'), 10)

    # Mock rationale: os.listdir depends on the actual file system state.
    # Mocking this allows deterministic testing of empty directory detection.
    @patch('src.collector.os.listdir')
    def test_is_empty_dir(self, mock_listdir):
        mock_listdir.return_value = []
        self.assertTrue(is_empty_dir('/path/to/empty_dir'))

        mock_listdir.return_value = ['file.txt']
        self.assertFalse(is_empty_dir('/path/to/non_empty_dir'))

    # Mock rationale: os.walk, os.path.exists, os.path.getmtime, os.listdir
    # All these functions interact with the actual file system, making tests non-deterministic.
    # Mocking them allows us to simulate various file system structures and states.
    @patch('src.collector.os.path.exists')
    @patch('src.collector.os.walk')
    @patch('src.collector.get_file_age_days') # Mock our own helper for age
    @patch('src.collector.is_empty_dir')     # Mock our own helper for empty dir
    @patch('src.collector.datetime')          # Mock datetime.now for report generation
    def test_collect_dust_bunnies(self, mock_datetime, mock_is_empty_dir, mock_get_file_age_days, mock_os_walk, mock_os_path_exists):
        # Setup fixed "now" for report generation
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.strftime = lambda *args, **kw: datetime.strftime(mock_datetime.now.return_value, *args, **kw)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.timedelta

        # Simulate paths existing
        mock_os_path_exists.return_value = True

        # Simulate file system structure
        # root, dirs, files
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['old_file.txt', 'recent_file.log', 'temp.tmp', 'CASE.LOG']),
            ('/root/dir1', [], ['another_old.bak', 'current.txt']),
            ('/root/dir2', [], []), # This dir is empty
        ]

        # Configure mocks for file properties
        mock_get_file_age_days.side_effect = lambda f: {
            '/root/old_file.txt': 40,
            '/root/recent_file.log': 5,
            '/root/temp.tmp': 15,
            '/root/CASE.LOG': 20,
            '/root/dir1/another_old.bak': 60,
            '/root/dir1/current.txt': 2,
        }.get(f, 0) # Default to 0 days if not specified

        mock_is_empty_dir.side_effect = lambda d: {
            '/root/dir1': False,
            '/root/dir2': True, # Simulate dir2 being empty
        }.get(d, False)

        # Test 1: Basic collection with age and extensions (case-insensitive)
        result = collect_dust_bunnies(
            paths=['/root'],
            age_threshold_days=30,
            extensions=['.tmp', '.bak', '.log'], # Test with and without leading dot, and case-insensitive
            report_empty_dirs=False
        )

        self.assertIn('/root/old_file.txt', result['old_files'])
        self.assertNotIn('/root/recent_file.log', result['old_files'])
        self.assertIn('/root/dir1/another_old.bak', result['old_files']) # Also old

        self.assertIn('/root/temp.tmp', result['extension_files'])
        self.assertIn('/root/dir1/another_old.bak', result['extension_files'])
        self.assertIn('/root/recent_file.log', result['extension_files']) # Matched by .log extension
        self.assertIn('/root/CASE.LOG', result['extension_files']) # Matched by .log extension (case-insensitive)

        self.assertEqual(len(result['empty_directories']), 0) # Not reporting empty dirs

        # Test 2: Report empty directories
        result_empty_dirs = collect_dust_bunnies(
            paths=['/root'],
            age_threshold_days=100, # Make all files not old
            extensions=[],
            report_empty_dirs=True
        )
        self.assertEqual(len(result_empty_dirs['old_files']), 0)
        self.assertEqual(len(result_empty_dirs['extension_files']), 0)
        self.assertIn('/root/dir2', result_empty_dirs['empty_directories'])
        self.assertEqual(len(result_empty_dirs['empty_directories']), 1)

        # Test 3: Path not found
        mock_os_path_exists.return_value = False
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            result_not_found = collect_dust_bunnies(
                paths=['/nonexistent'],
                age_threshold_days=30,
                extensions=[],
                report_empty_dirs=False
            )
            self.assertEqual(len(result_not_found['old_files']), 0)
            self.assertTrue("Warning: Path not found" in mock_stderr.write.call_args[0][0])

    @patch('src.collector.datetime') # Mock datetime.now for report generation
    def test_generate_report(self, mock_datetime):
        # Setup fixed "now" for report generation
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.strftime = lambda *args, **kw: datetime.strftime(mock_datetime.now.return_value, *args, **kw)

        dust_bunnies_full = {
            "old_files": ["/path/to/another_old.log", "/path/to/old.txt"],
            "extension_files": ["/path/to/old.txt", "/path/to/temp.tmp"], # old.txt is also a temp file
            "empty_directories": ["/path/to/empty_dir"]
        }

        # Test with full report to stdout
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            generate_report(dust_bunnies_full)
            output = mock_stdout.write.call_args[0][0]
            self.assertIn("--- Cosmic Dust Bunny Report ---", output)
            self.assertIn("🌌 Ancient Artifacts", output)
            self.assertIn("- /path/to/old.txt", output)
            self.assertIn("✨ Peculiar Particles", output)
            self.assertIn("- /path/to/temp.tmp", output)
            self.assertIn("🕳️ Void Pockets", output)
            self.assertIn("- /path/to/empty_dir", output)

        # Test with empty report to stdout
        dust_bunnies_empty = {
            "old_files": [],
            "extension_files": [],
            "empty_directories": []
        }
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            generate_report(dust_bunnies_empty)
            output = mock_stdout.write.call_args[0][0]
            self.assertIn("🎉 All clear! No cosmic dust bunnies detected.", output)

        # Test saving report to file
        mock_output_file = "test_report.txt"
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            with patch('sys.stdout', new_callable=MagicMock) as mock_stdout: # To capture print statements
                generate_report(dust_bunnies_full, output_file=mock_output_file)
                mock_file.assert_called_once_with(mock_output_file, 'w')
                handle = mock_file()
                handle.write.assert_called_once()
                self.assertIn("Report saved to test_report.txt", mock_stdout.write.call_args[0][0])

    @patch('src.collector.collect_dust_bunnies')
    @patch('src.collector.generate_report')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_generate_report, mock_collect_dust_bunnies):
        # Mock command-line arguments
        mock_parse_args.return_value = argparse.Namespace(
            path=['/test/path1', '/test/path2'],
            age=60,
            extensions=['tmp', '.LOG'], # Test with and without leading dot, and mixed case
            report_empty_dirs=True,
            output='output.txt'
        )

        # Mock the return value of collect_dust_bunnies
        mock_collect_dust_bunnies.return_value = {
            "old_files": ["/test/path1/old.txt"],
            "extension_files": ["/test/path1/file.tmp"],
            "empty_directories": ["/test/path2/empty_dir"]
        }

        main()

        # Verify collect_dust_bunnies was called with correct arguments
        mock_collect_dust_bunnies.assert_called_once_with(
            ['/test/path1', '/test/path2'],
            60,
            ['.tmp', '.log'], # Should be normalized and lowercased
            True
        )

        # Verify generate_report was called with the collected data and output file
        mock_generate_report.assert_called_once_with(
            {
                "old_files": ["/test/path1/old.txt"],
                "extension_files": ["/test/path1/file.tmp"],
                "empty_directories": ["/test/path2/empty_dir"]
            },
            'output.txt'
        )

if __name__ == '__main__':
    unittest.main()
