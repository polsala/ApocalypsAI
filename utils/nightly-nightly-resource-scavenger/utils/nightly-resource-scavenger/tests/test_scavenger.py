import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Add the 'src' directory to sys.path for importing scavenger.py
# This makes the test runnable directly from its location.
current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.insert(0, src_dir)

# Mock the RESOURCE_FILE path to ensure tests don't touch real files
MOCK_RESOURCE_FILE = '/mock/path/to/resources.json'

# Now import scavenger. This import will use the modified sys.path
import scavenger # Import the module after sys.path is set

class TestScavenger(unittest.TestCase):

    # Patch the RESOURCE_FILE variable in the scavenger module
    # This ensures that scavenger.RESOURCE_FILE points to our mock path during tests.
    @patch('scavenger.RESOURCE_FILE', MOCK_RESOURCE_FILE)
    @patch('scavenger.os.path.exists')
    @patch('scavenger.json')
    @patch('scavenger.open', new_callable=mock_open)
    def setUp(self, mock_file_open, mock_json, mock_exists):
        # Mock rationale: We need to control file system interactions (read/write)
        # and JSON serialization/deserialization to ensure tests are deterministic
        # and don't affect the actual file system.
        # mock_open: Simulates file reading and writing.
        # mock_json: Simulates json.load and json.dump.
        # mock_exists: Simulates os.path.exists to control whether the resource file "exists".

        self.mock_file_open = mock_file_open
        self.mock_json = mock_json
        self.mock_exists = mock_exists
        self.mock_exists.return_value = False # Default: file doesn't exist initially

        # Capture print output
        self.held_output = StringIO()
        self.patcher_print = patch('sys.stdout', new=self.held_output)
        self.patcher_print.start()

    def tearDown(self):
        self.patcher_print.stop()
        # Remove the added path from sys.path to avoid side effects for other tests
        if src_dir in sys.path:
            sys.path.remove(src_dir)

    def get_printed_output(self):
        return self.held_output.getvalue().strip()

    def test_add_resource_new_item(self):
        # Mock rationale: Simulate an empty resource file, then verify adding an item.
        self.mock_exists.return_value = False # No file exists
        self.mock_json.load.return_value = {} # Load returns empty dict

        scavenger.add_resource("Canned Beans", 5)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once_with({"Canned Beans": 5}, self.mock_file_open(), indent=4)
        self.assertIn("Scavenged 5 units of 'Canned Beans'. Inventory updated, survivor!", self.get_printed_output())

    def test_add_resource_existing_item(self):
        # Mock rationale: Simulate an existing resource file, then verify updating an item.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 5}

        scavenger.add_resource("Canned Beans", 3)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once_with({"Canned Beans": 8}, self.mock_file_open(), indent=4)
        self.assertIn("Scavenged 3 units of 'Canned Beans'. Inventory updated, survivor!", self.get_printed_output())

    def test_add_resource_zero_quantity(self):
        # Mock rationale: Ensure adding zero or negative quantity is handled gracefully.
        scavenger.add_resource("Water", 0)
        self.mock_json.load.assert_not_called() # Should not attempt to load/save
        self.mock_json.dump.assert_not_called()
        self.assertIn("Quantity must be positive to add resources.", self.get_printed_output())

    def test_remove_resource_existing_item(self):
        # Mock rationale: Simulate removing a partial quantity of an existing item.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 5, "Duct Tape": 1}

        scavenger.remove_resource("Canned Beans", 2)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once_with({"Canned Beans": 3, "Duct Tape": 1}, self.mock_file_open(), indent=4)
        self.assertIn("Consumed 2 units of 'Canned Beans'. Remaining: 3. Inventory updated, survivor!", self.get_printed_output())

    def test_remove_resource_all_of_item(self):
        # Mock rationale: Simulate removing all of an item, ensuring it's deleted from inventory.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 2, "Duct Tape": 1}

        scavenger.remove_resource("Canned Beans", 2)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once_with({"Duct Tape": 1}, self.mock_file_open(), indent=4)
        self.assertIn("Consumed all remaining 'Canned Beans'. Item removed from inventory.", self.get_printed_output())

    def test_remove_resource_more_than_available(self):
        # Mock rationale: Simulate attempting to remove more than available, ensuring item is deleted.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 2}

        scavenger.remove_resource("Canned Beans", 5)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once_with({}, self.mock_file_open(), indent=4)
        self.assertIn("Consumed all remaining 'Canned Beans'. Item removed from inventory.", self.get_printed_output())

    def test_remove_resource_non_existent_item(self):
        # Mock rationale: Ensure removing a non-existent item is handled without error.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Duct Tape": 1}

        scavenger.remove_resource("Canned Beans", 1)

        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_not_called() # Should not attempt to save
        self.assertIn("'Canned Beans' not found in inventory. Can't remove what isn't there, survivor.", self.get_printed_output())

    def test_remove_resource_zero_quantity(self):
        # Mock rationale: Ensure removing zero or negative quantity is handled gracefully.
        scavenger.remove_resource("Water", 0)
        self.mock_json.load.assert_not_called()
        self.mock_json.dump.assert_not_called()
        self.assertIn("Quantity must be positive to remove resources.", self.get_printed_output())

    def test_list_resources_empty(self):
        # Mock rationale: Simulate an empty inventory when listing.
        self.mock_exists.return_value = False
        self.mock_json.load.return_value = {}

        scavenger.list_resources()

        self.mock_json.load.assert_called_once()
        self.assertIn("Your inventory is currently empty. Time to scavenge, survivor!", self.get_printed_output())

    def test_list_resources_with_items(self):
        # Mock rationale: Simulate an inventory with items and verify output format.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 3, "Duct Tape": 10, "Water Purifier Tablets": 5}

        scavenger.list_resources()

        self.mock_json.load.assert_called_once()
        output = self.get_printed_output()
        self.assertIn("--- Current Inventory ---", output)
        self.assertIn("Canned Beans: 3", output)
        self.assertIn("Duct Tape: 10", output)
        self.assertIn("Water Purifier Tablets: 5", output)
        self.assertIn("Stay vigilant, survivor!", output)

    def test_clear_resources(self):
        # Mock rationale: Simulate clearing an inventory.
        self.mock_exists.return_value = True
        self.mock_json.load.return_value = {"Canned Beans": 3} # Doesn't matter what's loaded, clear overwrites

        scavenger.clear_resources()

        self.mock_json.dump.assert_called_once_with({}, self.mock_file_open(), indent=4)
        self.assertIn("Inventory wiped clean. A fresh start, or a grave loss? Only time will tell.", self.get_printed_output())

    def test_load_resources_file_not_found(self):
        # Mock rationale: Ensure loading from a non-existent file returns an empty dict.
        self.mock_exists.return_value = False
        resources = scavenger.load_resources()
        self.assertEqual(resources, {})
        self.mock_file_open.assert_not_called()
        self.mock_json.load.assert_not_called()

    def test_load_resources_corrupted_json(self):
        # Mock rationale: Simulate a corrupted JSON file and ensure it's handled gracefully.
        self.mock_exists.return_value = True
        self.mock_file_open.return_value.__enter__.return_value.read.return_value = "not valid json"
        self.mock_json.load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        resources = scavenger.load_resources()
        self.assertEqual(resources, {})
        self.assertIn("Warning: /mock/path/to/resources.json is corrupted. Starting with an empty inventory.", self.get_printed_output())

    def test_save_resources_error(self):
        # Mock rationale: Simulate an error during file writing.
        self.mock_file_open.side_effect = IOError("Disk full")
        scavenger.save_resources({"item": 1})
        self.assertIn("Error saving resources: Disk full", self.get_printed_output())

    # Test main function with argparse (requires patching sys.argv)
    @patch('sys.argv', ['scavenger.py', 'add', 'Food Rations', '10'])
    @patch('scavenger.add_resource')
    def test_main_add_command(self, mock_add_resource):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        # We also mock the underlying function to prevent actual file operations during this test.
        scavenger.main()
        mock_add_resource.assert_called_once_with("Food Rations", 10)

    @patch('sys.argv', ['scavenger.py', 'remove', 'Water', '2'])
    @patch('scavenger.remove_resource')
    def test_main_remove_command(self, mock_remove_resource):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        scavenger.main()
        mock_remove_resource.assert_called_once_with("Water", 2)

    @patch('sys.argv', ['scavenger.py', 'list'])
    @patch('scavenger.list_resources')
    def test_main_list_command(self, mock_list_resources):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        scavenger.main()
        mock_list_resources.assert_called_once()

    @patch('sys.argv', ['scavenger.py', 'clear'])
    @patch('scavenger.clear_resources')
    def test_main_clear_command(self, mock_clear_resources):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        scavenger.main()
        mock_clear_resources.assert_called_once()

if __name__ == '__main__':
    unittest.main()
