import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime, date

# Mock rationale: We need to test file operations without actually touching the filesystem.
# mock_open allows us to simulate reading from and writing to a file in memory.
# Mock rationale: datetime.now() needs to be deterministic for tests involving dates (e.g., daily summary).
# Patching datetime.datetime.now allows us to control the 'current' date and time.

# Import the functions from the tracker script
# We need to adjust the import path for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import tracker

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure DATA_FILE is set correctly for tests
        self.test_data_file = os.path.join(os.path.dirname(__file__), '..', 'resources.json')
        tracker.DATA_FILE = self.test_data_file

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    @patch('os.path.exists', return_value=False)
    def test_add_entry_new_file(self, mock_exists, mock_json_load, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate a scenario where the data file does not exist initially.
        # mock_exists ensures load_data returns an empty list.
        # mock_json_load ensures no actual loading happens.
        # mock_json_dump captures the data that would be saved.
        # mock_file_open captures file write operations.

        mock_json_load.return_value = []
        
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
            mock_dt.fromisoformat.side_effect = datetime.fromisoformat # Ensure fromisoformat works
            mock_dt.date.return_value = date(2023, 10, 26)
            
            tracker.add_entry('water', 10, 'consumption')
            
            mock_file_open.assert_called_with(self.test_data_file, 'w')
            mock_json_dump.assert_called_once()
            saved_data = mock_json_dump.call_args[0][0]
            self.assertEqual(len(saved_data), 1)
            self.assertEqual(saved_data[0]['resource'], 'water')
            self.assertEqual(saved_data[0]['amount'], -10.0)
            self.assertEqual(saved_data[0]['type'], 'consumption')
            self.assertEqual(saved_data[0]['timestamp'], '2023-10-26T10:00:00')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    @patch('os.path.exists', return_value=True)
    def test_add_entry_existing_file(self, mock_exists, mock_json_load, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate adding to an existing data file.
        # mock_exists ensures load_data attempts to load.
        # mock_json_load provides initial data.
        # mock_json_dump captures the updated data.
        initial_data = [{
            'timestamp': '2023-10-25T10:00:00',
            'resource': 'food',
            'amount': -5.0,
            'type': 'consumption'
        }]
        mock_json_load.return_value = initial_data

        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 26, 11, 0, 0)
            mock_dt.fromisoformat.side_effect = datetime.fromisoformat
            mock_dt.date.return_value = date(2023, 10, 26)

            tracker.add_entry('water', 20, 'production')

            mock_json_dump.assert_called_once()
            saved_data = mock_json_dump.call_args[0][0]
            self.assertEqual(len(saved_data), 2)
            self.assertEqual(saved_data[1]['resource'], 'water')
            self.assertEqual(saved_data[1]['amount'], 20.0)
            self.assertEqual(saved_data[1]['type'], 'production')
            self.assertEqual(saved_data[1]['timestamp'], '2023-10-26T11:00:00')
            # Ensure initial data is preserved
            self.assertEqual(saved_data[0], initial_data[0])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('os.path.exists', return_value=True)
    def test_get_daily_summary(self, mock_exists, mock_json_load, mock_file_open):
        # Mock rationale: Test the daily summary calculation with specific data.
        # mock_json_load provides the dataset.
        # mock_exists ensures load_data attempts to load.
        mock_json_load.return_value = [
            {'timestamp': '2023-10-26T09:00:00', 'resource': 'water', 'amount': -5.0, 'type': 'consumption'},
            {'timestamp': '2023-10-26T10:00:00', 'resource': 'food', 'amount': -2.0, 'type': 'consumption'},
            {'timestamp': '2023-10-25T11:00:00', 'resource': 'water', 'amount': -10.0, 'type': 'consumption'},
            {'timestamp': '2023-10-26T12:00:00', 'resource': 'water', 'amount': 3.0, 'type': 'production'},
            {'timestamp': '2023-10-26T13:00:00', 'resource': 'food', 'amount': 1.0, 'type': 'production'}
        ]

        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 26, 14, 0, 0)
            mock_dt.fromisoformat.side_effect = lambda x: datetime.fromisoformat(x) # Ensure fromisoformat works
            mock_dt.date.return_value = date(2023, 10, 26)

            summary = tracker.get_daily_summary()
            self.assertEqual(summary, {'water': -2.0, 'food': -1.0})

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('os.path.exists', return_value=False)
    def test_get_daily_summary_no_data_file(self, mock_exists, mock_json_load, mock_file_open):
        # Mock rationale: Test summary when no data file exists.
        # mock_exists ensures load_data returns an empty list.
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 26, 14, 0, 0)
            mock_dt.date.return_value = date(2023, 10, 26)
            summary = tracker.get_daily_summary()
            self.assertEqual(summary, {})

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('os.path.exists', return_value=True)
    def test_get_history(self, mock_exists, mock_json_load, mock_file_open):
        # Mock rationale: Test retrieving full history.
        # mock_json_load provides the dataset.
        # mock_exists ensures load_data attempts to load.
        history_data = [
            {'timestamp': '2023-10-25T10:00:00', 'resource': 'food', 'amount': -5.0, 'type': 'consumption'},
            {'timestamp': '2023-10-26T11:00:00', 'resource': 'water', 'amount': 20.0, 'type': 'production'}
        ]
        mock_json_load.return_value = history_data

        history = tracker.get_history()
        self.assertEqual(history, history_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError('Test Error', '', 0))
    @patch('os.path.exists', return_value=True)
    @patch('builtins.print')
    def test_load_data_corrupted_file(self, mock_print, mock_exists, mock_json_load, mock_file_open):
        # Mock rationale: Test handling of corrupted JSON file.
        # mock_json_load raises JSONDecodeError.
        # mock_exists ensures load_data attempts to load.
        # mock_print captures the warning message.
        data = tracker.load_data()
        self.assertEqual(data, [])
        mock_print.assert_called_with(f"Warning: {self.test_data_file} is corrupted. Starting with empty data.")

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load', return_value=[])
    @patch('os.path.exists', return_value=False)
    def test_add_entry_invalid_amount(self, mock_exists, mock_json_load, mock_json_dump, mock_file_open, mock_print):
        # Mock rationale: Test input validation for amount.
        # mock_print captures the error message.
        tracker.add_entry('water', -5, 'consumption')
        mock_print.assert_called_with("Error: Amount must be a positive number.")
        mock_json_dump.assert_not_called()
        mock_print.reset_mock()
        tracker.add_entry('food', 0, 'consumption')
        mock_print.assert_called_with("Error: Amount must be a positive number.")
        mock_json_dump.assert_not_called()

if __name__ == '__main__':
    unittest.main()
