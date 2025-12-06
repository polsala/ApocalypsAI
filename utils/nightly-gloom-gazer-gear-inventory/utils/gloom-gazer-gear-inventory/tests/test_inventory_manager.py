import unittest
import json
import os
from unittest.mock import patch, mock_open
import sys
from io import StringIO

# Add the src directory to the path to allow importing inventory_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import inventory_manager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Ensure INVENTORY_FILE is set to a test-specific name to avoid conflicts
        self.test_inventory_file = "test_inventory.json"
        inventory_manager.INVENTORY_FILE = self.test_inventory_file
        # Clean up any existing test inventory file
        if os.path.exists(self.test_inventory_file):
            os.remove(self.test_inventory_file)

    def tearDown(self):
        # Clean up the test inventory file after each test
        if os.path.exists(self.test_inventory_file):
            os.remove(self.test_inventory_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_add_item_new(self, mock_json_dump, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate no existing file, mock_open to capture file writes, json.dump to verify content.
        mock_exists.return_value = False # Simulate no existing inventory file

        inventory_manager.add_item("Water Bottle", 2, "Good", "Backpack")

        mock_exists.assert_called_with(self.test_inventory_file)
        mock_file_open.assert_called_with(self.test_inventory_file, 'w')
        mock_json_dump.assert_called_once()
        expected_inventory = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"}
        }
        self.assertEqual(mock_json_dump.call_args[0][0], expected_inventory)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_item_existing(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify updated content.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"}
        }

        inventory_manager.add_item("Water Bottle", 1, "Used", "Vest")

        mock_exists.assert_called_with(self.test_inventory_file)
        mock_file_open.assert_any_call(self.test_inventory_file, 'r')
        mock_file_open.assert_any_call(self.test_inventory_file, 'w')
        mock_json_dump.assert_called_once()
        expected_inventory = {
            "Water Bottle": {"quantity": 3, "condition": "Used", "location": "Vest"}
        }
        self.assertEqual(mock_json_dump.call_args[0][0], expected_inventory)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_remove_item_exists(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify updated content.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"},
            "Canned Food": {"quantity": 5, "condition": "New", "location": "Pantry"}
        }

        inventory_manager.remove_item("Water Bottle")

        mock_json_dump.assert_called_once()
        expected_inventory = {
            "Canned Food": {"quantity": 5, "condition": "New", "location": "Pantry"}
        }
        self.assertEqual(mock_json_dump.call_args[0][0], expected_inventory)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_remove_item_not_exists(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify no change.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Canned Food": {"quantity": 5, "condition": "New", "location": "Pantry"}
        }
        
        # Capture stdout to check printed message
        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.remove_item("Water Bottle")

        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertIn("Item 'Water Bottle' not found in inventory.", captured_output.getvalue())
        mock_json_dump.assert_not_called() # No change should be saved

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_item_quantity(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify updated content.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"}
        }

        inventory_manager.update_item("Water Bottle", quantity=3)

        mock_json_dump.assert_called_once()
        expected_inventory = {
            "Water Bottle": {"quantity": 3, "condition": "Good", "location": "Backpack"}
        }
        self.assertEqual(mock_json_dump.call_args[0][0], expected_inventory)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_item_all_details(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify updated content.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"}
        }

        inventory_manager.update_item("Water Bottle", quantity=1, condition="Damaged", location="Pocket")

        mock_json_dump.assert_called_once()
        expected_inventory = {
            "Water Bottle": {"quantity": 1, "condition": "Damaged", "location": "Pocket"}
        }
        self.assertEqual(mock_json_dump.call_args[0][0], expected_inventory)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_item_not_exists(self, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide initial data, json.dump to verify no change.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Canned Food": {"quantity": 5, "condition": "New", "location": "Pantry"}
        }

        # Capture stdout to check printed message
        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.update_item("Water Bottle", quantity=1)

        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertIn("Item 'Water Bottle' not found in inventory. Cannot update.", captured_output.getvalue())
        mock_json_dump.assert_not_called() # No change should be saved

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_items_empty(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate no existing file, mock_open for file operations, json.load to provide empty data.
        mock_exists.return_value = False
        mock_json_load.return_value = {} # Should not be called if exists is False, but good for safety

        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.list_items()

        sys.stdout = sys.__stdout__
        self.assertIn("Inventory is empty.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_items_with_data(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide data.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"},
            "Canned Food": {"quantity": 5, "condition": "New", "location": "Pantry"}
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.list_items()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("--- Current Inventory ---", output)
        self.assertIn("Water Bottle:", output)
        self.assertIn("Quantity: 2", output)
        self.assertIn("Condition: Good", output)
        self.assertIn("Location: Backpack", output)
        self.assertIn("Canned Food:", output)
        self.assertIn("Quantity: 5", output)
        self.assertIn("Condition: New", output)
        self.assertIn("Location: Pantry", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_check_status_empty(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate no existing file, mock_open for file operations, json.load to provide empty data.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.check_status()

        sys.stdout = sys.__stdout__
        self.assertIn("Inventory is empty. Nothing to check.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_check_status_with_data(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to provide data.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Water Bottle": {"quantity": 2, "condition": "Good", "location": "Backpack"},
            "Canned Food": {"quantity": 10, "condition": "New", "location": "Pantry"},
            "First Aid Kit": {"quantity": 1, "condition": "Used", "location": "Medical Box"},
            "Rope": {"quantity": 3, "condition": "Damaged", "location": "Tool Shed"}
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        inventory_manager.check_status(low_stock_threshold=3)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("--- Inventory Status Report ---", output)
        self.assertIn("Total unique items: 4", output)
        self.assertIn("Total quantity of all items: 16", output)
        self.assertIn("--- Low Stock Items (<= 3) ---", output)
        self.assertIn("  - Water Bottle: 2", output)
        self.assertIn("  - First Aid Kit: 1", output)
        self.assertIn("  - Rope: 3", output)
        self.assertIn("--- Items in Poor/Used Condition ---", output)
        self.assertIn("  - First Aid Kit: Used", output)
        self.assertIn("  - Rope: Damaged", output)
        self.assertNotIn("Canned Food", output) # Should not be low stock or damaged

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_inventory_corrupted_file(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists to simulate an existing file, mock_open for file operations, json.load to simulate a JSONDecodeError.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        inventory = inventory_manager._load_inventory()

        self.assertEqual(inventory, {})
        self.assertIn(f"Warning: {self.test_inventory_file} is corrupted. Starting with an empty inventory.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
