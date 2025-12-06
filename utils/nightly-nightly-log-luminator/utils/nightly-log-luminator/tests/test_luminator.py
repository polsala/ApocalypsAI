import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO
from src.luminator import scan_logs, generate_report, main

class TestLuminator(unittest.TestCase):

    def setUp(self):
        self.test_dir = "/mock/logs"
        self.patterns = ["ERROR", "WARNING", "CRITICAL", r"failed to \w+"]
        self.extensions = ["log", "txt"]
        self.max_snippets = 2

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_logs_basic(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file system structure and file content without actual disk I/O.
        # This ensures deterministic tests and avoids side effects.

        # Simulate os.walk returning a directory with two log files
        mock_os_walk.return_value = [
            (self.test_dir, [], ["app.log", "auth.txt", "ignore.md"]),
            (os.path.join(self.test_dir, "subdir"), [], ["db.log"])
        ]

        # Simulate content for each log file
        log_content_app = (
            "INFO: Application started.\n"
            "WARNING: Disk space low.\n"
            "ERROR: Failed to connect to database.\n"
            "DEBUG: Some debug message.\n"
            "ERROR: Another error occurred.\n"
            "CRITICAL: System shutdown initiated.\n"
        )
        log_content_auth = (
            "INFO: User login successful.\n"
            "WARNING: Invalid login attempt.\n"
            "Failed to authenticate user.\n"
        )
        log_content_db = (
            "INFO: DB connection established.\n"
            "ERROR: Query execution failed.\n"
            "WARNING: High latency detected.\n"
        )

        # Configure mock_file_open to return specific content based on file path
        def mock_open_side_effect(file_path, mode='r', encoding=None, errors=None):
            if file_path == os.path.join(self.test_dir, "app.log"):
                return StringIO(log_content_app)
            elif file_path == os.path.join(self.test_dir, "auth.txt"):
                return StringIO(log_content_auth)
            elif file_path == os.path.join(self.test_dir, "subdir", "db.log"):
                return StringIO(log_content_db)
            return mock_open().return_value # Default for other files

        mock_file_open.side_effect = mock_open_side_effect

        results = scan_logs(self.test_dir, self.patterns, self.extensions, self.max_snippets)

        self.assertIn(os.path.join(self.test_dir, "app.log"), results)
        self.assertIn(os.path.join(self.test_dir, "auth.txt"), results)
        self.assertIn(os.path.join(self.test_dir, "subdir", "db.log"), results)
        self.assertNotIn(os.path.join(self.test_dir, "ignore.md"), results) # Should ignore non-log files

        # Verify app.log results
        app_log_results = results[os.path.join(self.test_dir, "app.log")]
        self.assertEqual(app_log_results["ERROR"]["count"], 2)
        self.assertEqual(len(app_log_results["ERROR"]["snippets"]), self.max_snippets)
        self.assertIn("[Line 3] ERROR: Failed to connect to database.", app_log_results["ERROR"]["snippets"])
        self.assertIn("[Line 5] ERROR: Another error occurred.", app_log_results["ERROR"]["snippets"])

        self.assertEqual(app_log_results["WARNING"]["count"], 1)
        self.assertEqual(len(app_log_results["WARNING"]["snippets"]), 1)
        self.assertIn("[Line 2] WARNING: Disk space low.", app_log_results["WARNING"]["snippets"])

        self.assertEqual(app_log_results["CRITICAL"]["count"], 1)
        self.assertEqual(len(app_log_results["CRITICAL"]["snippets"]), 1)
        self.assertIn("[Line 6] CRITICAL: System shutdown initiated.", app_log_results["CRITICAL"]["snippets"])

        # Verify auth.txt results (regex pattern)
        auth_txt_results = results[os.path.join(self.test_dir, "auth.txt")]
        self.assertEqual(auth_txt_results[r"failed to \w+"]["count"], 1)
        self.assertIn("[Line 3] Failed to authenticate user.", auth_txt_results[r"failed to \w+"]["snippets"])

        # Verify db.log results
        db_log_results = results[os.path.join(self.test_dir, "subdir", "db.log")]
        self.assertEqual(db_log_results["ERROR"]["count"], 1)
        self.assertIn("[Line 2] ERROR: Query execution failed.", db_log_results["ERROR"]["snippets"])

    def test_scan_logs_no_matches(self):
        # Mock rationale: Test scenario where no patterns are found in the logs.
        mock_os_walk = patch('os.walk').start()
        mock_file_open = patch('builtins.open', new_callable=mock_open).start()

        mock_os_walk.return_value = [
            (self.test_dir, [], ["clean.log"])
        ]
        mock_file_open.return_value = StringIO("INFO: Everything is fine.\nDEBUG: All good.\n")

        results = scan_logs(self.test_dir, self.patterns, self.extensions, self.max_snippets)
        self.assertIn(os.path.join(self.test_dir, "clean.log"), results)
        self.assertEqual(len(results[os.path.join(self.test_dir, "clean.log")]), 0) # No patterns matched

        patch.stopall() # Clean up patches

    def test_scan_logs_empty_directory(self):
        # Mock rationale: Test scenario with an empty directory.
        mock_os_walk = patch('os.walk').start()
        mock_os_walk.return_value = [] # No files or subdirectories

        results = scan_logs(self.test_dir, self.patterns, self.extensions, self.max_snippets)
        self.assertEqual(len(results), 0)

        patch.stopall()

    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_report_to_console(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed report content.
        results = {
            os.path.join(self.test_dir, "app.log"): {
                "ERROR": {
                    "count": 2,
                    "snippets": [
                        "[Line 3] ERROR: Failed to connect to database.",
                        "[Line 5] ERROR: Another error occurred."
                    ]
                },
                "WARNING": {
                    "count": 1,
                    "snippets": [
                        "[Line 2] WARNING: Disk space low."
                    ]
                }
            }
        }
        generate_report(results, self.test_dir, ["ERROR", "WARNING"], ["log"], output_file=None)
        output = mock_stdout.getvalue()

        self.assertIn("Luminator's Report - Scan Summary", output)
        self.assertIn(f"Scanning directory: {self.test_dir}", output)
        self.assertIn("Patterns searched: ERROR, WARNING", output)
        self.assertIn("File: /mock/logs/app.log", output)
        self.assertIn("Pattern 'ERROR': 2 matches", output)
        self.assertIn("[Snippet 1] [Line 3] ERROR: Failed to connect to database.", output)
        self.assertIn("Pattern 'WARNING': 1 match", output)
        self.assertIn("Total files scanned: 1", output)
        self.assertIn("Total pattern matches found: 3", output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_report_to_file(self, mock_stdout, mock_file_open):
        # Mock rationale: Simulate writing the report to a file and verify its content.
        results = {
            os.path.join(self.test_dir, "app.log"): {
                "ERROR": {
                    "count": 1,
                    "snippets": ["[Line 10] ERROR: Critical failure."]
                }
            }
        }
        output_file = "/tmp/luminator_report.txt"
        generate_report(results, self.test_dir, ["ERROR"], ["log"], output_file=output_file)

        mock_file_open.assert_called_once_with(output_file, 'w', encoding='utf-8')
        handle = mock_file_open()
        written_content = handle.write.call_args[0][0]

        self.assertIn("Luminator's Report - Scan Summary", written_content)
        self.assertIn("Report saved to /tmp/luminator_report.txt", mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('src.luminator.scan_logs', return_value={})
    @patch('src.luminator.generate_report')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_generate_report, mock_scan_logs, mock_isdir):
        # Mock rationale: Isolate the main function's argument parsing and flow control.
        # Avoids actual file system interaction and report generation side effects.
        mock_parse_args.return_value = argparse.Namespace(
            path=self.test_dir,
            patterns="ERROR,WARNING",
            extensions="log,txt",
            output=None,
            max_snippets=self.max_snippets
        )

        main()

        mock_isdir.assert_called_once_with(self.test_dir)
        mock_scan_logs.assert_called_once_with(
            self.test_dir, ["ERROR", "WARNING"], ["log", "txt"], self.max_snippets
        )
        mock_generate_report.assert_called_once()

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_sys_exit, mock_stdout, mock_isdir):
        # Mock rationale: Test error handling for an invalid directory path.
        mock_parse_args.return_value = argparse.Namespace(
            path="/nonexistent/path",
            patterns="ERROR",
            extensions="log",
            output=None,
            max_snippets=3
        )

        main()

        mock_isdir.assert_called_once_with("/nonexistent/path")
        self.assertIn("Error: Directory '/nonexistent/path' not found.", mock_stdout.getvalue())
        mock_sys_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
