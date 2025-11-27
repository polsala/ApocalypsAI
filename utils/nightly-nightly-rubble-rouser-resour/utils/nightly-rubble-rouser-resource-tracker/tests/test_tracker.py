import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Mock rationale: We need to test file I/O operations (loading and saving JSON) without actually touching the filesystem.
# `os.path.exists` is mocked to control whether the resource file is 'found'.
# `builtins.open` is mocked to intercept file read/write operations and provide/capture content.
# `json.load` and `json.dump` are mocked to ensure JSON parsing/serialization works with our mock file content.
# `sys.stdout` is mocked to capture print statements for assertion.

# Add the src directory to the Python path to allow importing tracker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import load_resources, save_resources, add_resource, update_resource, list_resources, RESOURCE_FILE

class TestTracker(unittest.TestCase):

    def setUp(self):
        self.initial_resources = {
            "Shelter A": {
                "Water Filter": 2,
                "Canned Beans": 10
            },
            "Old Gas Station": {
                "Fuel Can": 5,
                "Tire Patch Kit": 1
            }
        }
        self.mock_json_content = json.dumps(self.initial_resources, indent=4)

    @patch('os.path.exists', return_value=False)
    def test_load_resources_no_file(self, mock_exists):
        # Mock rationale: Simulate the scenario where the resource file does not exist.
        resources = load_resources()
        self.assertEqual(resources, {})

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_resources_corrupted_file(self, mock_stdout, mock_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file to test error handling.
        resources = load_resources()
        self.assertEqual(resources, {})
        self.assertIn("Warning: resources.json is corrupted.", mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_success(self, mock_json_load, mock_file, mock_exists):
        # Mock rationale: Simulate a successful read of a valid JSON file.
        mock_json_load.return_value = self.initial_resources
        resources = load_resources()
        self.assertEqual(resources, self.initial_resources)
        mock_file.assert_called_once_with(RESOURCE_FILE, 'r', encoding='utf-8')
        mock_json_load.assert_called_once_with(mock_file())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources_success(self, mock_json_dump, mock_file):
        # Mock rationale: Simulate a successful write of resources to a JSON file.
        save_resources(self.initial_resources)
        mock_file.assert_called_once_with(RESOURCE_FILE, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(self.initial_resources, mock_file(), indent=4)

    def test_add_resource_new_location_new_item(self):
        resources = {}
        updated_resources = add_resource(resources, "New Camp", "First Aid Kit", 3)
        self.assertEqual(updated_resources, {"New Camp": {"First Aid Kit": 3}})

    def test_add_resource_existing_location_new_item(self):
        resources = {"Shelter A": {"Water Filter": 2}}
        updated_resources = add_resource(resources, "Shelter A", "Bandages", 5)
        self.assertEqual(updated_resources, {"Shelter A": {"Water Filter": 2, "Bandages": 5}})

    def test_add_resource_existing_item_increment_quantity(self):
        resources = {"Shelter A": {"Water Filter": 2}}
        updated_resources = add_resource(resources, "Shelter A", "Water Filter", 1)
        self.assertEqual(updated_resources, {"Shelter A": {"Water Filter": 3}})

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_resource_existing_item(self, mock_stdout):
        resources = {"Shelter A": {"Water Filter": 2}}
        updated_resources = update_resource(resources, "Shelter A", "Water Filter", 5)
        self.assertEqual(updated_resources, {"Shelter A": {"Water Filter": 5}})
        self.assertIn("Updated Water Filter at Shelter A to 5.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_resource_non_existent_item(self, mock_stdout):
        resources = {"Shelter A": {"Water Filter": 2}}
        updated_resources = update_resource(resources, "Shelter A", "Canned Food", 10)
        self.assertEqual(updated_resources, {"Shelter A": {"Water Filter": 2}})
        self.assertIn("Error: Item 'Canned Food' not found at location 'Shelter A'.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_resource_non_existent_location(self, mock_stdout):
        resources = {"Shelter A": {"Water Filter": 2}}
        updated_resources = update_resource(resources, "New Location", "Water Filter", 10)
        self.assertEqual(updated_resources, {"Shelter A": {"Water Filter": 2}})
        self.assertIn("Error: Item 'Water Filter' not found at location 'New Location'.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_empty(self, mock_stdout):
        list_resources({})
        self.assertIn("No resources tracked yet.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_all(self, mock_stdout):
        list_resources(self.initial_resources)
        output = mock_stdout.getvalue()
        self.assertIn("All Tracked Resources:", output)
        self.assertIn("  Shelter A:", output)
        self.assertIn("    - Water Filter x2", output)
        self.assertIn("    - Canned Beans x10", output)
        self.assertIn("  Old Gas Station:", output)
        self.assertIn("    - Fuel Can x5", output)
        self.assertIn("    - Tire Patch Kit x1", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_location(self, mock_stdout):
        list_resources(self.initial_resources, location="Shelter A")
        output = mock_stdout.getvalue()
        self.assertIn("Resources at Shelter A:", output)
        self.assertIn("  - Water Filter x2", output)
        self.assertIn("  - Canned Beans x10", output)
        self.assertNotIn("Old Gas Station", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_location_not_found(self, mock_stdout):
        list_resources(self.initial_resources, location="Non Existent Base")
        self.assertIn("Location 'Non Existent Base' not found.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_item(self, mock_stdout):
        list_resources(self.initial_resources, item="Water Filter")
        output = mock_stdout.getvalue()
        self.assertIn("'Water Filter' found across locations:", output)
        self.assertIn("  - Shelter A: x2", output)
        self.assertNotIn("Old Gas Station", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_item_not_found(self, mock_stdout):
        list_resources(self.initial_resources, item="Shotgun")
        self.assertIn("No 'Shotgun' found anywhere.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_location_and_item(self, mock_stdout):
        list_resources(self.initial_resources, location="Shelter A", item="Water Filter")
        output = mock_stdout.getvalue()
        self.assertIn("  Shelter A: Water Filter x2", output)
        self.assertNotIn("Canned Beans", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_resources_by_location_and_item_not_found(self, mock_stdout):
        list_resources(self.initial_resources, location="Shelter A", item="Shotgun")
        self.assertIn("Item 'Shotgun' not found at location 'Shelter A'.", mock_stdout.getvalue())
