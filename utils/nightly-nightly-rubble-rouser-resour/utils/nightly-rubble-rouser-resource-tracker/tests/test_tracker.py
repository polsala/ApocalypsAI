import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Add the src directory to the Python path for importing tracker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker
sys.path.pop(0) # Clean up path after import

class TestRubbleRouserResourceTracker(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        # Define a dummy data file name for testing
        self.test_data_file = 'test_resources.json'
        # Ensure the tracker functions use this test file
        tracker.DATA_FILE = self.test_data_file

    def tearDown(self):
        # Restore stdout
        sys.stdout = sys.__stdout__
        # Clean up the test_data_file if it was created (though mocks prevent actual creation)
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_resource_new_stash_new_item(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty data file initially.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        tracker.add_resource("Shelter A", "Water", 10, self.test_data_file)

        expected_data = {"Shelter A": {"Water": 10}}
        mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=2)
        self.assertIn("Added 10 'Water' to 'Shelter A'. Current: 10", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_resource_existing_stash_existing_item(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file with some resources.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Shelter A": {"Water": 5}}

        tracker.add_resource("Shelter A", "Water", 3, self.test_data_file)

        expected_data = {"Shelter A": {"Water": 8}}
        mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=2)
        self.assertIn("Added 3 'Water' to 'Shelter A'. Current: 8", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_remove_resource_success(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file with enough resources to remove.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Shelter A": {"Food Rations": 10, "Water": 5}}

        tracker.remove_resource("Shelter A", "Food Rations", 3, self.test_data_file)

        expected_data = {"Shelter A": {"Food Rations": 7, "Water": 5}}
        mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=2)
        self.assertIn("Removed 3 'Food Rations' from 'Shelter A'. Remaining: 7", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_remove_resource_not_enough(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file where removal quantity exceeds available.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Shelter A": {"Food Rations": 2}}

        tracker.remove_resource("Shelter A", "Food Rations", 5, self.test_data_file)

        expected_data = {}
        mock_json_dump.assert_called_once_with(expected_data, mock_open_file(), indent=2)
        self.assertIn("Warning: Trying to remove 5 'Food Rations' from 'Shelter A', but only 2 available. Removing all 2.", self.captured_output.getvalue())
        self.assertIn("Removed 5 'Food Rations' from 'Shelter A'. Remaining: 0", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_remove_resource_item_not_found(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file where the item to remove does not exist.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Shelter A": {"Water": 5}}

        tracker.remove_resource("Shelter A", "First Aid Kit", 1, self.test_data_file)

        # Data should not change, and dump should not be called with new data
        mock_json_dump.assert_not_called()
        self.assertIn("Error: 'First Aid Kit' not found in 'Shelter A'.", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_resources_all_stashes(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file with multiple stashes and items.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Shelter A": {"Water": 5, "Food Rations": 10},
            "Cache B": {"Batteries": 20}
        }

        tracker.list_resources(data_file=self.test_data_file)

        output = self.captured_output.getvalue()
        self.assertIn("All Stashes and Resources:", output)
        self.assertIn("'Shelter A':", output)
        self.assertIn("  - Water: 5", output)
        self.assertIn("  - Food Rations: 10", output)
        self.assertIn("'Cache B':", output)
        self.assertIn("  - Batteries: 20", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_resources_specific_stash(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing data file with multiple stashes.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Shelter A": {"Water": 5, "Food Rations": 10},
            "Cache B": {"Batteries": 20}
        }

        tracker.list_resources("Shelter A", data_file=self.test_data_file)

        output = self.captured_output.getvalue()
        self.assertIn("Resources in 'Shelter A':", output)
        self.assertIn("  - Water: 5", output)
        self.assertIn("  - Food Rations: 10", output)
        self.assertNotIn("'Cache B':", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_resources_empty_data(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty data file.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        tracker.list_resources(data_file=self.test_data_file)

        self.assertIn("No resources tracked yet. Start by adding some!", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_total_item_across_stashes(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate data with an item spread across multiple stashes.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Shelter A": {"Water": 5, "Food Rations": 10},
            "Cache B": {"Water": 3, "Batteries": 20},
            "Outpost C": {"Food Rations": 2}
        }

        tracker.total_item("Water", self.test_data_file)
        self.assertIn("Total 'Water' across all stashes: 8", self.captured_output.getvalue())

        self.captured_output = StringIO() # Reset for next assertion
        sys.stdout = self.captured_output

        tracker.total_item("Food Rations", self.test_data_file)
        self.assertIn("Total 'Food Rations' across all stashes: 12", self.captured_output.getvalue())

        self.captured_output = StringIO() # Reset for next assertion
        sys.stdout = self.captured_output

        tracker.total_item("NonExistentItem", self.test_data_file)
        self.assertIn("Total 'NonExistentItem' across all stashes: 0", self.captured_output.getvalue())
