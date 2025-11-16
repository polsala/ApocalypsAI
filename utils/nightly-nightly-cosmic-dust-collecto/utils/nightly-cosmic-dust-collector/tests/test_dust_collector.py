import unittest
from unittest.mock import patch, mock_open
import sys
import os
import io
import argparse

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_collector

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr to prevent test output from cluttering console
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = self._devnull = open(os.devnull, 'w')
        sys.stderr = self._devnull

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr
        self._devnull.close()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_anomalies(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with no keywords to ensure no anomalies are reported.
        mock_exists.return_value = True
        log_content = "\n".join([
            "INFO: This is a normal log line.",
            "DEBUG: Another routine entry.",
            "INFO: Everything is fine.",
            "DEBUG: No issues here.",
            "INFO: All good."
        ])
        mock_file_open.return_value.read.return_value = log_content
        mock_file_open.return_value.__iter__.return_value = iter(log_content.splitlines(keepends=True))

        anomalies = dust_collector._analyze_file(
            'test.log', ['ERROR', 'CRITICAL'], threshold=0.1, window_size=3
        )
        self.assertEqual(len(anomalies), 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_anomaly_spike(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with a concentrated spike of error keywords
        # to verify that the anomaly detection triggers correctly.
        mock_exists.return_value = True
        log_content = "\n".join([
            "INFO: Normal line 1.",
            "INFO: Normal line 2.",
            "ERROR: Critical issue detected!",
            "WARNING: Something is amiss.",
            "ERROR: Another problem.",
            "INFO: Normal line 3.",
            "INFO: Normal line 4."
        ])
        mock_file_open.return_value.read.return_value = log_content
        mock_file_open.return_value.__iter__.return_value = iter(log_content.splitlines(keepends=True))

        # Window size 3, threshold 0.33 (1/3). Lines 3,4,5: ERROR, WARNING, ERROR -> 3/3 = 1.0 > 0.33
        anomalies = dust_collector._analyze_file(
            'test.log', ['ERROR', 'WARNING'], threshold=0.33, window_size=3
        )
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['start_line'], 3)
        self.assertEqual(anomalies[0]['end_line'], 5)
        self.assertAlmostEqual(anomalies[0]['density'], 1.0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_anomalies(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with multiple distinct error spikes
        # to ensure all anomalies are captured.
        mock_exists.return_value = True
        log_content = "\n".join([
            "INFO: Normal line 1.",
            "ERROR: Problem A.",
            "INFO: Normal line 2.",
            "ERROR: Problem B.",
            "ERROR: Problem C.",
            "INFO: Normal line 3.",
            "INFO: Normal line 4.",
            "ERROR: Problem D.",
            "ERROR: Problem E.",
            "INFO: Normal line 5."
        ])
        mock_file_open.return_value.read.return_value = log_content
        mock_file_open.return_value.__iter__.return_value = iter(log_content.splitlines(keepends=True))

        # Window size 3, threshold 0.6 (e.g., 2/3 lines with keywords)
        anomalies = dust_collector._analyze_file(
            'test.log', ['ERROR'], threshold=0.6, window_size=3
        )
        self.assertEqual(len(anomalies), 2)
        self.assertEqual(anomalies[0]['start_line'], 3) # Lines 3,4,5: INFO, ERROR, ERROR -> 2/3
        self.assertEqual(anomalies[0]['end_line'], 5)
        self.assertAlmostEqual(anomalies[0]['density'], 2/3)
        self.assertEqual(anomalies[1]['start_line'], 7) # Lines 7,8,9: INFO, ERROR, ERROR -> 2/3
        self.assertEqual(anomalies[1]['end_line'], 9)
        self.assertAlmostEqual(anomalies[1]['density'], 2/3)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_case_insensitivity(self, mock_file_open, mock_exists):
        # Mock rationale: Verify that keyword matching is case-insensitive.
        mock_exists.return_value = True
        log_content = "\n".join([
            "info: normal line.",
            "error: lowercase error.",
            "WARNING: uppercase warning.",
            "Info: Mixed case info."
        ])
        mock_file_open.return_value.read.return_value = log_content
        mock_file_open.return_value.__iter__.return_value = iter(log_content.splitlines(keepends=True))

        anomalies = dust_collector._analyze_file(
            'test.log', ['error', 'warning'], threshold=0.5, window_size=2
        )
        self.assertEqual(len(anomalies), 1) # Lines 2,3: error, WARNING -> 2/2 = 1.0 > 0.5
        self.assertEqual(anomalies[0]['start_line'], 2)
        self.assertEqual(anomalies[0]['end_line'], 3)
        self.assertAlmostEqual(anomalies[0]['density'], 1.0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file_open, mock_exists):
        # Mock rationale: Ensure the utility handles non-existent files gracefully.
        mock_exists.return_value = False
        anomalies = dust_collector._analyze_file(
            'non_existent.log', ['ERROR'], threshold=0.1, window_size=10
        )
        self.assertEqual(len(anomalies), 0)
        mock_file_open.assert_not_called() # Ensure open is not called if file doesn't exist

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_file(self, mock_file_open, mock_exists):
        # Mock rationale: Test behavior with an empty log file.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = ""
        mock_file_open.return_value.__iter__.return_value = iter([])

        anomalies = dust_collector._analyze_file(
            'empty.log', ['ERROR'], threshold=0.1, window_size=10
        )
        self.assertEqual(len(anomalies), 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_partial_window_anomaly(self, mock_file_open, mock_exists):
        # Mock rationale: Test anomaly detection when the file ends with a partial window
        # that still meets the anomaly threshold.
        mock_exists.return_value = True
        log_content = "\n".join([
            "INFO: Normal line 1.",
            "INFO: Normal line 2.",
            "ERROR: Problem A.",
            "ERROR: Problem B."
        ])
        mock_file_open.return_value.read.return_value = log_content
        mock_file_open.return_value.__iter__.return_value = iter(log_content.splitlines(keepends=True))

        # Window size 5, threshold 0.5. Last 2 lines are errors. Total 4 lines.
        # Partial window (lines 3,4): ERROR, ERROR -> 2/2 = 1.0 > 0.5
        anomalies = dust_collector._analyze_file(
            'test.log', ['ERROR'], threshold=0.5, window_size=5
        )
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['start_line'], 3)
        self.assertEqual(anomalies[0]['end_line'], 4)
        self.assertAlmostEqual(anomalies[0]['density'], 1.0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_io_error_handling(self, mock_file_open, mock_exists):
        # Mock rationale: Ensure the utility gracefully handles IOError during file reading.
        mock_exists.return_value = True
        mock_file_open.side_effect = IOError("Permission denied")
        
        # Redirect stderr to capture the error message
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            anomalies = dust_collector._analyze_file(
                'unreadable.log', ['ERROR'], threshold=0.1, window_size=10
            )
            self.assertEqual(len(anomalies), 0)
            self.assertIn("Error reading file unreadable.log: Permission denied", mock_stderr.getvalue())

    @patch('sys.exit')
    @patch('dust_collector.scan_logs')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_anomalies_exit_0(self, mock_parse_args, mock_scan_logs, mock_sys_exit):
        # Mock rationale: Test the main function's exit code when no anomalies are found.
        mock_parse_args.return_value = argparse.Namespace(
            log_paths=['/var/log/test.log'],
            keywords=['ERROR'],
            threshold=0.1,
            window_size=10
        )
        mock_scan_logs.return_value = []
        dust_collector.main()
        mock_sys_exit.assert_called_once_with(0)

    @patch('sys.exit')
    @patch('dust_collector.scan_logs')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_anomalies_exit_1(self, mock_parse_args, mock_scan_logs, mock_sys_exit):
        # Mock rationale: Test the main function's exit code when anomalies are found.
        mock_parse_args.return_value = argparse.Namespace(
            log_paths=['/var/log/test.log'],
            keywords=['ERROR'],
            threshold=0.1,
            window_size=10
        )
        mock_scan_logs.return_value = [{'file': 'test.log', 'start_line': 1, 'end_line': 5, 'density': 0.2, 'message': 'test'}]
        dust_collector.main()
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_threshold_exit_1(self, mock_parse_args, mock_sys_exit):
        # Mock rationale: Test argument validation for threshold.
        mock_parse_args.return_value = argparse.Namespace(
            log_paths=['/var/log/test.log'],
            keywords=['ERROR'],
            threshold=1.5,
            window_size=10
        )
        dust_collector.main()
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_window_size_exit_1(self, mock_parse_args, mock_sys_exit):
        # Mock rationale: Test argument validation for window size.
        mock_parse_args.return_value = argparse.Namespace(
            log_paths=['/var/log/test.log'],
            keywords=['ERROR'],
            threshold=0.1,
            window_size=0
        )
        dust_collector.main()
        mock_sys_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
