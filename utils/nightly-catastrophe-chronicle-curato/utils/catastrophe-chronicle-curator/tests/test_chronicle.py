import unittest
from unittest.mock import patch, mock_open
import json
from datetime import datetime
import os

# Import the functions to be tested
from src.chronicle import add_event, list_events, search_events, DATA_FILE

class TestChronicle(unittest.TestCase):

    def setUp(self):
        # Ensure DATA_FILE doesn't exist before each test if not mocked.
        # With mocks, this is less critical but good practice for robustness.
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        # Clean up DATA_FILE after each test if not mocked.
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    @patch('src.chronicle.os.path.exists', return_value=False)
    @patch('src.chronicle.os.path.getsize', return_value=0)
    @patch('src.chronicle.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.chronicle.json.dump')
    @patch('src.chronicle.json.load', return_value=[])
    def test_add_event_first_event(self, mock_json_load, mock_json_dump, mock_file_open, mock_datetime, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate no data file initially.
        # - os.path.getsize: Simulate empty file if it existed (though exists=False makes this less critical).
        # - datetime: Control the timestamp for deterministic testing.
        # - builtins.open: Mock file I/O operations.
        # - json.dump: Verify what gets written to the file.
        # - json.load: Simulate reading an empty list of events.

        mock_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.isoformat.return_value = mock_now.isoformat()

        description = "Global Wi-Fi went down."
        expected_event = {"timestamp": mock_now.isoformat(), "description": description}

        result = add_event(description, filepath="test_data.json")

        # Verify _load_events was called (simulating empty file)
        mock_exists.assert_called_with("test_data.json")
        mock_json_load.assert_called_once()

        # Verify _save_events was called with the new event
        mock_json_dump.assert_called_once_with([expected_event], mock_file_open(), indent=4)
        self.assertIn(description, result)
        self.assertIn(mock_now.isoformat(), result)

    @patch('src.chronicle.os.path.exists', return_value=True)
    @patch('src.chronicle.os.path.getsize', return_value=100) # Simulate non-empty file
    @patch('src.chronicle.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.chronicle.json.dump')
    @patch('src.chronicle.json.load')
    def test_add_event_existing_events(self, mock_json_load, mock_json_dump, mock_file_open, mock_datetime, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate an existing data file.
        # - os.path.getsize: Simulate a non-empty file.
        # - datetime: Control the timestamp for deterministic testing.
        # - builtins.open: Mock file I/O operations.
        # - json.dump: Verify what gets written to the file.
        # - json.load: Simulate reading existing events.

        existing_events = [{"timestamp": "2023-10-26T09:00:00", "description": "Zombies sighted in sector 7."}]
        mock_json_load.return_value = existing_events

        mock_now = datetime(2023, 10, 27, 11, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.isoformat.return_value = mock_now.isoformat()

        description = "Giant mutant squirrels attacked the bunker."
        new_event = {"timestamp": mock_now.isoformat(), "description": description}
        expected_events_after_add = existing_events + [new_event]

        add_event(description, filepath="test_data.json")

        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once_with(expected_events_after_add, mock_file_open(), indent=4)

    @patch('src.chronicle.os.path.exists', return_value=False)
    @patch('src.chronicle.os.path.getsize', return_value=0)
    @patch('src.chronicle.json.load', return_value=[])
    def test_list_events_no_events(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate no data file.
        # - os.path.getsize: Simulate empty file.
        # - json.load: Simulate reading an empty list.

        result = list_events(filepath="test_data.json")
        self.assertEqual(result, "No catastrophic events recorded yet.")
        mock_json_load.assert_called_once()

    @patch('src.chronicle.os.path.exists', return_value=True)
    @patch('src.chronicle.os.path.getsize', return_value=100)
    @patch('src.chronicle.json.load')
    def test_list_events_with_events(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate an existing data file.
        # - os.path.getsize: Simulate a non-empty file.
        # - json.load: Simulate reading existing events.

        events = [
            {"timestamp": "2023-10-26T09:00:00", "description": "Zombies sighted."},
            {"timestamp": "2023-10-27T10:00:00", "description": "Global Wi-Fi down."}
        ]
        mock_json_load.return_value = events

        result = list_events(filepath="test_data.json")
        expected_output = (
            "--- Chronicle of Catastrophes ---\n"
            "[2023-10-26T09:00:00] Zombies sighted.\n"
            "[2023-10-27T10:00:00] Global Wi-Fi down."
        )
        self.assertEqual(result, expected_output)
        mock_json_load.assert_called_once()

    @patch('src.chronicle.os.path.exists', return_value=False)
    @patch('src.chronicle.os.path.getsize', return_value=0)
    @patch('src.chronicle.json.load', return_value=[])
    def test_search_events_no_events(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate no data file.
        # - os.path.getsize: Simulate empty file.
        # - json.load: Simulate reading an empty list.

        result = search_events("zombie", filepath="test_data.json")
        self.assertEqual(result, "No events found matching 'zombie'.")
        mock_json_load.assert_called_once()

    @patch('src.chronicle.os.path.exists', return_value=True)
    @patch('src.chronicle.os.path.getsize', return_value=100)
    @patch('src.chronicle.json.load')
    def test_search_events_found(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate an existing data file.
        # - os.path.getsize: Simulate a non-empty file.
        # - json.load: Simulate reading existing events.

        events = [
            {"timestamp": "2023-10-26T09:00:00", "description": "Zombies sighted in sector 7."},
            {"timestamp": "2023-10-27T10:00:00", "description": "Global Wi-Fi down."},
            {"timestamp": "2023-10-28T11:00:00", "description": "Another zombie outbreak near the river."}
        ]
        mock_json_load.return_value = events

        result = search_events("zombie", filepath="test_data.json")
        expected_output = (
            "--- Search Results for 'zombie' ---\n"
            "[2023-10-26T09:00:00] Zombies sighted in sector 7.\n"
            "[2023-10-28T11:00:00] Another zombie outbreak near the river."
        )
        self.assertEqual(result, expected_output)
        mock_json_load.assert_called_once()

    @patch('src.chronicle.os.path.exists', return_value=True)
    @patch('src.chronicle.os.path.getsize', return_value=100)
    @patch('src.chronicle.json.load')
    def test_search_events_not_found(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate an existing data file.
        # - os.path.getsize: Simulate a non-empty file.
        # - json.load: Simulate reading existing events.

        events = [
            {"timestamp": "2023-10-26T09:00:00", "description": "Zombies sighted."},
            {"timestamp": "2023-10-27T10:00:00", "description": "Global Wi-Fi down."}
        ]
        mock_json_load.return_value = events

        result = search_events("alien", filepath="test_data.json")
        self.assertEqual(result, "No events found matching 'alien'.")
        mock_json_load.assert_called_once()

    @patch('src.chronicle.os.path.exists', return_value=True)
    @patch('src.chronicle.os.path.getsize', return_value=100)
    @patch('src.chronicle.json.load')
    def test_search_events_case_insensitivity(self, mock_json_load, mock_getsize, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulate an existing data file.
        # - os.path.getsize: Simulate a non-empty file.
        # - json.load: Simulate reading existing events.

        events = [
            {"timestamp": "2023-10-26T09:00:00", "description": "ZOMBIES sighted."},
            {"timestamp": "2023-10-27T10:00:00", "description": "global wi-fi down."}
        ]
        mock_json_load.return_value = events

        result = search_events("zombies", filepath="test_data.json")
        expected_output = (
            "--- Search Results for 'zombies' ---\n"
            "[2023-10-26T09:00:00] ZOMBIES sighted."
        )
        self.assertEqual(result, expected_output)
        mock_json_load.assert_called_once()

if __name__ == '__main__':
    unittest.main()
