import unittest
from unittest.mock import mock_open, patch
import sys
import io
from pathlib import Path

# Mock rationale: We need to test the core logic of `analyze_log` and `print_summary`
# without actually touching the filesystem or printing to stdout/stderr.
# `mock_open` simulates file reading, `patch('sys.stdout')` and `patch('sys.stderr')`
# capture output for verification, and `patch('sys.exit')` prevents the program from exiting.

# Temporarily add src to sys.path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from luminary import analyze_log, print_summary, main
sys.path.pop(0) # Clean up sys.path

class TestNightlyLogLuminary(unittest.TestCase):

    def test_analyze_log_no_matches(self):
        log_content = "line 1\nline 2\nline 3"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            results = analyze_log("dummy.log", ["ERROR", "WARNING"])
            self.assertEqual(results["total_lines"], 3)
            self.assertEqual(len(results["matches_by_pattern"]["ERROR"]), 0)
            self.assertEqual(len(results["matches_by_pattern"]["WARNING"]), 0)

    def test_analyze_log_single_match(self):
        log_content = "line 1\nERROR: Something went wrong\nline 3"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            results = analyze_log("dummy.log", ["ERROR"])
            self.assertEqual(results["total_lines"], 3)
            self.assertEqual(len(results["matches_by_pattern"]["ERROR"]), 1)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][0]["line_number"], 2)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][0]["content"], "ERROR: Something went wrong")

    def test_analyze_log_multiple_matches_same_pattern(self):
        log_content = "ERROR 1\nline 2\nERROR 2\nline 4 ERROR 3"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            results = analyze_log("dummy.log", ["ERROR"])
            self.assertEqual(results["total_lines"], 4)
            self.assertEqual(len(results["matches_by_pattern"]["ERROR"]), 3)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][0]["line_number"], 1)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][1]["line_number"], 3)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][2]["line_number"], 4)

    def test_analyze_log_multiple_matches_different_patterns(self):
        log_content = "ERROR: Critical issue\nWARNING: Minor glitch\nINFO: All good"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            results = analyze_log("dummy.log", ["ERROR", "WARNING"])
            self.assertEqual(results["total_lines"], 3)
            self.assertEqual(len(results["matches_by_pattern"]["ERROR"]), 1)
            self.assertEqual(len(results["matches_by_pattern"]["WARNING"]), 1)
            self.assertEqual(results["matches_by_pattern"]["ERROR"][0]["content"], "ERROR: Critical issue")
            self.assertEqual(results["matches_by_pattern"]["WARNING"][0]["content"], "WARNING: Minor glitch")

    def test_analyze_log_file_not_found(self):
        # Mock rationale: Simulate FileNotFoundError without creating a file.
        with patch('builtins.open', side_effect=FileNotFoundError),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             patch('sys.exit') as mock_exit:
            analyze_log("non_existent.log", ["ERROR"])
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    def test_print_summary_no_matches(self):
        results = {
            "total_lines": 5,
            "matches_by_pattern": {"ERROR": [], "WARNING": []}
        }
        # Mock rationale: Capture stdout to verify printed output.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            print_summary(results)
            output = mock_stdout.getvalue()
            self.assertIn("Total lines scanned: 5", output)
            self.assertIn("No specified patterns found in the log file.", output)
            self.assertNotIn("Pattern: 'ERROR'", output)

    def test_print_summary_with_matches(self):
        results = {
            "total_lines": 10,
            "matches_by_pattern": {
                "ERROR": [
                    {"line_number": 3, "content": "ERROR: Disk full"},
                    {"line_number": 7, "content": "ERROR: Connection lost"}
                ],
                "WARNING": [
                    {"line_number": 5, "content": "WARNING: Low memory"}
                ]
            }
        }
        # Mock rationale: Capture stdout to verify printed output.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            print_summary(results)
            output = mock_stdout.getvalue()
            self.assertIn("Total lines scanned: 10", output)
            self.assertIn("Pattern: 'ERROR' (2 matches)", output)
            self.assertIn("  L3: ERROR: Disk full", output)
            self.assertIn("  L7: ERROR: Connection lost", output)
            self.assertIn("Pattern: 'WARNING' (1 matches)", output)
            self.assertIn("  L5: WARNING: Low memory", output)

    def test_main_functionality(self):
        log_content = "line 1\nERROR: Test error\nline 3 WARNING\nline 4"
        m = mock_open(read_data=log_content)
        # Mock rationale: Simulate command-line arguments, file reading, and capture output.
        with patch('builtins.open', m),
             patch('sys.argv', ['luminary.py', 'dummy.log', 'ERROR', 'WARNING']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit: # Patch sys.exit to prevent actual exit during test
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Total lines scanned: 4", output)
            self.assertIn("Pattern: 'ERROR' (1 matches)", output)
            self.assertIn("  L2: ERROR: Test error", output)
            self.assertIn("Pattern: 'WARNING' (1 matches)", output)
            self.assertIn("  L3: WARNING", output)
            mock_exit.assert_not_called() # Ensure it doesn't exit on success

    def test_main_file_not_found_exit(self):
        # Mock rationale: Simulate FileNotFoundError and verify sys.exit(1) is called.
        with patch('builtins.open', side_effect=FileNotFoundError),
             patch('sys.argv', ['luminary.py', 'non_existent.log', 'ERROR']),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    def test_main_no_patterns_exit(self):
        # Mock rationale: Simulate calling main without any patterns and verify sys.exit(1) is called.
        with patch('sys.argv', ['luminary.py', 'dummy.log']),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: At least one pattern must be provided.", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
