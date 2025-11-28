import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Import the functions from the tracker.py script
# Assuming tracker.py is in the parent directory for testing purposes
# In a real setup, you might adjust sys.path or use a proper package structure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker
sys.path.pop(0)

class TestTracker(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

        # Capture stderr for testing error messages
        self.held_stderr = sys.stderr
        self.mock_stderr = StringIO()
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_no_file(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate the scenario where the inventory file does not exist.
        mock_exists.return_value = False
        inventory = tracker.load_inventory()
        self.assertEqual(inventory, {})
        mock_exists.assert_called_once_with(tracker.INVENTORY_FILE)
        mock_file_open.assert_not_called()
        mock_json_load.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_empty_file(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty or corrupted JSON file.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        inventory = tracker.load_inventory()
        self.assertEqual(inventory, {})
        self.assertIn("Warning: inventory.json is corrupted or empty.", self.mock_stderr.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_success(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate a successful load of a valid inventory file.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Water": 10, "Food": 5}
        inventory = tracker.load_inventory()
        self.assertEqual(inventory, {"Water": 10, "Food": 5})
        mock_file_open.assert_called_once_with(tracker.INVENTORY_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_inventory(self, mock_json_dump, mock_file_open):
        # Mock rationale: Verify that the inventory is correctly serialized and written to file.
        inventory = {"Water": 10, "Food": 5}
        tracker.save_inventory(inventory)
        mock_file_open.assert_called_once_with(tracker.INVENTORY_FILE, 'w')
        mock_json_dump.assert_called_once_with(inventory, mock_file_open(), indent=4)

    def test_add_resource_new_item(self):
        # Mock rationale: Test adding a completely new item to an empty inventory.
        inventory = {}
        result = tracker.add_resource(inventory, "Bandages", 3)
        self.assertTrue(result)
        self.assertEqual(inventory, {"Bandages": 3})
        self.assertIn("Added 3 x Bandages. Current total: 3", self.mock_stdout.getvalue())

    def test_add_resource_existing_item(self):
        # Mock rationale: Test adding more quantity to an item already in inventory.
        inventory = {"Bandages": 3}
        result = tracker.add_resource(inventory, "Bandages", 2)
        self.assertTrue(result)
        self.assertEqual(inventory, {"Bandages": 5})
        self.assertIn("Added 2 x Bandages. Current total: 5", self.mock_stdout.getvalue())

    def test_add_resource_invalid_quantity(self):
        # Mock rationale: Test adding with non-positive or non-integer quantity.
        inventory = {}
        result = tracker.add_resource(inventory, "Bandages", 0)
        self.assertFalse(result)
        self.assertEqual(inventory, {})
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stderr.getvalue())

        self.mock_stderr.truncate(0)
        self.mock_stderr.seek(0)
        result = tracker.add_resource(inventory, "Bandages", -5)
        self.assertFalse(result)
        self.assertEqual(inventory, {})
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stderr.getvalue())

    def test_remove_resource_partial(self):
        # Mock rationale: Test removing a portion of an item's quantity.
        inventory = {"Water": 10, "Food": 5}
        result = tracker.remove_resource(inventory, "Water", 3)
        self.assertTrue(result)
        self.assertEqual(inventory, {"Water": 7, "Food": 5})
        self.assertIn("Removed 3 x Water. Remaining: 7", self.mock_stdout.getvalue())

    def test_remove_resource_all(self):
        # Mock rationale: Test removing all of an item, leading to its removal from inventory.
        inventory = {"Water": 10, "Food": 5}
        result = tracker.remove_resource(inventory, "Food", 5)
        self.assertTrue(result)
        self.assertEqual(inventory, {"Water": 10})
        self.assertIn("Removed all 5 x Food. Item no longer in inventory.", self.mock_stdout.getvalue())

    def test_remove_resource_more_than_available(self):
        # Mock rationale: Test attempting to remove more than available, which should remove the item entirely.
        inventory = {"Water": 10, "Food": 5}
        result = tracker.remove_resource(inventory, "Water", 15)
        self.assertTrue(result)
        self.assertEqual(inventory, {"Food": 5})
        self.assertIn("Removed all 10 x Water. Item no longer in inventory.", self.mock_stdout.getvalue())

    def test_remove_resource_not_found(self):
        # Mock rationale: Test attempting to remove an item that doesn't exist.
        inventory = {"Water": 10}
        result = tracker.remove_resource(inventory, "Bandages", 1)
        self.assertFalse(result)
        self.assertEqual(inventory, {"Water": 10})
        self.assertIn("Error: 'Bandages' not found in inventory.", self.mock_stderr.getvalue())

    def test_remove_resource_invalid_quantity(self):
        # Mock rationale: Test removing with non-positive or non-integer quantity.
        inventory = {"Water": 10}
        result = tracker.remove_resource(inventory, "Water", 0)
        self.assertFalse(result)
        self.assertEqual(inventory, {"Water": 10})
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stderr.getvalue())

        self.mock_stderr.truncate(0)
        self.mock_stderr.seek(0)
        result = tracker.remove_resource(inventory, "Water", -2)
        self.assertFalse(result)
        self.assertEqual(inventory, {"Water": 10})
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stderr.getvalue())

    def test_list_resources_empty(self):
        # Mock rationale: Test listing when the inventory is empty.
        inventory = {}
        tracker.list_resources(inventory)
        self.assertIn("Inventory is empty.", self.mock_stdout.getvalue())

    def test_list_resources_populated(self):
        # Mock rationale: Test listing when the inventory contains items.
        inventory = {"Water": 10, "Food": 5, "Medkit": 1}
        tracker.list_resources(inventory)
        expected_output = (
            "\n--- Current Inventory ---"
            "\n- Food: 5"
            "\n- Medkit: 1"
            "\n- Water: 10"
            "\n-------------------------"
        )
        self.assertEqual(self.mock_stdout.getvalue().strip(), expected_output.strip())

    @patch('tracker.load_inventory')
    @patch('tracker.save_inventory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_add_command(self, mock_parse_args, mock_save, mock_load):
        # Mock rationale: Simulate CLI arguments for 'add' command and verify flow.
        mock_parse_args.return_value = argparse.Namespace(command='add', item='Fuel', quantity=2)
        mock_load.return_value = {}
        tracker.main()
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({'Fuel': 2})
        self.assertIn("Added 2 x Fuel. Current total: 2", self.mock_stdout.getvalue())

    @patch('tracker.load_inventory')
    @patch('tracker.save_inventory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_remove_command(self, mock_parse_args, mock_save, mock_load):
        # Mock rationale: Simulate CLI arguments for 'remove' command and verify flow.
        mock_parse_args.return_value = argparse.Namespace(command='remove', item='Fuel', quantity=1)
        mock_load.return_value = {'Fuel': 2}
        tracker.main()
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({'Fuel': 1})
        self.assertIn("Removed 1 x Fuel. Remaining: 1", self.mock_stdout.getvalue())

    @patch('tracker.load_inventory')
    @patch('tracker.save_inventory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_command(self, mock_parse_args, mock_save, mock_load):
        # Mock rationale: Simulate CLI arguments for 'list' command and verify flow.
        mock_parse_args.return_value = argparse.Namespace(command='list')
        mock_load.return_value = {'Fuel': 2}
        tracker.main()
        mock_load.assert_called_once()
        mock_save.assert_not_called() # List command should not save
        self.assertIn("- Fuel: 2", self.mock_stdout.getvalue())

    @patch('tracker.load_inventory')
    @patch('tracker.save_inventory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_change_no_save(self, mock_parse_args, mock_save, mock_load):
        # Mock rationale: Simulate a command that doesn't modify inventory (e.g., failed add/remove) and verify no save.
        mock_parse_args.return_value = argparse.Namespace(command='add', item='Fuel', quantity=0) # Invalid quantity
        mock_load.return_value = {}
        tracker.main()
        mock_load.assert_called_once()
        mock_save.assert_not_called()
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
