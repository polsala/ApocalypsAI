import unittest
from unittest.mock import patch, mock_open
import sys
import io
import os

# Mock rationale: We need to test the core logic of `scrub_log_content` and the `main` function's
# interaction with the file system and standard output/error without performing actual I/O operations.
# `patch('builtins.open')` allows us to simulate reading from an input file and writing to an output file.
# `patch('sys.stdout', new_callable=io.StringIO)` allows us to capture console output for verification.
# `patch('sys.stderr', new_callable=io.StringIO)` allows us to capture error output for verification.
# `patch('sys.exit')` is used to prevent `sys.exit(1)` calls within `main` from terminating the test runner.

# Adjust sys.path to allow importing scrubber.py directly from src/
# This is a common pattern for self-contained utilities where tests are in a sibling directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scrubber import scrub_log_content, main
sys.path.pop(0) # Clean up sys.path after import

class TestScrubber(unittest.TestCase):

    def test_scrub_log_content_basic_filtering(self):
        log_content = """
INFO: User logged in
DEBUG: Database query executed
ERROR: Failed to connect to service
INFO: User logged out
"""
        glimmers = []
        glooms = ["DEBUG"]
        expected_output = [
            "INFO: User logged in",
            "ERROR: Failed to connect to service",
            "INFO: User logged out"
        ]
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    def test_scrub_log_content_basic_highlighting(self):
        log_content = """
INFO: User logged in
DEBUG: Database query executed
ERROR: Failed to connect to service
INFO: User logged out
"""
        glimmers = ["ERROR"]
        glooms = []
        expected_output = [
            "INFO: User logged in",
            "DEBUG: Database query executed",
            "[GLIMMER] ERROR: Failed to connect to service",
            "INFO: User logged out"
        ]
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    def test_scrub_log_content_both_filtering_and_highlighting(self):
        log_content = """
INFO: User logged in
DEBUG: Database query executed
WARNING: Low disk space
ERROR: Critical system failure
INFO: User logged out
"""
        glimmers = ["ERROR", "WARNING"]
        glooms = ["DEBUG", "INFO"]
        expected_output = [
            "[GLIMMER] WARNING: Low disk space",
            "[GLIMMER] ERROR: Critical system failure"
        ]
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    def test_scrub_log_content_empty_input(self):
        log_content = ""
        glimmers = ["ERROR"]
        glooms = ["DEBUG"]
        expected_output = []
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    def test_scrub_log_content_no_matches(self):
        log_content = """
Line 1
Line 2
Line 3
"""
        glimmers = ["ERROR"]
        glooms = ["DEBUG"]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    def test_scrub_log_content_glimmer_is_also_gloom(self):
        # Gloom takes precedence, so the line should be filtered out entirely.
        log_content = """
ERROR: This is a critical error.
"""
        glimmers = ["ERROR"]
        glooms = ["critical"]
        expected_output = []
        self.assertEqual(scrub_log_content(log_content, glimmers, glooms), expected_output)

    @patch('builtins.open', new_callable=mock_open, read_data="Test log content\nAnother line")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_output_to_stdout(self, mock_stderr, mock_stdout, mock_file_open):
        test_args = ['scrubber.py', 'input.log', '--glimmers', 'Test']
        with patch('sys.argv', test_args):
            main()
            self.assertIn('[GLIMMER] Test log content', mock_stdout.getvalue())
            self.assertIn('Another line', mock_stdout.getvalue())
            self.assertEqual(mock_stderr.getvalue(), '')

    @patch('builtins.open', new_callable=mock_open, read_data="Test log content\nAnother line")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_output_to_file(self, mock_stderr, mock_stdout, mock_file_open):
        test_args = ['scrubber.py', 'input.log', '--output', 'output.log', '--glimmers', 'Test']
        with patch('sys.argv', test_args):
            main()
            mock_file_open.assert_called_with('output.log', 'w')
            handle = mock_file_open()
            handle.write.assert_any_call('[GLIMMER] Test log content\n')
            handle.write.assert_any_call('Another line\n')
            self.assertIn("Scrubbed log written to 'output.log'.", mock_stdout.getvalue())
            self.assertEqual(mock_stderr.getvalue(), '')

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        mock_file_open.side_effect = FileNotFoundError
        test_args = ['scrubber.py', 'non_existent.log']
        with patch('sys.argv', test_args):
            main()
            self.assertIn("Error: Input file 'non_existent.log' not found.", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data="Test content")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_output_write_error(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Configure the mock_open for writing to raise an exception
        mock_file_open.return_value.__enter__.return_value.write.side_effect = IOError("Disk full")
        test_args = ['scrubber.py', 'input.log', '--output', 'output.log']
        with patch('sys.argv', test_args):
            main()
            self.assertIn("Error writing to output file: Disk full", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)
