import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime

# Adjust path to import the module from src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger_log

class TestScavengerLog(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.mock_log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src', scavenger_log.LOG_FILE)
        # Mock rationale: We don't want to create actual files during tests.
        # We'll use mock_open to simulate file operations.
        # We also mock os.path.exists to control whether the file "exists".

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    @patch('scavenger_log.datetime')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests
    def test_add_entry_new_log(self, mock_print, mock_datetime, mock_json_load, mock_json_dump, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate a new log file (doesn't exist yet)
        mock_path_exists.return_value = False
        # Mock rationale: Simulate an empty log when loading from a non-existent file
        mock_json_load.return_value = []
        # Mock rationale: Fix the timestamp for deterministic testing
        mock_datetime.now.return_value = datetime(2077, 10, 23, 13, 37, 0)

        scavenger_log.add_entry("Shiny Bottlecap", "Nuka-Cola Plant", 10, "Collector's item.")

        # Assert that _load_log was called (and returned empty list)
        mock_path_exists.assert_called_once_with(self.mock_log_file_path)
        mock_json_load.assert_not_called() # Because os.path.exists returned False

        # Assert that _save_log was called with the new entry
        expected_log_data = [{
            "timestamp": "2077-10-23T13:37:00",
            "item": "Shiny Bottlecap",
            "location": "Nuka-Cola Plant",
            "quantity": 10,
            "notes": "Collector's item."
        }]
        mock_json_dump.assert_called_once_with(expected_log_data, mock_open_file(), indent=4)
        mock_open_file.assert_called_once_with(self.mock_log_file_path, 'w', encoding='utf-8')
        mock_print.assert_called_once_with("Added: Shiny Bottlecap (x10) from Nuka-Cola Plant")


    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    @patch('scavenger_log.datetime')
    @patch('builtins.print')
    def test_add_entry_existing_log(self, mock_print, mock_datetime, mock_json_load, mock_json_dump, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an existing log file
        mock_path_exists.return_value = True
        # Mock rationale: Provide initial data for the log
        initial_log_data = [{
            "timestamp": "2077-10-22T10:00:00",
            "item": "Old Tire",
            "location": "Highway 101",
            "quantity": 4,
            "notes": "Might be useful for a buggy."
        }]
        mock_json_load.return_value = initial_log_data
        # Mock rationale: Fix the timestamp for deterministic testing
        mock_datetime.now.return_value = datetime(2077, 10, 23, 13, 37, 0)

        scavenger_log.add_entry("Broken Radio", "Vault 111 Entrance", 1, "Parts for repair.")

        # Assert that _load_log was called and returned initial data
        mock_path_exists.assert_called_once_with(self.mock_log_file_path)
        mock_json_load.assert_called_once()

        # Assert that _save_log was called with appended data
        expected_log_data = initial_log_data + [{
            "timestamp": "2077-10-23T13:37:00",
            "item": "Broken Radio",
            "location": "Vault 111 Entrance",
            "quantity": 1,
            "notes": "Parts for repair."
        }]
        mock_json_dump.assert_called_once_with(expected_log_data, mock_open_file(), indent=4)
        mock_print.assert_called_once_with("Added: Broken Radio (x1) from Vault 111 Entrance")


    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_view_log_empty(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an empty log file
        mock_path_exists.return_value = False
        mock_json_load.return_value = []

        scavenger_log.view_log()

        mock_print.assert_called_once_with("The scavenger log is empty. Time to get scavenging!")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_view_log_with_entries(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an existing log file with data
        mock_path_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2077-10-22T10:00:00", "item": "Old Tire", "location": "Highway 101", "quantity": 4, "notes": "Might be useful."},
            {"timestamp": "2077-10-23T13:37:00", "item": "Broken Radio", "location": "Vault 111", "quantity": 1, "notes": "Parts for repair."}
        ]

        scavenger_log.view_log()

        expected_calls = [
            unittest.mock.call("\n--- Scavenger Log ---"),
            unittest.mock.call("Entry #1:"),
            unittest.mock.call("  Timestamp: 2077-10-22T10:00:00"),
            unittest.mock.call("  Item: Old Tire"),
            unittest.mock.call("  Location: Highway 101"),
            unittest.mock.call("  Quantity: 4"),
            unittest.mock.call("  Notes: Might be useful."),
            unittest.mock.call("-" * 20),
            unittest.mock.call("Entry #2:"),
            unittest.mock.call("  Timestamp: 2077-10-23T13:37:00"),
            unittest.mock.call("  Item: Broken Radio"),
            unittest.mock.call("  Location: Vault 111"),
            unittest.mock.call("  Quantity: 1"),
            unittest.mock.call("  Notes: Parts for repair."),
            unittest.mock.call("-" * 20),
            unittest.mock.call("--- End of Log ---")
        ]
        mock_print.assert_has_calls(expected_calls)


    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_search_log_found(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an existing log file with data
        mock_path_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2077-10-22T10:00:00", "item": "Old Tire", "location": "Highway 101", "quantity": 4, "notes": "Might be useful."},
            {"timestamp": "2077-10-23T13:37:00", "item": "Broken Radio", "location": "Vault 111", "quantity": 1, "notes": "Parts for repair."},
            {"timestamp": "2077-10-24T08:00:00", "item": "Rusty Crowbar", "location": "Old Supermart", "quantity": 1, "notes": "Good for prying."}
        ]

        scavenger_log.search_log("radio")

        expected_calls = [
            unittest.mock.call("\n--- Search Results for 'radio' ---"),
            unittest.mock.call("Result #1:"),
            unittest.mock.call("  Timestamp: 2077-10-23T13:37:00"),
            unittest.mock.call("  Item: Broken Radio"),
            unittest.mock.call("  Location: Vault 111"),
            unittest.mock.call("  Quantity: 1"),
            unittest.mock.call("  Notes: Parts for repair."),
            unittest.mock.call("-" * 20),
            unittest.mock.call("--- End of Search Results ---")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_search_log_not_found(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an existing log file with data
        mock_path_exists.return_value = True
        mock_json_load.return_value = [
            {"timestamp": "2077-10-22T10:00:00", "item": "Old Tire", "location": "Highway 101", "quantity": 4, "notes": "Might be useful."},
            {"timestamp": "2077-10-23T13:37:00", "item": "Broken Radio", "location": "Vault 111", "quantity": 1, "notes": "Parts for repair."}
        ]

        scavenger_log.search_log("wrench")

        mock_print.assert_called_once_with("No entries found matching 'wrench'.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_search_log_empty_log(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an empty log file
        mock_path_exists.return_value = False
        mock_json_load.return_value = []

        scavenger_log.search_log("anything")

        mock_print.assert_called_once_with("No entries found matching 'anything'.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_load_log_corrupted_json(self, mock_print, mock_json_load, mock_open_file, mock_path_exists):
        # Mock rationale: Simulate an existing but corrupted log file
        mock_path_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_open_file.return_value.read.return_value = "invalid json" # Ensure open is called

        result = scavenger_log._load_log()

        self.assertEqual(result, [])
        mock_print.assert_called_once_with(f"Warning: {scavenger_log.LOG_FILE} is corrupted or empty. Starting with an empty log.")
        mock_open_file.assert_called_once_with(self.mock_log_file_path, 'r', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
