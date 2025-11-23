import unittest
from unittest.mock import patch, mock_open
import io
import sys
from src.analyzer import analyze_log_file, main

class TestLogAnalyzer(unittest.TestCase):

    def test_empty_file(self):
        # Mock rationale: Simulate an empty log file.
        mock_file_content = ""
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            # Capture stdout to check printed output
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            analyze_log_file('dummy_path.log')
            
            sys.stdout = sys.__stdout__ # Reset stdout
            output = captured_output.getvalue()

            self.assertIn("Total Lines: 0", output)
            self.assertIn("Errors: 0", output)
            self.assertIn("Warnings: 0", output)
            self.assertIn("Info: 0", output)
            self.assertIn("No unique lines found or file was empty.", output)
            mock_file.assert_called_once_with('dummy_path.log', 'r', encoding='utf-8', errors='ignore')

    def test_basic_log_file(self):
        # Mock rationale: Simulate a log file with various log levels and repeated lines.
        mock_file_content = (
            "2023-10-27 10:00:01 INFO User logged in\n"
            "2023-10-27 10:00:02 WARNING Disk space low\n"
            "2023-10-27 10:00:03 ERROR Failed to connect to DB\n"
            "2023-10-27 10:00:04 INFO User logged in\n"
            "2023-10-27 10:00:05 ERROR Failed to connect to DB\n"
            "2023-10-27 10:00:06 DEBUG Debug message (should be ignored)\n"
            "2023-10-27 10:00:07 WARNING Disk space low\n"
            "2023-10-27 10:00:08 ERROR Failed to connect to DB\n"
            "Another custom message\n"
            "Another custom message\n"
            "Another custom message\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            analyze_log_file('dummy_path.log')
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("Total Lines: 11", output)
            self.assertIn("Errors: 3", output)
            self.assertIn("Warnings: 2", output)
            self.assertIn("Info: 2", output)
            self.assertIn("[Count: 3] 2023-10-27 10:00:03 ERROR Failed to connect to DB", output)
            self.assertIn("[Count: 3] Another custom message", output)
            self.assertIn("[Count: 2] 2023-10-27 10:00:02 WARNING Disk space low", output)
            self.assertIn("[Count: 2] 2023-10-27 10:00:01 INFO User logged in", output)
            # Check that DEBUG is not counted as a specific level, but is part of unique lines
            self.assertIn("[Count: 1] 2023-10-27 10:00:06 DEBUG Debug message (should be ignored)", output)

    def test_top_n_parameter(self):
        # Mock rationale: Test the --top N functionality with a log file.
        mock_file_content = (
            "Line A\nLine B\nLine A\nLine C\nLine B\nLine A\nLine D\n"
        )
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            analyze_log_file('dummy_path.log', top_n=2)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("Total Lines: 7", output)
            self.assertIn("[Count: 3] Line A", output)
            self.assertIn("[Count: 2] Line B", output)
            self.assertNotIn("Line C", output) # Should not be in top 2
            self.assertNotIn("Line D", output) # Should not be in top 2

    def test_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError.
        with patch('builtins.open', side_effect=FileNotFoundError) as mock_file:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            analyze_log_file('non_existent_file.log')
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("Error: Log file not found at 'non_existent_file.log'", output)
            mock_file.assert_called_once_with('non_existent_file.log', 'r', encoding='utf-8', errors='ignore')

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(log_file_path='test.log', top=1))
    @patch('src.analyzer.analyze_log_file')
    def test_main_function(self, mock_analyze_log_file, mock_parse_args):
        # Mock rationale: Test the main function's argument parsing and call to analyze_log_file.
        # Mocking parse_args prevents actual command-line parsing during test.
        # Mocking analyze_log_file prevents actual file operations during test.
        main()
        mock_analyze_log_file.assert_called_once_with('test.log', 1)

if __name__ == '__main__':
    unittest.main()
