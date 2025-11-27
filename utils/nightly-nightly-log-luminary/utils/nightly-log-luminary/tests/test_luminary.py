import unittest
from unittest.mock import patch, mock_open
import sys
import io
import importlib.util

# Mock rationale: We need to simulate reading from a file without actually touching the filesystem.
# `unittest.mock.patch('builtins.open')` allows us to intercept calls to `open()`
# and provide a mock file object that returns predefined content, making tests deterministic and offline.

# Dynamically load luminary.py to ensure it's runnable regardless of current working directory
def load_luminary_module():
    spec = importlib.util.spec_from_file_location("luminary_module", "src/luminary.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

luminary_module = load_luminary_module()
analyze_log = luminary_module.analyze_log


class TestLogLuminary(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr to check printed output and error messages
        self.held_stdout = io.StringIO()
        sys.stdout = self.held_stdout
        self.held_stderr = io.StringIO()
        sys.stderr = self.held_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    @patch('builtins.open', new_callable=mock_open)
    def test_empty_log_file(self, mock_file):
        # Mock rationale: Simulate an empty log file to test edge cases.
        mock_file.return_value.__enter__.return_value = []
        analyze_log('dummy.log')
        output = self.held_stdout.getvalue()

        self.assertIn("Total Lines Processed: 0", output)
        self.assertIn("Errors Found: 0", output)
        self.assertIn("Warnings Found: 0", output)
        self.assertIn("Info Messages Found: 0", output)
        self.assertIn("Top 5 Most Frequent Lines:", output)
        self.assertIn("(No unique non-empty lines found)", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_basic_log_file(self, mock_file):
        # Mock rationale: Simulate a log file with various types of messages.
        log_content = [
            "INFO: Application started.\n",
            "WARNING: Disk space low.\n",
            "ERROR: Failed to connect to DB.\n",
            "INFO: User logged in.\n",
            "ERROR: Failed to connect to DB.\n",
            "DEBUG: Some debug message.\n",
            "WARNING: Disk space low.\n",
            "INFO: Application stopped.\n",
            "ERROR: Another critical error.\n",
            "INFO: User logged in.\n",
            "INFO: User logged in.\n",
        ]
        mock_file.return_value.__enter__.return_value = log_content
        analyze_log('test.log')
        output = self.held_stdout.getvalue()

        self.assertIn("Total Lines Processed: 11", output)
        self.assertIn("Errors Found: 3", output)
        self.assertIn("Warnings Found: 2", output)
        self.assertIn("Info Messages Found: 4", output)
        self.assertIn("Top 5 Most Frequent Lines:", output)
        self.assertIn("[Count: 3] INFO: User logged in.", output)
        self.assertIn("[Count: 2] ERROR: Failed to connect to DB.", output)
        self.assertIn("[Count: 2] WARNING: Disk space low.", output)
        self.assertIn("[Count: 1] INFO: Application started.", output)
        self.assertIn("[Count: 1] DEBUG: Some debug message.", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        # Mock rationale: Simulate a FileNotFoundError to test error handling.
        mock_file.side_effect = FileNotFoundError
        
        # We expect sys.exit(1) to be called, so we need to catch SystemExit
        with self.assertRaises(SystemExit) as cm:
            analyze_log('nonexistent.log')
        self.assertEqual(cm.exception.code, 1)
        
        stderr_output = self.held_stderr.getvalue()
        self.assertIn("Error: Log file not found at 'nonexistent.log'", stderr_output)

    @patch('builtins.open', new_callable=mock_open)
    def test_mixed_case_keywords(self, mock_file):
        # Mock rationale: Ensure keyword matching is case-insensitive.
        log_content = [
            "info: lower case info\n",
            "Warning: Mixed case warning\n",
            "ERROR: UPPER CASE ERROR\n",
            "error: another lower case error\n",
        ]
        mock_file.return_value.__enter__.return_value = log_content
        analyze_log('case.log')
        output = self.held_stdout.getvalue()

        self.assertIn("Total Lines Processed: 4", output)
        self.assertIn("Errors Found: 2", output)
        self.assertIn("Warnings Found: 1", output)
        self.assertIn("Info Messages Found: 1", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_log_with_empty_lines(self, mock_file):
        # Mock rationale: Test that empty lines are skipped for frequency counts and keyword checks,
        # but still contribute to the total lines processed.
        log_content = [
            "INFO: Line 1\n",
            "\n",
            "WARNING: Line 2\n",
            "\n",
            "INFO: Line 1\n",
        ]
        mock_file.return_value.__enter__.return_value = log_content
        analyze_log('empty_lines.log')
        output = self.held_stdout.getvalue()

        self.assertIn("Total Lines Processed: 5", output) # 5 lines read, 3 non-empty
        self.assertIn("Errors Found: 0", output)
        self.assertIn("Warnings Found: 1", output)
        self.assertIn("Info Messages Found: 2", output)
        self.assertIn("[Count: 2] INFO: Line 1", output)
        self.assertIn("[Count: 1] WARNING: Line 2", output)
        self.assertNotIn("\n", output) # Ensure empty lines are not in top lines

    @patch('builtins.open', new_callable=mock_open)
    def test_unicode_characters(self, mock_file):
        # Mock rationale: Ensure the utility handles unicode characters correctly.
        log_content = [
            "INFO: Привет мир!\n",
            "ERROR: ❌ Failed to process data.\n",
            "WARNING: ⚠️ Low battery.\n",
        ]
        mock_file.return_value.__enter__.return_value = log_content
        analyze_log('unicode.log')
        output = self.held_stdout.getvalue()

        self.assertIn("Total Lines Processed: 3", output)
        self.assertIn("Errors Found: 1", output)
        self.assertIn("Warnings Found: 1", output)
        self.assertIn("Info Messages Found: 1", output)
        self.assertIn("[Count: 1] INFO: Привет мир!", output)
        self.assertIn("[Count: 1] ERROR: ❌ Failed to process data.", output)
        self.assertIn("[Count: 1] WARNING: ⚠️ Low battery.", output)
