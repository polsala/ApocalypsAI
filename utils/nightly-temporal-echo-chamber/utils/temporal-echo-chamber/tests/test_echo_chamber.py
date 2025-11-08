import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta

# Import the functions from the main script
# We need to adjust the import path for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from echo_chamber import add_message, list_messages, recall_messages, clear_messages, DATA_FILE, _load_messages, _save_messages

class TestEchoChamber(unittest.TestCase):

    def setUp(self):
        # Ensure the data file doesn't exist before each test
        # Mocking file operations will prevent actual file creation
        pass

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_load_messages_empty_file(self, mock_exists, mock_file):
        # Mock rationale: Simulate an empty or non-existent data file.
        # `os.path.exists` returns False, then `open` is not called, or if it were, it would be empty.
        self.assertEqual(_load_messages(), [])

    @patch('builtins.open', new_callable=mock_open, read_data='[{"timestamp": "2023-01-01T10:00:00", "message": "Test 1"}]')
    @patch('os.path.exists', return_value=True)
    def test_load_messages_existing_data(self, mock_exists, mock_file):
        # Mock rationale: Simulate an existing data file with content.
        # `os.path.exists` returns True, then `open` reads the provided JSON string.
        expected = [{'timestamp': '2023-01-01T10:00:00', 'message': 'Test 1'}]
        self.assertEqual(_load_messages(), expected)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_load_messages_corrupted_json(self, mock_exists, mock_file):
        # Mock rationale: Simulate a data file with invalid JSON content.
        # `open` is mocked to return corrupted data, `json.JSONDecodeError` is expected.
        mock_file.return_value.read.return_value = 'invalid json'
        self.assertEqual(_load_messages(), [])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_messages(self, mock_file):
        # Mock rationale: Simulate saving messages to a file without actual disk I/O.
        # `open` is mocked, and we check if `json.dump` was called with the correct data.
        messages = [{'timestamp': '2023-01-01T10:00:00', 'message': 'Test 1'}]
        _save_messages(messages);
        mock_file.assert_called_once_with(DATA_FILE, 'w')
        handle = mock_file()
        handle.write.assert_called_once()
        # Verify the content written
        written_content = handle.write.call_args[0][0]
        self.assertEqual(json.loads(written_content), messages)

    @patch('echo_chamber._load_messages', return_value=[])
    @patch('echo_chamber._save_messages')
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_add_message(self, mock_print, mock_datetime, mock_save, mock_load):
        # Mock rationale: Test adding a message without actual file I/O or real time.
        # `_load_messages` returns empty, `_save_messages` is mocked to capture calls,
        # `datetime.datetime` is mocked to control the timestamp, `print` is mocked to capture output.
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for internal use

        add_message("New thought")

        mock_load.assert_called_once()
        mock_save.assert_called_once_with([{'timestamp': mock_now.isoformat(), 'message': 'New thought'}])
        mock_print.assert_called_once_with("Echo recorded: 'New thought'")

    @patch('echo_chamber._load_messages', return_value=[])
    @patch('builtins.print')
    def test_list_messages_empty(self, mock_print, mock_load):
        # Mock rationale: Test listing messages when the chamber is empty.
        # `_load_messages` returns empty, `print` is mocked to capture output.
        list_messages()
        mock_load.assert_called_once()
        mock_print.assert_called_once_with("The echo chamber is silent. No messages recorded.")

    @patch('echo_chamber._load_messages', return_value=[
        {'timestamp': '2023-01-01T10:00:00', 'message': 'Old thought'},
        {'timestamp': '2023-01-02T11:00:00', 'message': 'New thought'}
    ])
    @patch('builtins.print')
    def test_list_messages_with_content(self, mock_print, mock_load):
        # Mock rationale: Test listing messages when the chamber has content.
        # `_load_messages` returns predefined messages, `print` is mocked to capture output.
        list_messages()
        mock_load.assert_called_once()
        expected_calls = [
            unittest.mock.call("--- Temporal Echo Chamber Messages ---"),
            unittest.mock.call("2023-01-01 10:00:00 - Old thought"),
            unittest.mock.call("2023-01-02 11:00:00 - New thought"),
            unittest.mock.call("--------------------------------------")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('echo_chamber._load_messages', return_value=[])
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_recall_messages_empty(self, mock_print, mock_datetime, mock_load):
        # Mock rationale: Test recalling messages when the chamber is empty.
        # `_load_messages` returns empty, `print` is mocked to capture output.
        mock_datetime.now.return_value = datetime(2023, 1, 5, 12, 0, 0)
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for internal use

        recall_messages(3)
        mock_load.assert_called_once()
        mock_print.assert_called_once_with("The echo chamber is silent. No messages recorded.")

    @patch('echo_chamber._load_messages', return_value=[
        {'timestamp': '2023-01-01T10:00:00', 'message': 'Very old thought'},
        {'timestamp': '2023-01-03T11:00:00', 'message': 'Recent thought 1'},
        {'timestamp': '2023-01-04T12:00:00', 'message': 'Recent thought 2'}
    ])
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_recall_messages_with_content(self, mock_print, mock_datetime, mock_load):
        # Mock rationale: Test recalling messages from a specific period.
        # `_load_messages` returns predefined messages, `datetime.datetime` is mocked to control 'now',
        # `print` is mocked to capture output.
        mock_now = datetime(2023, 1, 5, 12, 0, 0) # 'now' is Jan 5th
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for internal use

        recall_messages(2) # Recall from Jan 3rd (inclusive) and Jan 4th

        mock_load.assert_called_once()
        expected_calls = [
            unittest.mock.call("--- Echoes from the last 2 day(s) ---"),
            unittest.mock.call("2023-01-03 11:00:00 - Recent thought 1"),
            unittest.mock.call("2023-01-04 12:00:00 - Recent thought 2"),
            unittest.mock.call("--------------------------------------")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('echo_chamber._load_messages', return_value=[
        {'timestamp': '2023-01-01T10:00:00', 'message': 'Very old thought'}
    ])
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_recall_messages_no_recent_content(self, mock_print, mock_datetime, mock_load):
        # Mock rationale: Test recalling messages when no messages are within the specified period.
        # `_load_messages` returns an old message, `datetime.datetime` is mocked to control 'now',
        # `print` is mocked to capture output.
        mock_now = datetime(2023, 1, 5, 12, 0, 0) # 'now' is Jan 5th
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for internal use

        recall_messages(1) # Recall from Jan 4th (inclusive)

        mock_load.assert_called_once()
        mock_print.assert_called_once_with("No echoes found from the last 1 day(s).")

    @patch('echo_chamber._save_messages')
    @patch('builtins.print')
    def test_clear_messages(self, mock_print, mock_save):
        # Mock rationale: Test clearing messages without actual file I/O.
        # `_save_messages` is mocked to capture calls, `print` is mocked to capture output.
        clear_messages()
        mock_save.assert_called_once_with([])
        mock_print.assert_called_once_with("All echoes have faded from the chamber.")

if __name__ == '__main__':
    unittest.main()
