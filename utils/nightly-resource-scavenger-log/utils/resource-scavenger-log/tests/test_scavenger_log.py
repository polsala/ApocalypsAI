import unittest
import json
import os
from unittest.mock import patch, mock_open, call
from datetime import datetime

# Mock rationale: We need to isolate file I/O and date/time for deterministic tests.
# Mocking `open` allows us to simulate reading from and writing to `resources.json`
# without actually touching the filesystem. Mocking `datetime.now` ensures that
# the 'date' field in new entries is consistent across test runs.
# Mocking `sys.stdout` allows capturing print output for verification.
# Mocking `os.path.exists` allows simulating the presence or absence of the data file.

# Add src directory to sys.path for direct import during testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger_log

class TestScavengerLog(unittest.TestCase):

    def setUp(self):
        # Reset the data file path for each test to ensure isolation
        self.mock_data_path = '/mock/path/resources.json'
        # Mock rationale: Ensure _get_data_path returns a consistent mock path.
        self.patch_get_data_path = patch('scavenger_log._get_data_path', return_value=self.mock_data_path)
        self.patch_get_data_path.start()

    def tearDown(self):
        self.patch_get_data_path.stop()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout')
    @patch('scavenger_log.datetime')
    def test_add_resource_new_file(self, mock_datetime, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Set a fixed date for deterministic testing of default date.
        mock_now = mock_datetime.now.return_value
        mock_now.strftime.return_value = '2024-07-20'

        scavenger_log.add_resource("Water Bottle", 5, "bottles", "Old Bunker Cache")

        # Verify file was opened for writing
        mock_file_open.assert_called_once_with(self.mock_data_path, 'w')
        handle = mock_file_open()
        # Verify content written
        expected_data = [
            {
                'resource': 'Water Bottle',
                'quantity': 5,
                'unit': 'bottles',
                'location': 'Old Bunker Cache',
                'date': '2024-07-20'
            }
        ]
        handle.write.assert_called_once_with(json.dumps(expected_data, indent=2))
        mock_stdout.write.assert_any_call("Added: 5 bottles of Water Bottle at Old Bunker Cache on 2024-07-20\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout')
    def test_add_resource_existing_file(self, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Simulate existing data in the file.
        initial_data = [
            {
                'resource': 'Canned Beans',
                'quantity': 10,
                'unit': 'cans',
                'location': 'Supermarket',
                'date': '2024-07-19'
            }
        ]
        mock_file_open.return_value.read.return_value = json.dumps(initial_data)

        scavenger_log.add_resource("Medical Kit", 2, "kits", "Clinic Ruins", date="2024-07-21")

        # Verify file was opened for reading and then writing
        mock_file_open.assert_any_call(self.mock_data_path, 'r')
        mock_file_open.assert_any_call(self.mock_data_path, 'w')
        handle = mock_file_open()
        # Verify content written (appended)
        expected_data = initial_data + [
            {
                'resource': 'Medical Kit',
                'quantity': 2,
                'unit': 'kits',
                'location': 'Clinic Ruins',
                'date': '2024-07-21'
            }
        ]
        handle.write.assert_called_with(json.dumps(expected_data, indent=2))
        mock_stdout.write.assert_any_call("Added: 2 kits of Medical Kit at Clinic Ruins on 2024-07-21\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout')
    def test_list_resources(self, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Provide specific data to be listed.
        test_data = [
            {'resource': 'Food Ration', 'quantity': 3, 'unit': 'packs', 'location': 'Shelter A', 'date': '2024-07-18'},
            {'resource': 'Ammo', 'quantity': 50, 'unit': 'rounds', 'location': 'Armory B', 'date': '2024-07-19'}
        ]
        mock_file_open.return_value.read.return_value = json.dumps(test_data)

        scavenger_log.list_resources()

        mock_file_open.assert_called_once_with(self.mock_data_path, 'r')
        output_calls = [call_arg[0] for call_arg in mock_stdout.write.call_args_list]
        self.assertIn("\n--- Logged Resources ---\n", output_calls)
        self.assertIn("[1] Resource: Food Ration\n", output_calls)
        self.assertIn("    Quantity: 3 packs\n", output_calls)
        self.assertIn("    Location: Shelter A\n", output_calls)
        self.assertIn("    Date:     2024-07-18\n", output_calls)
        self.assertIn("[2] Resource: Ammo\n", output_calls)
        self.assertIn("    Quantity: 50 rounds\n", output_calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout')
    def test_list_resources_empty(self, mock_stdout, mock_exists, mock_file_open):
        scavenger_log.list_resources()
        mock_stdout.write.assert_any_call("No resources logged yet. Go scavenge!\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout')
    def test_generate_report(self, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Provide data with multiple entries for reporting.
        test_data = [
            {'resource': 'Water Bottle', 'quantity': 5, 'unit': 'bottles', 'location': 'A', 'date': '2024-07-18'},
            {'resource': 'Canned Food', 'quantity': 10, 'unit': 'cans', 'location': 'B', 'date': '2024-07-18'},
            {'resource': 'Water Bottle', 'quantity': 3, 'unit': 'bottles', 'location': 'C', 'date': '2024-07-19'},
            {'resource': 'Canned Food', 'quantity': 2, 'unit': 'boxes', 'location': 'D', 'date': '2024-07-19'}
        ]
        mock_file_open.return_value.read.return_value = json.dumps(test_data)

        scavenger_log.generate_report()

        mock_file_open.assert_called_once_with(self.mock_data_path, 'r')
        output_calls = [call_arg[0] for call_arg in mock_stdout.write.call_args_list]
        self.assertIn("\n--- Resource Summary Report ---\n", output_calls)
        self.assertIn("Resource: Water Bottle\n", output_calls)
        self.assertIn("    Total: 8 bottles\n", output_calls)
        self.assertIn("Resource: Canned Food\n", output_calls)
        self.assertIn("    Total: 10 cans\n", output_calls)
        self.assertIn("    Total: 2 boxes\n", output_calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout')
    def test_generate_report_empty(self, mock_stdout, mock_exists, mock_file_open):
        scavenger_log.generate_report()
        mock_stdout.write.assert_any_call("No resources logged yet to generate a report.\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout')
    def test_load_resources_corrupted_json(self, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_file_open.return_value.read.return_value = "{invalid json"

        resources = scavenger_log._load_resources()
        self.assertEqual(resources, [])
        mock_stdout.write.assert_any_call(f"Warning: {scavenger_log.DATA_FILE} is corrupted. Starting with an empty log.\n")


if __name__ == '__main__':
    unittest.main()
