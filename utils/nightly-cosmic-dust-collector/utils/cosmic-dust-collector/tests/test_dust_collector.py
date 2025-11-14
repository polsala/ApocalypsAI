import unittest
from unittest.mock import mock_open, patch
import sys
import os

# Ensure the src directory is in the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dust_collector import CosmicDustCollector, main

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        self.collector = CosmicDustCollector()

    def test_categorize_line_warning(self):
        line = "2023-10-27 10:00:00 [WARN] Disk space low."
        self.assertEqual(self.collector._categorize_line(line), "WARNING")

    def test_categorize_line_error(self):
        line = "2023-10-27 10:01:00 [ERROR] Failed to connect."
        self.assertEqual(self.collector._categorize_line(line), "ERROR")

    def test_categorize_line_critical(self):
        line = "2023-10-27 10:02:00 [CRITICAL] System panic."
        self.assertEqual(self.collector._categorize_line(line), "CRITICAL")

    def test_categorize_line_exception(self):
        line = "2023-10-27 10:03:00 [INFO] An unhandled EXCEPTION occurred."
        self.assertEqual(self.collector._categorize_line(line), "EXCEPTION")

    def test_categorize_line_no_match(self):
        line = "2023-10-27 10:04:00 [INFO] Everything is fine."
        self.assertIsNone(self.collector._categorize_line(line))

    def test_collect_dust_single_file_no_anomalies(self):
        log_content = "Line 1: Info message\nLine 2: Debug message\n"
        # Mock rationale: We need to simulate reading a file without actually touching the filesystem.
        # `mock_open` allows us to provide a string as the file content.
        with patch("builtins.open", mock_open(read_data=log_content)) as mock_file:
            self.collector.collect_dust("test.log")
            mock_file.assert_called_with("test.log", 'r', encoding='utf-8', errors='ignore')
            self.assertEqual(len(self.collector.results["test.log"]["Cosmic Dust Bunnies"]), 0)
            self.assertEqual(len(self.collector.results["test.log"]["Gravitational Glitches"]), 0)
            self.assertEqual(len(self.collector.results["test.log"]["Temporal Anomalies"]), 0)
            self.assertEqual(self.collector.total_counts["Cosmic Dust Bunnies"], 0)
            self.assertEqual(self.collector.total_counts["Gravitational Glitches"], 0)
            self.assertEqual(self.collector.total_counts["Temporal Anomalies"], 0)

    def test_collect_dust_single_file_with_anomalies(self):
        log_content = (
            "INFO: Normal operation\n"
            "WARNING: Disk space low\n"
            "ERROR: Database connection failed\n"
            "DEBUG: Another normal line\n"
            "CRITICAL: Unhandled exception occurred\n"
            "WARN: Deprecated function used\n"
            "Exception in thread: ValueError\n"
        )
        # Mock rationale: Simulating file content for anomaly detection.
        with patch("builtins.open", mock_open(read_data=log_content)):
            self.collector.collect_dust("test.log")
            self.assertEqual(len(self.collector.results["test.log"]["Cosmic Dust Bunnies"]), 2)
            self.assertEqual(len(self.collector.results["test.log"]["Gravitational Glitches"]), 1)
            self.assertEqual(len(self.collector.results["test.log"]["Temporal Anomalies"]), 2) # CRITICAL + EXCEPTION
            self.assertEqual(self.collector.total_counts["Cosmic Dust Bunnies"], 2)
            self.assertEqual(self.collector.total_counts["Gravitational Glitches"], 1)
            self.assertEqual(self.collector.total_counts["Temporal Anomalies"], 2)

    def test_collect_dust_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError without creating a file.
        with patch("builtins.open", side_effect=FileNotFoundError):
            self.collector.collect_dust("nonexistent.log")
            self.assertEqual(len(self.collector.results["nonexistent.log"]["Gravitational Glitches"]), 1)
            self.assertIn("File not found: nonexistent.log", self.collector.results["nonexistent.log"]["Gravitational Glitches"][0])
            self.assertEqual(self.collector.total_counts["Gravitational Glitches"], 1)

    def test_generate_report_empty(self):
        report = self.collector.generate_report()
        self.assertIn("🌌 Cosmic Dust Collector Report 🌌", report)
        self.assertIn("Summary for all files:", report)
        self.assertIn("Total Cosmic Dust Bunnies: 0", report)

    def test_generate_report_with_data(self):
        log_content_1 = "WARNING: Test warning 1\nERROR: Test error 1\n"
        log_content_2 = "CRITICAL: Test critical 2\nWARNING: Test warning 2\n"

        # Mock rationale: Simulate multiple files with different contents.
        # `mock_open` can be configured to return different content for different file paths.
        m = mock_open()
        m.side_effect = [
            mock_open(read_data=log_content_1).return_value,
            mock_open(read_data=log_content_2).return_value
        ]
        with patch("builtins.open", m):
            self.collector.collect_dust("file1.log")
            self.collector.collect_dust("file2.log")

        report = self.collector.generate_report()

        self.assertIn("Scanning: file1.log", report)
        self.assertIn("✨ Cosmic Dust Bunnies (warnings): 1", report)
        self.assertIn("  - WARNING: Test warning 1", report)
        self.assertIn("💥 Gravitational Glitches (errors): 1", report)
        self.assertIn("  - ERROR: Test error 1", report)

        self.assertIn("Scanning: file2.log", report)
        self.assertIn("⏳ Temporal Anomalies (exceptions/criticals): 1", report)
        self.assertIn("  - CRITICAL: Test critical 2", report)
        self.assertIn("✨ Cosmic Dust Bunnies (warnings): 1", report)
        self.assertIn("  - WARNING: Test warning 2", report)

        self.assertIn("Summary for all files:", report)
        self.assertIn("Total Cosmic Dust Bunnies: 2", report)
        self.assertIn("Total Gravitational Glitches: 1", report)
        self.assertIn("Total Temporal Anomalies: 1", report)

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.argv', ['dust_collector.py', 'test.log'])
    def test_main_function_success(self, mock_stdout):
        log_content = "WARNING: Main test warning\n"
        # Mock rationale: Test the main function's output and file handling.
        # `mock_open` simulates the file, `patch('sys.stdout')` captures print output,
        # `patch('sys.argv')` simulates command-line arguments.
        with patch("builtins.open", mock_open(read_data=log_content)):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("🌌 Cosmic Dust Collector Report 🌌", output)
            self.assertIn("Scanning: test.log", output)
            self.assertIn("✨ Cosmic Dust Bunnies (warnings): 1", output)
            self.assertIn("Total Cosmic Dust Bunnies: 1", output)

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['dust_collector.py'])
    def test_main_function_no_args(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's error handling for missing arguments.
        # `patch('sys.exit')` prevents the program from actually exiting during the test.
        main()
        mock_exit.assert_called_with(1)
        self.assertIn("Usage: python src/dust_collector.py <path_to_log_file_1> [path_to_log_file_2 ...]", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
