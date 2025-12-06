import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Add the src directory to sys.path to allow importing ledger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ledger import load_ledger, save_ledger, add_item, update_item, remove_item, list_items, LEDGER_FILE, main

class TestScavengerLedger(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()
        # Capture stderr for testing print statements
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_ledger_existing_file(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing ledger file with content.
        mock_exists.return_value = True
        mock_json_load.return_value = {"water": {"qty": 5, "condition": "clean", "notes": ""}}
        
        ledger = load_ledger("test_file.json")
        self.assertEqual(ledger, {"water": {"qty": 5, "condition": "clean", "notes": ""}})
        mock_exists.assert_called_once_with("test_file.json")
        mock_open_file.assert_called_once_with("test_file.json", 'r')
        mock_json_load.assert_called_once_with(mock_open_file())

    @patch('os.path.exists')
    def test_load_ledger_non_existing_file(self, mock_exists):
        # Mock rationale: Simulate no ledger file existing.
        mock_exists.return_value = False
        
        ledger = load_ledger("test_file.json")
        self.assertEqual(ledger, {})
        mock_exists.assert_called_once_with("test_file.json")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_ledger_corrupted_file(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        ledger = load_ledger("test_file.json")
        self.assertEqual(ledger, {})
        mock_exists.assert_called_once_with("test_file.json")
        mock_open_file.assert_called_once_with("test_file.json", 'r')
        mock_json_load.assert_called_once_with(mock_open_file())
        self.assertIn("Warning: Ledger file 'test_file.json' is corrupted.", self.mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_ledger(self, mock_json_dump, mock_open_file):
        # Mock rationale: Simulate saving ledger data to a file.
        test_ledger = {"food": {"qty": 10, "condition": "canned", "notes": ""}}
        save_ledger(test_ledger, "test_file.json")
        mock_open_file.assert_called_once_with("test_file.json", 'w')
        mock_json_dump.assert_called_once_with(test_ledger, mock_open_file(), indent=4)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump', side_effect=IOError("Disk full"))
    def test_save_ledger_error(self, mock_json_dump, mock_open_file):
        # Mock rationale: Simulate an error during saving the ledger.
        test_ledger = {"food": {"qty": 10, "condition": "canned", "notes": ""}}
        save_ledger(test_ledger, "test_file.json")
        self.assertIn("Error saving ledger to 'test_file.json': Disk full", self.mock_stderr.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={})
    def test_add_item_new(self, mock_load, mock_save):
        # Mock rationale: Simulate adding a new item to an empty ledger.
        result = add_item("medkit", 2, "new", "first aid", "test_file.json")
        self.assertTrue(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_called_once_with(
            {"medkit": {"qty": 2, "condition": "new", "notes": "first aid"}},
            "test_file.json"
        )
        self.assertIn("Added 'medkit' to the ledger.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={
        "water": {"qty": 5, "condition": "clean", "notes": ""}
    })
    def test_add_item_existing(self, mock_load, mock_save):
        # Mock rationale: Simulate attempting to add an item that already exists.
        result = add_item("water", 10, "dirty", "found in puddle", "test_file.json")
        self.assertFalse(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_not_called()
        self.assertIn("Warning: Item 'water' already exists. Use 'update' to modify it.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={
        "water": {"qty": 5, "condition": "clean", "notes": ""}
    })
    def test_update_item_existing(self, mock_load, mock_save):
        # Mock rationale: Simulate updating an existing item's details.
        result = update_item("water", 10, "filtered", "from rain collector", "test_file.json")
        self.assertTrue(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_called_once_with(
            {"water": {"qty": 10, "condition": "filtered", "notes": "from rain collector"}},
            "test_file.json"
        )
        self.assertIn("Updated 'water' in the ledger.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={
        "water": {"qty": 5, "condition": "clean", "notes": ""}
    })
    def test_update_item_partial(self, mock_load, mock_save):
        # Mock rationale: Simulate updating only a subset of an item's details.
        result = update_item("water", qty=None, condition="stale", notes=None, file_path="test_file.json")
        self.assertTrue(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_called_once_with(
            {"water": {"qty": 5, "condition": "stale", "notes": ""}},
            "test_file.json"
        )
        self.assertIn("Updated 'water' in the ledger.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={})
    def test_update_item_non_existing(self, mock_load, mock_save):
        # Mock rationale: Simulate attempting to update a non-existent item.
        result = update_item("medkit", 1, "used", "", "test_file.json")
        self.assertFalse(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_not_called()
        self.assertIn("Error: Item 'medkit' not found. Use 'add' to create it.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={
        "water": {"qty": 5, "condition": "clean", "notes": ""}
    })
    def test_remove_item_existing(self, mock_load, mock_save):
        # Mock rationale: Simulate removing an existing item.
        result = remove_item("water", "test_file.json")
        self.assertTrue(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_called_once_with({}, "test_file.json")
        self.assertIn("Removed 'water' from the ledger.", self.mock_stdout.getvalue())

    @patch('ledger.save_ledger')
    @patch('ledger.load_ledger', return_value={})
    def test_remove_item_non_existing(self, mock_load, mock_save):
        # Mock rationale: Simulate attempting to remove a non-existent item.
        result = remove_item("medkit", "test_file.json")
        self.assertFalse(result)
        mock_load.assert_called_once_with("test_file.json")
        mock_save.assert_not_called()
        self.assertIn("Error: Item 'medkit' not found.", self.mock_stdout.getvalue())

    @patch('ledger.load_ledger', return_value={})
    def test_list_items_empty(self, mock_load):
        # Mock rationale: Simulate listing items when the ledger is empty.
        list_items("test_file.json")
        mock_load.assert_called_once_with("test_file.json")
        self.assertIn("The scavenger's ledger is empty. Time to scavenge!", self.mock_stdout.getvalue())

    @patch('ledger.load_ledger', return_value={
        "water": {"qty": 5, "condition": "clean", "notes": "from rain collector"},
        "canned beans": {"qty": 12, "condition": "sealed", "notes": "expiration 2050"}
    })
    def test_list_items_populated(self, mock_load):
        # Mock rationale: Simulate listing items from a populated ledger.
        list_items("test_file.json")
        mock_load.assert_called_once_with("test_file.json")
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Scavenger's Supply Ledger ---", output)
        self.assertIn("Item: water", output)
        self.assertIn("Qty: 5", output)
        self.assertIn("Condition: clean", output)
        self.assertIn("Notes: from rain collector", output)
        self.assertIn("Item: canned beans", output)
        self.assertIn("Qty: 12", output)
        self.assertIn("Condition: sealed", output)
        self.assertIn("Notes: expiration 2050", output)

    @patch('sys.argv', ['ledger.py', 'add', 'flashlight', '--qty', '1', '--condition', 'broken', '--notes', 'needs batteries', '--ledger-file', 'custom.json'])
    @patch('ledger.add_item')
    def test_main_add_command(self, mock_add_item):
        # Mock rationale: Simulate running the script via CLI for 'add' command with custom ledger file.
        main()
        mock_add_item.assert_called_once_with('flashlight', 1, 'broken', 'needs batteries', 'custom.json')

    @patch('sys.argv', ['ledger.py', 'update', 'flashlight', '--qty', '2', '--ledger-file', 'custom.json'])
    @patch('ledger.update_item')
    def test_main_update_command(self, mock_update_item):
        # Mock rationale: Simulate running the script via CLI for 'update' command with custom ledger file.
        main()
        mock_update_item.assert_called_once_with('flashlight', 2, None, None, 'custom.json')

    @patch('sys.argv', ['ledger.py', 'remove', 'flashlight', '--ledger-file', 'custom.json'])
    @patch('ledger.remove_item')
    def test_main_remove_command(self, mock_remove_item):
        # Mock rationale: Simulate running the script via CLI for 'remove' command with custom ledger file.
        main()
        mock_remove_item.assert_called_once_with('flashlight', 'custom.json')

    @patch('sys.argv', ['ledger.py', 'list', '--ledger-file', 'custom.json'])
    @patch('ledger.list_items')
    def test_main_list_command(self, mock_list_items):
        # Mock rationale: Simulate running the script via CLI for 'list' command with custom ledger file.
        main()
        mock_list_items.assert_called_once_with('custom.json')

    @patch('sys.argv', ['ledger.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        # Mock rationale: Simulate running the script with no command, expecting help message.
        main()
        mock_print_help.assert_called_once()


if __name__ == '__main__':
    unittest.main()
