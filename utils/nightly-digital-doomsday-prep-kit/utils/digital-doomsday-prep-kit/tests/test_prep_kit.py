import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime
import sys

# Mock rationale: Allows the test file to import the utility script as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prep_kit import add_asset, list_assets, verify_asset, DATA_FILE, _load_data, _save_data

class TestPrepKit(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.mock_datetime_now = datetime(2023, 10, 27, 10, 0, 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('datetime.datetime')
    def test_add_asset_new(self, mock_dt, mock_json_dump, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a non-existent data file initially, then successful write.
        # Mock rationale: Control the current time for deterministic 'last_verified' timestamps.
        mock_os_exists.return_value = False
        mock_json_load.return_value = {}
        mock_dt.now.return_value = self.mock_datetime_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime to be called for isoformat

        add_asset("Family Photos", "Cloud Storage Gamma")

        expected_data = {
            "Family Photos": {
                "location": "Cloud Storage Gamma",
                "last_verified": self.mock_datetime_now.isoformat()
            }
        }
        mock_json_dump.assert_called_once_with(expected_data, mock_file_open(), indent=4)
        mock_os_exists.assert_called_once_with(DATA_FILE)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('datetime.datetime')
    def test_add_asset_existing(self, mock_dt, mock_json_dump, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing data file with an asset already present.
        # Mock rationale: Control the current time for deterministic 'last_verified' timestamps.
        mock_os_exists.return_value = True
        mock_json_load.return_value = {
            "Family Photos": {
                "location": "Cloud Storage Gamma",
                "last_verified": "2023-10-26T10:00:00"
            }
        }
        mock_dt.now.return_value = self.mock_datetime_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        with patch('sys.stdout') as mock_stdout:
            add_asset("Family Photos", "Cloud Storage Gamma")
            mock_stdout.assert_called_with("Error: Asset 'Family Photos' already exists. Use 'verify' to update it.\n")
        mock_json_dump.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_list_assets_empty(self, mock_stdout, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an empty data file.
        mock_os_exists.return_value = False
        mock_json_load.return_value = {}

        list_assets()
        mock_stdout.assert_called_with("No digital assets tracked yet. Add some with 'add' command.\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_list_assets_populated(self, mock_stdout, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a data file with multiple assets.
        mock_os_exists.return_value = True
        mock_json_load.return_value = {
            "Family Photos": {
                "location": "Cloud Storage Gamma",
                "last_verified": "2023-10-26T10:00:00"
            },
            "Tax Documents": {
                "location": "Local NAS",
                "last_verified": "2023-09-15T14:30:00"
            }
        }

        list_assets()
        expected_output = (
            "\n--- Digital Doomsday Prep Kit Assets ---\n" +
            "  Asset: Family Photos\n" +
            "    Location: Cloud Storage Gamma\n" +
            "    Last Verified: 2023-10-26T10:00:00\n" +
            "----------------------------------------\n" +
            "  Asset: Tax Documents\n" +
            "    Location: Local NAS\n" +
            "    Last Verified: 2023-09-15T14:30:00\n" +
            "----------------------------------------\n"
        )
        mock_stdout.assert_called_with(expected_output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('datetime.datetime')
    def test_verify_asset_existing(self, mock_dt, mock_json_dump, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing data file and update an asset's timestamp.
        # Mock rationale: Control the current time for deterministic 'last_verified' timestamps.
        initial_data = {
            "Family Photos": {
                "location": "Cloud Storage Gamma",
                "last_verified": "2023-10-26T10:00:00"
            }
        }
        mock_os_exists.return_value = True
        mock_json_load.return_value = initial_data
        mock_dt.now.return_value = self.mock_datetime_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        verify_asset("Family Photos")

        expected_data = {
            "Family Photos": {
                "location": "Cloud Storage Gamma",
                "last_verified": self.mock_datetime_now.isoformat()
            }
        }
        mock_json_dump.assert_called_once_with(expected_data, mock_file_open(), indent=4)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout')
    def test_verify_asset_non_existent(self, mock_stdout, mock_json_dump, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a data file where the requested asset does not exist.
        mock_os_exists.return_value = True
        mock_json_load.return_value = {
            "Other Asset": {
                "location": "Somewhere",
                "last_verified": "2023-01-01T00:00:00"
            }
        }

        verify_asset("NonExistent Asset")

        mock_stdout.assert_called_with("Error: Asset 'NonExistent Asset' not found. Add it first with 'add' command.\n")
        mock_json_dump.assert_not_called()

    # Test _load_data and _save_data directly for completeness
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_data_exists(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing data file with content.
        mock_os_exists.return_value = True
        mock_json_load.return_value = {"test": "data"}
        result = _load_data()
        self.assertEqual(result, {"test": "data"})
        mock_os_exists.assert_called_once_with(DATA_FILE)
        mock_file_open.assert_called_once_with(DATA_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_data_not_exists(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a non-existent data file.
        mock_os_exists.return_value = False
        result = _load_data()
        self.assertEqual(result, {})
        mock_os_exists.assert_called_once_with(DATA_FILE)
        mock_file_open.assert_not_called() # open should not be called if file doesn't exist

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError('Expecting value', '', 0))
    @patch('sys.stdout')
    def test_load_data_corrupted(self, mock_stdout, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a corrupted JSON data file.
        mock_os_exists.return_value = True
        mock_file_open.return_value.__enter__.return_value.read.return_value = 'invalid json'
        result = _load_data()
        self.assertEqual(result, {})
        mock_stdout.assert_called_with(f"Warning: {DATA_FILE} is corrupted or empty. Starting with empty data.\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_data(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate saving data to a file.
        data_to_save = {"new": "data"}
        _save_data(data_to_save)
        mock_file_open.assert_called_once_with(DATA_FILE, 'w')
        mock_json_dump.assert_called_once_with(data_to_save, mock_file_open(), indent=4)
