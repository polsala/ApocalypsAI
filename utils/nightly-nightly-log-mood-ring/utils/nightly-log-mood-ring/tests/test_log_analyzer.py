import unittest
import os
from unittest.mock import patch, mock_open
from collections import defaultdict
from src.log_analyzer import LogMoodAnalyzer

class TestLogMoodAnalyzer(unittest.TestCase):

    def setUp(self):
        # Initialize LogMoodAnalyzer with a dummy path for testing
        self.analyzer = LogMoodAnalyzer("/dummy/path")

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_empty(self, mock_file_open):
        # Mock rationale: Simulate an empty log file without actual file I/O.
        mock_file_open.return_value.read.return_value = ""
        mock_file_open.return_value.__iter__.return_value = [] # For line-by-line iteration

        result = self.analyzer.analyze_log_file("/dummy/path/empty.log")
        self.assertEqual(result["counts"], defaultdict(int))
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["emoji"], "💬")
        self.assertEqual(result["description"], "Neutral")

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_positive(self, mock_file_open):
        # Mock rationale: Simulate a log file with positive sentiment.
        log_content = [
            "INFO: Application started successfully.",
            "SUCCESS: User 'admin' logged in.",
            "INFO: Processing request.",
            "SUCCESS: Data saved.",
            "INFO: All good."
        ]
        mock_file_open.return_value.__iter__.return_value = log_content

        result = self.analyzer.analyze_log_file("/dummy/path/positive.log")
        self.assertEqual(result["counts"]["SUCCESS"], 2)
        self.assertEqual(result["counts"]["INFO"], 3)
        self.assertEqual(result["score"], 4) # 2 * 2 (SUCCESS) + 3 * 0 (INFO)
        self.assertEqual(result["emoji"], "✨")
        self.assertEqual(result["description"], "Optimistic")

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_negative(self, mock_file_open):
        # Mock rationale: Simulate a log file with negative sentiment.
        log_content = [
            "WARNING: Disk space low.",
            "ERROR: Failed to connect to DB.",
            "INFO: Retrying...",
            "WARNING: High CPU usage.",
            "CRITICAL: System halted."
        ]
        mock_file_open.return_value.__iter__.return_value = log_content

        result = self.analyzer.analyze_log_file("/dummy/path/negative.log")
        self.assertEqual(result["counts"]["WARNING"], 2)
        self.assertEqual(result["counts"]["ERROR"], 1)
        self.assertEqual(result["counts"]["CRITICAL"], 1)
        self.assertEqual(result["counts"]["INFO"], 1)
        self.assertEqual(result["score"], -10) # 2*-1 (WARN) + 1*-3 (ERROR) + 1*-5 (CRITICAL) + 1*0 (INFO) = -2 -3 -5 = -10
        self.assertEqual(result["emoji"], "💀")
        self.assertEqual(result["description"], "Catastrophic")

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_log_file_mixed(self, mock_file_open):
        # Mock rationale: Simulate a log file with mixed sentiment.
        log_content = [
            "SUCCESS: Operation completed.",
            "WARNING: Minor issue.",
            "ERROR: Something went wrong.",
            "INFO: Debug message.",
            "SUCCESS: Another success."
        ]
        mock_file_open.return_value.__iter__.return_value = log_content

        result = self.analyzer.analyze_log_file("/dummy/path/mixed.log")
        self.assertEqual(result["counts"]["SUCCESS"], 2)
        self.assertEqual(result["counts"]["WARNING"], 1)
        self.assertEqual(result["counts"]["ERROR"], 1)
        self.assertEqual(result["counts"]["INFO"], 1)
        self.assertEqual(result["score"], 0) # 2*2 (SUCCESS) + 1*-1 (WARN) + 1*-3 (ERROR) + 1*0 (INFO) = 4 - 1 - 3 = 0
        self.assertEqual(result["emoji"], "💬")
        self.assertEqual(result["description"], "Neutral")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_and_analyze_multiple_files(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with multiple log files
        # and their content, without touching the actual filesystem.
        mock_os_walk.return_value = [
            ('/dummy/path', ('subdir',), ('app.log', 'sys.log')),
            ('/dummy/path/subdir', (), ('auth.log',))
        ]

        # Define content for each mocked file
        def mock_open_side_effect(filepath, *args, **kwargs):
            if "app.log" in filepath:
                m = mock_open(read_data="INFO: App started.\nSUCCESS: Init complete.\n")
            elif "sys.log" in filepath:
                m = mock_open(read_data="WARNING: Low memory.\nERROR: Service failed.\n")
            elif "auth.log" in filepath:
                m = mock_open(read_data="SUCCESS: User logged in.\nINFO: Auth check.\n")
            else:
                m = mock_open() # Default empty
            return m.return_value

        mock_file_open.side_effect = mock_open_side_effect

        results = self.analyzer.scan_and_analyze()

        self.assertIn("/dummy/path/app.log", results["files"])
        self.assertIn("/dummy/path/sys.log", results["files"])
        self.assertIn("/dummy/path/subdir/auth.log", results["files"])

        # Verify app.log
        app_log_data = results["files"]["/dummy/path/app.log"]
        self.assertEqual(app_log_data["counts"]["SUCCESS"], 1)
        self.assertEqual(app_log_data["score"], 2) # 1*2 (SUCCESS) + 1*0 (INFO)

        # Verify sys.log
        sys_log_data = results["files"]["/dummy/path/sys.log"]
        self.assertEqual(sys_log_data["counts"]["WARNING"], 1)
        self.assertEqual(sys_log_data["counts"]["ERROR"], 1)
        self.assertEqual(sys_log_data["score"], -4) # 1*-1 (WARN) + 1*-3 (ERROR)

        # Verify auth.log
        auth_log_data = results["files"]["/dummy/path/subdir/auth.log"]
        self.assertEqual(auth_log_data["counts"]["SUCCESS"], 1)
        self.assertEqual(auth_log_data["score"], 2) # 1*2 (SUCCESS) + 1*0 (INFO)

        # Verify overall mood
        overall_mood = results["overall_mood"]
        self.assertEqual(overall_mood["counts"]["SUCCESS"], 2)
        self.assertEqual(overall_mood["counts"]["WARNING"], 1)
        self.assertEqual(overall_mood["counts"]["ERROR"], 1)
        self.assertEqual(overall_mood["counts"]["INFO"], 2)
        # Overall score: (2*2) + (1*-1) + (1*-3) + (2*0) = 4 - 1 - 3 = 0
        self.assertEqual(overall_mood["emoji"], "💬")
        self.assertEqual(overall_mood["description"], "Neutral")

    @patch('os.walk')
    def test_scan_and_analyze_no_files(self, mock_os_walk):
        # Mock rationale: Simulate a directory with no log files.
        mock_os_walk.return_value = [
            ('/dummy/path', (), ('not_a_log.txt', 'image.png'))
        ]
        results = self.analyzer.scan_and_analyze()
        self.assertEqual(results["files"], {})
        self.assertEqual(results["overall_mood"]["emoji"], "🤷")
        self.assertEqual(results["overall_mood"]["description"], "No logs found")

    @patch('builtins.open', new_callable=mock_open)
    def test_unreadable_file_handling(self, mock_file_open):
        # Mock rationale: Simulate an IOError when trying to open a log file.
        mock_file_open.side_effect = IOError("Permission denied")
        result = self.analyzer.analyze_log_file("/dummy/path/unreadable.log")
        self.assertEqual(result["emoji"], "❓")
        self.assertEqual(result["description"], "Unreadable")
        self.assertEqual(result["score"], 0) # Score should be 0 if unreadable

    def test_get_mood_from_score(self):
        # Test specific score ranges for mood assignment
        self.assertEqual(self.analyzer._get_mood_from_score(-15), ("💀", "Catastrophic"))
        self.assertEqual(self.analyzer._get_mood_from_score(-10), ("💀", "Catastrophic"))
        self.assertEqual(self.analyzer._get_mood_from_score(-9), ("🚨", "Alarming"))
        self.assertEqual(self.analyzer._get_mood_from_score(-5), ("🚨", "Alarming"))
        self.assertEqual(self.analyzer._get_mood_from_score(-4), ("😬", "Anxious"))
        self.assertEqual(self.analyzer._get_mood_from_score(-1), ("😬", "Anxious"))
        self.assertEqual(self.analyzer._get_mood_from_score(0), ("💬", "Neutral"))
        self.assertEqual(self.analyzer._get_mood_from_score(1), ("✨", "Optimistic"))
        self.assertEqual(self.analyzer._get_mood_from_score(4), ("✨", "Optimistic"))
        self.assertEqual(self.analyzer._get_mood_from_score(5), ("✅", "Serene"))
        self.assertEqual(self.analyzer._get_mood_from_score(10), ("✅", "Serene"))

if __name__ == '__main__':
    unittest.main()
