import unittest
from unittest.mock import patch, mock_open
import sys
import json
import re

# Import the functions to be tested
# Assuming analyzer.py is in the same directory for testing purposes
# In a real scenario, you might adjust sys.path or use a proper package structure
# For self-contained utility, this is fine.
from src.analyzer import analyze_log, load_config, DEFAULT_PREMONITIONS

class TestWhispersOfTheVoidLogAnalyzer(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.mock_stdout = unittest.mock.StringIO()
        self.mock_stderr = unittest.mock.StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_with_keywords(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate reading a log file with specific content.
        # This allows testing the keyword matching logic without actual file I/O.
        log_content = (
            "INFO: System started.\n"
            "WARNING: Disk space low.\n"
            "ERROR: Database connection failed.\n"
            "DEBUG: Routine check.\n"
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        # Mock rationale: Ensure load_config returns a controlled set of premonitions.
        # This isolates the analyze_log function from load_config's file reading.
        with patch('src.analyzer.load_config', return_value={
            "keywords": ["low", "failed"],
            "regexes": []
        }):
            analyze_log("dummy_log.log")

        output = self.mock_stdout.getvalue()
        self.assertIn("[LINE 2] Premonition: 'low' found in 'WARNING: Disk space low.'", output)
        self.assertIn("[LINE 3] Premonition: 'failed' found in 'ERROR: Database connection failed.'", output)
        self.assertNotIn("No whispers of the void detected", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_with_regexes(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate reading a log file with specific content.
        log_content = (
            "INFO: System started.\n"
            "CRITICAL: Core meltdown imminent.\n"
            "WARNING: Connection reset by peer.\n"
            "DEBUG: Routine check.\n"
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        # Mock rationale: Ensure load_config returns a controlled set of premonitions.
        with patch('src.analyzer.load_config', return_value={
            "keywords": [],
            "regexes": [r"CRITICAL: .*imminent", r"connection reset by peer"]
        }):
            analyze_log("dummy_log.log")

        output = self.mock_stdout.getvalue()
        self.assertIn("[LINE 2] Premonition: Regex 'CRITICAL: .*imminent' matched in 'CRITICAL: Core meltdown imminent.'", output)
        self.assertIn("[LINE 3] Premonition: Regex 'connection reset by peer' matched in 'WARNING: Connection reset by peer.'", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_no_matches(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate a log file with no matching content.
        log_content = (
            "INFO: System started.\n"
            "DEBUG: Routine check.\n"
            "VERBOSE: All systems nominal.\n"
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        # Mock rationale: Ensure load_config returns a controlled set of premonitions.
        with patch('src.analyzer.load_config', return_value={
            "keywords": ["error", "fail"],
            "regexes": [r"CRITICAL: .*"]
        }):
            analyze_log("dummy_log.log")

        output = self.mock_stdout.getvalue()
        self.assertIn("No whispers of the void detected. All clear... for now.", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_file_not_found(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate FileNotFoundError when opening the log file.
        mock_file_open.side_effect = FileNotFoundError
        analyze_log("non_existent_log.log")
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Error: Log file not found at 'non_existent_log.log'", error_output)
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_from_file(self, mock_file_open):
        # Mock rationale: Simulate reading a valid JSON config file.
        config_content = json.dumps({
            "keywords": ["custom_error", "custom_fail"],
            "regexes": ["custom_regex_.*"]
        })
        mock_file_open.side_effect = [
            mock_open(read_data=config_content).return_value, # For config file
        ]
        config = load_config("dummy_config.json")
        self.assertEqual(config['keywords'], ["custom_error", "custom_fail"])
        self.assertEqual(config['regexes'], ["custom_regex_.*"])

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_load_config_file_not_found(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate FileNotFoundError when opening the config file.
        mock_file_open.side_effect = FileNotFoundError
        load_config("non_existent_config.json")
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Error: Configuration file not found at 'non_existent_config.json'", error_output)
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_load_config_invalid_json(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate reading an invalid JSON config file.
        invalid_json_content = "{'keywords': ['bad_json']"
        mock_file_open.side_effect = [
            mock_open(read_data=invalid_json_content).return_value, # For config file
        ]
        load_config("invalid_config.json")
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Error: Invalid JSON in configuration file 'invalid_config.json'", error_output)
        mock_exit.assert_called_once_with(1)

    def test_load_config_default(self):
        # Mock rationale: Test that load_config returns default premonitions when no config path is given.
        config = load_config(None)
        self.assertEqual(config, DEFAULT_PREMONITIONS)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_with_default_config(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate a log file and ensure default premonitions are used.
        log_content = (
            "INFO: System started.\n"
            "WARNING: Disk space low.\n" # Matches default keyword "low" and regex "disk (full|space low)"
            "ERROR: Database connection failed.\n" # Matches default keyword "fail"
            "CRITICAL: Unhandled exception occurred.\n" # Matches default keyword "critical" and regex "unhandled exception"
            "DEBUG: Routine check.\n"
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        analyze_log("dummy_log.log", config_path=None)

        output = self.mock_stdout.getvalue()
        self.assertIn("[LINE 2] Premonition: 'low' found in 'WARNING: Disk space low.'", output)
        self.assertIn("[LINE 2] Premonition: Regex 'disk (full|space low)' matched in 'WARNING: Disk space low.'", output)
        self.assertIn("[LINE 3] Premonition: 'fail' found in 'ERROR: Database connection failed.'", output)
        self.assertIn("[LINE 4] Premonition: 'critical' found in 'CRITICAL: Unhandled exception occurred.'", output)
        self.assertIn("[LINE 4] Premonition: Regex 'unhandled exception' matched in 'CRITICAL: Unhandled exception occurred.'", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_case_insensitivity(self, mock_exit, mock_file_open):
        # Mock rationale: Test that keyword matching is case-insensitive.
        log_content = (
            "info: system started.\n"
            "warning: DISK SPACE LOW.\n"
            "error: database CONNECTION FAILED.\n"
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        with patch('src.analyzer.load_config', return_value={
            "keywords": ["low", "failed"],
            "regexes": []
        }):
            analyze_log("dummy_log.log")

        output = self.mock_stdout.getvalue()
        self.assertIn("[LINE 2] Premonition: 'low' found in 'warning: DISK SPACE LOW.'", output)
        self.assertIn("[LINE 3] Premonition: 'failed' found in 'error: database CONNECTION FAILED.'", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_empty_log_file(self, mock_exit, mock_file_open):
        # Mock rationale: Simulate an empty log file.
        log_content = ""
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        with patch('src.analyzer.load_config', return_value={
            "keywords": ["error"],
            "regexes": []
        }):
            analyze_log("empty.log")

        output = self.mock_stdout.getvalue()
        self.assertIn("No whispers of the void detected. All clear... for now.", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_analyze_log_multiple_matches_per_line(self, mock_exit, mock_file_open):
        # Mock rationale: Test that only the first keyword and first regex match are reported per line.
        log_content = (
            "ERROR: Disk full and connection failed.\n" # Matches 'full', 'failed', and regex 'disk (full|space low)'
        )
        mock_file_open.side_effect = [
            mock_open(read_data=log_content).return_value, # For log file
        ]

        with patch('src.analyzer.load_config', return_value={
            "keywords": ["full", "failed"],
            "regexes": [r"disk (full|space low)", r"connection failed"]
        }):
            analyze_log("multi_match.log")

        output = self.mock_stdout.getvalue()
        # Expect only one keyword match and one regex match per line due to 'break'
        self.assertIn("[LINE 1] Premonition: 'full' found in 'ERROR: Disk full and connection failed.'", output)
        self.assertIn("[LINE 1] Premonition: Regex 'disk (full|space low)' matched in 'ERROR: Disk full and connection failed.'", output)
        self.assertNotIn("Premonition: 'failed'", output) # Should not be reported if 'full' already matched
        self.assertNotIn("Premonition: Regex 'connection failed'", output) # Should not be reported if 'disk (full|space low)' already matched
        mock_exit.assert_called_once_with(0)
