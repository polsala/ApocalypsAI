import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.analyzer import analyze_log_content, analyze_log_file, main

class TestGloomGlimmerLogAnalyzer(unittest.TestCase):

    def test_analyze_log_content_empty(self):
        content = ""
        gloom = ["error"]
        glimmer = ["success"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 0)
        self.assertEqual(results["glimmer_count"], 0)
        self.assertEqual(results["gloom_lines"], [])
        self.assertEqual(results["glimmer_lines"], [])

    def test_analyze_log_content_gloom_only(self):
        content = "This is an error line.\nAnother failure here."
        gloom = ["error", "failure"]
        glimmer = ["success"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 2)
        self.assertEqual(results["glimmer_count"], 0)
        self.assertEqual(results["gloom_lines"], ["Line 1: This is an error line.", "Line 2: Another failure here."])
        self.assertEqual(results["glimmer_lines"], [])

    def test_analyze_log_content_glimmer_only(self):
        content = "Operation success.\nSystem healthy and ready."
        gloom = ["error"]
        glimmer = ["success", "healthy"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 0)
        self.assertEqual(results["glimmer_count"], 2)
        self.assertEqual(results["gloom_lines"], [])
        self.assertEqual(results["glimmer_lines"], ["Line 1: Operation success.", "Line 2: System healthy and ready."])

    def test_analyze_log_content_both_gloom_and_glimmer(self):
        content = "INFO: System started.\nERROR: Disk full.\nSUCCESS: Data processed.\nWARNING: Low memory."
        gloom = ["error", "warning"]
        glimmer = ["info", "success"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 2)
        self.assertEqual(results["glimmer_count"], 2)
        self.assertEqual(results["gloom_lines"], ["Line 2: ERROR: Disk full.", "Line 4: WARNING: Low memory."])
        self.assertEqual(results["glimmer_lines"], ["Line 1: INFO: System started.", "Line 3: SUCCESS: Data processed."])

    def test_analyze_log_content_case_insensitivity(self):
        content = "Error: Something went wrong.\nsuccess: All good."
        gloom = ["ERROR"]
        glimmer = ["SUCCESS"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 1)
        self.assertEqual(results["glimmer_count"], 1)
        self.assertEqual(results["gloom_lines"], ["Line 1: Error: Something went wrong."])
        self.assertEqual(results["glimmer_lines"], ["Line 2: success: All good."])

    def test_analyze_log_content_no_matches(self):
        content = "Just some random text.\nAnother line of text."
        gloom = ["error"]
        glimmer = ["success"]
        results = analyze_log_content(content, gloom, glimmer)
        self.assertEqual(results["gloom_count"], 0)
        self.assertEqual(results["glimmer_count"], 0)

    def test_analyze_log_content_multiple_keywords_on_one_line(self):
        content = "ERROR: Failed to connect. Exception occurred."
        gloom = ["error", "failed", "exception"]
        glimmer = ["success"]
        results = analyze_log_content(content, gloom, glimmer)
        # A line is counted once if it contains any gloom keyword, not per keyword match
        self.assertEqual(results["gloom_count"], 1) 
        self.assertEqual(results["glimmer_count"], 0)
        self.assertEqual(results["gloom_lines"], ["Line 1: ERROR: Failed to connect. Exception occurred."])

    @patch("builtins.open", new_callable=mock_open)
    def test_analyze_log_file_success(self, mock_file):
        # Mock rationale: Avoids actual file system interaction, making tests deterministic and offline.
        # Simulates reading a file with specific content.
        mock_file.return_value.read.return_value = "Line 1: ERROR\nLine 2: SUCCESS"
        gloom = ["error"]
        glimmer = ["success"]
        results = analyze_log_file("dummy_path.log", gloom, glimmer)
        self.assertEqual(results["gloom_count"], 1)
        self.assertEqual(results["glimmer_count"], 1)
        mock_file.assert_called_once_with("dummy_path.log", 'r', encoding='utf-8')

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    def test_analyze_log_file_not_found(self, mock_exit, mock_stderr, mock_open_file):
        # Mock rationale: Avoids actual file system interaction.
        # Mocks FileNotFoundError to test error handling for non-existent files.
        # Mocks sys.stderr to capture error output and sys.exit to prevent actual program termination.
        gloom = ["error"]
        glimmer = ["success"]
        analyze_log_file("non_existent.log", gloom, glimmer)
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_function_output(self, mock_parse_args, mock_stdout, mock_stderr, mock_file):
        # Mock rationale: Mocks command-line arguments, file content, and stdout/stderr
        # to test the main function's behavior and output without actual file I/O or CLI interaction.
        mock_parse_args.return_value = argparse.Namespace(
            filepath="test.log",
            gloom_keywords=["error"],
            glimmer_keywords=["success"]
        )
        mock_file.return_value.read.return_value = "This is an ERROR.\nThis is a SUCCESS."

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Analyzing 'test.log' for gloom and glimmer...", output)
        self.assertIn("Gloom detected: 1 instances", output)
        self.assertIn("  [Gloom] Line 1: This is an ERROR.", output)
        self.assertIn("Glimmer detected: 1 instances", output)
        self.assertIn("  [Glimmer] Line 2: This is a SUCCESS.", output)
        self.assertIn("Overall Outlook: The logs are silent. Is that good or bad? Only time will tell.", output) # Equal counts

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_function_gloom_outlook(self, mock_parse_args, mock_stdout, mock_stderr, mock_file):
        # Mock rationale: Same as above, but specifically tests the "gloom" outlook message.
        mock_parse_args.return_value = argparse.Namespace(
            filepath="test.log",
            gloom_keywords=["error"],
            glimmer_keywords=["success"]
        )
        mock_file.return_value.read.return_value = "ERROR 1\nERROR 2\nSUCCESS 1"

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Overall Outlook: The shadows lengthen. Proceed with caution, survivor.", output)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_function_glimmer_outlook(self, mock_parse_args, mock_stdout, mock_stderr, mock_file):
        # Mock rationale: Same as above, but specifically tests the "glimmer" outlook message.
        mock_parse_args.return_value = argparse.Namespace(
            filepath="test.log",
            gloom_keywords=["error"],
            glimmer_keywords=["success"]
        )
        mock_file.return_value.read.return_value = "ERROR 1\nSUCCESS 1\nSUCCESS 2"

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Overall Outlook: A faint light pierces the gloom! Hope remains.", output)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_function_no_matches_outlook(self, mock_parse_args, mock_stdout, mock_stderr, mock_file):
        # Mock rationale: Same as above, but specifically tests the "no matches" outlook message.
        mock_parse_args.return_value = argparse.Namespace(
            filepath="test.log",
            gloom_keywords=["error"],
            glimmer_keywords=["success"]
        )
        mock_file.return_value.read.return_value = "Just some text.\nAnother line."

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Overall Outlook: The logs are silent. Is that good or bad? Only time will tell.", output)


if __name__ == '__main__':
    unittest.main()
