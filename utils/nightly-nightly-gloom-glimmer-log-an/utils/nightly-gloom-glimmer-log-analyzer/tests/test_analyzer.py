import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = LogAnalyzer()

    @patch('builtins.open', new_callable=mock_open)
    def test_empty_log_file(self, mock_file):
        # Mock rationale: Simulate an empty log file without actual file I/O.
        mock_file.return_value.__enter__.return_value = io.StringIO("")

        self.analyzer.analyze_log("empty.log")
        summary = self.analyzer.generate_summary("empty.log")

        self.assertIn("No significant gloom detected.", summary)
        self.assertIn("No significant glimmer detected.", summary)
        self.assertIn("Overall Morale: Balanced.", summary)
        self.assertEqual(self.analyzer.gloom_counts, {})
        self.assertEqual(self.analyzer.glimmer_counts, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_all_gloom_log(self, mock_file):
        # Mock rationale: Simulate a log file with only negative events.
        log_content = """
        2023-10-27 ERROR System failure detected.
        2023-10-27 WARNING Disk space low.
        2023-10-27 CRITICAL Core meltdown imminent.
        2023-10-27 FAILED Backup operation.
        """
        mock_file.return_value.__enter__.return_value = io.StringIO(log_content)

        self.analyzer.analyze_log("gloom.log")
        summary = self.analyzer.generate_summary("gloom.log")

        self.assertIn("Total Gloom Events: 4", summary)
        self.assertIn("No significant glimmer detected.", summary)
        self.assertIn("Overall Morale: Cautious. Gloom is prevalent. Stay alert!", summary)
        self.assertEqual(self.analyzer.gloom_counts["ERROR"], 3) # ERROR, CRITICAL, FAILED
        self.assertEqual(self.analyzer.gloom_counts["WARNING"], 1)
        self.assertEqual(self.analyzer.glimmer_counts, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_all_glimmer_log(self, mock_file):
        # Mock rationale: Simulate a log file with only positive events.
        log_content = """
        2023-10-27 INFO System startup initiated.
        2023-10-27 SUCCESS Data backup completed.
        2023-10-27 RECOVERED All systems online.
        2023-10-27 OPTIMIZED Resource allocation.
        """
        mock_file.return_value.__enter__.return_value = io.StringIO(log_content)

        self.analyzer.analyze_log("glimmer.log")
        summary = self.analyzer.generate_summary("glimmer.log")

        self.assertIn("No significant gloom detected.", summary)
        self.assertIn("Total Glimmer Events: 4", summary)
        self.assertIn("Overall Morale: Optimistic! Glimmers outshine the Gloom.", summary)
        self.assertEqual(self.analyzer.glimmer_counts["SUCCESS"], 2) # SUCCESS, RECOVERED, OPTIMIZED
        self.assertEqual(self.analyzer.glimmer_counts["INFO"], 2) # INFO, ONLINE (from RECOVERED line)
        self.assertEqual(self.analyzer.gloom_counts, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_mixed_log(self, mock_file):
        # Mock rationale: Simulate a log file with a mix of positive and negative events.
        log_content = """
        2023-10-27 08:00:01 INFO System startup initiated.
        2023-10-27 08:00:05 ERROR Failed to connect to external sensor array. Retrying...
        2023-10-27 08:00:10 SUCCESS Data backup completed.
        2023-10-27 08:00:15 WARNING Low power detected on auxiliary unit.
        2023-10-27 08:00:20 INFO Resource allocation optimized.
        2023-10-27 08:00:25 RECOVERY External sensor array reconnected.
        2023-10-27 08:00:30 CRITICAL Core meltdown imminent. Just kidding! System stable.
        """
        mock_file.return_value.__enter__.return_value = io.StringIO(log_content)

        self.analyzer.analyze_log("mixed.log")
        summary = self.analyzer.generate_summary("mixed.log")

        self.assertIn("Total Gloom Events: 3", summary)
        self.assertIn("Total Glimmer Events: 4", summary)
        self.assertIn("Overall Morale: Optimistic! Glimmers outshine the Gloom.", summary)

        self.assertEqual(self.analyzer.gloom_counts["ERROR"], 2) # Line 2 (ERROR), Line 7 (CRITICAL)
        self.assertEqual(self.analyzer.gloom_counts["WARNING"], 1) # Line 4 (WARNING)
        self.assertEqual(self.analyzer.glimmer_counts["SUCCESS"], 3) # Line 3 (SUCCESS), Line 5 (OPTIMIZED), Line 6 (RECOVERY)
        self.assertEqual(self.analyzer.glimmer_counts["INFO"], 1) # Line 1 (INFO)

    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        # Mock rationale: Simulate a FileNotFoundError without needing to create/delete files.
        mock_file.side_effect = FileNotFoundError

        # Capture sys.stderr output
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr

        with self.assertRaises(SystemExit) as cm:
            self.analyzer.analyze_log("non_existent.log")

        sys.stderr = sys.__stderr__ # Restore stderr
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Log file not found at 'non_existent.log'", captured_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_main_function_no_args(self, mock_file):
        # Mock rationale: Test the main function's argument handling.
        # Capture sys.stdout and sys.stderr
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        # Simulate no arguments
        with patch('sys.argv', ['analyzer.py']):
            with self.assertRaises(SystemExit) as cm:
                from src.analyzer import main
                main()

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/analyzer.py <path_to_log_file>", captured_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_with_args(self, mock_stdout, mock_file):
        # Mock rationale: Test the main function's full execution path with a valid log.
        log_content = """
        2023-10-27 INFO System startup initiated.
        2023-10-27 SUCCESS Data backup completed.
        """
        mock_file.return_value.__enter__.return_value = io.StringIO(log_content)

        # Simulate arguments
        with patch('sys.argv', ['analyzer.py', 'test.log']):
            from src.analyzer import main
            main()

        output = mock_stdout.getvalue()
        self.assertIn("--- Gloom-Glimmer Log Analysis ---", output)
        self.assertIn("Log File: test.log", output)
        self.assertIn("Total Glimmer Events: 2", output)
        self.assertIn("No significant gloom detected.", output)
        self.assertIn("Overall Morale: Optimistic! Glimmers outshine the Gloom.", output)


if __name__ == '__main__':
    unittest.main()
