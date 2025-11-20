import unittest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to the path to allow importing analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from analyzer import analyze_log_file, analyze_logs, DEFAULT_GLOOM_KEYWORDS, DEFAULT_GLIMMER_KEYWORDS, main

class TestAnalyzer(unittest.TestCase):

    def test_analyze_log_file_basic(self):
        log_content = (
            "INFO: System started successfully.\n"
            "ERROR: Failed to connect to database.\n"
            "DEBUG: Processing user input.\n"
            "SUCCESS: Data saved.\n"
            "WARNING: Low disk space.\n"
        )
        # Mock rationale: Simulate reading a file without actual file I/O.
        with patch("builtins.open", mock_open(read_data=log_content)):
            result = analyze_log_file("dummy.log", ["ERROR", "WARNING"], ["SUCCESS", "INFO"])
            self.assertEqual(result["gloom"], 2) # ERROR, WARNING
            self.assertEqual(result["glimmer"], 2) # INFO, SUCCESS
            self.assertEqual(result["lines"], 5)

    def test_analyze_log_file_no_matches(self):
        log_content = (
            "DEBUG: System heartbeat.\n"
            "TRACE: Variable x = 10.\n"
        )
        # Mock rationale: Simulate reading a file without actual file I/O.
        with patch("builtins.open", mock_open(read_data=log_content)):
            result = analyze_log_file("dummy.log", ["ERROR"], ["SUCCESS"])
            self.assertEqual(result["gloom"], 0)
            self.assertEqual(result["glimmer"], 0)
            self.assertEqual(result["lines"], 2)

    def test_analyze_log_file_case_insensitivity(self):
        log_content = (
            "error: something went wrong.\n"
            "Success: all good.\n"
        )
        # Mock rationale: Simulate reading a file without actual file I/O.
        with patch("builtins.open", mock_open(read_data=log_content)):
            result = analyze_log_file("dummy.log", ["ERROR"], ["SUCCESS"])
            self.assertEqual(result["gloom"], 1)
            self.assertEqual(result["glimmer"], 1)
            self.assertEqual(result["lines"], 2)

    def test_analyze_log_file_multiple_keywords_per_line(self):
        log_content = (
            "ERROR: Failed to connect. CRITICAL issue.\n"
            "INFO: Connected successfully. SUCCESS.\n"
        )
        # Mock rationale: Simulate reading a file without actual file I/O.
        with patch("builtins.open", mock_open(read_data=log_content)):
            result = analyze_log_file("dummy.log", ["ERROR", "CRITICAL"], ["INFO", "SUCCESS"])
            self.assertEqual(result["gloom"], 1)   # Only counts once per line for gloom
            self.assertEqual(result["glimmer"], 1) # Only counts once per line for glimmer
            self.assertEqual(result["lines"], 2)

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_logs_single_file(self, mock_file_open, mock_walk, mock_isdir, mock_isfile):
        mock_isfile.return_value = True
        mock_isdir.return_value = False
        mock_file_open.return_value.__enter__.return_value = StringIO(
            "INFO: Connected.\nERROR: Failed.\nSUCCESS: Done.\n"
        )
        # Mock rationale: Simulate file system checks and file content without actual disk access.
        # mock_isfile and mock_isdir control path type. mock_file_open provides file content.

        result = analyze_logs("single.log", ["ERROR"], ["SUCCESS", "INFO"])
        self.assertEqual(result["files_scanned"], 1)
        self.assertEqual(result["total_lines_processed"], 3)
        self.assertEqual(result["total_gloom_entries"], 1)
        self.assertEqual(result["total_glimmer_entries"], 2)
        self.assertAlmostEqual(result["glimmer_ratio"], 2/3)

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_logs_directory(self, mock_file_open, mock_walk, mock_isdir, mock_isfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory structure and file contents.
        # os.walk returns (dirpath, dirnames, filenames).
        mock_walk.return_value = [
            ('/logs', [], ['app.log', 'sys.log', 'other.txt']),
            ('/logs/archive', [], ['old.log'])
        ]

        # Let's mock analyze_log_file for this test to simplify
        with patch('analyzer.analyze_log_file') as mock_analyze_log_file:
            mock_analyze_log_file.side_effect = [
                {"gloom": 1, "glimmer": 2, "lines": 5}, # app.log
                {"gloom": 0, "glimmer": 1, "lines": 3}, # sys.log
                {"gloom": 2, "glimmer": 0, "lines": 4}, # old.log
            ]
            # Mock rationale: Instead of mocking file I/O for each file, mock the function that processes a single file.
            # This makes the test for `analyze_logs` focus on directory traversal and aggregation.

            result = analyze_logs("/logs", ["ERROR"], ["SUCCESS"])
            self.assertEqual(result["files_scanned"], 3) # app.log, sys.log, old.log
            self.assertEqual(result["total_lines_processed"], 5 + 3 + 4) # 12
            self.assertEqual(result["total_gloom_entries"], 1 + 0 + 2) # 3
            self.assertEqual(result["total_glimmer_entries"], 2 + 1 + 0) # 3
            self.assertAlmostEqual(result["glimmer_ratio"], 3 / (3 + 3)) # 0.5

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_analyze_logs_path_not_found(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = False
        # Mock rationale: Simulate a non-existent path.
        with self.assertRaises(FileNotFoundError):
            analyze_logs("non_existent_path")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('analyzer.analyze_logs')
    def test_main_function_success(self, mock_analyze_logs, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments and the core analysis function.
        # Capture stdout to check printed output.
        mock_parse_args.return_value = argparse.Namespace(
            path="test.log",
            gloom_keywords="ERROR",
            glimmer_keywords="SUCCESS"
        )
        mock_analyze_logs.return_value = {
            "files_scanned": 1,
            "total_lines_processed": 10,
            "total_gloom_entries": 2,
            "total_glimmer_entries": 8,
            "glimmer_ratio": 0.8
        }

        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Gloom-Glimmer Log Analysis Report ---", output)
        self.assertIn("Files Scanned: 1", output)
        self.assertIn("Total Gloom Entries: 2", output)
        self.assertIn("Total Glimmer Entries: 8", output)
        self.assertIn("Glimmer Ratio (Glimmers / Total Relevant): 0.8000", output)
        self.assertIn("Outlook: Highly hopeful! Keep up the good work.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO) # Capture stderr for exit(1) messages
    @patch('argparse.ArgumentParser.parse_args')
    @patch('analyzer.analyze_logs')
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_function_file_not_found_error(self, mock_exit, mock_analyze_logs, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a FileNotFoundError from analyze_logs and check error output.
        mock_parse_args.return_value = argparse.Namespace(
            path="non_existent.log",
            gloom_keywords="ERROR",
            glimmer_keywords="SUCCESS"
        )
        mock_analyze_logs.side_effect = FileNotFoundError("Path not found: non_existent.log")

        main()
        err_output = mock_stderr.getvalue() # Check stderr for error messages
        self.assertIn("Error: Path not found: non_existent.log", err_output)
        mock_exit.assert_called_once_with(1) # Ensure exit code 1 is called

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('analyzer.analyze_logs')
    def test_main_function_zero_relevant_entries(self, mock_analyze_logs, mock_parse_args, mock_stdout):
        # Mock rationale: Test scenario where no gloom or glimmer entries are found.
        mock_parse_args.return_value = argparse.Namespace(
            path="empty.log",
            gloom_keywords="ERROR",
            glimmer_keywords="SUCCESS"
        )
        mock_analyze_logs.return_value = {
            "files_scanned": 1,
            "total_lines_processed": 5,
            "total_gloom_entries": 0,
            "total_glimmer_entries": 0,
            "glimmer_ratio": 0.0
        }

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Glimmer Ratio (Glimmers / Total Relevant): 0.0000", output)
        self.assertIn("Outlook: Grim. Prepare for potential system collapse or a very bad day.", output)

    def test_default_keywords(self):
        self.assertIsInstance(DEFAULT_GLOOM_KEYWORDS, list)
        self.assertIsInstance(DEFAULT_GLIMMER_KEYWORDS, list)
        self.assertGreater(len(DEFAULT_GLOOM_KEYWORDS), 0)
        self.assertGreater(len(DEFAULT_GLIMMER_KEYWORDS), 0)

if __name__ == '__main__':
    unittest.main()
