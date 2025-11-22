import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.analyzer import analyze_log, main

class TestGloomGlimmerLogAnalyzer(unittest.TestCase):

    def test_analyze_empty_log(self):
        log_content = ""
        results = analyze_log(log_content)
        self.assertEqual(results['total_lines'], 0)
        self.assertEqual(results['total_gloom'], 0)
        self.assertEqual(results['total_glimmer'], 0)
        self.assertEqual(results['gloom_keywords'], {})
        self.assertEqual(results['glimmer_keywords'], {})

    def test_analyze_only_gloom(self):
        log_content = (
            "2023-10-27 10:00:01 ERROR: Disk full\n"
            "2023-10-27 10:00:02 WARNING: High CPU usage\n"
            "2023-10-27 10:00:03 CRITICAL: System failure imminent\n"
            "Another line with an exception occurred.\n"
        )
        results = analyze_log(log_content)
        self.assertEqual(results['total_lines'], 4)
        self.assertEqual(results['total_gloom'], 4)
        self.assertEqual(results['total_glimmer'], 0)
        self.assertIn('ERROR', results['gloom_keywords'])
        self.assertIn('WARNING', results['gloom_keywords'])
        self.assertIn('CRITICAL', results['gloom_keywords'])
        self.assertIn('EXCEPTION', results['gloom_keywords'])
        self.assertEqual(results['gloom_keywords']['ERROR'], 1)
        self.assertEqual(results['gloom_keywords']['WARNING'], 1)
        self.assertEqual(results['gloom_keywords']['CRITICAL'], 1)
        self.assertEqual(results['gloom_keywords']['EXCEPTION'], 1)

    def test_analyze_only_glimmer(self):
        log_content = (
            "2023-10-27 10:00:01 INFO: Service started\n"
            "2023-10-27 10:00:02 SUCCESS: Operation completed\n"
            "2023-10-27 10:00:03 OK: All systems ready\n"
            "2023-10-27 10:00:04 HEALED: Self-repair successful\n"
        )
        results = analyze_log(log_content)
        self.assertEqual(results['total_lines'], 4)
        self.assertEqual(results['total_gloom'], 0)
        self.assertEqual(results['total_glimmer'], 4)
        self.assertIn('INFO', results['glimmer_keywords'])
        self.assertIn('SUCCESS', results['glimmer_keywords'])
        self.assertIn('OK', results['glimmer_keywords'])
        self.assertIn('HEALED', results['glimmer_keywords'])
        self.assertEqual(results['glimmer_keywords']['INFO'], 1)
        self.assertEqual(results['glimmer_keywords']['SUCCESS'], 1)
        self.assertEqual(results['glimmer_keywords']['OK'], 1)
        self.assertEqual(results['glimmer_keywords']['HEALED'], 1)

    def test_analyze_mixed_log(self):
        log_content = (
            "2023-10-27 10:00:01 INFO: Service started\n"
            "2023-10-27 10:00:02 ERROR: Disk full\n"
            "2023-10-27 10:00:03 SUCCESS: Operation completed\n"
            "2023-10-27 10:00:04 WARNING: High CPU usage\n"
            "2023-10-27 10:00:05 OK: All systems ready\n"
            "2023-10-27 10:00:06 CRITICAL: System failure imminent\n"
        )
        results = analyze_log(log_content)
        self.assertEqual(results['total_lines'], 6)
        self.assertEqual(results['total_gloom'], 3)
        self.assertEqual(results['total_glimmer'], 3)
        self.assertEqual(results['gloom_keywords']['ERROR'], 1)
        self.assertEqual(results['gloom_keywords']['WARNING'], 1)
        self.assertEqual(results['gloom_keywords']['CRITICAL'], 1)
        self.assertEqual(results['glimmer_keywords']['INFO'], 1)
        self.assertEqual(results['glimmer_keywords']['SUCCESS'], 1)
        self.assertEqual(results['glimmer_keywords']['OK'], 1)

    def test_analyze_no_matches(self):
        log_content = (
            "2023-10-27 10:00:01 Debug: This is a debug message\n"
            "2023-10-27 10:00:02 Trace: Another trace message\n"
        )
        results = analyze_log(log_content)
        self.assertEqual(results['total_lines'], 2)
        self.assertEqual(results['total_gloom'], 0)
        self.assertEqual(results['total_glimmer'], 0)
        self.assertEqual(results['gloom_keywords'], {})
        self.assertEqual(results['glimmer_keywords'], {})

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'test.log'])
    def test_main_empty_log_file(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate reading an empty log file and capture stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Lines Scanned: 0", output)
        self.assertIn("No significant gloom detected.", output)
        self.assertIn("No significant glimmer detected.", output)
        self.assertIn("Feeling: Balanced, or eerily quiet.", output)

    @patch('builtins.open', new_callable=mock_open, read_data="ERROR: Something went wrong\nSUCCESS: All good")
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'test.log'])
    def test_main_mixed_log_file(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate reading a mixed log file and capture stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Lines Scanned: 2", output)
        self.assertIn("ERROR: 1", output)
        self.assertIn("SUCCESS: 1", output)
        self.assertIn("Feeling: Balanced, or eerily quiet.", output)

    @patch('builtins.open', new_callable=mock_open, read_data="ERROR: Critical failure\nERROR: Another error")
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'test.log'])
    def test_main_gloomy_log_file(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate reading a gloomy log file and capture stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Gloom: 2", output)
        self.assertIn("Total Glimmer: 0", output)
        self.assertIn("Feeling: Deeply Gloomy.", output)

    @patch('builtins.open', new_callable=mock_open, read_data="SUCCESS: Task done\nINFO: Everything is fine\nSUCCESS: Another success")
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'test.log'])
    def test_main_glimmering_log_file(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate reading a glimmering log file and capture stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Gloom: 0", output)
        self.assertIn("Total Glimmer: 3", output)
        self.assertIn("Feeling: Mostly Glimmering!", output)

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'non_existent.log'])
    def test_main_file_not_found(self, mock_stdout, mock_exists):
        # Mock rationale: Simulate a non-existent log file and capture stderr/stdout.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file not found", mock_stdout.getvalue())

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py', 'unreadable.log'])
    def test_main_file_read_error(self, mock_stdout, mock_exists, mock_open_call):
        # Mock rationale: Simulate an IOError during file reading and capture stderr/stdout.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error reading log file: Permission denied", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['analyzer.py'])
    def test_main_no_arguments(self, mock_stdout):
        # Mock rationale: Simulate running the script without arguments and capture stderr/stdout.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python3 analyzer.py <path_to_log_file>", mock_stdout.getvalue())
