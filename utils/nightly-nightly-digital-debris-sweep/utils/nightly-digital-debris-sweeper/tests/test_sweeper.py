import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import scan_directory, get_file_age_days

class TestDigitalDebrisSweeper(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('time.time')
    def test_get_file_age_days(self, mock_time_time, mock_getmtime):
        # Mock rationale: get_file_age_days relies on current time and file modification time.
        # We mock these to ensure deterministic age calculation for testing.
        
        # Simulate current time
        mock_time_time.return_value = datetime(2023, 1, 31, 12, 0, 0).timestamp()

        # Test a file modified 10 days ago
        mock_getmtime.return_value = datetime(2023, 1, 21, 12, 0, 0).timestamp()
        self.assertAlmostEqual(get_file_age_days("/path/to/file1"), 10.0, places=5)

        # Test a file modified 0 days ago (current time)
        mock_getmtime.return_value = mock_time_time.return_value
        self.assertAlmostEqual(get_file_age_days("/path/to/file2"), 0.0, places=5)

        # Test a file modified in the future (should result in negative age)
        mock_getmtime.return_value = datetime(2023, 2, 1, 12, 0, 0).timestamp()
        self.assertLess(get_file_age_days("/path/to/file3"), 0.0)

        # Test OSError (file not found)
        mock_getmtime.side_effect = OSError
        self.assertEqual(get_file_age_days("/path/to/nonexistent"), -1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_age_based(self, mock_time_time, mock_getmtime, mock_os_walk, mock_isdir):
        # Mock rationale: scan_directory relies heavily on file system operations (isdir, walk, getmtime).
        # We mock these to create a virtual file system for deterministic testing without actual disk I/O.
        
        mock_isdir.return_value = True
        
        # Simulate current time for age calculation
        current_timestamp = datetime(2023, 1, 31, 12, 0, 0).timestamp()
        mock_time_time.return_value = current_timestamp

        # Define file modification times relative to current_timestamp
        # File older than 30 days
        old_file_mtime = (datetime(2023, 1, 31) - timedelta(days=31)).timestamp()
        # File exactly 30 days old
        exact_age_file_mtime = (datetime(2023, 1, 31) - timedelta(days=30)).timestamp()
        # File newer than 30 days
        new_file_mtime = (datetime(2023, 1, 31) - timedelta(days=10)).timestamp()

        # Mock os.walk to simulate a directory structure
        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_log.txt', 'new_report.txt', 'exact_age.txt']),
            ('/test_dir/subdir', [], ['another_old.log'])
        ]

        # Mock os.path.getmtime for each file
        def mock_getmtime_side_effect(path):
            if 'old_log.txt' in path:
                return old_file_mtime
            elif 'new_report.txt' in path:
                return new_file_mtime
            elif 'exact_age.txt' in path:
                return exact_age_file_mtime
            elif 'another_old.log' in path:
                return old_file_mtime
            return current_timestamp # Default for unexpected files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test with age threshold of 30 days
        debris = scan_directory('/test_dir', age_threshold_days=30)
        expected_debris = [
            os.path.join('/test_dir', 'old_log.txt'),
            os.path.join('/test_dir', 'subdir', 'another_old.log')
        ]
        self.assertCountEqual(debris, expected_debris) # exact_age.txt should not be included if threshold is > 30

        # Test with age threshold of 29 days (should include exact_age.txt)
        debris_29_days = scan_directory('/test_dir', age_threshold_days=29)
        expected_debris_29_days = [
            os.path.join('/test_dir', 'old_log.txt'),
            os.path.join('/test_dir', 'exact_age.txt'),
            os.path.join('/test_dir', 'subdir', 'another_old.log')
        ]
        self.assertCountEqual(debris_29_days, expected_debris_29_days)

        # Test with age threshold 0 (disable age-based filtering)
        debris_no_age = scan_directory('/test_dir', age_threshold_days=0)
        self.assertEqual(debris_no_age, [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime') # Still needed, but age_threshold_days=0 will make it irrelevant for filtering
    @patch('time.time')
    def test_scan_directory_pattern_based(self, mock_time_time, mock_getmtime, mock_os_walk, mock_isdir):
        # Mock rationale: Similar to age-based, we mock file system operations to test pattern matching deterministically.
        
        mock_isdir.return_value = True
        mock_time_time.return_value = datetime(2023, 1, 31, 12, 0, 0).timestamp() # irrelevant for this test, but good practice
        mock_getmtime.return_value = mock_time_time.return_value # irrelevant for this test

        # Mock os.walk to simulate a directory structure
        mock_os_walk.return_value = [
            ('/test_dir', [], ['report.txt', 'temp_file.tmp', 'backup.bak', 'image.jpg', 'old.log.old']),
            ('/test_dir/data', [], ['another.tmp', 'config.ini'])
        ]

        # Test with specific patterns
        patterns = ['*.tmp', '*.bak', '*.log.old']
        debris = scan_directory('/test_dir', age_threshold_days=0, patterns=patterns)
        expected_debris = [
            os.path.join('/test_dir', 'temp_file.tmp'),
            os.path.join('/test_dir', 'backup.bak'),
            os.path.join('/test_dir', 'old.log.old'),
            os.path.join('/test_dir', 'data', 'another.tmp')
        ]
        self.assertCountEqual(debris, expected_debris)

        # Test with no matching patterns
        no_match_patterns = ['*.xyz']
        debris_no_match = scan_directory('/test_dir', age_threshold_days=0, patterns=no_match_patterns)
        self.assertEqual(debris_no_match, [])

        # Test with empty patterns list
        debris_empty_patterns = scan_directory('/test_dir', age_threshold_days=0, patterns=[])
        self.assertEqual(debris_empty_patterns, [])

        # Test with None patterns
        debris_none_patterns = scan_directory('/test_dir', age_threshold_days=0, patterns=None)
        self.assertEqual(debris_none_patterns, [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_combined_criteria(self, mock_time_time, mock_getmtime, mock_os_walk, mock_isdir):
        # Mock rationale: Combine age and pattern mocking to ensure both criteria work together correctly.
        
        mock_isdir.return_value = True
        
        current_timestamp = datetime(2023, 1, 31, 12, 0, 0).timestamp()
        mock_time_time.return_value = current_timestamp

        old_mtime = (datetime(2023, 1, 31) - timedelta(days=31)).timestamp() # Older than 30 days
        new_mtime = (datetime(2023, 1, 31) - timedelta(days=10)).timestamp() # Newer than 30 days

        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.tmp', 'old_report.log', 'config.ini']),
        ]

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path: return old_mtime
            if 'new_file.tmp' in path: return new_mtime
            if 'old_report.log' in path: return old_mtime
            if 'config.ini' in path: return new_mtime
            return current_timestamp

        mock_getmtime.side_effect = mock_getmtime_side_effect

        patterns = ['*.tmp', '*.log'] # Note: old_report.log matches this
        age_threshold = 30

        debris = scan_directory('/test_dir', age_threshold_days=age_threshold, patterns=patterns)
        expected_debris = [
            os.path.join('/test_dir', 'old_file.txt'), # Old
            os.path.join('/test_dir', 'new_file.tmp'), # Matches pattern, even if new
            os.path.join('/test_dir', 'old_report.log') # Old AND matches pattern
        ]
        self.assertCountEqual(debris, expected_debris)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_scan_directory_non_existent(self, mock_os_walk, mock_isdir):
        # Mock rationale: Test error handling for non-existent directories.
        
        mock_isdir.return_value = False
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            debris = scan_directory('/non_existent_dir', age_threshold_days=10, patterns=['*.tmp'])
            self.assertEqual(debris, [])
            mock_print.assert_called_with("Error: Directory '/non_existent_dir' not found or is not a directory.")

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[]) # Empty directory
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_scan_directory_empty(self, mock_time_time, mock_getmtime, mock_os_walk, mock_isdir):
        # Mock rationale: Ensure the scanner handles empty directories gracefully.
        
        mock_time_time.return_value = datetime(2023, 1, 31, 12, 0, 0).timestamp()
        mock_getmtime.return_value = mock_time_time.return_value
        
        debris = scan_directory('/empty_dir', age_threshold_days=10, patterns=['*.tmp'])
        self.assertEqual(debris, [])

    @patch('sys.argv', ['sweeper.py', '/test_dir', '--age', '1', '--patterns', '*.tmp,*.log'])
    @patch('src.sweeper.scan_directory', return_value=['/test_dir/old.log', '/test_dir/temp.tmp'])
    @patch('builtins.print')
    def test_main_with_debris(self, mock_print, mock_scan_directory):
        # Mock rationale: Test the main CLI entry point without actual file system interaction.
        # We mock sys.argv to control command-line arguments and scan_directory to control its output.
        
        from src.sweeper import main
        main()
        mock_scan_directory.assert_called_once_with('/test_dir', 1, ['*.tmp', '*.log'])
        mock_print.assert_any_call("\nIdentified Digital Debris:")
        mock_print.assert_any_call("  - /test_dir/old.log")
        mock_print.assert_any_call("  - /test_dir/temp.tmp")
        mock_print.assert_any_call("\nTotal debris found: 2 files.")

    @patch('sys.argv', ['sweeper.py', '/test_dir', '--age', '1', '--patterns', '*.tmp'])
    @patch('src.sweeper.scan_directory', return_value=[])
    @patch('builtins.print')
    def test_main_no_debris(self, mock_print, mock_scan_directory):
        # Mock rationale: Test the main CLI entry point when no debris is found.
        
        from src.sweeper import main
        main()
        mock_scan_directory.assert_called_once_with('/test_dir', 1, ['*.tmp'])
        mock_print.assert_any_call("\nNo digital debris found. Your digital landscape is pristine!")
