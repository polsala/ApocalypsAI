import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add the src directory to the path to allow importing luminator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import luminator

class TestLogLuminator(unittest.TestCase):

    def test_get_default_patterns(self):
        # Test that default patterns are returned and are of the correct type
        patterns = luminator.get_default_patterns()
        self.assertIsInstance(patterns, dict)
        self.assertIn("ERROR", patterns)
        self.assertIn("WARNING", patterns)
        self.assertIsInstance(patterns["ERROR"], str)

    def test_scan_log_content_basic_errors(self):
        # Test scanning for basic error patterns
        log_content = (
            "INFO: Application started\n"
            "ERROR: Something went wrong\n"
            "WARNING: Disk space low\n"
            "ERROR: Another critical issue\n"
            "DEBUG: Processing data\n"
            "EXCEPTION: NullPointerException\n"
        )
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)

        self.assertEqual(counts["ERROR"], 2)
        self.assertEqual(counts["WARNING"], 1)
        self.assertEqual(counts["EXCEPTION"], 1)
        self.assertNotIn("INFO", counts)
        self.assertNotIn("DEBUG", counts)
        self.assertEqual(len(anomalies), 2)
        self.assertIn("INFO: Application started", anomalies)
        self.assertIn("DEBUG: Processing data", anomalies)

    def test_scan_log_content_no_errors(self):
        # Test scanning a log with no defined error patterns
        log_content = (
            "INFO: Application started\n"
            "DEBUG: Processing data\n"
            "VERBOSE: User activity logged\n"
        )
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)

        self.assertEqual(len(counts), 0)
        self.assertEqual(len(anomalies), 3)
        self.assertIn("INFO: Application started", anomalies)
        self.assertIn("DEBUG: Processing data", anomalies)
        self.assertIn("VERBOSE: User activity logged", anomalies)

    def test_scan_log_content_all_anomalies(self):
        # Test scanning a log where every line is an anomaly
        log_content = (
            "This is a completely random line.\n"
            "Another line with no known patterns.\n"
            "Just some gibberish here.\n"
        )
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)

        self.assertEqual(len(counts), 0)
        self.assertEqual(len(anomalies), 3)
        self.assertIn("This is a completely random line.", anomalies)

    def test_scan_log_content_case_insensitivity(self):
        # Test that patterns are matched case-insensitively
        log_content = (
            "error: lower case error\n"
            "Warning: mixed case warning\n"
            "EXCEPTION: UPPER CASE EXCEPTION\n"
        )
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)

        self.assertEqual(counts["ERROR"], 1)
        self.assertEqual(counts["WARNING"], 1)
        self.assertEqual(counts["EXCEPTION"], 1)
        self.assertEqual(len(anomalies), 0)

    def test_scan_log_content_empty_log(self):
        # Test scanning an empty log file
        log_content = ""
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)

        self.assertEqual(len(counts), 0)
        self.assertEqual(len(anomalies), 0)

    def test_scan_log_content_with_empty_lines(self):
        # Test scanning a log file with empty lines
        log_content = (
            "INFO: App started\n"
            "\n"
            "ERROR: Failed to connect\n"
            "\n\n"
            "WARNING: Low memory\n"
        )
        patterns = luminator.get_default_patterns()
        counts, anomalies = luminator.scan_log_content(log_content, patterns)
        self.assertEqual(counts["ERROR"], 1)
        self.assertEqual(counts["WARNING"], 1)
        self.assertEqual(len(anomalies), 1)
        self.assertIn("INFO: App started", anomalies)

    def test_main_success(self):
        # Mock file reading and sys.argv for main function test
        mock_log_content = (
            "INFO: App started\n"
            "ERROR: Failed to connect\n"
            "WARNING: Low memory\n"
            "ERROR: Database down\n"
            "DEBUG: Heartbeat\n"
            "CRITICAL: System meltdown imminent\n"
            "Unknown anomaly detected.\n"
        )
        # Mock rationale: Simulate reading a log file from the filesystem without actually creating one.
        with patch('builtins.open', mock_open(read_data=mock_log_content)) as mock_file,
             patch('sys.argv', ['luminator.py', 'test.log']),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            luminator.main()
            output = mock_stdout.getvalue()

            self.assertIn("--- Log Luminator Report ---", output)
            self.assertIn("Scanning: test.log", output)
            self.assertIn("ERROR: 2 occurrences", output)
            self.assertIn("WARNING: 1 occurrence", output)
            self.assertIn("CRITICAL: 1 occurrence", output)
            self.assertIn("Anomalous Lines (3 total):", output)
            self.assertIn("INFO: App started", output)
            self.assertIn("DEBUG: Heartbeat", output)
            self.assertIn("Unknown anomaly detected.", output)
            mock_file.assert_called_once_with('test.log', 'r', encoding='utf-8')

    def test_main_file_not_found(self):
        # Mock file reading to simulate FileNotFoundError
        # Mock rationale: Simulate a non-existent log file without relying on actual file system state.
        with patch('builtins.open', side_effect=FileNotFoundError) as mock_file,
             patch('sys.argv', ['luminator.py', 'non_existent.log']),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            luminator.main()
            output = mock_stdout.getvalue()

            self.assertIn("Error: Log file not found at 'non_existent.log'", output)
            mock_exit.assert_called_once_with(1)
            mock_file.assert_called_once_with('non_existent.log', 'r', encoding='utf-8')

    def test_main_no_arguments(self):
        # Test main function when no log file path is provided
        # Mock rationale: Simulate running the script without arguments to test argument parsing.
        with patch('sys.argv', ['luminator.py']),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            luminator.main()
            output = mock_stdout.getvalue()

            self.assertIn("Usage: python3 src/luminator.py <path_to_log_file>", output)
            mock_exit.assert_called_once_with(1)

    def test_main_other_file_error(self):
        # Mock file reading to simulate a generic IOError
        # Mock rationale: Simulate an unexpected file reading error (e.g., permissions) without actual file system issues.
        with patch('builtins.open', side_effect=IOError("Permission denied")) as mock_file,
             patch('sys.argv', ['luminator.py', 'protected.log']),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            luminator.main()
            output = mock_stdout.getvalue()

            self.assertIn("Error reading file 'protected.log': Permission denied", output)
            mock_exit.assert_called_once_with(1)
            mock_file.assert_called_once_with('protected.log', 'r', encoding='utf-8')

    def test_main_anomaly_line_limit(self):
        # Test that anomalous lines are limited in the report output
        long_anomaly_content = "\n".join([f"Anomaly line {i}" for i in range(20)])
        mock_log_content = (
            "ERROR: First error\n"
            + long_anomaly_content
            + "\nWARNING: Last warning\n"
        )
        # Mock rationale: Simulate a log file with many anomalies to test the output limiting feature.
        with patch('builtins.open', mock_open(read_data=mock_log_content)) as mock_file,
             patch('sys.argv', ['luminator.py', 'long_anomaly.log']),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            luminator.main()
            output = mock_stdout.getvalue()

            self.assertIn("Anomalous Lines (20 total):", output)
            self.assertIn("Anomaly line 0", output)
            self.assertIn("Anomaly line 9", output)
            self.assertNotIn("Anomaly line 10", output) # Should be hidden by '...'
            self.assertIn("... (10 more anomalies not shown)", output)

if __name__ == '__main__':
    unittest.main()
