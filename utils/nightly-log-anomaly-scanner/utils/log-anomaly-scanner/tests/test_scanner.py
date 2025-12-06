import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from src.scanner import scan_logs, main

class TestLogAnomalyScanner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_test_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_no_anomalies(self):
        self._create_test_file("log1.txt", "This is a normal log line.\nAnother normal line.")
        self._create_test_file("log2.txt", "Info message here.\nDebug output.")
        patterns = ["ERROR", "WARN", "CRITICAL"]
        results = scan_logs(self.test_dir, patterns)
        self.assertEqual(results, {})

    def test_single_anomaly_single_file(self):
        self._create_test_file("log.txt", "Info line.\nERROR: Something went wrong.\nAnother info line.")
        patterns = ["ERROR"]
        results = scan_logs(self.test_dir, patterns)
        expected = {
            "log.txt": [
                {'line_num': 2, 'line_content': 'ERROR: Something went wrong.', 'pattern': 'ERROR'}
            ]
        }
        self.assertEqual(results, expected)

    def test_multiple_anomalies_single_file(self):
        self._create_test_file("app.log", "Info.\nWARN: Low disk space.\nERROR: Failed to connect.\nDebug.")
        patterns = ["WARN", "ERROR"]
        results = scan_logs(self.test_dir, patterns)
        expected = {
            "app.log": [
                {'line_num': 2, 'line_content': 'WARN: Low disk space.', 'pattern': 'WARN'},
                {'line_num': 3, 'line_content': 'ERROR: Failed to connect.', 'pattern': 'ERROR'}
            ]
        }
        self.assertEqual(results, expected)

    def test_multiple_anomalies_multiple_files(self):
        self._create_test_file("web.log", "Request received.\nERROR: DB connection lost.\nSuccess.")
        self._create_test_file("api.log", "API call.\nWARN: Deprecated endpoint used.\nResponse sent.")
        patterns = ["ERROR", "WARN"]
        results = scan_logs(self.test_dir, patterns)
        expected = {
            "web.log": [
                {'line_num': 2, 'line_content': 'ERROR: DB connection lost.', 'pattern': 'ERROR'}
            ],
            "api.log": [
                {'line_num': 2, 'line_content': 'WARN: Deprecated endpoint used.', 'pattern': 'WARN'}
            ]
        }
        # Sort keys for consistent comparison, as os.listdir order is not guaranteed
        self.assertEqual(sorted(results.keys()), sorted(expected.keys()))
        for key in results:
            self.assertEqual(results[key], expected[key])

    def test_empty_directory(self):
        patterns = ["ERROR"]
        results = scan_logs(self.test_dir, patterns)
        self.assertEqual(results, {})

    def test_non_existent_directory(self):
        patterns = ["ERROR"]
        results = scan_logs("/non/existent/path", patterns)
        self.assertEqual(results, {}) # Should return empty dict and print error

    def test_regex_patterns(self):
        self._create_test_file("complex.log", "Line 1.\nFailed to process request ID: 12345.\nLine 3.")
        patterns = [r"Failed to process request ID: \d+"]
        results = scan_logs(self.test_dir, patterns)
        expected = {
            "complex.log": [
                {'line_num': 2, 'line_content': 'Failed to process request ID: 12345.', 'pattern': r'Failed to process request ID: \d+'}
            ]
        }
        self.assertEqual(results, expected)

    @patch('builtins.print') # Mock rationale: Capture print statements to verify error messages.
    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate a non-existent directory without actually creating one.
    def test_main_non_existent_directory_cli(self, mock_isdir, mock_print):
        # Mock sys.argv for argparse
        with patch('sys.argv', ['scanner.py', '/non/existent/path', '-p', 'ERROR']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Should exit 0 if no anomalies found (or directory error)
            mock_print.assert_any_call("Error: Directory not found at '/non/existent/path'")

    @patch('builtins.print') # Mock rationale: Capture print statements to verify output.
    @patch('os.listdir', return_value=['log.txt']) # Mock rationale: Control the files seen in the directory.
    @patch('os.path.isfile', return_value=True) # Mock rationale: Assume all listed items are files.
    def test_main_anomalies_found_cli(self, mock_isfile, mock_listdir, mock_print):
        # Mock open to simulate file content
        m = mock_open(read_data="Normal line\nERROR: Critical issue\nAnother line")
        with patch('builtins.open', m): # Mock rationale: Simulate reading file content without actual file I/O.
            with patch('sys.argv', ['scanner.py', '/mock/dir', '-p', 'ERROR']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1) # Should exit 1 if anomalies found
                mock_print.assert_any_call("\n--- Anomaly Report ---")
                mock_print.assert_any_call("  Line 2 (Pattern: 'ERROR'): ERROR: Critical issue")

    @patch('builtins.print') # Mock rationale: Capture print statements to verify output.
    @patch('os.listdir', return_value=['log.txt']) # Mock rationale: Control the files seen in the directory.
    @patch('os.path.isfile', return_value=True) # Mock rationale: Assume all listed items are files.
    def test_main_no_anomalies_cli(self, mock_isfile, mock_listdir, mock_print):
        # Mock open to simulate file content
        m = mock_open(read_data="Normal line\nAnother line")
        with patch('builtins.open', m): # Mock rationale: Simulate reading file content without actual file I/O.
            with patch('sys.argv', ['scanner.py', '/mock/dir', '-p', 'ERROR']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 0) # Should exit 0 if no anomalies found
                mock_print.assert_any_call("\n--- Scan Complete: No Anomalies Detected. All clear! ---")
