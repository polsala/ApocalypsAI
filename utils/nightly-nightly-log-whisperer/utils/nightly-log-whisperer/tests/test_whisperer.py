import unittest
from unittest.mock import patch, mock_open
import os
import time
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system operations (listing directories, reading files, checking modification times)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't rely on the host system's file structure.
# `os.path.isdir` is mocked to control if a directory exists.
# `os.walk` is mocked to control which files are 'found' within a directory structure.
# `os.path.getmtime` is mocked to control the 'age' of files, allowing time-window filtering.
# `builtins.open` is mocked to control the content of files, simulating log file reads.
# `builtins.print` is mocked to capture and assert on console output for summary tests.

# Import the functions to be tested
from src.whisperer import scan_logs, summarize_findings

class TestLogWhisperer(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic time-based checks
        self.mock_current_time = datetime(2023, 10, 27, 10, 0, 0).timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_basic_functionality(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock os.walk to return a single log file
        mock_walk.return_value = [
            ('/mock/logs', [], ['app.log'])
        ]

        # Mock file content
        mock_file_open.return_value.read.side_effect = [
            "INFO: App started\nERROR: Failed to connect to DB\nWARNING: Low memory\nERROR: Another DB error\n"
        ]

        # Mock file modification time (within the last 24 hours)
        mock_getmtime.return_value = self.mock_current_time - timedelta(hours=1).total_seconds()

        results = scan_logs('/mock/logs', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 1)
        self.assertEqual(results['total_error_lines'], 2)
        self.assertIn('ERROR: Failed to connect to DB', results['error_details'])
        self.assertEqual(results['error_details']['ERROR: Failed to connect to DB'], 1)
        self.assertIn('ERROR: Another DB error', results['error_details'])
        self.assertEqual(results['error_details']['ERROR: Another DB error'], 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_no_errors(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/logs', [], ['clean.log'])
        ]
        mock_file_open.return_value.read.side_effect = [
            "INFO: App started\nDEBUG: Processing data\nWARNING: Minor issue\n"
        ]
        mock_getmtime.return_value = self.mock_current_time - timedelta(hours=1).total_seconds()

        results = scan_logs('/mock/logs', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 1)
        self.assertEqual(results['total_error_lines'], 0)
        self.assertEqual(len(results['error_details']), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_old_files_ignored(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/logs', [], ['old.log', 'recent.log'])
        ]
        # Mock content for both files
        mock_file_open.side_effect = [
            mock_open(read_data="ERROR: Old error\n").return_value, # Content for old.log
            mock_open(read_data="ERROR: Recent error\n").return_value # Content for recent.log
        ]

        # Mock modification times: old.log is too old, recent.log is within window
        def getmtime_side_effect(path):
            if 'old.log' in path:
                return self.mock_current_time - timedelta(days=2).total_seconds() # 48 hours old
            elif 'recent.log' in path:
                return self.mock_current_time - timedelta(hours=1).total_seconds() # 1 hour old
            return self.mock_current_time # Default for other paths

        mock_getmtime.side_effect = getmtime_side_effect

        results = scan_logs('/mock/logs', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 1) # Only recent.log should be scanned
        self.assertEqual(results['total_error_lines'], 1)
        self.assertIn('ERROR: Recent error', results['error_details'])
        self.assertNotIn('ERROR: Old error', results['error_details'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_directory_not_found(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = False # Directory does not exist

        results = scan_logs('/nonexistent/path', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 0)
        self.assertEqual(results['total_error_lines'], 0)
        self.assertEqual(len(results['error_details']), 0)
        mock_walk.assert_not_called() # os.walk should not be called if dir doesn't exist

    @patch('builtins.print')
    def test_summarize_findings_with_errors(self, mock_print):
        results = {
            "files_scanned": 3,
            "total_error_lines": 5,
            "error_details": {
                "ERROR: Disk full": 3,
                "CRITICAL: Service down": 2
            }
        }
        summarize_findings(results)

        mock_print.assert_any_call("\nNightly Log Whisperer Report")
        mock_print.assert_any_call("Files scanned: 3")
        mock_print.assert_any_call("Total error lines found: 5")
        mock_print.assert_any_call("Top 5 Error Messages:")
        mock_print.assert_any_call("1. ERROR: Disk full (3 occurrences)")
        mock_print.assert_any_call("2. CRITICAL: Service down (2 occurrences)")
        mock_print.assert_any_call("\nAll clear, for now. Keep whispering!")

    @patch('builtins.print')
    def test_summarize_findings_no_errors(self, mock_print):
        results = {
            "files_scanned": 2,
            "total_error_lines": 0,
            "error_details": {}
        }
        summarize_findings(results)

        mock_print.assert_any_call("\nNightly Log Whisperer Report")
        mock_print.assert_any_call("Files scanned: 2")
        mock_print.assert_any_call("Total error lines found: 0")
        mock_print.assert_any_call("\nNo significant error whispers detected.")
        mock_print.assert_any_call("\nAll clear, for now. Keep whispering!")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_multiple_files_and_types(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/logs', [], ['app.log', 'sys.txt', 'data.csv'])
        ]

        mock_file_open.side_effect = [
            mock_open(read_data="INFO: App started\nERROR: Failed\n").return_value, # app.log
            mock_open(read_data="CRITICAL: System crash\nWARNING: Minor\n").return_value, # sys.txt
            mock_open(read_data="header,value\n1,2\n").return_value # data.csv (should be ignored)
        ]

        mock_getmtime.return_value = self.mock_current_time - timedelta(hours=1).total_seconds()

        results = scan_logs('/mock/logs', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 2) # app.log and sys.txt
        self.assertEqual(results['total_error_lines'], 2)
        self.assertIn('ERROR: Failed', results['error_details'])
        self.assertIn('CRITICAL: System crash', results['error_details'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_file_read_error(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/logs', [], ['unreadable.log'])
        ]
        mock_file_open.side_effect = IOError("Permission denied") # Simulate read error
        mock_getmtime.return_value = self.mock_current_time - timedelta(hours=1).total_seconds()

        results = scan_logs('/mock/logs', time_window_hours=24)

        self.assertEqual(results['files_scanned'], 0) # File was not successfully scanned
        self.assertEqual(results['total_error_lines'], 0)
        self.assertEqual(len(results['error_details']), 0)

if __name__ == '__main__':
    unittest.main()
