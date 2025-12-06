import unittest
import os
from unittest.mock import patch, mock_open
from src.analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        # Common setup for tests
        self.default_patterns = [
            r"error", r"fail", r"exception", r"timeout", r"denied",
            r"resource limit", r"memory exhausted", r"disk full",
            r"unhandled", r"deprecated", r"warning", r"critical",
        ]

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_clean_log(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file that exists and contains no patterns above threshold.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "INFO: Application started successfully.\n"
            "DEBUG: Processing request 123.\n"
            "INFO: User 'admin' logged in.\n"
        )
        mock_file_open.return_value.__iter__.return_value = mock_file_open.return_value.read.return_value.splitlines(True)

        analyzer = LogAnalyzer(anomaly_threshold=1) # Set threshold to 1 for easier testing of 'no anomalies'
        result = analyzer.analyze_log_file("test.log")

        self.assertEqual(result["status"], "clean")
        self.assertIn("No significant 'whispers of the void' detected", result["summary"])
        self.assertEqual(result["anomalies"], {})
        self.assertEqual(result["total_lines"], 3)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_log_with_anomalies(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with multiple occurrences of specific error patterns.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "INFO: Application started.\n"
            "ERROR: Connection timeout to database.\n"
            "WARNING: Deprecated API usage detected.\n"
            "ERROR: Connection timeout to database.\n"
            "INFO: Another normal line.\n"
            "ERROR: Connection timeout to database.\n"
            "CRITICAL: Disk full error.\n"
            "WARNING: Deprecated API usage detected.\n"
        )
        mock_file_open.return_value.__iter__.return_value = mock_file_open.return_value.read.return_value.splitlines(True)

        analyzer = LogAnalyzer(anomaly_threshold=2) # Patterns must appear at least twice
        result = analyzer.analyze_log_file("test.log")

        self.assertEqual(result["status"], "anomalies_detected")
        self.assertIn("Detected 3 potential 'whispers of the void'", result["summary"])
        self.assertEqual(result["total_lines"], 8)
        self.assertIn(r"timeout", result["anomalies"])
        self.assertEqual(result["anomalies"][r"timeout"], 3)
        self.assertIn(r"deprecated", result["anomalies"])
        self.assertEqual(result["anomalies"][r"deprecated"], 2)
        self.assertIn(r"error", result["anomalies"]) # 'error' is a default pattern, should catch 'Connection timeout' and 'Disk full'
        self.assertEqual(result["anomalies"][r"error"], 4) # 3 timeouts + 1 disk full

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_log(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty log file.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = ""
        mock_file_open.return_value.__iter__.return_value = []

        analyzer = LogAnalyzer()
        result = analyzer.analyze_log_file("empty.log")

        self.assertEqual(result["status"], "empty_log")
        self.assertIn("The log file is empty. No whispers detected.", result["summary"])
        self.assertEqual(result["anomalies"], {})
        self.assertEqual(result["total_lines"], 0)

    @patch('os.path.exists')
    def test_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a scenario where the log file does not exist.
        mock_exists.return_value = False

        analyzer = LogAnalyzer()
        result = analyzer.analyze_log_file("non_existent.log")

        self.assertEqual(result["status"], "error")
        self.assertIn("Error: File not found", result["summary"])
        self.assertEqual(result["anomalies"], {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_custom_patterns(self, mock_file_open, mock_exists):
        # Mock rationale: Test the analyzer with user-defined custom patterns.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "DEBUG: Initiating phase alpha.\n"
            "WARNING: Phase beta encountered a glitch.\n"
            "DEBUG: Initiating phase alpha.\n"
            "ERROR: Phase gamma failed critically.\n"
            "WARNING: Phase beta encountered a glitch.\n"
            "WARNING: Phase beta encountered a glitch.\n"
        )
        mock_file_open.return_value.__iter__.return_value = mock_file_open.return_value.read.return_value.splitlines(True)

        custom_patterns = [r"phase alpha", r"phase beta", r"phase gamma"]
        analyzer = LogAnalyzer(whisper_patterns=custom_patterns, anomaly_threshold=2)
        result = analyzer.analyze_log_file("custom.log")

        self.assertEqual(result["status"], "anomalies_detected")
        self.assertIn("Detected 2 potential 'whispers of the void'", result["summary"])
        self.assertEqual(result["total_lines"], 6)
        self.assertIn(r"phase beta", result["anomalies"])
        self.assertEqual(result["anomalies"][r"phase beta"], 3)
        self.assertIn(r"phase alpha", result["anomalies"])
        self.assertEqual(result["anomalies"][r"phase alpha"], 2)
        self.assertNotIn(r"phase gamma", result["anomalies"]) # Only 1 occurrence, below threshold 2

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_default_patterns_used_when_none_provided(self, mock_file_open, mock_exists):
        # Mock rationale: Ensure that the default patterns are used when no custom patterns are specified.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "INFO: System boot.\n"
            "ERROR: Critical system failure.\n"
            "WARNING: Low disk space.\n"
            "ERROR: Critical system failure.\n"
        )
        mock_file_open.return_value.__iter__.return_value = mock_file_open.return_value.read.return_value.splitlines(True)

        analyzer = LogAnalyzer(anomaly_threshold=2) # Default patterns, threshold 2
        result = analyzer.analyze_log_file("default.log")

        self.assertEqual(result["status"], "anomalies_detected")
        self.assertIn(r"error", result["anomalies"])
        self.assertEqual(result["anomalies"][r"error"], 2)
        self.assertNotIn(r"warning", result["anomalies"]) # Only 1 occurrence, below threshold 2

if __name__ == '__main__':
    unittest.main()
