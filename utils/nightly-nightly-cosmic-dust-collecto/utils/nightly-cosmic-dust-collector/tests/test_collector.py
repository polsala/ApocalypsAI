import unittest
from unittest.mock import patch, mock_open
import os
import argparse
from collections import defaultdict

# Mock rationale: We need to simulate file system interactions (reading files, walking directories)
# without actually touching the disk. This ensures tests are deterministic, fast, and isolated.

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_log_files(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a directory existing but containing no .log files.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['file.txt', 'image.jpg'])
        ]
        from src.collector import collect_dust
        results = collect_dust('/mock/path', ['ERROR'])

        self.assertEqual(results['total_files_scanned'], 0)
        self.assertEqual(results['total_anomalies_found'], 0)
        self.assertEqual(len(results['unique_anomaly_lines']), 0)
        self.assertEqual(results['pattern_counts'], defaultdict(int))
        mock_file_open.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_log_file_no_anomalies(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a log file with no matching patterns.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['app.log'])
        ]
        mock_file_open.return_value.read.return_value = (
            "Info: Application started.\n"
            "Debug: Processing request.\n"
            "Warning: Low disk space.\n"
        )
        from src.collector import collect_dust
        results = collect_dust('/mock/path', ['ERROR', 'FAIL'])

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_lines_scanned'], 3)
        self.assertEqual(results['total_anomalies_found'], 0)
        self.assertEqual(len(results['unique_anomaly_lines']), 0)
        self.assertEqual(results['pattern_counts'], defaultdict(int))
        mock_file_open.assert_called_once_with('/mock/path/app.log', 'r', encoding='utf-8', errors='ignore')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_log_file_with_anomalies(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a log file containing multiple matching patterns.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['app.log'])
        ]
        mock_file_open.return_value.read.return_value = (
            "Info: Application started.\n"
            "ERROR: Something went wrong!\n"
            "Debug: Processing request.\n"
            "FAIL: Critical operation failed.\n"
            "Warning: Low disk space.\n"
            "Another ERROR occurred.\n"
        )
        from src.collector import collect_dust
        results = collect_dust('/mock/path', ['ERROR', 'FAIL'])

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_lines_scanned'], 6)
        self.assertEqual(results['total_anomalies_found'], 3)
        self.assertEqual(len(results['unique_anomaly_lines']), 3)
        self.assertIn('ERROR: Something went wrong!', results['unique_anomaly_lines'])
        self.assertIn('FAIL: Critical operation failed.', results['unique_anomaly_lines'])
        self.assertIn('Another ERROR occurred.', results['unique_anomaly_lines'])
        self.assertEqual(results['pattern_counts']['ERROR'], 2)
        self.assertEqual(results['pattern_counts']['FAIL'], 1)
        self.assertIn('/mock/path/app.log', results['files_with_anomalies'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_log_files_with_anomalies(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate multiple log files across different directories with various anomalies.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', ['sub1'], ['app.log']),
            ('/mock/path/sub1', [], ['worker.log', 'api.log'])
        ]

        # Configure mock_open to return different content based on the file path
        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path == '/mock/path/app.log':
                return mock_open(read_data="Info\nERROR: App crash\nDebug").return_value
            elif file_path == '/mock/path/sub1/worker.log':
                return mock_open(read_data="Worker started\nFAIL: Task failed\nWorker stopped").return_value
            elif file_path == '/mock/path/sub1/api.log':
                return mock_open(read_data="API up\nException: DB error\nAPI down").return_value
            return mock_open().return_value # Default for other files

        mock_file_open.side_effect = mock_open_side_effect

        from src.collector import collect_dust
        results = collect_dust('/mock/path', ['ERROR', 'FAIL', 'Exception'])

        self.assertEqual(results['total_files_scanned'], 3)
        self.assertEqual(results['total_lines_scanned'], 9)
        self.assertEqual(results['total_anomalies_found'], 3)
        self.assertEqual(len(results['unique_anomaly_lines']), 3)
        self.assertIn('ERROR: App crash', results['unique_anomaly_lines'])
        self.assertIn('FAIL: Task failed', results['unique_anomaly_lines'])
        self.assertIn('Exception: DB error', results['unique_anomaly_lines'])
        self.assertEqual(results['pattern_counts']['ERROR'], 1)
        self.assertEqual(results['pattern_counts']['FAIL'], 1)
        self.assertEqual(results['pattern_counts']['Exception'], 1)
        self.assertIn('/mock/path/app.log', results['files_with_anomalies'])
        self.assertIn('/mock/path/sub1/worker.log', results['files_with_anomalies'])
        self.assertIn('/mock/path/sub1/api.log', results['files_with_anomalies'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_directory_not_found(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate the scenario where the specified root directory does not exist.
        mock_os_path_isdir.return_value = False
        from src.collector import collect_dust
        results = collect_dust('/nonexistent/path', ['ERROR'])

        self.assertEqual(results['total_files_scanned'], 0)
        self.assertEqual(results['total_anomalies_found'], 0)
        mock_os_walk.assert_not_called() # os.walk should not be called if dir doesn't exist
        mock_file_open.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_case_insensitivity(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Ensure pattern matching is case-insensitive as intended by re.IGNORECASE.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['case.log'])
        ]
        mock_file_open.return_value.read.return_value = (
            "info: all good\n"
            "error: lowercase error\n"
            "WARNING: something bad\n"
            "Error: Mixed case error\n"
            "EXCEPTION: Uppercase exception\n"
        )
        from src.collector import collect_dust
        results = collect_dust('/mock/path', ['error', 'exception'])

        self.assertEqual(results['total_files_scanned'], 1)
        self.assertEqual(results['total_lines_scanned'], 5)
        self.assertEqual(results['total_anomalies_found'], 3)
        self.assertIn('error: lowercase error', results['unique_anomaly_lines'])
        self.assertIn('Error: Mixed case error', results['unique_anomaly_lines'])
        self.assertIn('EXCEPTION: Uppercase exception', results['unique_anomaly_lines'])
        self.assertEqual(results['pattern_counts']['error'], 2)
        self.assertEqual(results['pattern_counts']['exception'], 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_main_with_default_patterns(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Test that the main function correctly uses default patterns when none are provided via CLI.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['default.log'])
        ]
        mock_file_open.return_value.read.return_value = (
            "Info: Normal line\n"
            "This is an ERROR line.\n"
            "A Traceback occurred.\n"
            "Another line with FAIL.\n"
        )

        from src.collector import main, collect_dust
        
        # Mock argparse to simulate CLI arguments without actually running sys.argv
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('src.collector.collect_dust') as mock_collect_dust,
             patch('builtins.print'): # Suppress print output for cleaner test
            
            # Simulate calling main without --patterns argument
            mock_parse_args.return_value = argparse.Namespace(
                path='/mock/path',
                patterns=['ERROR', 'FAIL', 'Exception', 'Traceback'] # This is what argparse returns when default is used
            )
            main()
            
            # Verify that collect_dust was called with the correct path and default patterns
            mock_collect_dust.assert_called_once_with('/mock/path', ['ERROR', 'FAIL', 'Exception', 'Traceback'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_read_error(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a scenario where a log file exists but cannot be read (e.g., permission error).
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['unreadable.log'])
        ]
        mock_file_open.side_effect = IOError("Permission denied")
        
        from src.collector import collect_dust
        with patch('builtins.print') as mock_print:
            results = collect_dust('/mock/path', ['ERROR'])

            self.assertEqual(results['total_files_scanned'], 1)
            self.assertEqual(results['total_lines_scanned'], 0) # No lines read if file can't be opened
            self.assertEqual(results['total_anomalies_found'], 0)
            mock_print.assert_called_with("Warning: Could not read file '/mock/path/unreadable.log': Permission denied")
            mock_file_open.assert_called_once_with('/mock/path/unreadable.log', 'r', encoding='utf-8', errors='ignore')


if __name__ == '__main__':
    unittest.main()
