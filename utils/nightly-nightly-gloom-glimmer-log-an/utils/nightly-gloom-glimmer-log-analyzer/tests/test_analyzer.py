import unittest
import io
from unittest.mock import patch
from src.analyzer import LogAnalyzer, main # Assuming main is in src/analyzer.py

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = LogAnalyzer()

    def test_empty_log(self):
        log_content = ""
        report = self.analyzer.analyze(log_content)
        self.assertEqual(report["total_lines"], 0)
        self.assertEqual(report["level_counts"], {})
        self.assertEqual(report["error_details"], {})
        self.assertEqual(report["gloom_glimmer_score"], 100.0) # Empty log means no gloom

    def test_info_only_log(self):
        log_content = "2023-10-27 10:00:00 INFO Application started.\n" \
                      "2023-10-27 10:00:01 INFO User 'admin' logged in.\n"
        report = self.analyzer.analyze(log_content)
        self.assertEqual(report["total_lines"], 2)
        self.assertEqual(report["level_counts"], {"INFO": 2})
        self.assertEqual(report["error_details"], {})
        self.assertEqual(report["gloom_glimmer_score"], 100.0) # No gloom points

    def test_mixed_log_with_warnings_and_errors(self):
        log_content = "INFO: App started\n" \
                      "DEBUG: Debug message\n" \
                      "WARNING: Disk space low\n" \
                      "ERROR: Failed to connect to DB\n" \
                      "INFO: Processing data\n" \
                      "CRITICAL: System halted\n" \
                      "WARN: Another warning\n"
        report = self.analyzer.analyze(log_content)
        self.assertEqual(report["total_lines"], 7)
        self.assertEqual(report["level_counts"]["INFO"], 2) # INFO + default for non-matched lines
        self.assertEqual(report["level_counts"]["DEBUG"], 1)
        self.assertEqual(report["level_counts"]["WARNING"], 2)
        self.assertEqual(report["level_counts"]["ERROR"], 1)
        self.assertEqual(report["level_counts"]["CRITICAL"], 1)
        self.assertIn("WARNING", report["error_details"])
        self.assertIn("ERROR", report["error_details"])
        self.assertIn("CRITICAL", report["error_details"])
        self.assertEqual(len(report["error_details"]["WARNING"]), 2)
        self.assertEqual(len(report["error_details"]["ERROR"]), 1)
        self.assertEqual(len(report["error_details"]["CRITICAL"]), 1)
        
        # Calculate expected gloom points:
        # WARNING: 2 * 2 = 4
        # ERROR: 1 * 5 = 5
        # CRITICAL: 1 * 10 = 10
        # Total gloom points = 4 + 5 + 10 = 19
        # Max gloom points = 7 lines * 10 (CRITICAL weight) = 70
        # Gloom score = (19 / 70) * 100 = 27.1428...
        # Glimmer score = 100 - 27.1428... = 72.8571...
        self.assertAlmostEqual(report["gloom_glimmer_score"], 72.86, places=2)

    def test_custom_log_patterns(self):
        log_content = "2023-10-27 11:00:00 [WARN] Something went wrong.\n" \
                      "2023-10-27 11:01:00 [ERROR] Critical failure.\n"
        report = self.analyzer.analyze(log_content)
        self.assertEqual(report["total_lines"], 2)
        self.assertEqual(report["level_counts"]["WARNING"], 1)
        self.assertEqual(report["level_counts"]["ERROR"], 1)
        self.assertIn("[WARN] Something went wrong.", report["error_details"]["WARNING"])
        self.assertIn("[ERROR] Critical failure.", report["error_details"]["ERROR"])
        
        # Gloom points: WARN (2) + ERROR (5) = 7
        # Max gloom: 2 * 10 = 20
        # Gloom score = (7 / 20) * 100 = 35
        # Glimmer score = 100 - 35 = 65
        self.assertAlmostEqual(report["gloom_glimmer_score"], 65.00, places=2)

    def test_no_matching_level(self):
        log_content = "Just a regular line of text.\n" \
                      "Another line without a specific level.\n"
        report = self.analyzer.analyze(log_content)
        self.assertEqual(report["total_lines"], 2)
        self.assertEqual(report["level_counts"]["INFO"], 2) # Default to INFO
        self.assertEqual(report["error_details"], {})
        self.assertEqual(report["gloom_glimmer_score"], 100.0)

    def test_main_function_file_not_found(self):
        # Mock rationale: We need to simulate a FileNotFoundError without actually creating/deleting files.
        # patch('builtins.open') allows us to control the behavior of open().
        # patch('sys.stderr', new_callable=io.StringIO) captures stderr output.
        # patch('sys.exit') prevents the test from exiting the runner.
        with patch('builtins.open', side_effect=FileNotFoundError),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             patch('sys.exit') as mock_exit:
            
            # Mock rationale: argparse.ArgumentParser.parse_args() reads sys.argv.
            # We need to provide a dummy argument for the log file path.
            with patch('sys.argv', ['analyzer.py', 'non_existent_file.log']):
                main()
                mock_exit.assert_called_with(1)
                self.assertIn("Error: Log file not found", mock_stderr.getvalue())

    def test_main_function_successful_analysis(self):
        log_content = "INFO: All good\nERROR: Something bad happened\n"
        # Mock rationale: Simulate reading from a file without actual file I/O.
        # io.StringIO provides a file-like object from a string.
        mock_file = io.StringIO(log_content)
        
        # Mock rationale: Capture stdout to verify the printed report.
        with patch('builtins.open', return_value=mock_file),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.argv', ['analyzer.py', 'dummy.log']):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("--- Gloom-Glimmer Log Analysis Report ---", output)
            self.assertIn("Total Lines: 2", output)
            self.assertIn("INFO: 1", output)
            self.assertIn("ERROR: 1", output)
            self.assertIn("Gloom-Glimmer Score:", output)
            self.assertIn("System is feeling a bit gloomy.", output) # Based on the score calculation

if __name__ == '__main__':
    unittest.main()
