import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Adjust sys.path to import the scavenger module correctly for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger
sys.path.pop(0)

class TestScavenger(unittest.TestCase):

    def setUp(self):
        # Define the inventory file name and its expected full path within the src directory
        self.inventory_filename = scavenger.INVENTORY_FILE
        self.mock_src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
        self.mock_file_path = os.path.join(self.mock_src_dir, self.inventory_filename)

        # Mock stdout to capture print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_existing_file(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing inventory file and its content.
        # os.path.exists is mocked to return True, indicating the file exists.
        # builtins.open is mocked to simulate opening the file.
        # json.load is mocked to return predefined JSON data, simulating file content.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Water": {"quantity": 10, "location": "Shelf"}}
        inventory = scavenger.load_inventory(self.mock_file_path)
        self.assertEqual(inventory, {"Water": {"quantity": 10, "location": "Shelf"}})
        mock_exists.assert_called_once_with(self.mock_file_path)
        mock_open_file.assert_called_once_with(self.mock_file_path, 'r')
        mock_json_load.assert_called_once_with(mock_open_file())

    @patch('os.path.exists')
    def test_load_inventory_no_file(self, mock_exists):
        # Mock rationale: Simulate no existing inventory file.
        # os.path.exists is mocked to return False.
        mock_exists.return_value = False
        inventory = scavenger.load_inventory(self.mock_file_path)
        self.assertEqual(inventory, {})
        mock_exists.assert_called_once_with(self.mock_file_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Test Error", "", 0))
    def test_load_inventory_corrupted_file(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        # os.path.exists returns True, but json.load raises JSONDecodeError.
        mock_exists.return_value = True
        inventory = scavenger.load_inventory(self.mock_file_path)
        self.assertEqual(inventory, {})
        self.assertIn(f"Warning: {self.inventory_filename} is corrupted or empty.", self.mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_inventory(self, mock_json_dump, mock_open_file):
        # Mock rationale: Simulate saving inventory to a file.
        # builtins.open is mocked to simulate file writing.
        # json.dump is mocked to ensure it's called with the correct data.
        inventory = {"Food": {"quantity": 5, "location": "Cache"}}
        scavenger.save_inventory(self.mock_file_path, inventory)
        mock_open_file.assert_called_once_with(self.mock_file_path, 'w')
        mock_json_dump.assert_called_once_with(inventory, mock_open_file(), indent=4)

    def test_add_resource_new(self):
        inventory = {}
        scavenger.add_resource(inventory, "Water", 10, "Backpack")
        self.assertEqual(inventory, {"Water": {"quantity": 10, "location": "Backpack"}})
        self.assertIn("Added/Updated: Water", self.mock_stdout.getvalue())

    def test_add_resource_existing(self):
        inventory = {"Water": {"quantity": 5, "location": "Old Spot"}}
        scavenger.add_resource(inventory, "Water", 15, "New Spot")
        self.assertEqual(inventory, {"Water": {"quantity": 15, "location": "New Spot"}})
        self.assertIn("Resource 'Water' already exists. Updating quantity and location.", self.mock_stdout.getvalue())
        self.assertIn("Added/Updated: Water", self.mock_stdout.getvalue())

    def test_update_resource_existing(self):
        inventory = {"Food": {"quantity": 5, "location": "Cache"}}
        scavenger.update_resource(inventory, "Food", 7)
        self.assertEqual(inventory, {"Food": {"quantity": 7, "location": "Cache"}})
        self.assertIn("Updated: Food", self.mock_stdout.getvalue())

    def test_update_resource_not_found(self):
        inventory = {}
        scavenger.update_resource(inventory, "NonExistent", 1)
        self.assertEqual(inventory, {})
        self.assertIn("Error: Resource 'NonExistent' not found.", self.mock_stdout.getvalue())

    def test_remove_resource_existing(self):
        inventory = {"Tools": {"quantity": 2, "location": "Shed"}}
        scavenger.remove_resource(inventory, "Tools")
        self.assertEqual(inventory, {})
        self.assertIn("Removed: Tools", self.mock_stdout.getvalue())

    def test_remove_resource_not_found(self):
        inventory = {}
        scavenger.remove_resource(inventory, "NonExistent")
        self.assertEqual(inventory, {})
        self.assertIn("Error: Resource 'NonExistent' not found.", self.mock_stdout.getvalue())

    def test_list_resources_empty(self):
        inventory = {}
        scavenger.list_resources(inventory)
        self.assertIn("Your inventory is currently empty. Time to scavenge!", self.mock_stdout.getvalue())

    def test_list_resources_populated(self):
        inventory = {
            "Water": {"quantity": 10, "location": "Backpack"},
            "Food": {"quantity": 5, "location": "Cache"}
        }
        scavenger.list_resources(inventory)
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Current Inventory ---", output)
        self.assertIn("Name: Water, Quantity: 10, Location: Backpack", output)
        self.assertIn("Name: Food, Quantity: 5, Location: Cache", output)
        self.assertIn("-------------------------", output)

    @patch('sys.argv', ['scavenger.py', 'add', '--name', 'Medkit', '--quantity', '1', '--location', 'First Aid'])
    @patch('scavenger.load_inventory', return_value={})
    @patch('scavenger.save_inventory')
    def test_main_add_command(self, mock_save, mock_load):
        # Mock rationale: Simulate command-line arguments for 'add' command.
        # scavenger.load_inventory is mocked to return an empty dict, simulating a fresh start.
        # scavenger.save_inventory is mocked to prevent actual file writes during test.
        scavenger.main()
        mock_load.assert_called_once_with(self.mock_file_path)
        mock_save.assert_called_once()
        saved_inventory = mock_save.call_args[0][1] # Get the inventory passed to save_inventory
        self.assertEqual(saved_inventory, {"Medkit": {"quantity": 1, "location": "First Aid"}})
        self.assertIn("Added/Updated: Medkit", self.mock_stdout.getvalue())

    @patch('sys.argv', ['scavenger.py', 'update', '--name', 'Medkit', '--quantity', '2'])
    @patch('scavenger.load_inventory', return_value={"Medkit": {"quantity": 1, "location": "First Aid"}}))
    @patch('scavenger.save_inventory')
    def test_main_update_command(self, mock_save, mock_load):
        # Mock rationale: Simulate command-line arguments for 'update' command.
        # scavenger.load_inventory is mocked to return an existing inventory.
        # scavenger.save_inventory is mocked to prevent actual file writes.
        scavenger.main()
        mock_load.assert_called_once_with(self.mock_file_path)
        mock_save.assert_called_once()
        saved_inventory = mock_save.call_args[0][1]
        self.assertEqual(saved_inventory, {"Medkit": {"quantity": 2, "location": "First Aid"}})
        self.assertIn("Updated: Medkit", self.mock_stdout.getvalue())

    @patch('sys.argv', ['scavenger.py', 'remove', '--name', 'Medkit'])
    @patch('scavenger.load_inventory', return_value={"Medkit": {"quantity": 1, "location": "First Aid"}}))
    @patch('scavenger.save_inventory')
    def test_main_remove_command(self, mock_save, mock_load):
        # Mock rationale: Simulate command-line arguments for 'remove' command.
        # scavenger.load_inventory is mocked to return an existing inventory.
        # scavenger.save_inventory is mocked to prevent actual file writes.
        scavenger.main()
        mock_load.assert_called_once_with(self.mock_file_path)
        mock_save.assert_called_once()
        saved_inventory = mock_save.call_args[0][1]
        self.assertEqual(saved_inventory, {})
        self.assertIn("Removed: Medkit", self.mock_stdout.getvalue())

    @patch('sys.argv', ['scavenger.py', 'list'])
    @patch('scavenger.load_inventory', return_value={"Medkit": {"quantity": 1, "location": "First Aid"}}))
    @patch('scavenger.save_inventory')
    def test_main_list_command(self, mock_save, mock_load):
        # Mock rationale: Simulate command-line arguments for 'list' command.
        # scavenger.load_inventory is mocked to return an existing inventory.
        # scavenger.save_inventory is mocked to prevent actual file writes (though list doesn't modify).
        scavenger.main()
        mock_load.assert_called_once_with(self.mock_file_path)
        # List command does not modify inventory, so save_inventory should be called with the same data
        mock_save.assert_called_once_with(self.mock_file_path, {"Medkit": {"quantity": 1, "location": "First Aid"}})
        self.assertIn("Name: Medkit, Quantity: 1, Location: First Aid", self.mock_stdout.getvalue())

    @patch('sys.argv', ['scavenger.py']) # No command
    @patch('scavenger.load_inventory')
    @patch('scavenger.save_inventory')
    def test_main_no_command(self, mock_save, mock_load):
        # Mock rationale: Simulate running the script with no command.
        # load_inventory and save_inventory should not be called if no valid command is given.
        scavenger.main()
        mock_load.assert_not_called()
        mock_save.assert_not_called()
        self.assertIn("usage: scavenger.py", self.mock_stdout.getvalue()) # argparse help message

if __name__ == '__main__':
    unittest.main()
