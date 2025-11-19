import unittest
from unittest.mock import mock_open, patch
import os
import argparse
from src.analyzer import analyze_logs, main

class TestGloomGlimmerLogAnalyzer(unittest.TestCase):

    def test_empty_log_file(self):
        # Mock rationale: Simulate an empty log file without actual file I/O.
        mock_file_content = ""
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            result = analyze_logs(["test.log"], ["ERROR"])
            self.assertEqual(result["total_files_scanned"], 1)
            self.assertEqual(result["files_with_issues"], 0)
            self.assertEqual(result["report"]["test.log"]["ERROR"], 0)
            self.assertEqual(result["report"]["test.log"]["total_matches"], 0)
            self.assertEqual(result["overall_summary"]["ERROR"], 0)
            self.assertEqual(result["overall_summary"].get("total_matches", 0), 0)
            mock_file.assert_called_with("test.log", 'r', encoding='utf-8', errors='ignore')

    def test_log_file_with_keywords(self):
        # Mock rationale: Simulate a log file with various keyword occurrences.
        mock_file_content = (
            "INFO: Application started.\n"
            "ERROR: Something went wrong.\n"
            "WARNING: Disk space low.\n"
            "error: Another critical issue.\n"
            "DEBUG: This is a debug message.\n"
            "CRITICAL: System failure imminent!\n"
        )
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            result = analyze_logs(["app.log"], ["ERROR", "WARNING", "CRITICAL"])
            self.assertEqual(result["total_files_scanned"], 1)
            self.assertEqual(result["files_with_issues"], 1)
            self.assertEqual(result["report"]["app.log"]["ERROR"], 2) # Case-insensitive
            self.assertEqual(result["report"]["app.log"]["WARNING"], 1)
            self.assertEqual(result["report"]["app.log"]["CRITICAL"], 1)
            self.assertEqual(result["report"]["app.log"]["total_matches"], 4)
            self.assertEqual(result["overall_summary"]["ERROR"], 2)
            self.assertEqual(result["overall_summary"]["WARNING"], 1)
            self.assertEqual(result["overall_summary"]["CRITICAL"], 1)
            self.assertEqual(result["overall_summary"]["total_matches"], 4)
            mock_file.assert_called_with("app.log", 'r', encoding='utf-8', errors='ignore')

    def test_multiple_log_files(self):
        # Mock rationale: Simulate multiple log files with different contents.
        mock_file_contents = {
            "log1.log": "ERROR: File 1 error.\nWARNING: File 1 warning.\n",
            "log2.log": "INFO: File 2 info.\nERROR: File 2 another error.\n",
            "log3.log": "DEBUG: No issues here.\n"
        }

        # Custom mock_open to handle different file paths
        def custom_mock_open(filename, *args, **kwargs):
            if filename in mock_file_contents:
                m = mock_open(read_data=mock_file_contents[filename])
                m.return_value.name = filename # Set the name attribute for os.path.basename
                return m.return_value
            raise FileNotFoundError(f"No such file: '{filename}'")

        with patch("builtins.open", side_effect=custom_mock_open) as mock_file:
            # Mock os.path.basename to return the correct base name for the mocked files
            with patch("os.path.basename", side_effect=lambda x: x):
                result = analyze_logs(["log1.log", "log2.log", "log3.log"], ["ERROR", "WARNING"])
                
                self.assertEqual(result["total_files_scanned"], 3)
                self.assertEqual(result["files_with_issues"], 2)

                self.assertEqual(result["report"]["log1.log"]["ERROR"], 1)
                self.assertEqual(result["report"]["log1.log"]["WARNING"], 1)
                self.assertEqual(result["report"]["log1.log"]["total_matches"], 2)

                self.assertEqual(result["report"]["log2.log"]["ERROR"], 1)
                self.assertEqual(result["report"]["log2.log"]["WARNING"], 0)
                self.assertEqual(result["report"]["log2.log"]["total_matches"], 1)

                self.assertEqual(result["report"]["log3.log"]["ERROR"], 0)
                self.assertEqual(result["report"]["log3.log"]["WARNING"], 0)
                self.assertEqual(result["report"]["log3.log"]["total_matches"], 0)

                self.assertEqual(result["overall_summary"]["ERROR"], 2)
                self.assertEqual(result["overall_summary"]["WARNING"], 1)
                self.assertEqual(result["overall_summary"]["total_matches"], 3)

    def test_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError without actual file I/O.
        with patch("builtins.open", side_effect=FileNotFoundError("No such file")) as mock_file:
            result = analyze_logs(["nonexistent.log"], ["ERROR"])
            self.assertEqual(result["total_files_scanned"], 1)
            self.assertEqual(result["files_with_issues"], 0) # File not found doesn't count as "issue" with matches
            self.assertIn("error", result["report"]["nonexistent.log"])
            self.assertEqual(result["overall_summary"].get("total_matches", 0), 0)
            mock_file.assert_called_with("nonexistent.log", 'r', encoding='utf-8', errors='ignore')

    def test_custom_keywords(self):
        # Mock rationale: Test with user-defined keywords.
        mock_file_content = (
            "User logged in.\n"
            "Failed attempt: Invalid password.\n"
            "SUCCESS: Operation completed.\n"
            "Failed to connect to DB.\n"
        )
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            result = analyze_logs(["auth.log"], ["Failed", "SUCCESS"])
            self.assertEqual(result["report"]["auth.log"]["Failed"], 2)
            self.assertEqual(result["report"]["auth.log"]["SUCCESS"], 1)
            self.assertEqual(result["report"]["auth.log"]["total_matches"], 3)
            self.assertEqual(result["overall_summary"]["Failed"], 2)
            self.assertEqual(result["overall_summary"]["SUCCESS"], 1)
            self.assertEqual(result["overall_summary"]["total_matches"], 3)

    def test_main_function_text_output(self):
        # Mock rationale: Capture stdout to verify the text output of the main function.
        # Mock analyze_logs to control its return value.
        mock_analysis_result = {
            "total_files_scanned": 1,
            "files_with_issues": 1,
            "report": {
                "test.log": {
                    "ERROR": 1,
                    "WARNING": 0,
                    "CRITICAL": 0,
                    "total_matches": 1
                }
            },
            "overall_summary": {
                "ERROR": 1,
                "WARNING": 0,
                "CRITICAL": 0,
                "total_matches": 1
            }
        }
        with patch("src.analyzer.analyze_logs", return_value=mock_analysis_result):
            with patch("sys.stdout", new_callable=unittest.mock.StringIO) as mock_stdout:
                with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
                    log_paths=["test.log"], keywords=["ERROR", "WARNING", "CRITICAL"], json=False
                )):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("--- Gloom-Glimmer Log Analysis Report ---", output)
                    self.assertIn("Total files scanned: 1", output)
                    self.assertIn("Files with issues: 1", output)
                    self.assertIn("File: test.log", output)
                    self.assertIn("ERROR: 1", output)
                    self.assertIn("Total matches in file: 1", output)
                    self.assertIn("--- Overall Summary ---", output)
                    self.assertIn("ERROR: 1", output)
                    self.assertIn("Total matches overall: 1", output)

    def test_main_function_json_output(self):
        # Mock rationale: Capture stdout and parse as JSON to verify the JSON output.
        # Mock analyze_logs to control its return value.
        mock_analysis_result = {
            "total_files_scanned": 1,
            "files_with_issues": 1,
            "report": {
                "test.log": {
                    "ERROR": 1,
                    "WARNING": 0,
                    "CRITICAL": 0,
                    "total_matches": 1
                }
            },
            "overall_summary": {
                "ERROR": 1,
                "WARNING": 0,
                "CRITICAL": 0,
                "total_matches": 1
            }
        }
        with patch("src.analyzer.analyze_logs", return_value=mock_analysis_result):
            with patch("sys.stdout", new_callable=unittest.mock.StringIO) as mock_stdout:
                with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
                    log_paths=["test.log"], keywords=["ERROR", "WARNING", "CRITICAL"], json=True
                )):
                    main()
                    import json
                    output_json = json.loads(mock_stdout.getvalue())
                    self.assertEqual(output_json["total_files_scanned"], 1)
                    self.assertEqual(output_json["report"]["test.log"]["ERROR"], 1)
                    self.assertEqual(output_json["overall_summary"]["total_matches"], 1)

    def test_main_function_no_log_paths_error(self):
        # Mock rationale: Test that main exits with an error if no log paths are provided.
        with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
            with patch("sys.exit") as mock_exit:
                with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
                    log_paths=[], keywords=["ERROR"], json=False
                )):
                    main()
                    mock_exit.assert_called_with(2) # argparse exits with 2 for argument errors
                    self.assertIn("At least one log file path is required.", mock_stderr.getvalue())

if __name__ == "__main__":
    unittest.main()
