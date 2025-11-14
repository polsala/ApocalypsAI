import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Mock rationale: We need to test file operations (read/write JSON) without actually touching the filesystem.
# `mock_open` allows us to simulate file content and track write calls.
# `patch('os.path.exists')` allows us to control whether a file is reported as existing.
# `patch('sys.argv')` allows us to simulate command-line arguments for the `main` function.
# `patch('sys.stdout')` and `patch('sys.stderr')` allow us to capture printed output for verification.

# Import the functions directly from the module to avoid issues with `sys.modules` during patching
from src.planner import load_json, save_json, get_shopping_list, update_inventory, main, PROVISIONS_FILE, INVENTORY_FILE

class TestApocalypseProvisionsPlanner(unittest.TestCase):

    def setUp(self):
        self.mock_provisions_data = {
            "emergency glitter": {"target": 10, "unit": "jars"},
            "canned beans": {"target": 24, "unit": "cans"},
            "artisanal jerky": {"target": 5, "unit": "packs"}
        }
        self.mock_inventory_data = {
            "emergency glitter": 7,
            "canned beans": 20,
            "artisanal jerky": 3
        }

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'test': 'data'}))
    @patch('os.path.exists', return_value=True)
    def test_load_json_success(self, mock_exists, mock_file):
        # Mock rationale: Simulate a successful file read operation.
        data = load_json('test.json')
        self.assertEqual(data, {'test': 'data'})
        mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_load_json_file_not_found(self, mock_exists, mock_file):
        # Mock rationale: Simulate a file not existing, expecting an empty dict.
        data = load_json('non_existent.json')
        self.assertEqual(data, {})
        mock_exists.assert_called_once_with('non_existent.json')
        mock_file.assert_not_called() # open should not be called if file doesn't exist

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stderr') # Mock rationale: Capture stderr output for error messages
    def test_load_json_malformed(self, mock_stderr, mock_exists, mock_file):
        # Mock rationale: Simulate a file with invalid JSON content.
        mock_file.return_value.read.return_value = 'invalid json'
        data = load_json('malformed.json')
        self.assertEqual(data, {})
        mock_stderr.write.assert_called_with('Error: Could not decode JSON from malformed.json. File might be malformed.\n')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_json(self, mock_file):
        # Mock rationale: Simulate a file write operation and check the content written.
        data_to_save = {'new_item': 10}
        save_json('output.json', data_to_save)
        mock_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        handle = mock_file()
        handle.write.assert_called_once_with(json.dumps(data_to_save, indent=4))

    def test_get_shopping_list_empty(self):
        # Mock rationale: Test scenario where all items are sufficiently stocked.
        provisions = {"item1": {"target": 5}, "item2": {"target": 10}}
        inventory = {"item1": 5, "item2": 10}
        shopping_list = get_shopping_list(provisions, inventory)
        self.assertEqual(shopping_list, {})

    def test_get_shopping_list_some_needed(self):
        # Mock rationale: Test scenario where some items need replenishment.
        provisions = {
            "item1": {"target": 5, "unit": "pcs"},
            "item2": {"target": 10, "unit": "boxes"},
            "item3": {"target": 3, "unit": "kits"}
        }
        inventory = {"item1": 3, "item2": 10, "item3": 1}
        expected_list = {
            "item1": {'quantity': 2, 'unit': 'pcs'},
            "item3": {'quantity': 2, 'unit': 'kits'}
        }
        shopping_list = get_shopping_list(provisions, inventory)
        self.assertEqual(shopping_list, expected_list)

    def test_get_shopping_list_all_needed(self):
        # Mock rationale: Test scenario where all items need replenishment.
        provisions = {
            "item1": {"target": 5, "unit": "pcs"},
            "item2": {"target": 10, "unit": "boxes"}
        }
        inventory = {"item1": 0, "item2": 0}
        expected_list = {
            "item1": {'quantity': 5, 'unit': 'pcs'},
            "item2": {'quantity': 10, 'unit': 'boxes'}
        }
        shopping_list = get_shopping_list(provisions, inventory)
        self.assertEqual(shopping_list, expected_list)

    def test_update_inventory_consume_success(self):
        # Mock rationale: Test successful consumption of an item.
        inventory = {"item": 10}
        result = update_inventory("item", -5, inventory)
        self.assertTrue(result)
        self.assertEqual(inventory["item"], 5)

    def test_update_inventory_add_success(self):
        # Mock rationale: Test successful addition of an item.
        inventory = {"item": 10}
        result = update_inventory("item", 5, inventory)
        self.assertTrue(result)
        self.assertEqual(inventory["item"], 15)

    def test_update_inventory_add_new_item(self):
        # Mock rationale: Test adding a new item not previously in inventory.
        inventory = {}
        result = update_inventory("new_item", 5, inventory)
        self.assertTrue(result)
        self.assertEqual(inventory["new_item"], 5)

    @patch('sys.stderr')
    def test_update_inventory_consume_not_found(self, mock_stderr):
        # Mock rationale: Test consuming a non-existent item, expecting a warning.
        inventory = {"existing_item": 5}
        result = update_inventory("non_existent", -2, inventory)
        self.assertFalse(result)
        self.assertNotIn("non_existent", inventory)
        mock_stderr.write.assert_called_with("Warning: Item 'non_existent' not found in inventory. Cannot consume.\n")

    @patch('sys.stderr')
    def test_update_inventory_insufficient_stock(self, mock_stderr):
        # Mock rationale: Test consuming more than available, expecting an error.
        inventory = {"item": 3}
        result = update_inventory("item", -5, inventory)
        self.assertFalse(result)
        self.assertEqual(inventory["item"], 3) # Should not change
        mock_stderr.write.assert_called_with("Error: Not enough 'item' in stock to consume 5. Current: 3\n")

    @patch('src.planner.load_json', side_effect=[{}, {}])
    @patch('sys.stdout')
    @patch('sys.argv', ['planner.py', 'check'])
    def test_main_check_empty_inventory(self, mock_stdout, mock_load_json):
        # Mock rationale: Simulate an empty provisions and inventory, expecting a 'stocked' message.
        main()
        mock_stdout.write.assert_called_with("All provisions are stocked! You are ready for anything.\n")

    @patch('src.planner.load_json', side_effect=[json.loads(json.dumps(self.mock_provisions_data)), json.loads(json.dumps(self.mock_inventory_data))])
    @patch('sys.stdout')
    @patch('sys.argv', ['planner.py', 'check'])
    def test_main_check_needs_items(self, mock_stdout, mock_load_json):
        # Mock rationale: Simulate provisions and inventory where items are needed, expecting a shopping list.
        main()
        expected_output = (
            "\n--- Shopping List ---\n"
            "- emergency glitter: 3 jars\n"
            "- canned beans: 4 cans\n"
            "- artisanal jerky: 2 packs\n"
            "---------------------\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('src.planner.load_json', side_effect=[json.loads(json.dumps(self.mock_provisions_data)), json.loads(json.dumps(self.mock_inventory_data))])
    @patch('src.planner.save_json')
    @patch('sys.stdout')
    @patch('sys.argv', ['planner.py', 'consume', 'emergency glitter', '2'])
    def test_main_consume_success(self, mock_stdout, mock_save_json, mock_load_json):
        # Mock rationale: Simulate consuming an item successfully.
        main()
        mock_save_json.assert_called_once()
        saved_inventory = mock_save_json.call_args[0][1]
        self.assertEqual(saved_inventory['emergency glitter'], 5) # 7 - 2 = 5
        mock_stdout.write.assert_called_with("Consumed 2 of 'emergency glitter'. Current stock: 5\n")

    @patch('src.planner.load_json', side_effect=[json.loads(json.dumps(self.mock_provisions_data)), json.loads(json.dumps(self.mock_inventory_data))])
    @patch('src.planner.save_json')
    @patch('sys.stdout')
    @patch('sys.argv', ['planner.py', 'add', 'new_item', '5'])
    def test_main_add_new_item_success(self, mock_stdout, mock_save_json, mock_load_json):
        # Mock rationale: Simulate adding a new item successfully.
        main()
        mock_save_json.assert_called_once()
        saved_inventory = mock_save_json.call_args[0][1]
        self.assertEqual(saved_inventory['new_item'], 5)
        mock_stdout.write.assert_called_with("Added 5 of 'new_item'. Current stock: 5\n")

    @patch('src.planner.load_json', side_effect=[json.loads(json.dumps(self.mock_provisions_data)), json.loads(json.dumps(self.mock_inventory_data))])
    @patch('src.planner.save_json')
    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('sys.argv', ['planner.py', 'consume', 'emergency glitter', 'invalid'])
    def test_main_consume_invalid_quantity(self, mock_exit, mock_stderr, mock_save_json, mock_load_json):
        # Mock rationale: Simulate invalid quantity input for consume command.
        main()
        mock_stderr.write.assert_called_with("Error: Quantity must be a positive integer.\n")
        mock_exit.assert_called_once_with(1)
        mock_save_json.assert_not_called()

    @patch('src.planner.load_json', side_effect=[json.loads(json.dumps(self.mock_provisions_data)), json.loads(json.dumps(self.mock_inventory_data))])
    @patch('src.planner.save_json')
    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('sys.argv', ['planner.py', 'consume', 'emergency glitter', '100'])
    def test_main_consume_insufficient_stock(self, mock_exit, mock_stderr, mock_save_json, mock_load_json):
        # Mock rationale: Simulate consuming more than available, expecting an error.
        main()
        mock_stderr.write.assert_called_with("Error: Not enough 'emergency glitter' in stock to consume 100. Current: 7\n")
        mock_save_json.assert_not_called() # Inventory should not be saved if consumption fails

    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('sys.argv', ['planner.py', 'unknown_command'])
    def test_main_unknown_command(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate an unknown command, expecting an error and exit.
        main()
        mock_stderr.write.assert_called_with("Unknown command: unknown_command\n")
        mock_exit.assert_called_once_with(1)

    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('sys.argv', ['planner.py'])
    def test_main_no_command(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate running without any command, expecting usage info and exit.
        main()
        mock_stderr.write.assert_any_call("Usage: python src/planner.py <command> [args...]\n")
        mock_stderr.write.assert_any_call("Commands: check, consume <item_name> <quantity>, add <item_name> <quantity>\n")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
