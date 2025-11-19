import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from collections import defaultdict
from io import StringIO

# Import functions from the analyzer script
from src.analyzer import analyze_log_file, calculate_optimism_rating, main, KEYWORDS, WEIGHTS

class TestAnalyzer(unittest.TestCase):

    def test_analyze_log_file_basic(self):
        # Mock rationale: Simulate reading a log file without actual file system access.
        log_content = "INFO: App started\nERROR: Something went wrong\nWARNING: Low disk space\nSUCCESS: Operation complete"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            counts, critical_lines, lines_processed = analyze_log_file("dummy.log")

        self.assertIsNotNone(counts)
        self.assertEqual(counts['INFO'], 1)
        self.assertEqual(counts['ERROR'], 1)
        self.assertEqual(counts['WARNING'], 1)
        self.assertEqual(counts['SUCCESS'], 1)
        self.assertEqual(counts['CRITICAL'], 1) # ERROR is a CRITICAL keyword
        self.assertEqual(counts['POSITIVE'], 1) # SUCCESS is a POSITIVE keyword
        self.assertEqual(critical_lines, ["ERROR: Something went wrong"])
        self.assertEqual(lines_processed, 4)

    def test_analyze_log_file_empty(self):
        # Mock rationale: Simulate reading an empty log file.
        log_content = ""
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            counts, critical_lines, lines_processed = analyze_log_file("empty.log")

        self.assertIsNotNone(counts)
        self.assertEqual(sum(counts.values()), 0)
        self.assertEqual(critical_lines, [])
        self.assertEqual(lines_processed, 0)

    def test_analyze_log_file_max_lines(self):
        # Mock rationale: Test the max_lines limit without creating a large file.
        log_content = "INFO: Line 1\nINFO: Line 2\nINFO: Line 3\nINFO: Line 4\nINFO: Line 5"
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            counts, _, lines_processed = analyze_log_file("limited.log", max_lines=3)

        self.assertEqual(lines_processed, 3)
        self.assertEqual(counts['INFO'], 3)

    def test_analyze_log_file_no_keywords(self):
        # Mock rationale: Test a log file with no recognized keywords.
        log_content = "This is a plain line.\nAnother plain line here."
        m = mock_open(read_data=log_content)
        with patch('builtins.open', m):
            counts, critical_lines, lines_processed = analyze_log_file("plain.log")

        self.assertIsNotNone(counts)
        self.assertEqual(counts['UNKNOWN'], 2)
        self.assertEqual(sum(counts.values()), 2)
        self.assertEqual(critical_lines, [])
        self.assertEqual(lines_processed, 2)

    def test_analyze_log_file_read_error(self):
        # Mock rationale: Simulate an IOError when trying to open a file.
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            counts, critical_lines, lines_processed = analyze_log_file("unreadable.log")

        self.assertIsNone(counts)
        self.assertIsNone(critical_lines)
        self.assertEqual(lines_processed, 0)

    def test_calculate_optimism_rating_high_optimism(self):
        counts = defaultdict(int, {'POSITIVE': 100, 'INFO': 50, 'WARNING': 5})
        rating, message = calculate_optimism_rating(counts)
        self.assertGreaterEqual(rating, 8.0)
        self.assertIn("triumphant song", message)

    def test_calculate_optimism_rating_low_optimism(self):
        counts = defaultdict(int, {'CRITICAL': 10, 'WARNING': 20, 'INFO': 5})
        rating, message = calculate_optimism_rating(counts)
        self.assertLessEqual(rating, 4.0)
        self.assertIn("Dark clouds gather", message)

    def test_calculate_optimism_rating_mixed_optimism(self):
        counts = defaultdict(int, {'POSITIVE': 50, 'INFO': 100, 'WARNING': 10, 'CRITICAL': 2})
        rating, message = calculate_optimism_rating(counts)
        self.assertGreaterEqual(rating, 4.0)
        self.assertLessEqual(rating, 8.0)
        self.assertIn("steady hum", message) # Could also be "minor turbulence" depending on exact score

    def test_calculate_optimism_rating_only_unknown(self):
        counts = defaultdict(int, {'UNKNOWN': 100})
        rating, message = calculate_optimism_rating(counts)
        self.assertEqual(rating, 5.0)
        self.assertIn("Orb is silent", message)

    def test_calculate_optimism_rating_empty_counts(self):
        counts = defaultdict(int)
        rating, message = calculate_optimism_rating(counts)
        self.assertEqual(rating, 5.0)
        self.assertIn("Orb is silent", message)

    def test_main_function_integration(self):
        # Mock rationale: Simulate file system structure and content, and capture stdout.
        mock_log_content_app = "INFO: App started\nERROR: Failed to connect\nSUCCESS: Task A done"
        mock_log_content_worker = "WARNING: Queue nearly full\nCRITICAL: Worker crashed\nINFO: Heartbeat"
        mock_log_content_access = "127.0.0.1 - user [date] \"GET /\" 200" # Should be excluded

        # Create a mock file system structure
        mock_files = {
            '/mock/logs/app.log': mock_log_content_app,
            '/mock/logs/worker.log': mock_log_content_worker,
            '/mock/logs/access.log': mock_log_content_access,
            '/mock/logs/subdir/another.txt': "INFO: Subdir log\nPOSITIVE: Subdir success",
            '/mock/logs/temp.log': "DEBUG: Temp file content" # Should be excluded by exclude-patterns
        }

        def mock_open_func(filename, mode='r', encoding='utf-8', errors='ignore'):
            if filename in mock_files:
                return StringIO(mock_files[filename])
            raise FileNotFoundError(f"No such file or directory: '{filename}'")

        # Mock os.walk to simulate directory structure
        def mock_os_walk(path):
            if path == '/mock/logs':
                yield '/mock/logs', ['subdir'], ['app.log', 'worker.log', 'access.log', 'temp.log']
                yield '/mock/logs/subdir', [], ['another.txt']
            else:
                yield path, [], []

        with patch('os.walk', side_effect=mock_os_walk), \
             patch('builtins.open', side_effect=mock_open_func), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path='/mock/logs',
                 patterns=['*.log', '*.txt'],
                 exclude_patterns=['access.log', 'temp.log'],
                 max_lines=10000
             )):
            main()
            output = mock_stdout.getvalue()

            self.assertIn("Total files scanned: 3", output) # app.log, worker.log, another.txt
            self.assertIn("Total lines processed: 8", output) # 3 + 3 + 2
            self.assertIn("Critical Messages: 2", output) # 1 from app.log, 1 from worker.log
            self.assertIn("Warning Messages: 1", output) # 1 from worker.log
            self.assertIn("Positive Messages: 2", output) # 1 from app.log, 1 from another.txt
            self.assertIn("Informative Messages: 3", output) # 1 from app.log, 1 from worker.log, 1 from another.txt
            self.assertIn("Optimism Rating:", output)
            self.assertIn("Found in: /mock/logs/app.log, /mock/logs/worker.log", output)

        # Test with no matching files
        with patch('os.walk', return_value=[('/mock/empty', [], [])]), \
             patch('builtins.open', side_effect=mock_open_func), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
                 path='/mock/empty',
                 patterns=['*.log'],
                 exclude_patterns=[],
                 max_lines=10000
             )):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Total files scanned: 0", output)
            self.assertIn("Total lines processed: 0", output)
            self.assertIn("Optimism Rating: 5.0/10", output)
            self.assertIn("The Orb is silent", output)


if __name__ == '__main__':
    unittest.main()
