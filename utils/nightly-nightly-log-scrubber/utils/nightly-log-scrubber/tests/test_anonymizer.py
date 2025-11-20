import unittest
import sys
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to the path to allow importing scrubber.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scrubber import scrub_log_content, main

class TestScrubber(unittest.TestCase):

    def test_scrub_ip_addresses(self):
        # Test redaction of IPv4 addresses
        log_content = "User logged in from 192.168.1.1 and 10.0.0.255. Also 172.16.0.1."
        expected = "User logged in from [REDACTED_IP] and [REDACTED_IP]. Also [REDACTED_IP]."
        self.assertEqual(scrub_log_content(log_content, []), expected)

    def test_scrub_email_addresses(self):
        # Test redaction of email addresses
        log_content = "Contact support at user@example.com or admin@sub.domain.org."
        expected = "Contact support at [REDACTED_EMAIL] or [REDACTED_EMAIL]."
        self.assertEqual(scrub_log_content(log_content, []), expected)

    def test_scrub_mixed_content(self):
        # Test redaction of both IPs and emails in the same content
        log_content = "Login from 1.2.3.4 by test@mail.com. Another from 203.0.113.10."
        expected = "Login from [REDACTED_IP] by [REDACTED_EMAIL]. Another from [REDACTED_IP]."
        self.assertEqual(scrub_log_content(log_content, []), expected)

    def test_scrub_no_matches(self):
        # Test content with no sensitive information
        log_content = "This is a safe log entry with no sensitive data."
        expected = "This is a safe log entry with no sensitive data."
        self.assertEqual(scrub_log_content(log_content, []), expected)

    def test_scrub_empty_content(self):
        # Test empty log content
        log_content = ""
        expected = ""
        self.assertEqual(scrub_log_content(log_content, []), expected)

    def test_scrub_custom_pattern(self):
        # Test redaction with a single custom pattern
        log_content = "User ID: 12345, Session: abcdef123456. Another ID: 67890."
        custom_patterns = [("User ID: \\d+", "[REDACTED_USER_ID]")]
        expected = "[REDACTED_USER_ID], Session: abcdef123456. Another ID: 67890."
        self.assertEqual(scrub_log_content(log_content, custom_patterns), expected)

    def test_scrub_multiple_custom_patterns(self):
        # Test redaction with multiple custom patterns
        log_content = "API Key: XYZ123, Token: TKN456. Secret: SSS789."
        custom_patterns = [
            ("API Key: [A-Z0-9]+", "[REDACTED_API_KEY]"),
            ("Token: [A-Z0-9]+", "[REDACTED_TOKEN]")
        ]
        expected = "[REDACTED_API_KEY], [REDACTED_TOKEN]. Secret: SSS789."
        self.assertEqual(scrub_log_content(log_content, custom_patterns), expected)

    def test_main_output_to_stdout(self):
        # Mock rationale: We need to simulate file reading and stdout writing without actual file I/O or console output.
        # `mock_open` simulates `open()` calls, and `patch('sys.stdout', ...)` captures print statements.
        mock_input_content = "Login from 192.168.1.1 by user@example.com."
        expected_output = "Login from [REDACTED_IP] by [REDACTED_EMAIL]."

        with patch('builtins.open', mock_open(read_data=mock_input_content)) as m_open,
             patch('sys.stdout', new_callable=StringIO) as mock_stdout,
             patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                 input='dummy_input.log', output=None, custom_pattern=None, replacement='[REDACTED_CUSTOM]'
             )):
            main()
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            m_open.assert_called_once_with('dummy_input.log', 'r', encoding='utf-8')

    def test_main_output_to_file(self):
        # Mock rationale: Simulate file reading and writing to an output file without actual disk operations.
        # `mock_open` handles both read and write modes based on how it's called.
        mock_input_content = "Login from 192.168.1.1 by user@example.com."
        expected_output = "Login from [REDACTED_IP] by [REDACTED_EMAIL]."
        mock_output_file = 'dummy_output.log'

        with patch('builtins.open', mock_open(read_data=mock_input_content)) as m_open,
             patch('sys.stdout', new_callable=StringIO) as mock_stdout,
             patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                 input='dummy_input.log', output=mock_output_file, custom_pattern=None, replacement='[REDACTED_CUSTOM]'
             )):
            main()
            # Check that open was called for input and output
            m_open.assert_any_call('dummy_input.log', 'r', encoding='utf-8')
            m_open.assert_any_call(mock_output_file, 'w', encoding='utf-8')
            # Check that the write method of the mock file handle was called with the scrubbed content
            m_open().write.assert_called_once_with(expected_output)
            # Check that a success message was printed to stdout
            self.assertIn(f"Scrubbed content written to '{mock_output_file}'", mock_stdout.getvalue())

    def test_main_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the input file.
        # `side_effect=FileNotFoundError` makes `open()` raise the error.
        with patch('builtins.open', side_effect=FileNotFoundError) as m_open,
             patch('sys.stderr', new_callable=StringIO) as mock_stderr,
             patch('sys.exit', side_effect=SystemExit) as mock_exit,
             patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                 input='non_existent.log', output=None, custom_pattern=None, replacement='[REDACTED_CUSTOM]'
             )):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Input file 'non_existent.log' not found.", mock_stderr.getvalue())

    def test_main_custom_pattern_cli(self):
        # Mock rationale: Test the main function's ability to handle custom patterns from CLI arguments.
        mock_input_content = "Secret key: ABC123DEF. Another key: GHI456JKL."
        expected_output = "Secret key: [REDACTED_KEY]. Another key: [REDACTED_KEY]."
        custom_pattern = "Key: [A-Z0-9]+"
        replacement = "[REDACTED_KEY]"

        with patch('builtins.open', mock_open(read_data=mock_input_content)) as m_open,
             patch('sys.stdout', new_callable=StringIO) as mock_stdout,
             patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                 input='dummy_input.log', output=None, custom_pattern=[custom_pattern], replacement=replacement
             )):
            main()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_main_multiple_custom_patterns_cli(self):
        # Mock rationale: Test the main function's ability to handle multiple custom patterns from CLI arguments.
        # The current implementation applies a single replacement string to all custom patterns.
        mock_input_content = "User ID: 12345. Transaction ID: TXN67890. Secret: XYZ."
        custom_patterns = ["User ID: \\d+", "Transaction ID: [A-Z0-9]+"]
        replacement = "[REDACTED_ID]" # This replacement applies to all custom patterns

        expected_output_adjusted = "User ID: [REDACTED_ID]. Transaction ID: [REDACTED_ID]. Secret: XYZ."

        with patch('builtins.open', mock_open(read_data=mock_input_content)) as m_open,
             patch('sys.stdout', new_callable=StringIO) as mock_stdout,
             patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
                 input='dummy_input.log', output=None, custom_pattern=custom_patterns, replacement=replacement
             )):
            main()
            self.assertEqual(mock_stdout.getvalue(), expected_output_adjusted)
