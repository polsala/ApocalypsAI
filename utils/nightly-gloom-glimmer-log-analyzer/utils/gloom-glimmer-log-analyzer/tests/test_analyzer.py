import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
from io import StringIO
from src.analyzer import LogAnalyzer, main

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = LogAnalyzer()

    def test_analyze_empty_file(self):
        # Mock rationale: Simulate an empty log file without actual file I/O.
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            result = self.analyzer.analyze_file("dummy.log")
            self.assertEqual(result["gloom_count"], 0)
            self.assertEqual(result["glimmer_count"], 0)
            self.assertIsNone(result["error"])
            mock_file.assert_called_once_with("dummy.log", 'r', encoding='utf-8', errors='ignore')

    def test_analyze_file_with_gloom(self):
        log_content = "This is an error line.\nAnother line with a warning.\nNormal line."
        # Mock rationale: Simulate a log file containing gloom keywords.
        with patch("builtins.open", mock_open(read_data=log_content)) as mock_file:
            result = self.analyzer.analyze_file("gloom.log")
            self.assertEqual(result["gloom_count"], 2)
            self.assertEqual(result["glimmer_count"], 0)
            self.assertIsNone(result["error"])
            self.assertIn("Line 1: This is an error line.", result["gloom_lines"])
            self.assertIn("Line 2: Another line with a warning.", result["gloom_lines"])

    def test_analyze_file_with_glimmer(self):
        log_content = "Operation success.\nSystem healthy and complete.\nNormal line."
        # Mock rationale: Simulate a log file containing glimmer keywords.
        with patch("builtins.open", mock_open(read_data=log_content)) as mock_file:
            result = self.analyzer.analyze_file("glimmer.log")
            self.assertEqual(result["gloom_count"], 0)
            self.assertEqual(result["glimmer_count"], 2)
            self.assertIsNone(result["error"])
            self.assertIn("Line 1: Operation success.", result["glimmer_lines"])
            self.assertIn("Line 2: System healthy and complete.", result["glimmer_lines"])

    def test_analyze_file_with_mixed_content(self):
        log_content = "Error occurred.\nOperation success.\nWarning detected.\nSystem restored."
        # Mock rationale: Simulate a log file with both gloom and glimmer keywords.
        with patch("builtins.open", mock_open(read_data=log_content)) as mock_file:
            result = self.analyzer.analyze_file("mixed.log")
            self.assertEqual(result["gloom_count"], 2)
            self.assertEqual(result["glimmer_count"], 2)
            self.assertIsNone(result["error"])
            self.assertIn("Line 1: Error occurred.", result["gloom_lines"])
            self.assertIn("Line 3: Warning detected.", result["gloom_lines"])
            self.assertIn("Line 2: Operation success.", result["glimmer_lines"])
            self.assertIn("Line 4: System restored.", result["glimmer_lines"])

    def test_analyze_file_with_custom_keywords(self):
        custom_analyzer = LogAnalyzer(gloom_keywords=["failfast"], glimmer_keywords=["allgood"])
        log_content = "This should failfast.\nEverything is allgood now."
        # Mock rationale: Test custom keywords without actual file I/O.
        with patch("builtins.open", mock_open(read_data=log_content)) as mock_file:
            result = custom_analyzer.analyze_file("custom.log")
            self.assertEqual(result["gloom_count"], 1)
            self.assertEqual(result["glimmer_count"], 1)
            self.assertIn("Line 1: This should failfast.", result["gloom_lines"])
            self.assertIn("Line 2: Everything is allgood now.", result["glimmer_lines"])

    def test_analyze_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError without needing to create a non-existent file.
        with patch("builtins.open", side_effect=IOError("No such file")) as mock_file:
            result = self.analyzer.analyze_file("nonexistent.log")
            self.assertEqual(result["gloom_count"], 0)
            self.assertEqual(result["glimmer_count"], 0)
            self.assertIsNotNone(result["error"])
            self.assertIn("No such file", result["error"])

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_directory(self, mock_file_open, mock_walk, mock_isdir, mock_isfile):
        # Mock rationale: Simulate a directory structure and file contents without actual file system interaction.
        mock_isfile.side_effect = lambda x: x in ["/tmp/logs/app.log", "/tmp/logs/sys.log"]
        mock_isdir.side_effect = lambda x: x == "/tmp/logs"
        mock_walk.return_value = [
            ("/tmp/logs", [], ["app.log", "sys.log"])
        ]

        # Simulate content for app.log
        mock_file_open.side_effect = [
            mock_open(read_data="Error in app.\nApp started successfully.").return_value,
            mock_open(read_data="System warning.\nSystem healthy.").return_value
        ]

        results = self.analyzer.analyze_paths(["/tmp/logs"])

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["filepath"], "/tmp/logs/app.log")
        self.assertEqual(results[0]["gloom_count"], 1)
        self.assertEqual(results[0]["glimmer_count"], 1)

        self.assertEqual(results[1]["filepath"], "/tmp/logs/sys.log")
        self.assertEqual(results[1]["gloom_count"], 1)
        self.assertEqual(results[1]["glimmer_count"], 1)

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_analyze_nonexistent_path(self, mock_isdir, mock_isfile):
        # Mock rationale: Simulate a path that doesn't exist.
        mock_isfile.return_value = False
        mock_isdir.return_value = False
        results = self.analyzer.analyze_paths(["/nonexistent/path"])
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0]["error"])
        self.assertIn("Path not found", results[0]["error"])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.analyzer.LogAnalyzer.analyze_paths')
    def test_main_function_output(self, mock_analyze_paths, mock_parse_args, mock_stdout):
        # Mock rationale: Capture stdout and mock CLI arguments and analysis results
        # to test the main function's output formatting without actual file I/O or CLI parsing.
        mock_parse_args.return_value = argparse.Namespace(
            paths=["dummy.log"],
            gloom_keywords=None,
            glimmer_keywords=None,
            show_lines=False
        )
        mock_analyze_paths.return_value = [
            {
                "filepath": "dummy.log",
                "gloom_count": 1,
                "glimmer_count": 2,
                "gloom_lines": ["  Line 1: An error occurred."],
                "glimmer_lines": ["  Line 2: Success!", "  Line 3: Healthy system."],
                "error": None
            }
        ]

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Gloom-Glimmer Log Analysis Report ---", output)
        self.assertIn("File: dummy.log", output)
        self.assertIn("Gloom Count: 1", output)
        self.assertIn("Glimmer Count: 2", output)
        self.assertIn("Overall System Vibe", output)
        self.assertIn("Total Gloom Events: 1", output)
        self.assertIn("Total Glimmer Events: 2", output)
        self.assertIn("Good: More glimmer than gloom. System is generally healthy.", output)
        self.assertNotIn("An error occurred.", output) # Should not show lines without --show-lines

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.analyzer.LogAnalyzer.analyze_paths')
    def test_main_function_output_with_show_lines(self, mock_analyze_paths, mock_parse_args, mock_stdout):
        # Mock rationale: Capture stdout and mock CLI arguments and analysis results
        # to test the main function's output formatting with --show-lines.
        mock_parse_args.return_value = argparse.Namespace(
            paths=["dummy.log"],
            gloom_keywords=None,
            glimmer_keywords=None,
            show_lines=True
        )
        mock_analyze_paths.return_value = [
            {
                "filepath": "dummy.log",
                "gloom_count": 1,
                "glimmer_count": 2,
                "gloom_lines": ["  Line 1: An error occurred."],
                "glimmer_lines": ["  Line 2: Success!", "  Line 3: Healthy system."],
                "error": None
            }
        ]

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Gloom Lines:", output)
        self.assertIn("  Line 1: An error occurred.", output)
        self.assertIn("Glimmer Lines:", output)
        self.assertIn("  Line 2: Success!", output)
        self.assertIn("  Line 3: Healthy system.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.analyzer.LogAnalyzer.analyze_paths')
    def test_main_function_output_no_events(self, mock_analyze_paths, mock_parse_args, mock_stdout):
        # Mock rationale: Capture stdout and mock CLI arguments and analysis results
        # to test the main function's output when no gloom or glimmer is found.
        mock_parse_args.return_value = argparse.Namespace(
            paths=["dummy.log"],
            gloom_keywords=None,
            glimmer_keywords=None,
            show_lines=False
        )
        mock_analyze_paths.return_value = [
            {
                "filepath": "dummy.log",
                "gloom_count": 0,
                "glimmer_count": 0,
                "gloom_lines": [],
                "glimmer_lines": [],
                "error": None
            }
        ]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("The logs are silent... perhaps too silent.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.analyzer.LogAnalyzer.analyze_paths')
    def test_main_function_output_heavy_gloom(self, mock_analyze_paths, mock_parse_args, mock_stdout):
        # Mock rationale: Capture stdout and mock CLI arguments and analysis results
        # to test the main function's output when heavy gloom is detected.
        mock_parse_args.return_value = argparse.Namespace(
            paths=["dummy.log"],
            gloom_keywords=None,
            glimmer_keywords=None,
            show_lines=False
        )
        mock_analyze_paths.return_value = [
            {
                "filepath": "dummy.log",
                "gloom_count": 10,
                "glimmer_count": 2,
                "gloom_lines": [],
                "glimmer_lines": [],
                "error": None
            }
        ]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Warning: Heavy gloom detected. System integrity might be compromised.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.analyzer.LogAnalyzer.analyze_paths')
    def test_main_function_output_abundant_glimmer(self, mock_analyze_paths, mock_parse_args, mock_stdout):
        # Mock rationale: Capture stdout and mock CLI arguments and analysis results
        # to test the main function's output when abundant glimmer is detected.
        mock_parse_args.return_value = argparse.Namespace(
            paths=["dummy.log"],
            gloom_keywords=None,
            glimmer_keywords=None,
            show_lines=False
        )
        mock_analyze_paths.return_value = [
            {
                "filepath": "dummy.log",
                "gloom_count": 2,
                "glimmer_count": 10,
                "gloom_lines": [],
                "glimmer_lines": [],
                "error": None
            }
        ]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Excellent! Abundant glimmer. System appears robust.", output)


if __name__ == '__main__':
    unittest.main()
