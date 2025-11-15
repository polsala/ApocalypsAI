import unittest
import os
import datetime
import json
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the functions from the collector script
# Mock rationale: We need to mock os.walk, os.path.getmtime, and datetime.datetime.now
# to ensure deterministic and offline testing of file system scanning logic and age calculations.
# This prevents actual file system access and time-dependent test failures.
with patch('os.path.isdir', return_value=True):
    from src.collector import scan_directory, generate_report, main

class TestDataDebrisCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

        # Capture stderr for testing error messages
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = StringIO()

        # Define a fixed 'current time' for deterministic age calculations
        self.mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0) # Oct 27, 2023, 10:00:00

        # Mock datetime.datetime.now()
        self.patcher_datetime_now = patch('datetime.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        # Allow other datetime calls to function normally (e.g., fromtimestamp, timedelta)
        self.mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        self.mock_datetime.timedelta.side_effect = datetime.timedelta

        # Mock os.walk and os.path.getmtime
        self.mock_os_walk = patch('os.walk').start()
        self.mock_os_path_getmtime = patch('os.path.getmtime').start()
        self.mock_os_path_isdir = patch('os.path.isdir').start()

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr
        patch.stopall() # Stop all patches started in setUp

    def test_scan_directory_finds_old_files(self):
        # Mock rationale: Simulate a directory structure with files of various ages
        # to test if scan_directory correctly identifies files older than the threshold.
        self.mock_os_walk.return_value = [
            ('/mock/path', ['subdir'], ['old_file.txt', 'new_file.log']),
            ('/mock/path/subdir', [], ['very_old_file.dat'])
        ]
        # Define modification times relative to self.mock_now (Oct 27, 2023)
        mock_mtimes = {
            '/mock/path/old_file.txt': (self.mock_now - datetime.timedelta(days=40)).timestamp(), # Older than 30 days
            '/mock/path/new_file.log': (self.mock_now - datetime.timedelta(days=10)).timestamp(), # Newer than 30 days
            '/mock/path/subdir/very_old_file.dat': (self.mock_now - datetime.timedelta(days=90)).timestamp() # Older than 30 days
        }
        self.mock_os_path_getmtime.side_effect = lambda p: mock_mtimes.get(p, 0.0)
        self.mock_os_path_isdir.return_value = True

        age_threshold = self.mock_now - datetime.timedelta(days=30)
        debris = scan_directory('/mock/path', age_threshold)

        self.assertEqual(len(debris), 2)
        self.assertIn(('/mock/path/old_file.txt', datetime.datetime.fromtimestamp(mock_mtimes['/mock/path/old_file.txt'])), debris)
        self.assertIn(('/mock/path/subdir/very_old_file.dat', datetime.datetime.fromtimestamp(mock_mtimes['/mock/path/subdir/very_old_file.dat'])), debris)

    def test_scan_directory_ignores_new_files(self):
        # Mock rationale: Ensure that files newer than the age threshold are not included in the debris report.
        self.mock_os_walk.return_value = [
            ('/mock/path', [], ['recent_file.txt', 'another_recent.log'])
        ]
        mock_mtimes = {
            '/mock/path/recent_file.txt': (self.mock_now - datetime.timedelta(days=5)).timestamp(),
            '/mock/path/another_recent.log': (self.mock_now - datetime.timedelta(days=20)).timestamp()
        }
        self.mock_os_path_getmtime.side_effect = lambda p: mock_mtimes.get(p, 0.0)
        self.mock_os_path_isdir.return_value = True

        age_threshold = self.mock_now - datetime.timedelta(days=30)
        debris = scan_directory('/mock/path', age_threshold)

        self.assertEqual(len(debris), 0)

    def test_scan_directory_empty_directory(self):
        # Mock rationale: Verify behavior when the scanned directory is empty or contains no files.
        self.mock_os_walk.return_value = [
            ('/mock/empty', [], []),
            ('/mock/empty/subdir', [], [])
        ]
        self.mock_os_path_getmtime.return_value = 0.0 # Should not be called
        self.mock_os_path_isdir.return_value = True

        age_threshold = self.mock_now - datetime.timedelta(days=30)
        debris = scan_directory('/mock/empty', age_threshold)

        self.assertEqual(len(debris), 0)

    def test_scan_directory_invalid_path(self):
        # Mock rationale: Test error handling for non-existent or invalid scan paths.
        self.mock_os_path_isdir.return_value = False

        debris = scan_directory('/non/existent/path', self.mock_now - datetime.timedelta(days=30))
        self.assertEqual(debris, [])
        self.assertIn("Error: Path '/non/existent/path' is not a valid directory.", self.mock_stderr.getvalue())

    def test_generate_report_text_format(self):
        # Mock rationale: Test the output formatting for the text report.
        debris_files = [
            ('/mock/path/old_file.txt', self.mock_now - datetime.timedelta(days=40)),
            ('/mock/path/subdir/very_old_file.dat', self.mock_now - datetime.timedelta(days=90))
        ]
        generate_report('/mock/path', 30, debris_files, 'text')
        output = self.mock_stdout.getvalue()

        self.assertIn("Data Debris Report for: /mock/path (Older than 30 days)", output)
        self.assertIn("Found 2 debris files:", output)
        self.assertIn("- /mock/path/old_file.txt (Modified: 2023-09-17 10:00:00)", output)
        self.assertIn("- /mock/path/subdir/very_old_file.dat (Modified: 2023-07-29 10:00:00)", output)
        self.assertIn("Consider reviewing these files for archiving or deletion.", output)

    def test_generate_report_text_format_no_debris(self):
        # Mock rationale: Test the output when no debris files are found.
        generate_report('/mock/path', 30, [], 'text')
        output = self.mock_stdout.getvalue()

        self.assertIn("No data debris found. Your digital landscape is pristine!", output)

    def test_generate_report_json_format(self):
        # Mock rationale: Test the output formatting for the JSON report.
        debris_files = [
            ('/mock/path/old_file.txt', self.mock_now - datetime.timedelta(days=40)),
            ('/mock/path/subdir/very_old_file.dat', self.mock_now - datetime.timedelta(days=90))
        ]
        generate_report('/mock/path', 30, debris_files, 'json')
        output = self.mock_stdout.getvalue()
        json_data = json.loads(output)

        self.assertEqual(json_data['scan_path'], '/mock/path')
        self.assertEqual(json_data['age_threshold_days'], 30)
        self.assertEqual(len(json_data['debris_files']), 2)
        self.assertEqual(json_data['debris_files'][0]['path'], '/mock/path/old_file.txt')
        self.assertEqual(json_data['debris_files'][0]['modified_datetime'], (self.mock_now - datetime.timedelta(days=40)).isoformat())

    @patch('sys.argv', ['collector.py', '/mock/path', '--age-days', '10', '--report-format', 'text'])
    def test_main_function_text_output(self):
        # Mock rationale: Test the main function's end-to-end behavior with specific CLI arguments.
        # This involves mocking os.walk, os.path.getmtime, and datetime.datetime.now.
        self.mock_os_walk.return_value = [
            ('/mock/path', [], ['old_file.txt', 'new_file.log'])
        ]
        mock_mtimes = {
            '/mock/path/old_file.txt': (self.mock_now - datetime.timedelta(days=15)).timestamp(), # Older than 10 days
            '/mock/path/new_file.log': (self.mock_now - datetime.timedelta(days=5)).timestamp()  # Newer than 10 days
        }
        self.mock_os_path_getmtime.side_effect = lambda p: mock_mtimes.get(p, 0.0)
        self.mock_os_path_isdir.return_value = True

        main()
        output = self.mock_stdout.getvalue()

        self.assertIn("Data Debris Report for: /mock/path (Older than 10 days)", output)
        self.assertIn("Found 1 debris files:", output)
        self.assertIn("- /mock/path/old_file.txt (Modified: 2023-10-12 10:00:00)", output)
        self.assertNotIn("new_file.log", output)

    @patch('sys.argv', ['collector.py', '/mock/path', '--age-days', '-5'])
    def test_main_function_negative_age_days(self):
        # Mock rationale: Test the main function's error handling for invalid input (negative age-days).
        self.mock_os_path_isdir.return_value = True
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: --age-days cannot be negative.", self.mock_stderr.getvalue())

    @patch('sys.argv', ['collector.py', '/non/existent/path'])
    def test_main_function_invalid_scan_path(self):
        # Mock rationale: Test the main function's error handling for an invalid scan path.
        self.mock_os_path_isdir.return_value = False
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Path '/non/existent/path' is not a valid directory.", self.mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
