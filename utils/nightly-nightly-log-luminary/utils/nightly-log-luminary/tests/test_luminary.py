import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.luminary import LogLuminary, main

class TestLogLuminary(unittest.TestCase):

    def setUp(self):
        self.luminary = LogLuminary()

    def test_analyze_log_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open a non-existent file.
        with patch('builtins.open', side_effect=FileNotFoundError),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             self.assertRaises(SystemExit) as cm:
            self.luminary.analyze_log('non_existent.log')
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    def test_analyze_log_empty_file(self):
        # Mock rationale: Simulate reading an empty log file.
        mock_file_content = ""
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            log_content, total_lines = self.luminary.analyze_log('empty.log')
            mock_file.assert_called_once_with('empty.log', 'r', encoding='utf-8')
            self.assertEqual(log_content, [])
            self.assertEqual(total_lines, 0)
            self.assertEqual(self.luminary.log_levels, {
                'CRITICAL': 0, 'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'UNKNOWN': 0
            })

    def test_analyze_log_various_levels(self):
        # Mock rationale: Simulate reading a log file with various log levels.
        mock_file_content = (
            "INFO: Application started\n"
            "DEBUG: Processing request 123\n"
            "WARNING: Low disk space detected\n"
            "ERROR: Failed to connect to database\n"
            "CRITICAL: System meltdown imminent\n"
            "Another info message\n"
            "error: secondary failure\n"
            "warn: something minor\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            log_content, total_lines = self.luminary.analyze_log('test.log')
            mock_file.assert_called_once_with('test.log', 'r', encoding='utf-8')
            self.assertEqual(total_lines, 8)
            self.assertEqual(self.luminary.log_levels, {
                'CRITICAL': 1, 'ERROR': 2, 'WARNING': 2, 'INFO': 2, 'DEBUG': 1, 'UNKNOWN': 0
            })
            self.assertEqual(len(log_content), 8)

    def test_analyze_log_unknown_lines(self):
        # Mock rationale: Simulate reading a log file with lines that don't match known levels.
        mock_file_content = (
            "Just a regular line\n"
            "Another line without keywords\n"
            "INFO: Something happened\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            log_content, total_lines = self.luminary.analyze_log('unknown.log')
            self.assertEqual(total_lines, 3)
            self.assertEqual(self.luminary.log_levels, {
                'CRITICAL': 0, 'ERROR': 0, 'WARNING': 0, 'INFO': 1, 'DEBUG': 0, 'UNKNOWN': 2
            })

    def test_generate_report(self):
        self.luminary.log_levels = {
            'CRITICAL': 1,
            'ERROR': 2,
            'WARNING': 3,
            'INFO': 10,
            'DEBUG': 5,
            'UNKNOWN': 2
        }
        report = self.luminary.generate_report('test.log', 23)
        expected_report_parts = [
            "--- Log Luminary Report ---",
            "File: test.log",
            "Severity Summary:",
            "  CRITICAL: 1",
            "  ERROR   : 2",
            "  WARNING : 3",
            "  INFO    : 10",
            "  DEBUG   : 5",
            "  UNKNOWN : 2",
            "",
            "Total Lines Scanned: 23",
            "",
            "--- End Report ---"
        ]
        # We need to account for the extra newline at the end of the report string
        self.assertEqual(report, "\n".join(expected_report_parts))

    def test_generate_report_only_unknown(self):
        self.luminary.log_levels = {
            'CRITICAL': 0, 'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'UNKNOWN': 5
        }
        report = self.luminary.generate_report('only_unknown.log', 5)
        expected_report_parts = [
            "--- Log Luminary Report ---",
            "File: only_unknown.log",
            "Severity Summary:",
            "  UNKNOWN : 5",
            "",
            "Total Lines Scanned: 5",
            "",
            "--- End Report ---"
        ]
        self.assertEqual(report, "\n".join(expected_report_parts))

    def test_generate_report_empty_log_levels(self):
        self.luminary.log_levels = {
            'CRITICAL': 0, 'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'UNKNOWN': 0
        }
        report = self.luminary.generate_report('empty.log', 0)
        expected_report_parts = [
            "--- Log Luminary Report ---",
            "File: empty.log",
            "Severity Summary:",
            "",
            "Total Lines Scanned: 0",
            "",
            "--- End Report ---"
        ]
        self.assertEqual(report, "\n".join(expected_report_parts))

    def test_print_highlighted_log(self):
        log_content = [
            "INFO: Normal line",
            "WARNING: Something to watch",
            "ERROR: Critical failure",
            "DEBUG: Detailed info",
            "CRITICAL: System going down"
        ]
        # Mock rationale: Capture stdout to verify the printed output with ANSI escape codes.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.luminary.print_highlighted_log(log_content)
            output = mock_stdout.getvalue()
            self.assertIn("--- Highlighted Log Entries ---", output)
            self.assertIn("\033[93mWARNING: Something to watch\033[0m", output) # Yellow
            self.assertIn("\033[91mERROR: Critical failure\033[0m", output)   # Red
            self.assertIn("\033[91mCRITICAL: System going down\033[0m", output) # Red
            self.assertIn("INFO: Normal line", output) # Not highlighted
            self.assertIn("DEBUG: Detailed info", output) # Not highlighted
            self.assertIn("--- End Highlighted Log ---", output)

    @patch('src.luminary.LogLuminary.analyze_log')
    @patch('src.luminary.LogLuminary.generate_report')
    @patch('src.luminary.LogLuminary.print_highlighted_log')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['luminary.py', 'test.log'])
    def test_main_no_highlight(self, mock_stdout, mock_print_highlighted, mock_generate_report, mock_analyze_log):
        # Mock rationale: Simulate CLI arguments and mock internal methods to isolate main's logic.
        mock_analyze_log.return_value = (['line1'], 1)
        mock_generate_report.return_value = "Report content"
        main()
        mock_analyze_log.assert_called_once_with('test.log')
        mock_generate_report.assert_called_once_with('test.log', 1)
        mock_print_highlighted.assert_not_called()
        self.assertIn("Report content", mock_stdout.getvalue())

    @patch('src.luminary.LogLuminary.analyze_log')
    @patch('src.luminary.LogLuminary.generate_report')
    @patch('src.luminary.LogLuminary.print_highlighted_log')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['luminary.py', 'test.log', '--highlight'])
    def test_main_with_highlight(self, mock_stdout, mock_print_highlighted, mock_generate_report, mock_analyze_log):
        # Mock rationale: Simulate CLI arguments and mock internal methods to isolate main's logic.
        mock_analyze_log.return_value = (['line1', 'line2'], 2)
        mock_generate_report.return_value = "Report content"
        main()
        mock_analyze_log.assert_called_once_with('test.log')
        mock_generate_report.assert_called_once_with('test.log', 2)
        mock_print_highlighted.assert_called_once_with(['line1', 'line2'])
        self.assertIn("Report content", mock_stdout.getvalue())

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['luminary.py', 'non_existent.log'])
    def test_main_file_not_found_exit(self, mock_exit, mock_stderr, mock_open):
        # Mock rationale: Simulate FileNotFoundError during main execution and verify sys.exit is called.
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Log file not found", mock_stderr.getvalue())
