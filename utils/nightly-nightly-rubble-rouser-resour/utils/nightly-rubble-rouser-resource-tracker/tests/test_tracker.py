import unittest
from unittest.mock import patch, mock_open
import json
import os
import io

# Mock rationale: We mock file I/O operations (open, json.load, json.dump, os.path.exists)
# to ensure tests are deterministic and do not interact with the actual filesystem.
# This allows us to control the initial state of the resource data and verify
# how the utility modifies it, without creating temporary files or relying on
# external state. We also mock sys.stdout to capture printed output for verification.

class TestTracker(unittest.TestCase):

    def setUp(self):
        self.initial_resources = {
            "canned beans": {"quantity": 10, "category": "food"},
            "scrap metal": {"quantity": 25, "category": "materials"},
            "purified water": {"quantity": 5, "category": "hydration"}
        }
        self.empty_resources = {}

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_existing_file(self, mock_json_load, mock_file_open, mock_exists):
        mock_exists.return_value = True
        mock_json_load.return_value = self.initial_resources

        resources = self.tracker.load_resources()
        self.assertEqual(resources, self.initial_resources)
        mock_exists.assert_called_once_with(self.tracker.DATA_FILE)
        mock_file_open.assert_called_once_with(self.tracker.DATA_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_resources_no_file(self, mock_exists):
        mock_exists.return_value = False

        resources = self.tracker.load_resources()
        self.assertEqual(resources, {})
        mock_exists.assert_called_once_with(self.tracker.DATA_FILE)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print') # Mock print to avoid actual output
    def test_load_resources_corrupted_json(self, mock_print, mock_json_load, mock_file_open, mock_exists):
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        resources = self.tracker.load_resources()
        self.assertEqual(resources, {})
        mock_print.assert_called_once_with(f"Warning: {self.tracker.DATA_FILE} is corrupted. Starting with an empty inventory.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_file_open):
        resources_to_save = {"new item": {"quantity": 1, "category": "test"}}
        self.tracker.save_resources(resources_to_save)
        mock_file_open.assert_called_once_with(self.tracker.DATA_FILE, 'w')
        mock_json_dump.assert_called_once_with(resources_to_save, mock_file_open(), indent=4)

    @patch('builtins.print')
    def test_add_item_new(self, mock_print):
        resources = self.empty_resources.copy()
        self.assertTrue(self.tracker.add_item(resources, "medkit", 2, "medicine"))
        self.assertEqual(resources["medkit"], {"quantity": 2, "category": "medicine"})
        mock_print.assert_called_once_with("Added 2 of 'medkit' (Category: Medicine). Total: 2")

    @patch('builtins.print')
    def test_add_item_existing(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertTrue(self.tracker.add_item(resources, "canned beans", 5, "food"))
        self.assertEqual(resources["canned beans"], {"quantity": 15, "category": "food"})
        mock_print.assert_called_once_with("Added 5 of 'canned beans' (Category: Food). Total: 15")

    @patch('builtins.print')
    def test_add_item_existing_different_category(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertTrue(self.tracker.add_item(resources, "canned beans", 5, "survival"))
        # Category should not change
        self.assertEqual(resources["canned beans"], {"quantity": 15, "category": "food"})
        mock_print.assert_any_call("Warning: Item 'canned beans' already exists with category 'food'. Keeping existing category.")
        mock_print.assert_any_call("Added 5 of 'canned beans' (Category: Food). Total: 15")

    @patch('builtins.print')
    def test_add_item_invalid_quantity(self, mock_print):
        resources = self.empty_resources.copy()
        self.assertFalse(self.tracker.add_item(resources, "ammo", 0, "weapons"))
        self.assertFalse(self.tracker.add_item(resources, "ammo", -1, "weapons"))
        self.assertFalse(self.tracker.add_item(resources, "ammo", "two", "weapons"))
        self.assertEqual(resources, {})
        mock_print.assert_called_with("Error: Quantity must be a positive integer.")

    @patch('builtins.print')
    def test_remove_item_partial(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertTrue(self.tracker.remove_item(resources, "canned beans", 3))
        self.assertEqual(resources["canned beans"], {"quantity": 7, "category": "food"})
        mock_print.assert_called_once_with("Removed 3 of 'canned beans'. Remaining: 7")

    @patch('builtins.print')
    def test_remove_item_all(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertTrue(self.tracker.remove_item(resources, "purified water", 5))
        self.assertNotIn("purified water", resources)
        mock_print.assert_called_once_with("Removed all 5 of 'purified water'. Item depleted.")

    @patch('builtins.print')
    def test_remove_item_more_than_available(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertTrue(self.tracker.remove_item(resources, "scrap metal", 30))
        self.assertNotIn("scrap metal", resources)
        mock_print.assert_called_once_with("Removed all 25 of 'scrap metal'. Item depleted.")

    @patch('builtins.print')
    def test_remove_item_not_found(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertFalse(self.tracker.remove_item(resources, "nonexistent item", 1))
        self.assertEqual(resources, self.initial_resources)
        mock_print.assert_called_once_with("Error: Item 'nonexistent item' not found in inventory.")

    @patch('builtins.print')
    def test_remove_item_invalid_quantity(self, mock_print):
        resources = self.initial_resources.copy()
        self.assertFalse(self.tracker.remove_item(resources, "canned beans", 0))
        self.assertFalse(self.tracker.remove_item(resources, "canned beans", -1))
        self.assertFalse(self.tracker.remove_item(resources, "canned beans", "one"))
        self.assertEqual(resources, self.initial_resources)
        mock_print.assert_called_with("Error: Quantity must be a positive integer.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_items_all(self, mock_stdout):
        self.tracker.list_items(self.initial_resources)
        output = mock_stdout.getvalue()
        self.assertIn("--- Current Inventory ---", output)
        self.assertIn("  - Canned Beans: 10 (Category: Food)", output)
        self.assertIn("  - Purified Water: 5 (Category: Hydration)", output)
        self.assertIn("  - Scrap Metal: 25 (Category: Materials)", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_items_filtered(self, mock_stdout):
        self.tracker.list_items(self.initial_resources, "food")
        output = mock_stdout.getvalue()
        self.assertIn("  - Canned Beans: 10 (Category: Food)", output)
        self.assertNotIn("Purified Water", output)
        self.assertNotIn("Scrap Metal", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_items_empty_inventory(self, mock_stdout):
        self.tracker.list_items(self.empty_resources)
        output = mock_stdout.getvalue()
        self.assertIn("Your inventory is currently empty. Time to scavenge!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_items_no_category_found(self, mock_stdout):
        self.tracker.list_items(self.initial_resources, "weapons")
        output = mock_stdout.getvalue()
        self.assertIn("No items found in category 'weapons'.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_summary(self, mock_stdout):
        self.tracker.get_summary(self.initial_resources)
        output = mock_stdout.getvalue()
        self.assertIn("--- Inventory Summary by Category ---", output)
        self.assertIn("  - Food: 10 items", output)
        self.assertIn("  - Hydration: 5 items", output)
        self.assertIn("  - Materials: 25 items", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_summary_empty_inventory(self, mock_stdout):
        self.tracker.get_summary(self.empty_resources)
        output = mock_stdout.getvalue()
        self.assertIn("Your inventory is empty. No summary to provide.", output)

    # Mock the tracker module itself to ensure tests run against the correct functions
    @classmethod
    def setUpClass(cls):
        import sys
        from importlib import util
        # Create a spec for the module
        spec = util.spec_from_file_location("tracker", "utils/nightly-rubble-rouser-resource-tracker/src/tracker.py")
        cls.tracker = util.module_from_spec(spec)
        sys.modules["tracker"] = cls.tracker
        spec.loader.exec_module(cls.tracker)

    @classmethod
    def tearDownClass(cls):
        import sys
        del sys.modules["tracker"]

if __name__ == '__main__':
    unittest.main()
