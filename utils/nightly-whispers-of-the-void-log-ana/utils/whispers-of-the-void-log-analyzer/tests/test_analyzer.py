import unittest
from unittest.mock import patch, mock_open
import os
import sys
from io import StringIO

# Add the src directory to the path for importing analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from analyzer import analyze_log, load_patterns, DEFAULT_PATTERNS, main

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements in main()
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_with_default_patterns(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file existing and containing specific content.
        # This allows testing the core logic of `analyze_log` without actual file I/O.
        mock_exists.return_value = True
        log_content = (
            "INFO: Application started\n"
            "DEBUG: Processing request\n"
            "ERROR: Failed to connect to database\n"
            "WARNING: Disk space low\n"
            "INFO: User logged out\n"
            "CRITICAL: System panic detected\n"
        )
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        anomalies = analyze_log("dummy_log.log", DEFAULT_PATTERNS)

        self.assertEqual(len(anomalies), 3)
        self.assertEqual(anomalies[0]['line_number'], 3)
        self.assertIn("ERROR", anomalies[0]['content'])
        self.assertEqual(anomalies[1]['line_number'], 4)
        self.assertIn("WARNING", anomalies[1]['content'])
        self.assertEqual(anomalies[2]['line_number'], 6)
        self.assertIn("CRITICAL", anomalies[2]['content'])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_with_custom_patterns(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file existing and containing specific content.
        # This allows testing the core logic of `analyze_log` with custom patterns.
        mock_exists.return_value = True
        log_content = (
            "INFO: Normal operation\n"
            "ALERT: Intrusion attempt detected\n"
            "DEBUG: Another line\n"
            "FAILURE: Service down\n"
        )
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        custom_patterns = [r"ALERT", r"FAILURE"]
        anomalies = analyze_log("dummy_log.log", custom_patterns)

        self.assertEqual(len(anomalies), 2)
        self.assertEqual(anomalies[0]['line_number'], 2)
        self.assertIn("ALERT", anomalies[0]['content'])
        self.assertEqual(anomalies[1]['line_number'], 4)
        self.assertIn("FAILURE", anomalies[1]['content'])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_no_anomalies(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with no matching patterns.
        mock_exists.return_value = True
        log_content = (
            "INFO: All good here\n"
            "DEBUG: Everything is fine\n"
            "NOTICE: Just a regular message\n"
        )
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        anomalies = analyze_log("dummy_log.log", DEFAULT_PATTERNS)
        self.assertEqual(len(anomalies), 0)

    @patch('os.path.exists')
    def test_analyze_log_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent log file.
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            analyze_log("non_existent.log", DEFAULT_PATTERNS)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_patterns_from_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a patterns file existing and containing specific content.
        mock_exists.return_value = True
        patterns_content = (
            "# This is a comment\n"
            "CUSTOM_ERROR\n"
            "ANOMALY_DETECTED\n"
            "  # Another comment\n"
            "  WARNING  \n"
            "\n"
        )
        mock_file_open.return_value.__enter__.return_value = StringIO(patterns_content)

        patterns = load_patterns("dummy_patterns.txt")
        self.assertEqual(patterns, ["CUSTOM_ERROR", "ANOMALY_DETECTED", "WARNING"])

    @patch('os.path.exists')
    def test_load_patterns_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent patterns file.
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_patterns("non_existent_patterns.txt")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success_with_anomalies(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate a successful run of main() where anomalies are found.
        # This tests argument parsing, file reading, and output.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="test.log",
            patterns_file=None
        )
        mock_exists.side_effect = lambda x: x == "test.log" # Only test.log exists
        log_content = "INFO: Normal\nERROR: Something bad\nWARNING: Be careful\n"
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        result = main()
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("Anomalies Detected", output)
        self.assertIn("Line 2 (Pattern: 'ERROR'): ERROR: Something bad", output)
        self.assertIn("Line 3 (Pattern: 'WARNING'): WARNING: Be careful", output)
        self.assertIn("Total anomalies: 2", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success_no_anomalies(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate a successful run of main() where no anomalies are found.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="test.log",
            patterns_file=None
        )
        mock_exists.side_effect = lambda x: x == "test.log"
        log_content = "INFO: Normal\nDEBUG: All clear\n"
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        result = main()
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("No anomalies detected. All clear.", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_log_file_not_found(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate main() handling a non-existent log file.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="non_existent.log",
            patterns_file=None
        )
        mock_exists.return_value = False # No files exist

        result = main()
        self.assertEqual(result, 1)
        output = sys.stdout.getvalue()
        self.assertIn("Error: Log file not found: non_existent.log", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_patterns_file_not_found(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate main() handling a non-existent patterns file.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="test.log",
            patterns_file="non_existent_patterns.txt"
        )
        # Only test.log exists, not the patterns file
        mock_exists.side_effect = lambda x: x == "test.log"
        log_content = "INFO: Normal\n"
        mock_file_open.return_value.__enter__.return_value = StringIO(log_content)

        result = main()
        self.assertEqual(result, 1)
        output = sys.stdout.getvalue()
        self.assertIn("Error: Patterns file not found: non_existent_patterns.txt", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_custom_patterns_file_empty(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate main() handling an empty custom patterns file.
        # It should fall back to default patterns and still process the log.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="test.log",
            patterns_file="empty_patterns.txt"
        )
        mock_exists.side_effect = lambda x: x in ["test.log", "empty_patterns.txt"]
        mock_file_open.side_effect = [
            mock_open(read_data="").return_value, # For empty_patterns.txt
            mock_open(read_data="INFO: Normal\nERROR: Critical issue\n").return_value # For test.log
        ]

        result = main()
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("Warning: No patterns loaded from 'empty_patterns.txt'. Using default patterns.", output)
        self.assertIn("ERROR: Critical issue", output)
        self.assertIn("Total anomalies: 1", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_patterns_at_all(self, mock_parse_args, mock_file_open, mock_exists):
        # Mock rationale: Simulate a scenario where both custom and default patterns are empty.
        # This should result in an error and exit code 1.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="test.log",
            patterns_file="empty_patterns.txt"
        )
        mock_exists.side_effect = lambda x: x in ["test.log", "empty_patterns.txt"]
        # Mock load_patterns to return empty list, and then mock DEFAULT_PATTERNS to be empty
        with patch('analyzer.load_patterns', return_value=[]),
             patch('analyzer.DEFAULT_PATTERNS', []):
            mock_file_open.side_effect = [
                mock_open(read_data="").return_value, # For empty_patterns.txt
                mock_open(read_data="INFO: Normal\n").return_value # For test.log
            ]
            result = main()
            self.assertEqual(result, 1)
            output = sys.stdout.getvalue()
            self.assertIn("Error: No anomaly patterns defined. Exiting.", output)


if __name__ == '__main__':
    unittest.main()
