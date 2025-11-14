import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime

# Adjust path to import the module correctly
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import sentry_log

class TestSentryLog(unittest.TestCase):

    def setUp(self):
        # Ensure LOG_FILE points to a test-specific path to avoid interfering with real data
        self.test_log_file = os.path.join(os.path.dirname(__file__), 'test_sentry_log.json')
        sentry_log.LOG_FILE = self.test_log_file
        # Clean up any existing test log file before each test
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def tearDown(self):
        # Clean up the test log file after each test
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_add_log(self, mock_json_load, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty log file initially.
        mock_exists.return_value = False
        mock_json_load.return_value = []

        # Mock rationale: Fix the timestamp for deterministic testing.
        fixed_now = datetime(2023, 10, 27, 10, 0, 0)
        with patch('sentry_log.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_now
            mock_dt.isoformat.return_value = fixed_now.isoformat()

            sentry_log.add_log("SentryOne", "Perimeter clear.")

            # Mock rationale: Verify that json.dump was called with the correct data.
            expected_log = {
                "timestamp": fixed_now.isoformat(),
                "sentry_name": "SentryOne",
                "observation": "Perimeter clear."
            }
            mock_json_dump.assert_called_once()
            # Check the first argument of json.dump (the data being dumped)
            self.assertEqual(mock_json_dump.call_args[0][0][0], expected_log)
            self.assertEqual(mock_json_dump.call_args[1]['indent'], 4) # Ensure pretty printing

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_logs_no_logs(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty log file.
        mock_exists.return_value = False
        mock_json_load.return_value = []

        sentry_log.view_logs()
        self.assertIn("No sentry logs found.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_logs_all(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Provide a predefined set of logs.
        mock_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2023-10-27T10:00:00", "sentry_name": "SentryOne", "observation": "Perimeter clear."},
            {"timestamp": "2023-10-27T11:00:00", "sentry_name": "SentryTwo", "observation": "Strange lights."}
        ]

        sentry_log.view_logs()
        output = mock_stdout.getvalue()
        self.assertIn("Sentry:    SentryOne", output)
        self.assertIn("Observed:  Perimeter clear.", output)
        self.assertIn("Sentry:    SentryTwo", output)
        self.assertIn("Observed:  Strange lights.", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_logs_filtered(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Provide a predefined set of logs for filtering.
        mock_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2023-10-27T10:00:00", "sentry_name": "SentryOne", "observation": "Perimeter clear."},
            {"timestamp": "2023-10-27T11:00:00", "sentry_name": "SentryTwo", "observation": "Strange lights."},
            {"timestamp": "2023-10-27T12:00:00", "sentry_name": "SentryOne", "observation": "All quiet."}
        ]

        sentry_log.view_logs(sentry_name="SentryOne")
        output = mock_stdout.getvalue()
        self.assertIn("Sentry:    SentryOne", output)
        self.assertIn("Observed:  Perimeter clear.", output)
        self.assertIn("Observed:  All quiet.", output)
        self.assertNotIn("Sentry:    SentryTwo", output) # Ensure SentryTwo is not in output

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_logs_filtered_no_match(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Provide logs but no match for the filter.
        mock_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2023-10-27T10:00:00", "sentry_name": "SentryOne", "observation": "Perimeter clear."}
        ]

        sentry_log.view_logs(sentry_name="SentryThree")
        self.assertIn("No logs found for sentry: SentryThree", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_clear_logs(self, mock_stdout, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing log file that will be cleared.
        mock_exists.return_value = True

        sentry_log.clear_logs()
        # Mock rationale: Verify that json.dump was called with an empty list.
        mock_json_dump.assert_called_once_with([], mock_open_file(), indent=4)
        self.assertIn("All sentry logs cleared.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_load_logs_corrupted_json(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        logs = sentry_log._load_logs()
        self.assertEqual(logs, []) # Should return an empty list on error

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_load_logs_empty_file(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty file that causes JSONDecodeError.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0) # Empty file often causes this

        logs = sentry_log._load_logs()
        self.assertEqual(logs, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.makedirs')
    def test_save_logs_creates_directory(self, mock_makedirs, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate a scenario where the directory for the log file doesn't exist.
        mock_exists.return_value = False # For the directory check, not the file itself

        # Temporarily change LOG_FILE to simulate a nested path for directory creation test
        original_log_file = sentry_log.LOG_FILE
        sentry_log.LOG_FILE = os.path.join(os.path.dirname(__file__), 'temp_dir', 'test_sentry_log.json')

        sentry_log._save_logs([])
        mock_makedirs.assert_called_once_with(os.path.join(os.path.dirname(__file__), 'temp_dir'), exist_ok=True)
        mock_json_dump.assert_called_once()

        sentry_log.LOG_FILE = original_log_file # Restore original LOG_FILE

if __name__ == '__main__':
    unittest.main()
