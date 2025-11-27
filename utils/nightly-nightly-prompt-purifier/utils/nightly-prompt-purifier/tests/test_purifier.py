import unittest
from unittest.mock import patch, mock_open
import os
import sys
import argparse
from src.purifier import purify_content, main

class TestPurifier(unittest.TestCase):

    def test_redact_api_keys(self):
        input_content = "My API key is OPENROUTER_API_KEY=sk-1234567890abcdef1234567890abcdef. Another token: Bearer ghp_abcdefghijklmnopqrstuvwxyz1234567890. AWS_SECRET_KEY=AKIAIOSFODNN7EXAMPLE and secret: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY. Google token: ya29.a0AfH6SMB_example_token."
        expected_output = "My API key is OPENROUTER_API_KEY=[REDACTED_API_KEY]. Another token: Bearer [REDACTED_API_KEY]. AWS_SECRET_KEY=[REDACTED_API_KEY] and secret: [REDACTED_API_KEY]. Google token: [REDACTED_API_KEY]."
        self.assertEqual(purify_content(input_content, redact_api_keys=True), expected_output)

        # Test with no redaction
        self.assertEqual(purify_content(input_content, redact_api_keys=False), input_content)

    def test_redact_emails(self):
        input_content = "Contact me at test@example.com or support.team@my-company.co.uk. Not an email: user@localhost."
        expected_output = "Contact me at [REDACTED_EMAIL] or [REDACTED_EMAIL]. Not an email: user@localhost."
        self.assertEqual(purify_content(input_content, redact_emails=True), expected_output)

        # Test with no redaction
        self.assertEqual(purify_content(input_content, redact_emails=False), input_content)

    def test_redact_ips(self):
        input_content = "Server IP: 192.168.1.100. Public IP: 203.0.113.45. Not an IP: 999.999.999.999."
        expected_output = "Server IP: [REDACTED_IP]. Public IP: [REDACTED_IP]. Not an IP: 999.999.999.999."
        self.assertEqual(purify_content(input_content, redact_ips=True), expected_output)

        # Test with no redaction
        self.assertEqual(purify_content(input_content, redact_ips=False), input_content)

    def test_optimize_whitespace(self):
        input_content = """Line 1



Line 2
  Line 3 with leading space  

Line 4

"""
        expected_output = """Line 1

Line 2
Line 3 with leading space

Line 4"""
        self.assertEqual(purify_content(input_content, optimize_whitespace=True), expected_output)

        # Test with no optimization
        self.assertEqual(purify_content(input_content, optimize_whitespace=False), input_content.strip())

    def test_custom_keywords(self):
        input_content = "This document contains a secret_project and some confidential_data. Also, SECRET_PROJECT is here."
        custom_keywords = {"secret_project": "[PROJECT_NAME]", "confidential_data": "[CLASSIFIED]"}
        expected_output = "This document contains a [PROJECT_NAME] and some [CLASSIFIED]. Also, [PROJECT_NAME] is here."
        self.assertEqual(purify_content(input_content, custom_keywords=custom_keywords), expected_output)

    def test_combination_of_rules(self):
        input_content = """Hello, my name is John Doe. My email is john.doe@example.com.
My API key is MY_API_KEY=abc123xyz.



My server is at 192.168.0.1. This is a secret_word.

"""
        custom_keywords = {"secret_word": "[REDACTED_WORD]"}
        expected_output = """Hello, my name is John Doe. My email is [REDACTED_EMAIL].
My API key is MY_API_KEY=[REDACTED_API_KEY].

My server is at [REDACTED_IP]. This is a [REDACTED_WORD]."""
        self.assertEqual(purify_content(input_content, custom_keywords=custom_keywords), expected_output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate input file existence
    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print') # Mock rationale: Capture print statements
    def test_main_function_success(self, mock_print, mock_parse_args, mock_makedirs, mock_exists, mock_file_open):
        # Mock rationale: Simulate command-line arguments
        mock_parse_args.return_value = argparse.Namespace(
            input='input.txt',
            output='output.txt',
            keywords='secret=REDACTED_SECRET',
            redact_api_keys=True,
            redact_emails=True,
            redact_ips=True,
            optimize_whitespace=True
        )

        # Mock rationale: Simulate reading from input file
        mock_file_open.side_effect = [
            mock_open(read_data="My key is API_KEY=123. My email is test@example.com. A secret.").return_value,
            mock_open().return_value # For writing output
        ]

        main()

        # Mock rationale: Verify input file was opened for reading
        mock_file_open.assert_any_call('input.txt', 'r', encoding='utf-8')
        # Mock rationale: Verify output file was opened for writing
        mock_file_open.assert_any_call('output.txt', 'w', encoding='utf-8')

        # Mock rationale: Verify the purified content was written correctly
        expected_written_content = "My key is API_KEY=[REDACTED_API_KEY]. My email is [REDACTED_EMAIL]. A [REDACTED_SECRET]."
        mock_file_open().write.assert_called_once_with(expected_written_content)
        mock_print.assert_called_with("Successfully purified 'input.txt' to 'output.txt'.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate input file not found
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent actual system exit during test
    @patch('builtins.print') # Mock rationale: Capture print statements
    def test_main_function_file_not_found(self, mock_print, mock_exit, mock_parse_args, mock_file_open):
        # Mock rationale: Simulate command-line arguments
        mock_parse_args.return_value = argparse.Namespace(
            input='non_existent.txt',
            output='output.txt',
            keywords='',
            redact_api_keys=True,
            redact_emails=True,
            redact_ips=True,
            optimize_whitespace=True
        )

        # Mock rationale: Simulate FileNotFoundError when opening input file
        mock_file_open.side_effect = FileNotFoundError

        main()

        # Mock rationale: Verify error message was printed and program exited with code 1
        mock_print.assert_called_with("Error: Input file 'non_existent.txt' not found.")
        mock_exit.assert_called_with(1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_function_output_dir_creation(self, mock_print, mock_parse_args, mock_makedirs, mock_exists, mock_file_open):
        # Mock rationale: Simulate command-line arguments with an output path requiring directory creation
        mock_parse_args.return_value = argparse.Namespace(
            input='input.txt',
            output='new_dir/output.txt',
            keywords='',
            redact_api_keys=False,
            redact_emails=False,
            redact_ips=False,
            optimize_whitespace=False
        )

        # Mock rationale: Simulate input.txt exists, but 'new_dir' does not
        mock_exists.side_effect = [True, False] 
        mock_file_open.side_effect = [
            mock_open(read_data="content").return_value,
            mock_open().return_value
        ]

        main()

        # Mock rationale: Verify that os.makedirs was called for the new directory
        mock_makedirs.assert_called_once_with('new_dir')
        # Mock rationale: Verify output file was written
        mock_file_open().write.assert_called_once_with("content")
        mock_print.assert_called_with("Successfully purified 'input.txt' to 'new_dir/output.txt'.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_function_invalid_keyword_format(self, mock_print, mock_parse_args, mock_makedirs, mock_exists, mock_file_open):
        # Mock rationale: Simulate command-line arguments with an invalid keyword format
        mock_parse_args.return_value = argparse.Namespace(
            input='input.txt',
            output='output.txt',
            keywords='valid=replacement,invalid_format',
            redact_api_keys=False,
            redact_emails=False,
            redact_ips=False,
            optimize_whitespace=False
        )

        # Mock rationale: Simulate input file existence and content
        mock_file_open.side_effect = [
            mock_open(read_data="content").return_value,
            mock_open().return_value
        ]

        main()

        # Mock rationale: Verify warning message was printed for invalid keyword
        mock_print.assert_any_call("Warning: Invalid keyword format 'invalid_format'. Expected 'key=value'. Skipping.")
        # Mock rationale: Verify content was still written (other operations proceed)
        mock_file_open().write.assert_called_once_with("content")
        mock_print.assert_called_with("Successfully purified 'input.txt' to 'output.txt'.")
