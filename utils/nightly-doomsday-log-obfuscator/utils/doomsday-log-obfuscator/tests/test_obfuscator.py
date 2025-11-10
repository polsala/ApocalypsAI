import unittest
from unittest.mock import patch, mock_open
import os
import sys
import argparse

# Add the src directory to the path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from obfuscator import obfuscate_log_content, main

class TestObfuscator(unittest.TestCase):

    def test_obfuscate_ip_addresses(self):
        log_line = "Connection from 192.168.1.100 and 10.0.0.5."
        expected = "Connection from [OBFUSCATED_IP] and [OBFUSCATED_IP]."
        self.assertEqual(obfuscate_log_content(log_line), expected)

    def test_obfuscate_secret_project_names(self):
        log_line = "Initiating Project Chimera. Operation Phoenix is next. Project Mjolnir online."
        expected = "Initiating [CLASSIFIED_PROJECT]. [CLASSIFIED_PROJECT] is next. [CLASSIFIED_PROJECT] online."
        self.assertEqual(obfuscate_log_content(log_line), expected)

    def test_obfuscate_sensitive_numeric_ids(self):
        log_line = "Agent ID: 12345 reported. Target: 98765 confirmed."
        expected = "[REDACTED_ID] reported. [REDACTED_ID] confirmed."
        self.assertEqual(obfuscate_log_content(log_line), expected)

    def test_multiple_obfuscations_in_one_line(self):
        log_line = "[ERROR] Failed to connect 172.16.0.1. Agent ID: 11223. Project Chimera aborted."
        expected = "[ERROR] Failed to connect [OBFUSCATED_IP]. [REDACTED_ID]. [CLASSIFIED_PROJECT] aborted."
        self.assertEqual(obfuscate_log_content(log_line), expected)

    def test_no_obfuscation_needed(self):
        log_line = "Normal log message without sensitive data."
        expected = "Normal log message without sensitive data."
        self.assertEqual(obfuscate_log_content(log_line), expected)

    def test_empty_string(self):
        self.assertEqual(obfuscate_log_content(""), "")

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_success(self, mock_parse_args, mock_file_open):
        # Mock rationale: We need to simulate file I/O without actually touching the filesystem.
        # `builtins.open` is mocked to control what `infile.read()` returns and what `outfile.write()` receives.
        # `argparse.ArgumentParser.parse_args` is mocked to provide command-line arguments programmatically.

        mock_parse_args.return_value = argparse.Namespace(
            input_file='input.log',
            output_file='output.log'
        )

        mock_file_open.side_effect = [
            mock_open(read_data="INFO: 192.168.1.1 Project Chimera\nAgent ID: 12345").return_value, # For input file
            mock_open().return_value # For output file
        ]

        # Capture print output
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with("Log successfully obfuscated from 'input.log' to 'output.log'.")
        
        # Assert that the input file was opened for reading
        mock_file_open.assert_any_call('input.log', 'r')
        # Assert that the output file was opened for writing
        mock_file_open.assert_any_call('output.log', 'w')

        # Get the mock for the output file handle
        output_handle = mock_file_open().return_value
        # Assert that the correct obfuscated content was written
        output_handle.write.assert_called_once_with(
            "INFO: [OBFUSCATED_IP] [CLASSIFIED_PROJECT]\n[REDACTED_ID]"
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_file_not_found(self, mock_parse_args, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the input file.
        # `argparse.ArgumentParser.parse_args` is mocked to provide command-line arguments programmatically.
        # `builtins.open` is mocked to raise FileNotFoundError when called.

        mock_parse_args.return_value = argparse.Namespace(
            input_file='non_existent.log',
            output_file='output.log'
        )

        mock_file_open.side_effect = FileNotFoundError # Simulate file not found

        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with(
                "Error: One of the files not found. Check paths: non_existent.log, output.log"
            )

if __name__ == '__main__':
    unittest.main()
