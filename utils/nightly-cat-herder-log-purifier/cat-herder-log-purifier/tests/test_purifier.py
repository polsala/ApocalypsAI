import unittest
from unittest.mock import patch, mock_open
import io
import sys
import os
import argparse

# Adjust path to import purifier from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import purifier

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing console output
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_parse_log_line_standard_format(self):
        line = "[INFO] Application started successfully."
        level, message = purifier.parse_log_line(line)
        self.assertEqual(level, "INFO")
        self.assertEqual(message, "Application started successfully.")

    def test_parse_log_line_no_brackets(self):
        line = "ERROR Database connection failed."
        level, message = purifier.parse_log_line(line)
        self.assertEqual(level, "ERROR")
        self.assertEqual(message, "Database connection failed.")

    def test_parse_log_line_with_timestamp(self):
        line = "2023-10-27 10:00:00,123 INFO User logged in."
        level, message = purifier.parse_log_line(line)
        self.assertEqual(level, "INFO")
        self.assertEqual(message, "User logged in.")

    def test_parse_log_line_unclassified(self):
        line = "This is a random line without a log level."
        level, message = purifier.parse_log_line(line)
        self.assertIsNone(level)
        self.assertEqual(message, "This is a random line without a log level.")

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_no_filters(self, mock_file_open):
        # Mock rationale: Simulate reading a log file without actually creating one.
        # This ensures tests are deterministic and offline.
        log_content = [
            "[INFO] App started.\n",
            "[DEBUG] Debugging info.\n",
            "[WARNING] Something odd.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", no_color=True)
        output = self.mock_stdout.getvalue()

        self.assertIn("[1] [INFO] App started.", output)
        self.assertIn("[2] [DEBUG] Debugging info.", output)
        self.assertIn("[3] [WARNING] Something odd.", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_level_filter(self, mock_file_open):
        # Mock rationale: Simulate reading a log file and verify level filtering.
        log_content = [
            "[INFO] App started.\n",
            "[DEBUG] Debugging info.\n",
            "[ERROR] Critical failure.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", min_level_str="ERROR", no_color=True)
        output = self.mock_stdout.getvalue()

        self.assertNotIn("[INFO] App started.", output)
        self.assertNotIn("[DEBUG] Debugging info.", output)
        self.assertIn("[3] [ERROR] Critical failure.", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_keyword_highlight(self, mock_file_open):
        # Mock rationale: Simulate reading a log file and verify keyword highlighting.
        log_content = [
            "[INFO] User logged in.\n",
            "[ERROR] Connection failed.\n",
            "[WARNING] Disk space low.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", highlight_keywords=["failed"], no_color=True)
        output = self.mock_stdout.getvalue()

        # With no_color=True, rich still formats with tags, but no ANSI codes.
        # We check for the presence of the keyword and the rich tag.
        self.assertIn("Connection [bold magenta on black]failed[/bold magenta on black].", output)
        self.assertNotIn("User logged in.", output) # Should not be highlighted

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_summary(self, mock_file_open):
        # Mock rationale: Simulate reading a log file and verify the summary output.
        log_content = [
            "[INFO] Line 1\n",
            "[ERROR] Line 2\n",
            "[INFO] Line 3\n",
            "[WARNING] Line 4\n",
            "[CRITICAL] Line 5\n",
            "Unclassified line.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", show_summary=True, no_color=True)
        output = self.mock_stdout.getvalue()

        self.assertIn("--- Log Summary ---", output)
        self.assertIn("INFO:         2", output)
        self.assertIn("WARNING:      1", output)
        self.assertIn("ERROR:        1", output)
        self.assertIn("CRITICAL:     1", output)
        self.assertIn("UNCLASSIFIED: 1", output)
        self.assertIn("Total:        6", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError without needing a real file.
        mock_file_open.side_effect = FileNotFoundError

        with self.assertRaises(SystemExit) as cm:
            purifier.purify_logs("non_existent.log")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file not found", self.mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_unclassified_lines_with_level_filter(self, mock_file_open):
        # Mock rationale: Verify unclassified lines are skipped when a min_level is set.
        log_content = [
            "[INFO] Important info.\n",
            "Just some random text.\n",
            "[ERROR] Critical issue.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", min_level_str="INFO", no_color=True)
        output = self.mock_stdout.getvalue()

        self.assertIn("[1] [INFO] Important info.", output)
        self.assertIn("[3] [ERROR] Critical issue.", output)
        self.assertNotIn("Just some random text.", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_purify_logs_unclassified_lines_no_level_filter(self, mock_file_open):
        # Mock rationale: Verify unclassified lines are included when no min_level is set (default DEBUG).
        log_content = [
            "[INFO] Important info.\n",
            "Just some random text.\n",
            "[ERROR] Critical issue.\n"
        ]
        mock_file_open.return_value.__enter__.return_value = log_content

        purifier.purify_logs("dummy.log", min_level_str="DEBUG", no_color=True)
        output = self.mock_stdout.getvalue()

        self.assertIn("[1] [INFO] Important info.", output)
        self.assertIn("[2] [UNCLASSIFIED] Just some random text.", output)
        self.assertIn("[3] [ERROR] Critical issue.", output)

    def test_main_function_calls_purify_logs(self):
        # Mock rationale: Test the main function's argument parsing and call to purify_logs.
        # We mock argparse to control CLI arguments and purify_logs to check if it's called correctly.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('purifier.purify_logs') as mock_purify_logs:

            # Simulate CLI arguments
            mock_parse_args.return_value = argparse.Namespace(
                log_file_path="test.log",
                level="WARNING",
                highlight=["alert"],
                summary=True,
                no_color=False
            )

            purifier.main()

            mock_purify_logs.assert_called_once_with(
                "test.log",
                min_level_str="WARNING",
                highlight_keywords=["alert"],
                show_summary=True,
                no_color=False
            )

if __name__ == '__main__':
    unittest.main()
