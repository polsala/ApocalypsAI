import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.analyzer import analyze_log_content, get_sentiment_summary, main, GLOOM_PATTERNS, GLIMMER_PATTERNS

class TestLogAnalyzer(unittest.TestCase):

    def test_analyze_log_content_empty(self):
        log_content = []
        total_lines, gloom_count, glimmer_count, score = analyze_log_content(log_content)
        self.assertEqual(total_lines, 0)
        self.assertEqual(gloom_count, 0)
        self.assertEqual(glimmer_count, 0)
        self.assertEqual(score, 0)

    def test_analyze_log_content_only_gloom(self):
        log_content = [
            "This is an ERROR line.",
            "A critical failure occurred.",
            "Warning: disk space low."
        ]
        total_lines, gloom_count, glimmer_count, score = analyze_log_content(log_content)
        self.assertEqual(total_lines, 3)
        self.assertEqual(gloom_count, 3)
        self.assertEqual(glimmer_count, 0)
        self.assertEqual(score, 3 * -2) # 3 gloom events * -2 weight

    def test_analyze_log_content_only_glimmer(self):
        log_content = [
            "Operation SUCCESSFUL.",
            "INFO: System started.",
            "Connection READY."
        ]
        total_lines, gloom_count, glimmer_count, score = analyze_log_content(log_content)
        self.assertEqual(total_lines, 3)
        self.assertEqual(gloom_count, 0)
        self.assertEqual(glimmer_count, 3)
        self.assertEqual(score, 3 * 1) # 3 glimmer events * 1 weight

    def test_analyze_log_content_mixed(self):
        log_content = [
            "Operation SUCCESSFUL.",
            "ERROR: Something went wrong.",
            "INFO: User logged in.",
            "WARNING: Low memory.",
            "System READY for commands."
        ]
        total_lines, gloom_count, glimmer_count, score = analyze_log_content(log_content)
        self.assertEqual(total_lines, 5)
        self.assertEqual(gloom_count, 2) # ERROR, WARNING
        self.assertEqual(glimmer_count, 3) # SUCCESSFUL, INFO, READY
        self.assertEqual(score, (2 * -2) + (3 * 1)) # -4 + 3 = -1

    def test_analyze_log_content_gloom_and_glimmer_on_same_line(self):
        # Gloom should take precedence if both are on the same line
        log_content = [
            "ERROR: Operation SUCCESSFUL but with errors.", # Should be gloom
            "INFO: System READY and running."
        ]
        total_lines, gloom_count, glimmer_count, score = analyze_log_content(log_content)
        self.assertEqual(total_lines, 2)
        self.assertEqual(gloom_count, 1) # The first line is gloom
        self.assertEqual(glimmer_count, 1) # The second line is glimmer
        self.assertEqual(score, (1 * -2) + (1 * 1)) # -2 + 1 = -1

    def test_get_sentiment_summary_high_score(self):
        self.assertIn("beacon", get_sentiment_summary(25))
        self.assertIn("thriving", get_sentiment_summary(20))

    def test_get_sentiment_summary_medium_positive_score(self):
        self.assertIn("faint glimmer", get_sentiment_summary(10))
        self.assertIn("mostly holding together", get_sentiment_summary(5))

    def test_get_sentiment_summary_neutral_score(self):
        self.assertIn("grey expanse", get_sentiment_summary(0))
        self.assertIn("stable", get_sentiment_summary(-4))

    def test_get_sentiment_summary_medium_negative_score(self):
        self.assertIn("shadows lengthen", get_sentiment_summary(-10))
        self.assertIn("strain", get_sentiment_summary(-15))

    def test_get_sentiment_summary_low_score(self):
        self.assertIn("abyss stares back", get_sentiment_summary(-25))
        self.assertIn("dire straits", get_sentiment_summary(-20))

    @patch('builtins.open', new_callable=mock_open, read_data="") # Mock rationale: Simulates an empty log file for testing file reading without actual disk I/O.
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Captures stdout to verify printed output without affecting the console during tests.
    @patch('sys.argv', ['analyzer.py', 'non_existent_file.log']) # Mock rationale: Simulates command-line arguments for the main function.
    def test_main_file_not_found(self, mock_stdout, mock_argv):
        mock_open.side_effect = FileNotFoundError # Mock rationale: Simulates the scenario where the specified log file does not exist.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file not found", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="") # Mock rationale: Simulates a log file for testing file reading without actual disk I/O.
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Captures stdout to verify printed output without affecting the console during tests.
    @patch('sys.argv', ['analyzer.py', 'test.log']) # Mock rationale: Simulates command-line arguments for the main function.
    def test_main_empty_log(self, mock_stdout, mock_argv):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Lines Scanned: 0", output)
        self.assertIn("Gloom-Glimmer Score: 0", output)
        self.assertIn("The world is a grey expanse", output)

    @patch('builtins.open', new_callable=mock_open, read_data="ERROR: Disk full\nINFO: System started\nSUCCESS: Operation complete") # Mock rationale: Simulates a log file with specific content for testing analysis and output.
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Captures stdout to verify printed output without affecting the console during tests.
    @patch('sys.argv', ['analyzer.py', 'test.log']) # Mock rationale: Simulates command-line arguments for the main function.
    def test_main_with_content(self, mock_stdout, mock_argv):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Total Lines Scanned: 3", output)
        self.assertIn("Gloom Events (Errors, Warnings, etc.): 1", output)
        self.assertIn("Glimmer Events (Successes, Info, etc.): 2", output)
        # Score: (1 * -2) + (2 * 1) = 0
        self.assertIn("Gloom-Glimmer Score: 0", output)
        self.assertIn("The world is a grey expanse", output)

    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Captures stdout to verify printed output without affecting the console during tests.
    @patch('sys.argv', ['analyzer.py']) # Mock rationale: Simulates command-line arguments for the main function, specifically missing the file path.
    def test_main_no_arguments(self, mock_stdout, mock_argv):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/analyzer.py <path_to_your_log_file>", mock_stdout.getvalue())

    def test_patterns_are_compiled(self):
        for pattern in GLOOM_PATTERNS + GLIMMER_PATTERNS:
            self.assertIsInstance(pattern, re.Pattern)
