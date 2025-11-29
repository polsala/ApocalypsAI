import unittest
import sys
import os
from unittest.mock import patch, mock_open
from io import StringIO
from src.scavenger import extract_patterns, main

class TestScavenger(unittest.TestCase):

    def test_extract_patterns_url(self):
        text = "Visit https://example.com and http://sub.domain.org/path?query=1. Also ftp://not-a-url.com"
        expected = ["https://example.com", "http://sub.domain.org/path?query=1"]
        self.assertEqual(extract_patterns(text, pattern_type="url"), expected)

    def test_extract_patterns_email(self):
        text = "Contact test@example.com or support@sub.domain.org. Invalid: user@.com"
        expected = ["test@example.com", "support@sub.domain.org"]
        self.assertEqual(extract_patterns(text, pattern_type="email"), expected)

    def test_extract_patterns_custom_regex(self):
        text = "Item ID: ABC-123, Another ID: XYZ-456. No match here."
        expected = ["ABC-123", "XYZ-456"]
        self.assertEqual(extract_patterns(text, custom_regex=r"[A-Z]{3}-\d{3}"), expected)

    def test_extract_patterns_no_match(self):
        text = "No URLs or emails here."
        self.assertEqual(extract_patterns(text, pattern_type="url"), [])
        self.assertEqual(extract_patterns(text, pattern_type="email"), [])
        self.assertEqual(extract_patterns(text, custom_regex=r"\d{5}"), [])

    def test_extract_patterns_invalid_type(self):
        with self.assertRaises(ValueError):
            extract_patterns("some text", pattern_type="invalid_type")

    def test_extract_patterns_no_type_or_regex(self):
        with self.assertRaises(ValueError):
            extract_patterns("some text")

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_single_file_url_to_stdout(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: We need to simulate reading from a file without actually creating one.
        # `mock_open` allows us to control the content returned by `f.read()`.
        # `sys.stdout` and `sys.stderr` are mocked to capture printed output for assertion.
        # `sys.exit` is mocked to prevent the test from terminating the runner.
        mock_file_open.return_value.read.return_value = "Find me at https://my-site.com and http://another.org."
        
        test_args = ["scavenger.py", "test_file.txt", "--type", "url"]
        with patch('sys.argv', test_args):
            main()
        
        self.assertIn("https://my-site.com", mock_stdout.getvalue())
        self.assertIn("http://another.org", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")
        mock_exit.assert_not_called() # Should not exit on success

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_multiple_files_email_to_stdout(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: Similar to the single file test, but `mock_open` needs to handle multiple calls
        # for different files. `side_effect` allows us to provide different mock objects for each call.
        mock_file_open.side_effect = [
            mock_open(read_data="Email me at user1@domain.com.").return_value, # For file1.txt
            mock_open(read_data="And also user2@domain.org.").return_value # For file2.txt
        ]

        test_args = ["scavenger.py", "file1.txt", "file2.txt", "--type", "email"]
        with patch('sys.argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn("user1@domain.com", output)
        self.assertIn("user2@domain.org", output)
        self.assertEqual(mock_stderr.getvalue(), "")
        mock_exit.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: To simulate a FileNotFoundError, we configure `mock_open` to raise it.
        mock_file_open.side_effect = FileNotFoundError
        
        test_args = ["scavenger.py", "non_existent.txt", "--type", "url"]
        with patch('sys.argv', test_args):
            main()
        
        self.assertIn("Error: File not found at 'non_existent.txt'", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_output_to_file(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: `mock_open` is used twice: once for reading the input file,
        # and once for writing to the output file. `mock_file_open.return_value.write`
        # is then checked to see what was written.
        mock_file_open.side_effect = [
            mock_open(read_data="Data: 12345, 67890.").return_value, # For input file
            mock_open().return_value # For output file
        ]
        
        test_args = ["scavenger.py", "input.txt", "--regex", r"\\d{5}", "--output", "output.txt"]
        with patch('sys.argv', test_args):
            main()
        
        # Check that open was called for input.txt and output.txt
        mock_file_open.assert_any_call("input.txt", 'r', encoding='utf-8')
        mock_file_open.assert_any_call("output.txt", 'w', encoding='utf-8')
        
        # Get the mock for the output file handle
        output_file_handle = mock_file_open.side_effect[1]
        output_file_handle.write.assert_any_call("12345\n")
        output_file_handle.write.assert_any_call("67890\n")
        self.assertIn("Extracted data written to 'output.txt'", mock_stdout.getvalue())
        mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_type_or_regex_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: We only need to mock `sys.argv` to test the argument parsing logic.
        test_args = ["scavenger.py", "dummy.txt"]
        with patch('sys.argv', test_args):
            main()
        
        self.assertIn("error: Either --type or --regex must be specified.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(2) # argparse exits with 2 for argument errors

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_patterns_found(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: Simulate a file with no matching patterns.
        mock_file_open.return_value.read.return_value = "This file has no URLs."
        
        test_args = ["scavenger.py", "no_urls.txt", "--type", "url"]
        with patch('sys.argv', test_args):
            main()
        
        self.assertIn("No patterns found across specified files.", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")
        mock_exit.assert_not_called()
