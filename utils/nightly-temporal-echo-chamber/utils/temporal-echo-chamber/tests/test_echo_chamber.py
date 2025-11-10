import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime

# Mock rationale: We need to control the current time for testing message delivery.
# `datetime.now()` is mocked to return a specific time, allowing deterministic tests.
# Mock rationale: File I/O operations (`open`, `os.path.exists`) are mocked to prevent
# actual file system interaction, ensuring tests are isolated and deterministic.
# This allows simulating different states of the data file (empty, with messages, corrupted).

# Import the functions from the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import echo_chamber

class TestTemporalEchoChamber(unittest.TestCase):

    def setUp(self):
        # Ensure DATA_FILE points to a mockable path for tests
        self.mock_data_file = '/tmp/mock_echo_chamber_data.json'
        # Patch DATA_FILE in the module under test
        self.patcher_data_file = patch('echo_chamber.DATA_FILE', self.mock_data_file)
        self.patcher_data_file.start()

        # Reset the data file content for each test
        self.mock_file_content = '[]'

    def tearDown(self):
        self.patcher_data_file.stop()

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_add_message_to_empty_chamber(self, mock_file_open, mock_exists):
        echo_chamber.add_message("Test message 1", "2025-01-01 10:00:00")
        mock_file_open.assert_called_once_with(self.mock_data_file, 'w')
        written_data = json.loads(mock_file_open().write.call_args[0][0])
        self.assertEqual(len(written_data), 1)
        self.assertEqual(written_data[0]['message'], "Test message 1")
        self.assertEqual(written_data[0]['delivery_time'], "2025-01-01T10:00:00")
        self.assertFalse(written_data[0]['delivered'])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_add_message_to_existing_chamber(self, mock_file_open, mock_exists):
        initial_data = [{'message': 'Old message', 'delivery_time': '2024-01-01T00:00:00', 'delivered': True}]
        mock_file_open.return_value.read.return_value = json.dumps(initial_data)

        echo_chamber.add_message("Test message 2", "2025-02-02 11:00:00")

        # Check read call for loading existing data
        mock_file_open.assert_any_call(self.mock_data_file, 'r')
        # Check write call for saving updated data
        mock_file_open.assert_any_call(self.mock_data_file, 'w')

        written_data = json.loads(mock_file_open().write.call_args[0][0])
        self.assertEqual(len(written_data), 2)
        self.assertEqual(written_data[1]['message'], "Test message 2")
        self.assertEqual(written_data[1]['delivery_time'], "2025-02-02T11:00:00")
        self.assertFalse(written_data[1]['delivered'])

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_add_message_invalid_time_format(self, mock_file_open, mock_exists, mock_stderr, mock_exit):
        echo_chamber.add_message("Bad time", "2025-01-01") # Missing time part
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Invalid time format.", mock_stderr.getvalue())

    @patch('echo_chamber.datetime')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_check_and_deliver_no_messages_due(self, mock_file_open, mock_exists, mock_datetime):
        # Mock current time to be before any scheduled messages
        mock_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
        mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for parsing stored times

        initial_data = [
            {'message': 'Future message 1', 'delivery_time': '2024-01-02T00:00:00', 'delivered': False},
            {'message': 'Future message 2', 'delivery_time': '2024-01-03T00:00:00', 'delivered': False}
        ]
        mock_file_open.return_value.read.return_value = json.dumps(initial_data)

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            echo_chamber.check_and_deliver_messages()
            self.assertIn("No messages due for delivery at this time.", mock_stdout.getvalue())
            # Ensure no write operation happened as nothing was delivered
            mock_file_open.assert_called_once_with(self.mock_data_file, 'r')

    @patch('echo_chamber.datetime')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_check_and_deliver_some_messages_due(self, mock_file_open, mock_exists, mock_datetime):
        # Mock current time to be after one message, but before another
        mock_datetime.now.return_value = datetime(2024, 1, 2, 12, 0, 0)
        mock_datetime.fromisoformat = datetime.fromisoformat

        initial_data = [
            {'message': 'Past message', 'delivery_time': '2024-01-01T00:00:00', 'delivered': False},
            {'message': 'Future message', 'delivery_time': '2024-01-03T00:00:00', 'delivered': False},
            {'message': 'Already delivered', 'delivery_time': '2024-01-01T00:00:00', 'delivered': True}
        ]
        mock_file_open.return_value.read.return_value = json.dumps(initial_data)

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            echo_chamber.check_and_deliver_messages()
            output = mock_stdout.getvalue()
            self.assertIn("[Temporal Echo Chamber - Delivered] Past message", output)
            self.assertIn("1 message(s) delivered.", output)
            self.assertNotIn("Future message", output)
            self.assertNotIn("Already delivered", output)

            # Verify that the file was read and then written back with updated status
            mock_file_open.assert_any_call(self.mock_data_file, 'r')
            mock_file_open.assert_any_call(self.mock_data_file, 'w')
            written_data = json.loads(mock_file_open().write.call_args[0][0])
            self.assertTrue(written_data[0]['delivered'])
            self.assertFalse(written_data[1]['delivered'])
            self.assertTrue(written_data[2]['delivered'])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_load_messages_corrupted_file(self, mock_stderr, mock_file_open, mock_exists):
        mock_file_open.return_value.read.return_value = "{invalid json"
        messages = echo_chamber._load_messages()
        self.assertEqual(messages, [])
        self.assertIn("Warning: /tmp/mock_echo_chamber_data.json is corrupted.", mock_stderr.getvalue())

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('echo_chamber.add_message')
    def test_main_add_command(self, mock_add_message, mock_stderr, mock_exit):
        with patch('sys.argv', ['echo_chamber.py', 'add', 'Hello', '2024-12-31 23:59:59']):
            echo_chamber.main()
            mock_add_message.assert_called_once_with('Hello', '2024-12-31 23:59:59')
            mock_exit.assert_not_called()

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('echo_chamber.check_and_deliver_messages')
    def test_main_check_command(self, mock_check_and_deliver_messages, mock_stderr, mock_exit):
        with patch('sys.argv', ['echo_chamber.py', 'check']):
            echo_chamber.main()
            mock_check_and_deliver_messages.assert_called_once()
            mock_exit.assert_not_called()

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_invalid_command(self, mock_stderr, mock_exit):
        with patch('sys.argv', ['echo_chamber.py', 'unknown']):
            echo_chamber.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Unknown command: unknown", mock_stderr.getvalue())

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_add_command_missing_args(self, mock_stderr, mock_exit):
        with patch('sys.argv', ['echo_chamber.py', 'add', 'Hello']):
            echo_chamber.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Usage: python src/echo_chamber.py add", mock_stderr.getvalue())

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_no_command(self, mock_stderr, mock_exit):
        with patch('sys.argv', ['echo_chamber.py']):
            echo_chamber.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Usage: python src/echo_chamber.py <command>", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
