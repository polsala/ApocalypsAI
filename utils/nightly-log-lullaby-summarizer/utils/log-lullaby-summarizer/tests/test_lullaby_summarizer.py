import unittest
from unittest.mock import patch, mock_open
import sys
import io
from collections import defaultdict

# Mock rationale: The `summarize_logs` function reads from a file. To ensure
# deterministic and offline testing, we must mock the `open()` function.
# This allows us to provide arbitrary log content as if it were read from a real file,
# without actually touching the filesystem or requiring a physical log file.

from src.lullaby_summarizer import summarize_logs, main

class TestLullabySummarizer(unittest.TestCase):

    def test_empty_log_file(self):
        # Mock rationale: Simulate an empty log file.
        mock_file_content = ""
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            summary = summarize_logs("dummy.log")
            self.assertEqual(summary, defaultdict(int))

    def test_log_file_with_only_info(self):
        # Mock rationale: Simulate a log file with only INFO/DEBUG messages,
        # which should not be summarized as "problem patterns".
        mock_file_content = (
            "2023-10-27 10:00:01 INFO Starting application...\n"
            "2023-10-27 10:00:11 DEBUG User 'admin' logged in.\n"
            "2023-10-27 10:00:30 INFO Processing complete.\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            summary = summarize_logs("dummy.log")
            self.assertEqual(summary, defaultdict(int))

    def test_log_file_with_errors_and_warnings(self):
        # Mock rationale: Simulate a log file containing various error and warning messages.
        mock_file_content = (
            "2023-10-27 10:00:01 INFO Starting application...\n"
            "2023-10-27 10:00:05 WARNING Deprecated feature 'X' used.\n"
            "2023-10-27 10:00:10 ERROR Failed to connect to database 'mydb'.\n"
            "2023-10-27 10:00:15 ERROR Failed to connect to database 'mydb'.\n"
            "2023-10-27 10:00:20 CRITICAL Out of memory error.\n"
            "2023-10-27 10:00:25 WARNING Deprecated feature 'X' used.\n"
            "2023-10-27 10:00:30 INFO Processing complete.\n"
            "2023-10-27 10:00:35 ERROR Another unique error message.\n"
        )
        expected_summary = defaultdict(int, {
            "[ERROR] Failed to connect to database 'mydb'.": 2,
            "[WARNING] Deprecated feature 'X' used.": 2,
            "[CRITICAL] Out of memory error.": 1,
            "[ERROR] Another unique error message.": 1,
        })
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            summary = summarize_logs("dummy.log")
            self.assertEqual(summary, expected_summary)

    def test_log_file_with_different_log_formats(self):
        # Mock rationale: Simulate a log file with varied log line formats
        # to ensure the regex is robust.
        mock_file_content = (
            "Oct 27 10:00:05 host app[123]: WARNING: Deprecated feature 'Y'.\n"
            "2023-10-27 10:00:10 my_logger ERROR: Database connection failed.\n"
            "CRITICAL: System halted due to unhandled exception.\n"
            "2023-10-27 10:00:15 [ERROR] User 'guest' permission denied.\n"
            "2023-10-27 10:00:20 [WARN] Disk space low.\n"
        )
        expected_summary = defaultdict(int, {
            "[WARNING] Deprecated feature 'Y'.": 1,
            "[ERROR] Database connection failed.": 1,
            "[CRITICAL] System halted due to unhandled exception.": 1,
            "[ERROR] User 'guest' permission denied.": 1,
            "[WARNING] Disk space low.": 1,
        })
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            summary = summarize_logs("dummy.log")
            self.assertEqual(summary, expected_summary)

    def test_file_not_found_error(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open a non-existent file.
        # We expect the function to print an error and exit.
        with patch('builtins.open', side_effect=FileNotFoundError), \
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr, \
             self.assertRaises(SystemExit) as cm:
            summarize_logs("non_existent.log")
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    def test_main_function_output(self):
        # Mock rationale: Test the `main` function's console output.
        # We need to mock `sys.argv` for command-line arguments and `open()` for file content.
        mock_file_content = (
            "2023-10-27 10:00:05 WARNING Deprecated feature 'X' used.\n"
            "2023-10-27 10:00:10 ERROR Failed to connect to database 'mydb'.\n"
            "2023-10-27 10:00:15 ERROR Failed to connect to database 'mydb'.\n"
        )
        with patch('sys.argv', ['lullaby_summarizer.py', 'dummy.log']), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("🎶 Log Lullaby Summary 🎶", output)
            self.assertIn("[ERROR] Failed to connect to database 'mydb'. (2 times)", output)
            self.assertIn("[WARNING] Deprecated feature 'X' used. (1 time)", output)
            self.assertIn("Sweet dreams!", output)

    def test_main_function_no_errors_output(self):
        # Mock rationale: Test `main` function output when no errors/warnings are found.
        mock_file_content = (
            "2023-10-27 10:00:01 INFO Starting application...\n"
            "2023-10-27 10:00:11 DEBUG User 'admin' logged in.\n"
        )
        with patch('sys.argv', ['lullaby_summarizer.py', 'dummy.log']), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("🎶 Log Lullaby Summary 🎶", output)
            self.assertIn("No critical errors or warnings detected. Your logs are already sleeping soundly!", output)
            self.assertIn("Sweet dreams!", output)

    def test_main_function_missing_argument(self):
        # Mock rationale: Test `main` function's behavior when no log file argument is provided.
        with patch('sys.argv', ['lullaby_summarizer.py']), \
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr, \
             self.assertRaises(SystemExit) as cm:
            main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python src/lullaby_summarizer.py <path_to_your_log_file>", mock_stderr.getvalue())
