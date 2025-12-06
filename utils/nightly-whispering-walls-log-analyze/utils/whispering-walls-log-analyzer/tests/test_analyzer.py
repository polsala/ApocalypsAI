import unittest
import sys
import os
import json
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to sys.path to allow importing analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import analyzer

class TestWhisperingWallsLogAnalyzer(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_default_patterns_detection(self, mock_stdout):
        # Mock rationale: Simulate reading a log file without actual file I/O.
        mock_log_content = (
            "INFO: Application started.\n"
            "ERROR: Database connection failed.\n"
            "DEBUG: Processing request.\n"
            "WARNING: Disk space low.\n"
            "FATAL: System halted.\n"
            "INFO: User logged in.\n"
            "EXCEPTION: NullPointerException at line 123.\n"
            "CRITICAL: Memory allocation error.\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_log_content)):
            analyzer.analyze_log("dummy.log")

        output = mock_stdout.getvalue()
        self.assertIn("Listening to the digital whispers...", output)
        self.assertIn("[Line 2] A faint echo of despair: ERROR: Database connection failed. found!", output)
        self.assertIn("[Line 4] The walls murmur a caution: WARNING: Disk space low. detected.", output)
        self.assertIn("[Line 5] A strange ripple in the data stream: FATAL: System halted. observed.", output)
        self.assertIn("[Line 7] A sudden tremor in the fabric of reality: EXCEPTION: NullPointerException at line 123. occurred.", output)
        self.assertIn("[Line 8] The very foundations groan: CRITICAL: Memory allocation error. event.", output)
        self.assertIn("Analysis complete. The walls have spoken.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_patterns_found(self, mock_stdout):
        # Mock rationale: Simulate a log file with no matching patterns.
        mock_log_content = (
            "INFO: Application started.\n"
            "DEBUG: Processing request.\n"
            "INFO: User logged in.\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_log_content)):
            analyzer.analyze_log("dummy.log")

        output = mock_stdout.getvalue()
        self.assertIn("The walls are silent. No significant whispers detected.", output)
        self.assertIn("Analysis complete. The walls have spoken.", output)
        self.assertNotIn("ERROR", output)
        self.assertNotIn("WARNING", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_log_file_not_found(self, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the log file.
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(SystemExit) as cm:
                analyzer.analyze_log("non_existent.log")
            self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file 'non_existent.log' not found.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_custom_patterns_from_config(self, mock_stdout):
        # Mock rationale: Simulate reading a log file and a custom config file.
        mock_log_content = (
            "INFO: Application started.\n"
            "User 'admin' authentication failed.\n"
            "DEBUG: Data processing complete.\n"
            "System overload detected.\n"
        )
        mock_config_content = json.dumps({
            "patterns": [
                {"regex": "authentication failed", "narrative": "A shadowy figure tried to enter: '{match}'."},
                {"regex": "System overload", "narrative": "The core shudders under immense strain: '{match}'."}
            ]
        })

        # Mock open for both log file and config file
        mock_files = {
            "dummy.log": mock_open(read_data=mock_log_content).return_value,
            "custom_config.json": mock_open(read_data=mock_config_content).return_value
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in mock_files:
                return mock_files[file_path]
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")

        with patch('builtins.open', side_effect=mock_open_side_effect):
            analyzer.analyze_log("dummy.log", config_file="custom_config.json")

        output = mock_stdout.getvalue()
        self.assertIn("Listening to the digital whispers...", output)
        self.assertIn("[Line 2] A shadowy figure tried to enter: 'User 'admin' authentication failed.'.", output)
        self.assertIn("[Line 4] The core shudders under immense strain: 'System overload detected.'.", output)
        self.assertIn("Analysis complete. The walls have spoken.", output)
        # Ensure default patterns are still checked (if not overridden by custom logic)
        self.assertNotIn("ERROR", output) # No ERROR in log

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_malformed_config_file(self, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an invalid JSON config file.
        mock_log_content = "ERROR: Test error."
        mock_config_content = "{'patterns': [invalid json" # Malformed JSON

        mock_files = {
            "dummy.log": mock_open(read_data=mock_log_content).return_value,
            "malformed_config.json": mock_open(read_data=mock_config_content).return_value
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in mock_files:
                return mock_files[file_path]
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")

        with patch('builtins.open', side_effect=mock_open_side_effect):
            with self.assertRaises(SystemExit) as cm:
                analyzer.analyze_log("dummy.log", config_file="malformed_config.json")
            self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Invalid JSON in configuration file 'malformed_config.json'.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_first_match_only_per_line(self, mock_stdout):
        # Mock rationale: Ensure only the first matching pattern on a line is reported.
        mock_log_content = "ERROR: Critical failure detected. WARNING: Secondary issue."
        with patch('builtins.open', mock_open(read_data=mock_log_content)):
            analyzer.analyze_log("dummy.log")

        output = mock_stdout.getvalue()
        self.assertIn("[Line 1] A faint echo of despair: ERROR: Critical failure detected. WARNING: Secondary issue. found!", output)
        self.assertNotIn("The walls murmur a caution:", output) # Should not find WARNING as ERROR was first

if __name__ == '__main__':
    unittest.main()
