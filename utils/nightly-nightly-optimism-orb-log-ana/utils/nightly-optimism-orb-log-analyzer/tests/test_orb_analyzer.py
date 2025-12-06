import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from src.orb_analyzer import OptimismOrbAnalyzer

class TestOptimismOrbAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = OptimismOrbAnalyzer()
        self.default_keywords = self.analyzer.positive_keywords # Store for comparison

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}") # Mock rationale: Simulate path joining for consistent testing across OS.
    def test_analyze_directory_basic(self, mock_join, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory.
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory structure with log files.
        mock_walk.return_value = [
            ('/logs', ('sub1',), ('app.log', 'sys.txt')),
            ('/logs/sub1', (), ('error.log', 'data.json'))
        ]
        # Mock rationale: Simulate content for each log file.
        mock_file_open.side_effect = [
            mock_open(read_data="Operation SUCCESSFUL. System is HEALTHY.").return_value,
            mock_open(read_data="Task COMPLETED. Progress made.").return_value,
            mock_open(read_data="Critical failure. No optimism here.").return_value, # error.log, should be processed
        ]

        keyword_counts, processed_files = self.analyzer.analyze_directory('/logs')

        self.assertIn('/logs/app.log', processed_files)
        self.assertIn('/logs/sys.txt', processed_files)
        self.assertIn('/logs/sub1/error.log', processed_files)
        self.assertNotIn('/logs/sub1/data.json', processed_files) # Should not process .json

        self.assertEqual(keyword_counts['successful'], 1)
        self.assertEqual(keyword_counts['healthy'], 1)
        self.assertEqual(keyword_counts['completed'], 1)
        self.assertEqual(keyword_counts['progress'], 1)
        self.assertEqual(keyword_counts['success'], 1) # 'successful' contains 'success'
        self.assertEqual(keyword_counts['optimistic'], 0) # Not in content
        self.assertEqual(sum(keyword_counts.values()), 5) # successful, healthy, completed, progress, success

    @patch('os.path.isdir')
    def test_analyze_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Directory not found"):
            self.analyzer.analyze_directory('/nonexistent')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/logs', (), ('image.jpg', 'config.yaml'))])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}") # Mock rationale: Simulate path joining.
    def test_analyze_directory_no_log_files(self, mock_join, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with no relevant log files.
        keyword_counts, processed_files = self.analyzer.analyze_directory('/logs')
        self.assertEqual(len(processed_files), 0)
        self.assertTrue(all(count == 0 for count in keyword_counts.values()))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/logs', (), ('empty.log',))])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}") # Mock rationale: Simulate path joining.
    def test_analyze_directory_empty_log_file(self, mock_join, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty log file.
        mock_file_open.return_value.read.return_value = ""
        keyword_counts, processed_files = self.analyzer.analyze_directory('/logs')
        self.assertEqual(len(processed_files), 1) # File was processed, just empty
        self.assertTrue(all(count == 0 for count in keyword_counts.values()))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/logs', (), ('case.log',))])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}") # Mock rationale: Simulate path joining.
    def test_analyze_directory_case_insensitivity(self, mock_join, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Test case insensitivity for keywords.
        mock_file_open.return_value.read.return_value = "SUCCESS! Completed task. PROGRESS."
        keyword_counts, processed_files = self.analyzer.analyze_directory('/logs')
        self.assertEqual(keyword_counts['success'], 1)
        self.assertEqual(keyword_counts['completed'], 1)
        self.assertEqual(keyword_counts['progress'], 1)
        self.assertEqual(sum(keyword_counts.values()), 3) # success, completed, progress

    def test_generate_report_no_positives(self):
        # Mock rationale: Test report generation when no positive keywords are found.
        report = self.analyzer.generate_report({}, [])
        self.assertIn("No positive keywords detected", report)
        self.assertIn("No log files were found or processed", report)
        self.assertIn("Total Positive Mentions Found: `0` across `0` files.", report)

    def test_generate_report_with_positives(self):
        # Mock rationale: Test report generation with some positive keywords.
        keyword_counts = {'success': 5, 'completed': 2, 'progress': 1}
        processed_files = ['/logs/file1.log', '/logs/file2.log']
        report = self.analyzer.generate_report(keyword_counts, processed_files)
        self.assertIn("Total Positive Mentions Found: `8` across `2` files.", report)
        self.assertIn("- `success`: `5` times", report)
        self.assertIn("- `completed`: `2` times", report)
        self.assertIn("- `progress`: `1` times", report)
        self.assertIn("- `/logs/file1.log`", report)
        self.assertIn("- `/logs/file2.log`", report)

    def test_custom_keywords(self):
        # Mock rationale: Test initialization with custom keywords.
        custom_analyzer = OptimismOrbAnalyzer(keywords=['joyful', 'happy_path'])
        expected_keywords = self.default_keywords.union({'joyful', 'happy_path'})
        self.assertEqual(custom_analyzer.positive_keywords, expected_keywords)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/logs', (), ('unreadable.log',))])
    @patch('builtins.open', side_effect=IOError("Permission denied")) # Mock rationale: Simulate file read error.
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}") # Mock rationale: Simulate path joining.
    def test_file_read_error_handling(self, mock_join, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Ensure the analyzer handles unreadable files gracefully without crashing.
        # We expect a warning to be printed, but the process should continue.
        with patch('builtins.print') as mock_print:
            keyword_counts, processed_files = self.analyzer.analyze_directory('/logs')
            self.assertIn("Warning: Could not read file", mock_print.call_args_list[0].args[0])
            self.assertEqual(len(processed_files), 0) # File was not successfully processed
            self.assertTrue(all(count == 0 for count in keyword_counts.values()))

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(log_directory='/test_logs', keywords=['awesome']))
    @patch('src.orb_analyzer.OptimismOrbAnalyzer.analyze_directory', return_value=({'awesome': 1, 'success': 1}, ['/test_logs/log.log']))
    @patch('src.orb_analyzer.OptimismOrbAnalyzer.generate_report', return_value="Mock Report")
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_generate_report, mock_analyze_directory, mock_parse_args):
        # Mock rationale: Test the main function's successful execution path.
        from src.orb_analyzer import main
        main()
        mock_analyze_directory.assert_called_once_with('/test_logs')
        mock_generate_report.assert_called_once_with({'awesome': 1, 'success': 1}, ['/test_logs/log.log'])
        mock_print.assert_called_once_with("Mock Report")

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(log_directory='/nonexistent', keywords=None))
    @patch('src.orb_analyzer.OptimismOrbAnalyzer.analyze_directory', side_effect=ValueError("Directory not found: /nonexistent"))
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_value_error(self, mock_exit, mock_print, mock_analyze_directory, mock_parse_args):
        # Mock rationale: Test the main function's error handling for ValueError.
        from src.orb_analyzer import main
        main()
        mock_print.assert_called_once_with("Error: Directory not found: /nonexistent")
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(log_directory='/error_dir', keywords=None))
    @patch('src.orb_analyzer.OptimismOrbAnalyzer.analyze_directory', side_effect=Exception("Unexpected error"))
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_general_error(self, mock_exit, mock_print, mock_analyze_directory, mock_parse_args):
        # Mock rationale: Test the main function's error handling for general exceptions.
        from src.orb_analyzer import main
        main()
        mock_print.assert_called_once_with("An unexpected error occurred: Unexpected error")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
