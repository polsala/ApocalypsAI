import unittest
import sys
import os
import json
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scavenger import scavenge_logs, main

class TestScavenger(unittest.TestCase):

    def test_scavenge_logs_to_stdout(self):
        # Mock rationale: Simulate reading from a log file without actual file I/O.
        mock_log_content = (
            "[2023-01-01 12:00:00] INFO: System started.\n"
            "[2023-01-01 12:00:01] ERROR: Disk full. (Code: 500)\n"
            "This line should be ignored.\n"
            "[2023-01-01 12:00:02] WARNING: Low memory.\n"
        )
        # Mock rationale: Capture stdout to verify the printed output.
        mock_stdout = StringIO()

        log_file_path = "dummy_log.log"
        pattern = r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<message>.*)"

        with patch('builtins.open', mock_open(read_data=mock_log_content)) as mock_file_open, \
             patch('sys.stdout', mock_stdout):
            scavenge_logs(log_file_path, pattern)

            # Mock rationale: Ensure 'open' was called with the correct file and mode.
            mock_file_open.assert_called_with(log_file_path, 'r', encoding='utf-8')

            output = mock_stdout.getvalue().strip().split('\n')
            self.assertEqual(len(output), 3)

            expected_outputs = [
                {"timestamp": "2023-01-01 12:00:00", "level": "INFO", "message": "System started."},
                {"timestamp": "2023-01-01 12:00:01", "level": "ERROR", "message": "Disk full. (Code: 500)"},
                {"timestamp": "2023-01-01 12:00:02", "level": "WARNING", "message": "Low memory."}
            ]

            for i, line in enumerate(output):
                self.assertEqual(json.loads(line), expected_outputs[i])

    def test_scavenge_logs_to_file(self):
        # Mock rationale: Simulate reading from a log file without actual file I/O.
        mock_log_content = (
            "DEBUG: Initializing...\n"
            "INFO: User 'alice' logged in.\n"
            "ERROR: Authentication failed for 'bob'.\n"
        )
        # Mock rationale: Simulate writing to an output file without actual file I/O.
        mock_output_file_handle = StringIO()

        log_file_path = "another_dummy.log"
        output_file_path = "output.jsonl"
        pattern = r"(?P<level>\w+): (?P<message>.*)"

        # Mock rationale: Patch 'open' to return our mock file handle for the output file
        # when it's opened for writing, and the log content when opened for reading.
        # We need to handle different calls to 'open'.
        def mock_open_side_effect(file_path, mode, encoding='utf-8'):
            if file_path == log_file_path and mode == 'r':
                return mock_open(read_data=mock_log_content)(file_path, mode, encoding)
            elif file_path == output_file_path and mode == 'w':
                return mock_output_file_handle
            raise FileNotFoundError(f"No mock for {file_path} in mode {mode}")

        with patch('builtins.open', side_effect=mock_open_side_effect) as mock_file_open:
            scavenge_logs(log_file_path, pattern, output_file_path)

            # Mock rationale: Ensure 'open' was called for both input and output files.
            mock_file_open.assert_any_call(log_file_path, 'r', encoding='utf-8')
            mock_file_open.assert_any_call(output_file_path, 'w', encoding='utf-8')

            output = mock_output_file_handle.getvalue().strip().split('\n')
            self.assertEqual(len(output), 3)

            expected_outputs = [
                {"level": "DEBUG", "message": "Initializing..."},
                {"level": "INFO", "message": "User 'alice' logged in."},
                {"level": "ERROR", "message": "Authentication failed for 'bob'."}
            ]

            for i, line in enumerate(output):
                self.assertEqual(json.loads(line), expected_outputs[i])

    def test_scavenge_logs_no_match(self):
        # Mock rationale: Simulate a log file where no lines match the pattern.
        mock_log_content = (
            "Line one with no pattern.\n"
            "Line two also without a pattern.\n"
        )
        mock_stdout = StringIO()

        log_file_path = "no_match.log"
        pattern = r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<message>.*)"

        with patch('builtins.open', mock_open(read_data=mock_log_content)), \
             patch('sys.stdout', mock_stdout):
            scavenge_logs(log_file_path, pattern)
            self.assertEqual(mock_stdout.getvalue(), "") # Expect no output

    def test_scavenge_logs_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the log file.
        # We patch 'open' to raise FileNotFoundError directly.
        log_file_path = "non_existent.log"
        pattern = r"(?P<data>.*)"
        mock_stderr = StringIO()

        with patch('builtins.open', side_effect=FileNotFoundError), \
             patch('sys.stderr', mock_stderr), \
             self.assertRaises(SystemExit) as cm: # scavenge_logs calls sys.exit(1)
            scavenge_logs(log_file_path, pattern)

        self.assertEqual(cm.exception.code, 1)
        self.assertIn(f"Error: Log file not found at '{log_file_path}'", mock_stderr.getvalue())

    def test_scavenge_logs_invalid_regex(self):
        # Mock rationale: Simulate an invalid regex pattern.
        mock_log_content = "some content"
        log_file_path = "valid.log"
        pattern = r"((?P<invalid_pattern>" # Malformed regex
        mock_stderr = StringIO()

        with patch('builtins.open', mock_open(read_data=mock_log_content)), \
             patch('sys.stderr', mock_stderr), \
             self.assertRaises(SystemExit) as cm: # scavenge_logs calls sys.exit(1)
            scavenge_logs(log_file_path, pattern)

        self.assertEqual(cm.exception.code, 1)
        self.assertIn(f"Error: Invalid regex pattern '{pattern}'", mock_stderr.getvalue())

    def test_main_function_cli_args(self):
        # Mock rationale: Simulate command-line arguments.
        test_args = [
            'scavenger.py',
            '--log-file', 'cli_test.log',
            '--pattern', r'(?P<item>\w+)'
        ]
        # Mock rationale: Simulate log file content.
        mock_log_content = "apple\nbanana\norange\n"
        # Mock rationale: Capture stdout.
        mock_stdout = StringIO()

        with patch('sys.argv', test_args), \
             patch('builtins.open', mock_open(read_data=mock_log_content)), \
             patch('sys.stdout', mock_stdout):
            main()

            output = mock_stdout.getvalue().strip().split('\n')
            self.assertEqual(len(output), 3)
            self.assertEqual(json.loads(output[0]), {"item": "apple"})
            self.assertEqual(json.loads(output[1]), {"item": "banana"})
            self.assertEqual(json.loads(output[2]), {"item": "orange"})

    def test_main_function_cli_args_with_output_file(self):
        # Mock rationale: Simulate command-line arguments including an output file.
        test_args = [
            'scavenger.py',
            '--log-file', 'cli_test_out.log',
            '--pattern', r'(?P<data>\d+)',
            '--output-file', 'cli_output.jsonl'
        ]
        # Mock rationale: Simulate log file content.
        mock_log_content = "123\n456\n"
        # Mock rationale: Simulate output file handle.
        mock_output_file_handle = StringIO()

        def mock_open_side_effect(file_path, mode, encoding='utf-8'):
            if file_path == 'cli_test_out.log' and mode == 'r':
                return mock_open(read_data=mock_log_content)(file_path, mode, encoding)
            elif file_path == 'cli_output.jsonl' and mode == 'w':
                return mock_output_file_handle
            raise FileNotFoundError(f"No mock for {file_path} in mode {mode}")

        with patch('sys.argv', test_args), \
             patch('builtins.open', side_effect=mock_open_side_effect):
            main()

            output = mock_output_file_handle.getvalue().strip().split('\n')
            self.assertEqual(len(output), 2)
            self.assertEqual(json.loads(output[0]), {"data": "123"})
            self.assertEqual(json.loads(output[1]), {"data": "456"})
