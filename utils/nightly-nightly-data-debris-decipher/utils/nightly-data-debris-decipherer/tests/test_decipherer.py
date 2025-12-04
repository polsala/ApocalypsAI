import unittest
import json
import sys
import io
from unittest.mock import patch
import runpy

# Import the module under test
from src.decipherer import decipher_debris

class TestDecipherDebris(unittest.TestCase):

    def test_empty_string(self):
        # Test with an empty string, should return empty lists
        text = ""
        result = decipher_debris(text)
        expected = {
            "urls": [],
            "emails": [],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": []
        }
        self.assertEqual(result, expected)

    def test_no_matches(self):
        # Test with text that contains no recognizable patterns
        text = "This is just some plain text without any special data points."
        result = decipher_debris(text)
        expected = {
            "urls": [],
            "emails": [],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": []
        }
        self.assertEqual(result, expected)

    def test_all_patterns_found(self):
        # Test with a string containing all types of patterns
        text = (
            "Visit https://example.com/page?id=123. Contact me at user@domain.org. "
            "Server IP is 192.168.1.1. Logged on 2023-01-15T10:00:00Z. "
            "Another link: http://www.test.net. My email is another.user@sub.domain.co.uk. "
            "Local IP: 10.0.0.255. Event on 2024-02-29. "
            "Numbers: 123, -45.67, 0.0, 99999."
        )
        result = decipher_debris(text)
        expected = {
            "urls": [
                "http://www.test.net",
                "https://example.com/page?id=123"
            ],
            "emails": [
                "another.user@sub.domain.co.uk",
                "user@domain.org"
            ],
            "ipv4_addresses": [
                "10.0.0.255",
                "192.168.1.1"
            ],
            "iso_dates": [
                "2023-01-15T10:00:00Z",
                "2024-02-29"
            ],
            "iso_dates": [
                "2023-01-15T10:00:00Z",
                "2024-02-29"
            ],
            "numbers": [
                "-45.67",
                "0.0",
                "123",
                "99999"
            ]
        }
        self.assertEqual(result, expected)

    def test_duplicate_patterns(self):
        # Test that duplicate patterns are only listed once
        text = (
            "Link: https://duplicate.com. Again: https://duplicate.com. "
            "Email: test@example.com. Another: test@example.com."
        )
        result = decipher_debris(text)
        expected = {
            "urls": [
                "https://duplicate.com"
            ],
            "emails": [
                "test@example.com"
            ],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": []
        }
        self.assertEqual(result, expected)

    def test_noisy_input(self):
        # Test with text containing noise around patterns
        text = (
            "junk_data_https://noisy.url/path_more_junk "
            "email_user@noisy.domain.org_end_email "
            "ip_1.2.3.4_ip_end "
            "date_2025-12-31T23:59:59_date_end "
            "number_123.45_number_end"
        )
        result = decipher_debris(text)
        expected = {
            "urls": [
                "https://noisy.url/path"
            ],
            "emails": [
                "user@noisy.domain.org"
            ],
            "ipv4_addresses": [
                "1.2.3.4"
            ],
            "iso_dates": [
                "2025-12-31T23:59:59"
            ],
            "numbers": [
                "123.45"
            ]
        }
        self.assertEqual(result, expected)

    def test_mixed_case_emails(self):
        # Test that email patterns are case-insensitive for the domain part (standard behavior of regex)
        text = "Email: MixedCase@Domain.com and another@domain.ORG"
        result = decipher_debris(text)
        expected = {
            "urls": [],
            "emails": [
                "MixedCase@Domain.com",
                "another@domain.ORG"
            ],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": []
        }
        self.assertEqual(result, expected)

    def test_various_iso_dates(self):
        # Test different ISO 8601 date/datetime formats
        text = (
            "Date only: 2020-01-01. Datetime: 2021-02-03T11:22:33. "
            "With milliseconds: 2022-03-04T12:34:56.789. "
            "With timezone: 2023-04-05T13:45:00+01:00. "
            "Zulu time: 2024-05-06T14:00:00Z."
        )
        result = decipher_debris(text)
        expected = {
            "urls": [],
            "emails": [],
            "ipv4_addresses": [],
            "iso_dates": [
                "2020-01-01",
                "2021-02-03T11:22:33",
                "2022-03-04T12:34:56.789",
                "2023-04-05T13:45:00+01:00",
                "2024-05-06T14:00:00Z"
            ],
            "numbers": []
        }
        self.assertEqual(result, expected)

    def test_numbers_extraction(self):
        # Test various number formats
        text = "Integers: 123, 0, -45. Floats: 3.14, -0.5, 100.0. Mixed: 1, 2.0, 3."
        result = decipher_debris(text)
        expected = {
            "urls": [],
            "emails": [],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": [
                "-0.5",
                "-45",
                "0",
                "1",
                "100.0",
                "123",
                "2.0",
                "3",
                "3.14"
            ]
        }
        self.assertEqual(result, expected)

    def test_command_line_interface_output(self):
        # Mock rationale: We need to test the CLI output without actually running a subprocess.
        # This is done by temporarily redirecting stdout and capturing the output,
        # and mocking sys.argv to simulate command-line arguments.
        test_input = "CLI test with https://cli.example.com and user@cli.test"
        expected_output_dict = {
            "urls": ["https://cli.example.com"],
            "emails": ["user@cli.test"],
            "ipv4_addresses": [],
            "iso_dates": [],
            "numbers": []
        }
        expected_output_json = json.dumps(expected_output_dict, indent=2) + "\n"

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout,
             patch('sys.argv', ['decipherer.py', test_input]):
            with self.assertRaises(SystemExit) as cm: # sys.exit(0) is called implicitly on success
                runpy.run_module('src.decipherer', run_name='__main__')
            self.assertEqual(cm.exception.code, 0) # Expect successful exit
            self.assertEqual(fake_stdout.getvalue(), expected_output_json)

    def test_command_line_interface_no_args(self):
        # Mock rationale: Test CLI behavior when no arguments are provided, expecting an error message and exit code 1.
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr,
             patch('sys.stdout', new=io.StringIO()) as fake_stdout,
             patch('sys.argv', ['decipherer.py']):
            with self.assertRaises(SystemExit) as cm:
                runpy.run_module('src.decipherer', run_name='__main__')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python -m utils.nightly-data-debris-decipherer.src.decipherer <text_to_decipher>", fake_stderr.getvalue())
            self.assertEqual(fake_stdout.getvalue(), "") # No output to stdout on error

if __name__ == '__main__':
    unittest.main()
