import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO
from datetime import datetime

# Adjust import path for testing within the same folder structure.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from log_whisperer import analyze_log_file, format_report, main

class TestLogWhisperer(unittest.TestCase):

    def setUp(self):
        self.test_log_content = """
Line 1: This is a normal info message.
Line 2: Another regular log entry.
Line 3: [WARNING] Something might be wrong here.
Line 4: Debug info.
Line 5: [ERROR] Critical failure detected!
Line 6: More debug.
Line 7: [INFO] Operation completed.
Line 8: [CRITICAL] System meltdown imminent!
Line 9: Final log entry.
"""
        self.mock_log_file_path = "/var/log/test.log"
        self.mock_output_file_path = "report.txt"
        self.expected_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_basic(self, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate file presence
        # builtins.open is mocked to provide controlled log content without actual file I/O
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = self.test_log_content.strip().split('\n')

        keywords = ["ERROR", "WARNING"]
        results = analyze_log_file(self.mock_log_file_path, keywords, context_lines=1)

        self.assertIn("log_file", results)
        self.assertEqual(results["log_file"], self.mock_log_file_path)
        self.assertEqual(results["total_lines_scanned"], 9)
        self.assertEqual(results["matches_found"], 2) # WARNING and ERROR
        self.assertEqual(len(results["details"]), 2)

        # Check first match (WARNING)
        first_match = results["details"][0]
        self.assertEqual(first_match["keyword"], "WARNING")
        self.assertEqual(first_match["line_number"], 3)
        self.assertIn("Line 2: Another regular log entry.", first_match["context"])
        self.assertIn("Line 3: [WARNING] Something might be wrong here.", first_match["context"])
        self.assertIn("Line 4: Debug info.", first_match["context"])
        self.assertEqual(len(first_match["context"]), 3) # 1 before, match, 1 after

        # Check second match (ERROR)
        second_match = results["details"][1]
        self.assertEqual(second_match["keyword"], "ERROR")
        self.assertEqual(second_match["line_number"], 5)
        self.assertIn("Line 4: Debug info.", second_match["context"])
        self.assertIn("Line 5: [ERROR] Critical failure detected!", second_match["context"])
        self.assertIn("Line 6: More debug.", second_match["context"])
        self.assertEqual(len(second_match["context"]), 3)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_no_matches(self, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists and builtins.open are mocked to simulate a log file with no matching content.
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = [
            "Line 1: Info",
            "Line 2: Debug"
        ]

        keywords = ["CRITICAL"]
        results = analyze_log_file(self.mock_log_file_path, keywords)

        self.assertEqual(results["total_lines_scanned"], 2)
        self.assertEqual(results["matches_found"], 0)
        self.assertEqual(len(results["details"]), 0)

    @patch('os.path.exists')
    def test_analyze_log_file_not_found(self, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate a non-existent file.
        mock_exists.return_value = False
        keywords = ["ERROR"]
        with self.assertRaises(FileNotFoundError):
            analyze_log_file(self.mock_log_file_path, keywords)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_case_insensitivity(self, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists and builtins.open are mocked to test case-insensitive keyword matching.
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = [
            "line 1: this is an error.",
            "line 2: this is a warning."
        ]
        keywords = ["error", "WARNING"] # Mixed case
        results = analyze_log_file(self.mock_log_file_path, keywords, context_lines=0)
        self.assertEqual(results["matches_found"], 2)
        self.assertEqual(results["details"][0]["keyword"], "ERROR") # Stored as uppercase
        self.assertEqual(results["details"][1]["keyword"], "WARNING") # Stored as uppercase

    def test_format_report_with_matches(self):
        # Mock rationale: This test directly uses a pre-defined results dictionary
        # to ensure the formatting logic is correct without file I/O.
        mock_results = {
            "log_file": self.mock_log_file_path,
            "scan_date": self.expected_date_str,
            "keywords_searched": ["ERROR", "WARNING"],
            "total_lines_scanned": 5,
            "matches_found": 2,
            "details": [
                {
                    "keyword": "WARNING",
                    "line_number": 3,
                    "matched_line": "[WARNING] Something might be wrong here.",
                    "context": [
                        "Line 2: Another regular log entry.",
                        "Line 3: [WARNING] Something might be wrong here.",
                        "Line 4: Debug info."
                    ]
                },
                {
                    "keyword": "ERROR",
                    "line_number": 5,
                    "matched_line": "[ERROR] Critical failure detected!",
                    "context": [
                        "Line 4: Debug info.",
                        "Line 5: [ERROR] Critical failure detected!",
                        "Line 6: More debug."
                    ]
                }
            ]
        }
        report = format_report(mock_results)
        self.assertIn("--- Log Whisperer Report ---", report)
        self.assertIn(f"Scan Date: {self.expected_date_str}", report)
        self.assertIn(f"Log File: {self.mock_log_file_path}", report)
        self.assertIn("Keywords Searched: ERROR, WARNING", report)
        self.assertIn("Total lines scanned: 5", report)
        self.assertIn("Matches found: 2", report)
        self.assertIn("[Match 1] Keyword: WARNING (Line 3)", report)
        self.assertIn("  Line 3: [WARNING] Something might be wrong here.", report)
        self.assertIn("[Match 2] Keyword: ERROR (Line 5)", report)
        self.assertIn("  Line 5: [ERROR] Critical failure detected!", report)
        self.assertIn("--- End Report ---", report)

    def test_format_report_no_matches(self):
        # Mock rationale: This test directly uses a pre-defined results dictionary
        # to ensure the formatting logic for no matches is correct.
        mock_results = {
            "log_file": self.mock_log_file_path,
            "scan_date": self.expected_date_str,
            "keywords_searched": ["CRITICAL"],
            "total_lines_scanned": 2,
            "matches_found": 0,
            "details": []
        }
        report = format_report(mock_results)
        self.assertIn("No matches found for the specified keywords.", report)
        self.assertNotIn("[Match 1]", report)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_to_stdout(self, mock_parse_args, mock_file_open, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # os.path.exists and builtins.open are mocked for file I/O.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            log_file=self.mock_log_file_path,
            keywords=["ERROR"],
            output_file=None, # Output to stdout
            context_lines=0
        )
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = ["Line 1: [ERROR] Test error."]

        main()

        output = mock_stdout.getvalue()
        self.assertIn("--- Log Whisperer Report ---", output)
        self.assertIn("[Match 1] Keyword: ERROR (Line 1)", output)
        self.assertIn("Line 1: [ERROR] Test error.", output)
        self.assertEqual(mock_stderr.getvalue(), "") # No errors

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_to_file(self, mock_parse_args, mock_file_open, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # os.path.exists and builtins.open are mocked for file I/O and writing to output file.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            log_file=self.mock_log_file_path,
            keywords=["ERROR"],
            output_file=self.mock_output_file_path,
            context_lines=0
        )
        mock_exists.return_value = True
        mock_file_open.return_value.readlines.return_value = ["Line 1: [ERROR] Test error."]

        main()

        # Check that open was called to write to the output file
        mock_file_open.assert_called_with(self.mock_output_file_path, 'w', encoding='utf-8')
        # Check content written to the mock file
        handle = mock_file_open()
        written_content = handle.write.call_args[0][0]
        self.assertIn("--- Log Whisperer Report ---", written_content)
        self.assertIn("[Match 1] Keyword: ERROR (Line 1)", written_content)
        self.assertIn("Line 1: [ERROR] Test error.", written_content)

        self.assertIn(f"Report saved to {self.mock_output_file_path}", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.exists')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_sys_exit, mock_parse_args, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # os.path.exists is mocked to simulate a non-existent log file.
        # sys.exit is mocked to prevent actual program exit during testing.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            log_file="/nonexistent/log.log",
            keywords=["ERROR"],
            output_file=None,
            context_lines=0
        )
        mock_exists.return_value = False

        main()

        self.assertIn("Error: Log file not found: /nonexistent/log.log", mock_stderr.getvalue())
        mock_sys_exit.assert_called_with(1) # Ensure exit code 1 for error

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_unexpected_error(self, mock_sys_exit, mock_parse_args, mock_file_open, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # os.path.exists and builtins.open are mocked to simulate file I/O.
        # builtins.open is configured to raise an unexpected exception during read.
        # sys.exit is mocked to prevent actual program exit during testing.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        mock_parse_args.return_value = argparse.Namespace(
            log_file=self.mock_log_file_path,
            keywords=["ERROR"],
            output_file=None,
            context_lines=0
        )
        mock_exists.return_value = True
        mock_file_open.side_effect = Exception("Simulated unexpected error")

        main()

        self.assertIn("An unexpected error occurred: Simulated unexpected error", mock_stderr.getvalue())
        mock_sys_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
