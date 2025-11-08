import unittest
from unittest.mock import patch, mock_open
import os
from io import StringIO

from src.purifier import (
    remove_timestamps,
    redact_sensitive_data,
    collapse_redundant_lines,
    purify_log_content,
    main
)

class TestPurifier(unittest.TestCase):

    def test_remove_timestamps(self):
        # Mock rationale: Testing a pure function, direct string input is sufficient.
        self.assertEqual(remove_timestamps("2023-10-27 10:00:01 INFO: Message"), "INFO: Message")
        self.assertEqual(remove_timestamps("2023-10-27T10:00:01.123Z DEBUG: Message"), "DEBUG: Message")
        self.assertEqual(remove_timestamps("10:00:01 WARNING: Message"), "WARNING: Message")
        self.assertEqual(remove_timestamps("INFO: No timestamp here"), "INFO: No timestamp here")
        self.assertEqual(remove_timestamps("  2023-10-27 10:00:01  ERROR: Something bad  "), "ERROR: Something bad")
        self.assertEqual(remove_timestamps("2023-10-27 10:00:01.123456 INFO: High precision"), "INFO: High precision")
        self.assertEqual(remove_timestamps("2023-10-27 10:00:01+01:00 INFO: Timezone"), "INFO: Timezone")

    def test_redact_sensitive_data(self):
        # Mock rationale: Testing a pure function, direct string input is sufficient.
        self.assertEqual(
            redact_sensitive_data("Connecting to DB at 192.168.1.100 with API_KEY=sk_live_XXXXXXXXXXXXXXXXXXXX"),
            "Connecting to DB at [REDACTED_IP] with API_KEY=[REDACTED_SECRET]"
        )
        self.assertEqual(
            redact_sensitive_data("User token: TOKEN=abc123def456"),
            "User token: TOKEN=[REDACTED_SECRET]"
        )
        self.assertEqual(
            redact_sensitive_data("Secret value is SECRET=my_secret_value"),
            "Secret value is SECRET=[REDACTED_SECRET]"
        )
        self.assertEqual(
            redact_sensitive_data("No sensitive data here."),
            "No sensitive data here."
        )
        self.assertEqual(
            redact_sensitive_data("Access from 10.0.0.5 and 172.16.0.1"),
            "Access from [REDACTED_IP] and [REDACTED_IP]"
        )
        self.assertEqual(
            redact_sensitive_data("AWS key AKIAIOSFODNN7EXAMPLE"),
            "AWS key [REDACTED_SECRET]"
        )
        self.assertEqual(
            redact_sensitive_data("Bearer token BEARER=eyJhbGciOiJIUzI1NiI"),
            "Bearer token BEARER=[REDACTED_SECRET]"
        )

    def test_collapse_redundant_lines(self):
        # Mock rationale: Testing a pure function, direct list input is sufficient.
        self.assertEqual(
            collapse_redundant_lines([
                "Line 1",
                "Line 2",
                "Line 2",
                "Line 3",
                "Line 2",
                "Line 2"
            ]),
            [
                "Line 1",
                "Line 2",
                "Line 3",
                "Line 2"
            ]
        )
        self.assertEqual(collapse_redundant_lines([]), [])
        self.assertEqual(collapse_redundant_lines(["Single line"]), ["Single line"])
        self.assertEqual(collapse_redundant_lines(["A", "A", "A"]), ["A"])

    def test_purify_log_content(self):
        # Mock rationale: Testing the orchestration of pure functions, direct string input is sufficient.
        raw_log = """
2023-10-27 10:00:01 INFO: Starting system initialization.
2023-10-27 10:00:02 DEBUG: Connecting to database at 192.168.1.100 with API_KEY=sk_live_XXXXXXXXXXXXXXXXXXXX
2023-10-27 10:00:03 INFO: System initialized successfully.
2023-10-27 10:00:03 INFO: System initialized successfully.
2023-10-27 10:00:04 WARNING: Potential anomaly detected. TOKEN=abc123def456
2023-10-27 10:00:05 INFO: Another message.
2023-10-27 10:00:05 INFO: Another message.

2023-10-27 10:00:06 ERROR: Critical failure at 172.16.0.10
"""
        expected_purified_log = """
INFO: Starting system initialization.
DEBUG: Connecting to database at [REDACTED_IP] with API_KEY=[REDACTED_SECRET]
INFO: System initialized successfully.
WARNING: Potential anomaly detected. TOKEN=[REDACTED_SECRET]
INFO: Another message.
ERROR: Critical failure at [REDACTED_IP]
""".strip()
        
        self.assertEqual(purify_log_content(raw_log).strip(), expected_purified_log)

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_success(self, mock_stdout, mock_parse_args, mock_file_open):
        # Mock rationale: Mocking file I/O and command-line arguments to ensure deterministic, offline execution.
        # `mock_open` simulates file reading/writing, `parse_args` simulates CLI input, `sys.stdout` captures print output.
        
        mock_parse_args.return_value = argparse.Namespace(
            input='input.log',
            output='output.log'
        )
        
        mock_file_open.return_value.__enter__.return_value.read.return_value = """
2023-10-27 10:00:01 INFO: Test line 1.
2023-10-27 10:00:02 INFO: Test line 2.
2023-10-27 10:00:02 INFO: Test line 2.
"""
        
        main()
        
        mock_file_open.assert_any_call('input.log', 'r')
        mock_file_open.assert_any_call('output.log', 'w')
        
        handle = mock_file_open()
        handle.write.assert_called_once_with("INFO: Test line 1.\nINFO: Test line 2.")
        self.assertIn("Log file 'input.log' purified and saved to 'output.log'.", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_file_not_found(self, mock_stdout, mock_parse_args, mock_file_open):
        # Mock rationale: Mocking file I/O and command-line arguments to simulate a FileNotFoundError.
        # `mock_open` is configured to raise FileNotFoundError when reading.
        
        mock_parse_args.return_value = argparse.Namespace(
            input='non_existent.log',
            output='output.log'
        )
        
        mock_file_open.side_effect = FileNotFoundError
        
        main()
        
        self.assertIn("Error: Input file 'non_existent.log' not found.", mock_stdout.getvalue())
        mock_file_open.assert_called_once_with('non_existent.log', 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_general_exception(self, mock_stdout, mock_parse_args, mock_file_open):
        # Mock rationale: Mocking file I/O and command-line arguments to simulate a general exception during processing.
        # `mock_open` is configured to raise a generic Exception during file reading.
        
        mock_parse_args.return_value = argparse.Namespace(
            input='input.log',
            output='output.log'
        )
        
        mock_file_open.return_value.__enter__.return_value.read.side_effect = Exception("Disk full")
        
        main()
        
        self.assertIn("An error occurred: Disk full", mock_stdout.getvalue())
        mock_file_open.assert_any_call('input.log', 'r')

if __name__ == '__main__':
    unittest.main()
