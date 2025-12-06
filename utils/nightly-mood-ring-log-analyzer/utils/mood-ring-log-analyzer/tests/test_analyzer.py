import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Add the src directory to the path to allow importing analyzer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from analyzer import analyze_log_content, main

class TestMoodRingLogAnalyzer(unittest.TestCase):

    def test_empty_log(self):
        log_content = ""
        result = analyze_log_content(log_content)
        self.assertEqual(result['overall_mood'], 'SERENE')
        self.assertEqual(result['mood_counts'], {'Calm': 0, 'Anxious': 0, 'Critical': 0, 'Mysterious': 0})
        self.assertIn('serene', result['message'].lower())

    def test_calm_log(self):
        log_content = (
            "2023-10-27 10:00:01 INFO System started successfully.\n"
            "2023-10-27 10:00:02 DEBUG Processing user request.\n"
            "2023-10-27 10:00:03 NOTICE Database connection established."
        )
        result = analyze_log_content(log_content)
        self.assertEqual(result['overall_mood'], 'CALM')
        self.assertEqual(result['mood_counts'], {'Calm': 3, 'Anxious': 0, 'Critical': 0, 'Mysterious': 0})
        self.assertIn('calm', result['message'].lower())

    def test_anxious_log(self):
        log_content = (
            "2023-10-27 10:00:01 INFO System started successfully.\n"
            "2023-10-27 10:00:02 WARNING Disk space low.\n"
            "2023-10-27 10:00:03 WARN High CPU usage detected."
        )
        result = analyze_log_content(log_content)
        self.assertEqual(result['overall_mood'], 'ANXIOUS')
        self.assertEqual(result['mood_counts'], {'Calm': 1, 'Anxious': 2, 'Critical': 0, 'Mysterious': 0})
        self.assertIn('tense', result['message'].lower())

    def test_critical_log(self):
        log_content = (
            "2023-10-27 10:00:01 INFO System started successfully.\n"
            "2023-10-27 10:00:02 ERROR Failed to connect to external service.\n"
            "2023-10-27 10:00:03 CRITICAL System going down.\n"
            "2023-10-27 10:00:04 FATAL Unrecoverable error."
        )
        result = analyze_log_content(log_content)
        self.assertEqual(result['overall_mood'], 'CRITICAL')
        self.assertEqual(result['mood_counts'], {'Calm': 1, 'Anxious': 0, 'Critical': 3, 'Mysterious': 0})
        self.assertIn('criticality', result['message'].lower())

    def test_mysterious_log(self):
        log_content = (
            "2023-10-27 10:00:01 Some random unclassified line.\n"
            "2023-10-27 10:00:02 Another strange entry.\n"
            "2023-10-27 10:00:03 INFO Normal info line."
        )
        result = analyze_log_content(log_content)
        self.assertEqual(result['overall_mood'], 'MYSTERIOUS')
        self.assertEqual(result['mood_counts'], {'Calm': 1, 'Anxious': 0, 'Critical': 0, 'Mysterious': 2})
        self.assertIn('enigmatic', result['message'].lower())

    def test_mixed_log_priority(self):
        log_content = (
            "INFO: All good.\n"
            "WARNING: Something minor.\n"
            "ERROR: Major issue.\n"
            "DEBUG: Tracing.\n"
            "WARN: Another warning.\n"
            "CRITICAL: System failure.\n"
            "UNKNOWN: Unclassified line."
        )
        result = analyze_log_content(log_content)
        # Critical (2), Anxious (2), Calm (2), Mysterious (1)
        # Overall mood should be CRITICAL due to priority
        self.assertEqual(result['overall_mood'], 'CRITICAL')
        self.assertEqual(result['mood_counts'], {'Calm': 2, 'Anxious': 2, 'Critical': 2, 'Mysterious': 1})

    @patch('builtins.open', new_callable=mock_open, read_data="INFO: Test log line.\nWARNING: Another line.")
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['analyzer.py', 'test.log'])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_success(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: We mock 'builtins.open' to simulate reading a log file without actual file system access.
        # We mock 'os.path.exists' to confirm the file 'exists' for the script.
        # We mock 'sys.argv' to provide command-line arguments to the main function.
        # We mock 'sys.stdout' to capture printed output for assertion.
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Analyzing log file: test.log', output)
        self.assertIn('Overall System Mood: ANXIOUS', output)
        self.assertIn('Calm: 1', output)
        self.assertIn('Anxious: 1', output)

    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['analyzer.py', 'non_existent.log'])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_stdout, mock_exists):
        # Mock rationale: We mock 'os.path.exists' to simulate a non-existent file.
        # We mock 'sys.argv' to provide command-line arguments.
        # We mock 'sys.stdout' to capture printed output.
        # We mock 'sys.exit' to prevent the test from terminating the runner.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Log file not found at 'non_existent.log'", output)
        mock_exit.assert_called_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['analyzer.py', 'unreadable.log'])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_main_file_read_error(self, mock_exit, mock_stdout, mock_exists, mock_file):
        # Mock rationale: We mock 'builtins.open' to simulate a file that raises an error on read.
        # We mock 'os.path.exists' to confirm the file 'exists'.
        # We mock 'sys.argv' to provide command-line arguments.
        # We mock 'sys.stdout' to capture printed output.
        # We mock 'sys.exit' to prevent the test from terminating the runner.
        mock_file.side_effect = IOError("Permission denied")
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error reading log file 'unreadable.log': Permission denied", output)
        mock_exit.assert_called_with(1)

    @patch('sys.argv', ['analyzer.py'])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_main_no_arguments(self, mock_exit, mock_stdout):
        # Mock rationale: We mock 'sys.argv' to simulate no command-line arguments.
        # We mock 'sys.stdout' to capture printed output.
        # We mock 'sys.exit' to prevent the test from terminating the runner.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Usage: python analyzer.py <path_to_log_file>", output)
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
