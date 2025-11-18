import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add the src directory to the path to allow importing scrubber
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scrubber

class TestScrubber(unittest.TestCase):

    def test_scrub_ip_addresses(self):
        log_content = "Request from 192.168.1.1 and 10.0.0.254. Another IP: 172.16.0.1."
        expected_content = "Request from [SCRUBBED_IP] and [SCRUBBED_IP]. Another IP: [SCRUBBED_IP]."
        self.assertEqual(scrubber.scrub_log_content(log_content), expected_content)

    def test_scrub_email_addresses(self):
        log_content = "User foo@example.com logged in. Contact support@domain.org."
        expected_content = "User [SCRUBBED_EMAIL] logged in. Contact [SCRUBBED_EMAIL]."
        self.assertEqual(scrubber.scrub_log_content(log_content), expected_content)

    def test_scrub_generic_secrets(self):
        # Example of a long alphanumeric string that might be a token/key
        log_content = "API key: abcdefghijklmnopqrstuvwxyz0123456789ABCDEF. Another: GHIJKLMNOPQRSTUVWXYZ9876543210."
        expected_content = "API key: [SCRUBBED_SECRET]. Another: [SCRUBBED_SECRET]."
        self.assertEqual(scrubber.scrub_log_content(log_content), expected_content)

    def test_scrub_mixed_content(self):
        log_content = (
            "User test@mail.com from 192.168.1.1 accessed resource with token "
            "XYZ123ABC456DEF789GHI012JKL345MNO678PQR901STU234VWX567YZA890."
        )
        expected_content = (
            "User [SCRUBBED_EMAIL] from [SCRUBBED_IP] accessed resource with token "
            "[SCRUBBED_SECRET]."
        )
        self.assertEqual(scrubber.scrub_log_content(log_content), expected_content)

    def test_no_sensitive_data(self):
        log_content = "This is a clean log entry with no sensitive data."
        self.assertEqual(scrubber.scrub_log_content(log_content), log_content)

    def test_empty_content(self):
        log_content = ""
        self.assertEqual(scrubber.scrub_log_content(log_content), "")

    def test_custom_patterns(self):
        log_content = "Order ID: 1234567890. Transaction Ref: TXN-ABC-123. User ID: user_1234."
        custom_patterns = [r"Order ID: (\d+)", r"TXN-[A-Z]{3}-\d{3}", r"user_\d+"]
        expected_content = "Order ID: [SCRUBBED_CUSTOM_1]. Transaction Ref: [SCRUBBED_CUSTOM_2]. User ID: [SCRUBBED_CUSTOM_3]."
        self.assertEqual(scrubber.scrub_log_content(log_content, custom_patterns), expected_content)

    def test_custom_patterns_overlap_with_defaults(self):
        # Custom pattern for IPs should be applied first if it's passed via custom_patterns
        log_content = "IP address is 192.168.1.1. Another IP: 10.0.0.1."
        custom_patterns = [r"IP address is (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", r"Another IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"]
        expected_content = "IP address is [SCRUBBED_CUSTOM_1]. Another IP: [SCRUBBED_CUSTOM_2]."
        self.assertEqual(scrubber.scrub_log_content(log_content, custom_patterns), expected_content)

    def test_invalid_custom_pattern(self):
        log_content = "Some content with a secret: SECRET123."
        # An invalid regex pattern (unclosed parenthesis)
        custom_patterns = [r"SECRET("]
        # Expect the invalid pattern to be skipped, and default patterns still apply
        # In this case, 'SECRET123' is not long enough for default secret scrubbing
        expected_content = "Some content with a secret: SECRET123."

        with patch('sys.stderr', new_callable=mock_open) as mock_stderr:
            result = scrubber.scrub_log_content(log_content, custom_patterns)
            self.assertEqual(result, expected_content)
            # Mock rationale: We are testing that an invalid regex pattern is handled gracefully
            # by printing an error to stderr and continuing, rather than crashing.
            # We check if stderr was written to with an error message.
            mock_stderr().write.assert_called_once()
            self.assertIn("Error: Invalid custom regex pattern 'SECRET('", mock_stderr().write.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open, read_data="test content")
    @patch('sys.argv', ['scrubber.py', 'input.log', 'output.log'])
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_file_open):
        # Mock rationale: We are testing the main function's file I/O and argument parsing.
        # `builtins.open` is mocked to simulate reading from 'input.log' and writing to 'output.log'.
        # `sys.argv` is mocked to simulate command-line arguments.
        # `sys.exit` is mocked to prevent the test from actually exiting.
        scrubber.main()
        mock_file_open.assert_any_call('input.log', 'r', encoding='utf-8')
        mock_file_open.assert_any_call('output.log', 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with('test content') # No scrubbing for 'test content'
        mock_exit.assert_not_called()

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.argv', ['scrubber.py', 'nonexistent.log', 'output.log'])
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=mock_open)
    def test_main_input_file_not_found(self, mock_stderr, mock_exit, mock_file_open):
        # Mock rationale: Testing error handling when the input file does not exist.
        # `builtins.open` is mocked to raise FileNotFoundError.
        # `sys.exit` is mocked to check if the program attempts to exit with an error code.
        # `sys.stderr` is mocked to capture error messages.
        scrubber.main()
        mock_exit.assert_called_once_with(1)
        mock_stderr().write.assert_called_once()
        self.assertIn("Error: Input file 'nonexistent.log' not found.", mock_stderr().write.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open, read_data="content")
    @patch('sys.argv', ['scrubber.py', 'input.log', 'output.log'])
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=mock_open)
    def test_main_output_file_write_error(self, mock_stderr, mock_exit, mock_file_open):
        # Mock rationale: Testing error handling during writing to the output file.
        # `builtins.open` is configured to raise an exception during the write operation.
        # `sys.exit` and `sys.stderr` are mocked as above.
        mock_file_open.return_value.__enter__.return_value.write.side_effect = IOError("Disk full")
        scrubber.main()
        mock_exit.assert_called_once_with(1)
        mock_stderr().write.assert_called_once()
        self.assertIn("Error writing to output file 'output.log': Disk full", mock_stderr().write.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open, read_data="log with 192.168.1.1")
    @patch('sys.argv', ['scrubber.py', 'input.log', 'output.log', '--patterns', 'user_\\d+'])
    @patch('sys.exit')
    def test_main_with_custom_patterns(self, mock_exit, mock_file_open):
        # Mock rationale: Testing main function with custom patterns.
        # `builtins.open` is mocked to provide content and capture written output.
        # `sys.argv` is mocked to include custom patterns.
        # `sys.exit` is mocked to prevent actual exit.
        scrubber.main()
        mock_file_open.assert_any_call('input.log', 'r', encoding='utf-8')
        mock_file_open.assert_any_call('output.log', 'w', encoding='utf-8')
        # The default IP pattern should still apply, as the custom pattern is for 'user_\d+'
        mock_file_open().write.assert_called_once_with('log with [SCRUBBED_IP]')
        mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
