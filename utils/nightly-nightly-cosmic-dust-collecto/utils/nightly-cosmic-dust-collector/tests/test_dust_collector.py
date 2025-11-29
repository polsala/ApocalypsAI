import unittest
import os
import re
from unittest.mock import patch, mock_open
from collections import defaultdict

# Import the function to be tested
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests to keep test output clean.
    def test_empty_directory(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an empty directory structure to ensure no errors and correct empty results.
        mock_os_walk.return_value = []

        results = collect_dust(['/nonexistent/dir'])

        self.assertEqual(results['total_files_scanned'], 0)
        self.assertEqual(results['total_issues_found'], 0)
        self.assertEqual(results['file_results'], {})
        self.assertEqual(results['summary'], {})

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_no_log_files(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with non-log files to ensure only .log files are processed.
        mock_os_walk.return_value = [
            ('/test/dir', [], ['file.txt', 'image.jpg'])
        ]

        results = collect_dust(['/test/dir'])

        self.assertEqual(results['total_files_scanned'], 0)
        self.assertEqual(results['total_issues_found'], 0)
        self.assertEqual(results['file_results'], {})
        self.assertEqual(results['summary'], {})

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_single_log_file_with_matches(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a single log file with known content and expected pattern matches.
        mock_os_walk.return_value = [
            ('/test/dir', [], ['app.log'])
        ]
        log_content = "INFO: App started\nERROR: Something went wrong\nWARNING: Low disk space\nERROR: Another error\n"
        mock_file_open.return_value.__enter__.return_value.read.return_value = log_content

        results = collect_dust(['/test/dir'])

        expected_file_results = {
            '/test/dir/app.log': {
                'ERROR': 2,
                'WARNING': 1,
                'CRITICAL': 0
            }
        }
        expected_summary = {
            'ERROR': 2,
            'WARNING': 1,
            'CRITICAL': 0
        }

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_issues_found'], 3)
        self.assertEqual(results['file_results'], expected_file_results)
        self.assertEqual(results['summary'], expected_summary)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_multiple_log_files_with_matches(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate multiple log files across different directories with varied content.
        mock_os_walk.return_value = [
            ('/test/dir1', [], ['app1.log']),
            ('/test/dir2', [], ['app2.log', 'old.log'])
        ]

        # Mock rationale: Use a side_effect for mock_open to return different content for different files based on path.
        def mock_open_side_effect(file_path, *args, **kwargs):
            if 'app1.log' in file_path:
                return mock_open(read_data="ERROR: Fatal error\nINFO: OK").return_value
            elif 'app2.log' in file_path:
                return mock_open(read_data="WARNING: Disk full\nERROR: DB connection failed\nWARNING: Retrying").return_value
            elif 'old.log' in file_path:
                return mock_open(read_data="CRITICAL: System crash\n").return_value
            return mock_open().return_value # Default for other files

        mock_file_open.side_effect = mock_open_side_effect

        results = collect_dust(['/test/dir1', '/test/dir2'])

        expected_file_results = {
            '/test/dir1/app1.log': {'ERROR': 1, 'WARNING': 0, 'CRITICAL': 0},
            '/test/dir2/app2.log': {'ERROR': 1, 'WARNING': 2, 'CRITICAL': 0},
            '/test/dir2/old.log': {'ERROR': 0, 'WARNING': 0, 'CRITICAL': 1}
        }
        expected_summary = {
            'ERROR': 2,
            'WARNING': 2,
            'CRITICAL': 1
        }

        self.assertEqual(results['total_files_scanned'], 3)
        self.assertEqual(results['total_issues_found'], 5)
        self.assertEqual(results['file_results'], expected_file_results)
        self.assertEqual(results['summary'], expected_summary)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_custom_patterns(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Test the utility's ability to use user-defined regex patterns.
        mock_os_walk.return_value = [
            ('/test/dir', [], ['custom.log'])
        ]
        log_content = "User logged in\nFailed login attempt\nAPI_CALL_ERROR: Invalid token\n"
        mock_file_open.return_value.__enter__.return_value.read.return_value = log_content

        custom_pats = {'LOGIN_FAIL': r'Failed login', 'API_ERROR': r'API_CALL_ERROR'}
        results = collect_dust(['/test/dir'], custom_patterns=custom_pats)

        expected_file_results = {
            '/test/dir/custom.log': {
                'LOGIN_FAIL': 1,
                'API_ERROR': 1
            }
        }
        expected_summary = {
            'LOGIN_FAIL': 1,
            'API_ERROR': 1
        }

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_issues_found'], 2)
        self.assertEqual(results['file_results'], expected_file_results)
        self.assertEqual(results['summary'], expected_summary)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_file_io_error_handling(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure the utility handles file reading errors gracefully without crashing.
        mock_os_walk.return_value = [
            ('/test/dir', [], ['unreadable.log'])
        ]
        mock_file_open.side_effect = IOError("Permission denied")

        results = collect_dust(['/test/dir'])

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_issues_found'], 0) # No issues counted if file can't be read
        self.assertEqual(results['file_results'], {})
        self.assertEqual(results['summary'], {})
        # Check if error message was printed (optional, but good for robustness)
        mock_stdout.write.assert_any_call(unittest.mock.ANY)
        self.assertIn("Error reading file", mock_stdout.write.call_args_list[0].args[0])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_non_existent_scan_dir(self, mock_stdout, mock_file_open, mock_os_walk, mock_isdir):
        # Mock rationale: Test behavior when a specified scan directory does not exist.
        mock_isdir.side_effect = lambda path: path == '/existent/dir'
        mock_os_walk.return_value = [
            ('/existent/dir', [], ['log.log'])
        ]
        log_content = "ERROR: Test error\n"
        mock_file_open.return_value.__enter__.return_value.read.return_value = log_content

        results = collect_dust(['/nonexistent/dir', '/existent/dir'])

        expected_file_results = {
            '/existent/dir/log.log': {
                'ERROR': 1,
                'WARNING': 0,
                'CRITICAL': 0
            }
        }
        expected_summary = {
            'ERROR': 1,
            'WARNING': 0,
            'CRITICAL': 0
        }

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_issues_found'], 1)
        self.assertEqual(results['file_results'], expected_file_results)
        self.assertEqual(results['summary'], expected_summary)
        mock_stdout.write.assert_any_call(unittest.mock.ANY)
        self.assertIn("Warning: Directory not found", mock_stdout.write.call_args_list[0].args[0])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout') # Mock rationale: Suppress print statements during tests.
    def test_regex_compilation_error(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure that invalid regex patterns provided by the user are handled gracefully.
        mock_os_walk.return_value = [
            ('/test/dir', [], ['log.log'])
        ]
        log_content = "ERROR: Test error\n"
        mock_file_open.return_value.__enter__.return_value.read.return_value = log_content

        custom_pats = {'BAD_REGEX': r'['}
        results = collect_dust(['/test/dir'], custom_patterns=custom_pats)

        # Expect no patterns to be used if the only custom one fails to compile
        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_issues_found'], 0)
        self.assertEqual(results['file_results'], {})
        self.assertEqual(results['summary'], {})
        mock_stdout.write.assert_any_call(unittest.mock.ANY)
        self.assertIn("Error compiling regex", mock_stdout.write.call_args_list[0].args[0])
