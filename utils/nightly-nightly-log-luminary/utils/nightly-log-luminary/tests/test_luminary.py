import unittest
from unittest.mock import patch, mock_open
import sys
import io
import os

# Add the src directory to the path to allow importing luminary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from luminary import LogLuminary

class TestLogLuminary(unittest.TestCase):

    def setUp(self):
        self.log_file_path = 'test.log'
        self.output_file_path = 'report.txt'

    @patch('builtins.open', new_callable=mock_open)
    def test_empty_log_file(self, mock_file):
        # Mock rationale: Simulate an empty log file for testing edge cases.
        mock_file.return_value.read.return_value = ''
        mock_file.return_value.__iter__.return_value = []

        luminary = LogLuminary(self.log_file_path)
        results = luminary.analyze_log()

        self.assertEqual(results['total_lines'], 0)
        self.assertEqual(results['level_counts'], {'OTHER': 0})
        self.assertEqual(results['custom_pattern_counts'], {})
        self.assertEqual(results['error_samples'], [])
        self.assertEqual(results['custom_pattern_samples'], {})

    @patch('builtins.open', new_callable=mock_open)
    def test_basic_log_file(self, mock_file):
        # Mock rationale: Simulate a log file with various standard log levels.
        log_content = (
            "INFO: Application started\n"
            "DEBUG: Loading configuration\n"
            "WARNING: Disk space low\n"
            "ERROR: Failed to connect to database\n"
            "INFO: User logged in\n"
            "Another line without a specific level\n"
            "error: secondary failure\n"
        )
        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        luminary = LogLuminary(self.log_file_path)
        results = luminary.analyze_log()

        self.assertEqual(results['total_lines'], 7)
        self.assertEqual(results['level_counts']['INFO'], 2)
        self.assertEqual(results['level_counts']['DEBUG'], 1)
        self.assertEqual(results['level_counts']['WARNING'], 1)
        self.assertEqual(results['level_counts']['ERROR'], 2)
        self.assertEqual(results['level_counts']['OTHER'], 1)
        self.assertEqual(len(results['error_samples']), 2)
        self.assertIn('ERROR: Failed to connect to database', results['error_samples'][0])
        self.assertIn('error: secondary failure', results['error_samples'][1])

    @patch('builtins.open', new_callable=mock_open)
    def test_custom_patterns(self, mock_file):
        # Mock rationale: Simulate a log file and test matching custom regex patterns.
        log_content = (
            "INFO: User 'admin' logged in\n"
            "ERROR: Authentication failed for user 'guest'\n"
            "WARNING: High CPU usage detected\n"
            "CRITICAL: System meltdown imminent!\n"
            "Failed login attempt from 192.168.1.1\n"
            "ERROR: Another auth failure for user 'admin'\n"
        )
        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        custom_patterns = ["Authentication failed", "CRITICAL", "Failed login attempt"]
        luminary = LogLuminary(self.log_file_path, custom_patterns=custom_patterns)
        results = luminary.analyze_log()

        self.assertEqual(results['total_lines'], 6)
        self.assertEqual(results['level_counts']['ERROR'], 2)
        self.assertEqual(results['level_counts']['INFO'], 1)
        self.assertEqual(results['level_counts']['WARNING'], 1)
        self.assertEqual(results['level_counts']['OTHER'], 2)
        
        self.assertEqual(results['custom_pattern_counts']['Authentication failed'], 2)
        self.assertEqual(results['custom_pattern_counts']['CRITICAL'], 1)
        self.assertEqual(results['custom_pattern_counts']['Failed login attempt'], 1)
        
        self.assertEqual(len(results['custom_pattern_samples']['Authentication failed']), 2)
        self.assertEqual(len(results['custom_pattern_samples']['CRITICAL']), 1)
        self.assertEqual(len(results['custom_pattern_samples']['Failed login attempt']), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_report_to_console(self, mock_stdout, mock_file):
        # Mock rationale: Simulate log file content and capture console output to verify report generation.
        log_content = (
            "INFO: Test message\n"
            "ERROR: Critical error\n"
        )
        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        luminary = LogLuminary(self.log_file_path)
        results = luminary.analyze_log()
        luminary.generate_report(results)

        output = mock_stdout.getvalue()
        self.assertIn('Total Lines Processed: 2', output)
        self.assertIn('INFO: 1', output)
        self.assertIn('ERROR: 1', output)
        self.assertIn('Critical error', output)
        self.assertNotIn('Report saved to', output)

    @patch('builtins.open', new_callable=mock_open)
    def test_generate_report_to_file(self, mock_file):
        # Mock rationale: Simulate log file content and verify that the report is written to the specified output file.
        log_content = (
            "DEBUG: Debug info\n"
            "WARNING: Something is off\n"
        )
        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        luminary = LogLuminary(self.log_file_path, output_file_path=self.output_file_path)
        results = luminary.analyze_log()
        luminary.generate_report(results)

        # Ensure open was called with the output file path in write mode
        mock_file.assert_called_with(self.output_file_path, 'w', encoding='utf-8')
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        self.assertIn('Total Lines Processed: 2', written_content)
        self.assertIn('DEBUG: 1', written_content)
        self.assertIn('WARNING: 1', written_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the log file.
        mock_file.side_effect = FileNotFoundError

        luminary = LogLuminary(self.log_file_path)
        
        with self.assertRaises(SystemExit) as cm:
            luminary.analyze_log()
        self.assertEqual(cm.exception.code, 1)

    @patch('builtins.open', new_callable=mock_open)
    def test_case_sensitivity(self, mock_file):
        # Mock rationale: Test if case-sensitive matching works correctly for log levels and custom patterns.
        log_content = (
            "info: lower case info\n"
            "ERROR: UPPER CASE ERROR\n"
            "Error: Mixed case error\n"
            "CustomPattern: specific match\n"
            "custompattern: no match\n"
        )
        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        # Case-insensitive (default)
        luminary_ci = LogLuminary(self.log_file_path, custom_patterns=["CustomPattern"])
        results_ci = luminary_ci.analyze_log()
        self.assertEqual(results_ci['level_counts']['INFO'], 1)
        self.assertEqual(results_ci['level_counts']['ERROR'], 2)
        self.assertEqual(results_ci['custom_pattern_counts']['CustomPattern'], 2)

        # Case-sensitive
        luminary_cs = LogLuminary(self.log_file_path, custom_patterns=["CustomPattern"], case_sensitive=True)
        results_cs = luminary_cs.analyze_log()
        self.assertEqual(results_cs['level_counts']['INFO'], 0) # 'info' is not 'INFO'
        self.assertEqual(results_cs['level_counts']['ERROR'], 1) # Only 'ERROR' matches
        self.assertEqual(results_cs['custom_pattern_counts']['CustomPattern'], 1) # Only 'CustomPattern' matches

    @patch('builtins.open', new_callable=mock_open)
    def test_max_samples_per_category(self, mock_file):
        # Mock rationale: Ensure that only the first 10 samples are collected for errors and custom patterns.
        error_lines = [f"ERROR: Error {i}" for i in range(15)]
        custom_lines = [f"CUSTOM: Custom {i}" for i in range(15)]
        log_content = "\n".join(error_lines + custom_lines)

        mock_file.return_value.read.return_value = log_content
        mock_file.return_value.__iter__.return_value = log_content.splitlines(keepends=True)

        luminary = LogLuminary(self.log_file_path, custom_patterns=["CUSTOM"])
        results = luminary.analyze_log()

        self.assertEqual(len(results['error_samples']), 10)
        self.assertEqual(len(results['custom_pattern_samples']['CUSTOM']), 10)
        self.assertIn('ERROR: Error 0', results['error_samples'][0])
        self.assertIn('ERROR: Error 9', results['error_samples'][9])
        self.assertIn('CUSTOM: Custom 0', results['custom_pattern_samples']['CUSTOM'][0])
        self.assertIn('CUSTOM: Custom 9', results['custom_pattern_samples']['CUSTOM'][9])

if __name__ == '__main__':
    unittest.main()
