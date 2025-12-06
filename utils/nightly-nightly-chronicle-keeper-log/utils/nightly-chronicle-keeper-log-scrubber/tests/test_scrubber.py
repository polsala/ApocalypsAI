import unittest
import io
import os
from unittest.mock import patch, mock_open
from src.scrubber import anonymize_line, scrub_log, main

class TestScrubber(unittest.TestCase):

    def test_anonymize_ip(self):
        self.assertEqual(anonymize_line("Access from 192.168.1.1 and 10.0.0.2"), "Access from [ANONYMIZED_IP] and [ANONYMIZED_IP]")
        self.assertEqual(anonymize_line("No IP here."), "No IP here.")
        self.assertEqual(anonymize_line("IPv6 is not covered yet: 2001:0db8::1"), "IPv6 is not covered yet: 2001:0db8::1")

    def test_anonymize_email(self):
        self.assertEqual(anonymize_line("Contact support@example.com or user.name@domain.co.uk"), "Contact [REDACTED_EMAIL] or [REDACTED_EMAIL]")
        self.assertEqual(anonymize_line("No email here."), "No email here.")

    def test_anonymize_credit_card(self):
        # Visa
        self.assertEqual(anonymize_line("Card 4111222233334444 expires 12/25"), "Card [HIDDEN_CARD] expires 12/25")
        # MasterCard
        self.assertEqual(anonymize_line("Payment with 5111222233334444"), "Payment with [HIDDEN_CARD]")
        # Amex
        self.assertEqual(anonymize_line("Amex 341122223333444"), "Amex [HIDDEN_CARD]")
        # Discover
        self.assertEqual(anonymize_line("Discover 6011222233334444"), "Discover [HIDDEN_CARD]")
        self.assertEqual(anonymize_line("No card here."), "No card here.")

    def test_anonymize_multiple_patterns(self):
        log_line = "User user@test.com logged in from 192.168.1.1 with card 4111222233334444."
        expected = "User [REDACTED_EMAIL] logged in from [ANONYMIZED_IP] with card [HIDDEN_CARD]."
        self.assertEqual(anonymize_line(log_line), expected)

    def test_scrub_log_anonymize_only(self):
        input_content = "Line 1: user@example.com\nLine 2: 192.168.1.1\nLine 3: No sensitive data."
        expected_output = "Line 1: [REDACTED_EMAIL]\nLine 2: [ANONYMIZED_IP]\nLine 3: No sensitive data.\n"
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, anonymize=True)
        self.assertEqual(output_stream.getvalue(), expected_output)

    def test_scrub_log_filter_only(self):
        input_content = "ERROR: Something went wrong.\nINFO: All good.\nWARNING: Check this."
        expected_output = "ERROR: Something went wrong.\nWARNING: Check this.\n"
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, keywords=['ERROR', 'WARNING'], anonymize=False)
        self.assertEqual(output_stream.getvalue(), expected_output)

    def test_scrub_log_filter_case_insensitive(self):
        input_content = "error: Something went wrong.\nINFO: All good.\nWarning: Check this."
        expected_output = "error: Something went wrong.\nWarning: Check this.\n"
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, keywords=['error', 'warning'], anonymize=False)
        self.assertEqual(output_stream.getvalue(), expected_output)

    def test_scrub_log_anonymize_and_filter(self):
        input_content = (
            "ERROR: Failed login for user@example.com from 192.168.1.1\n"
            "INFO: System heartbeat OK.\n"
            "WARNING: Suspicious activity from 10.0.0.5\n"
            "ERROR: Another critical issue."
        )
        expected_output = (
            "ERROR: Failed login for [REDACTED_EMAIL] from [ANONYMIZED_IP]\n"
            "WARNING: Suspicious activity from [ANONYMIZED_IP]\n"
            "ERROR: Another critical issue.\n"
        )
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, keywords=['ERROR', 'WARNING'], anonymize=True)
        self.assertEqual(output_stream.getvalue(), expected_output)

    def test_scrub_log_no_anonymize_no_filter(self):
        input_content = "Line 1\nLine 2\nLine 3"
        expected_output = "Line 1\nLine 2\nLine 3\n"
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, anonymize=False)
        self.assertEqual(output_stream.getvalue(), expected_output)

    def test_scrub_log_empty_input(self):
        input_content = ""
        expected_output = ""
        
        input_stream = io.StringIO(input_content)
        output_stream = io.StringIO()
        
        scrub_log(input_stream, output_stream, anonymize=True)
        self.assertEqual(output_stream.getvalue(), expected_output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: We need to simulate command-line arguments and file I/O without
        # actually touching the filesystem or affecting the real stdout/stderr.
        # `mock_parse_args` simulates the CLI arguments.
        # `mock_file_open` simulates opening and reading/writing files.
        # `mock_stdout` and `mock_stderr` capture print statements.

        mock_parse_args.return_value = argparse.Namespace(
            input_file='input.log',
            output_file='output.log',
            keywords=None,
            no_anonymize=False
        )
        
        # Configure the mock_open to return specific content when 'input.log' is opened for reading
        # and to capture output when 'output.log' is opened for writing.
        mock_file_open.side_effect = [
            io.StringIO("User user@test.com logged in from 192.168.1.1."), # For input.log 'r'
            io.StringIO() # For output.log 'w'
        ]

        # Call main
        main()

        # Check if files were opened correctly
        mock_file_open.assert_any_call('input.log', 'r', encoding='utf-8')
        mock_file_open.assert_any_call('output.log', 'w', encoding='utf-8')

        # Check the content written to the output file mock
        # The second call to mock_open.side_effect returns the StringIO for output.log
        written_content = mock_file_open.side_effect[1].getvalue()
        self.assertEqual(written_content, "User [REDACTED_EMAIL] logged in from [ANONYMIZED_IP].\n")
        self.assertIn("Log scrubbed successfully", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: Similar to test_main_success, but specifically testing the FileNotFoundError path.
        # `mock_exit` is used to prevent the test from actually exiting the process.

        mock_parse_args.return_value = argparse.Namespace(
            input_file='non_existent.log',
            output_file='output.log',
            keywords=None,
            no_anonymize=False
        )
        
        # Simulate FileNotFoundError when opening the input file
        mock_file_open.side_effect = FileNotFoundError

        main()

        mock_file_open.assert_called_once_with('non_existent.log', 'r', encoding='utf-8')
        self.assertIn("Error: Input file 'non_existent.log' not found.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_stdout.getvalue(), "")
