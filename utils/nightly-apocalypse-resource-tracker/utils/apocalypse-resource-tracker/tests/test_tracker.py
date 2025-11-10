import unittest
import json
import os
from unittest.mock import patch, mock_open

# Mock rationale: We need to test file I/O operations (_load, _save) without actually touching the filesystem.
# `mock_open` allows us to simulate file reading and writing, and `patch('os.path.exists')` lets us control
# whether the 'inventory.json' file is considered present or not. This ensures tests are deterministic and offline.

from src.tracker import ResourceTracker

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure each test starts with a clean slate for the tracker instance
        self.test_inventory_file = 'test_inventory.json'
        # Reset the tracker instance for each test by re-initializing it
        # We'll mock file operations for the actual tests.
        self.tracker = ResourceTracker(self.test_inventory_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_empty_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty or non-existent inventory file.
        mock_exists.return_value = False
        tracker = ResourceTracker(self.test_inventory_file)
        self.assertEqual(tracker.inventory, {})
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = '{}'
        tracker = ResourceTracker(self.test_inventory_file)
        self.assertEqual(tracker.inventory, {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_existing_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing inventory file with content.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = json.dumps({"water": 10, "food": 5})
        tracker = ResourceTracker(self.test_inventory_file)
        self.assertEqual(tracker.inventory, {"water": 10, "food": 5})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corrupted_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file to test error handling.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = 'invalid json'
        with patch('builtins.print') as mock_print:
            tracker = ResourceTracker(self.test_inventory_file)
            self.assertEqual(tracker.inventory, {})
            mock_print.assert_called_with(f"Warning: Inventory file '{self.test_inventory_file}' is corrupted. Starting with empty inventory.")

    @patch('builtins.open', new_callable=mock_open)
    def test_save_file(self, mock_file_open):
        # Mock rationale: Simulate saving inventory to a file and verify content.
        tracker = ResourceTracker(self.test_inventory_file)
        tracker.inventory = {"medkit": 2}
        tracker._save()
        mock_file_open.assert_called_once_with(self.test_inventory_file, 'w')
        mock_file_open.return_value.write.assert_called_once_with(json.dumps({"medkit": 2}, indent=4))

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_add_resource_new_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the add_resource logic from file I/O and console output.
        self.tracker.add_resource("Canned Food", 5)
        self.assertEqual(self.tracker.inventory, {"canned food": 5})
        mock_save.assert_called_once()
        mock_print.assert_called_with("Added 5 of 'canned food'. Current total: 5")

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_add_resource_existing_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the add_resource logic from file I/O and console output.
        self.tracker.inventory = {"water": 10}
        self.tracker.add_resource("Water", 3)
        self.assertEqual(self.tracker.inventory, {"water": 13})
        mock_save.assert_called_once()
        mock_print.assert_called_with("Added 3 of 'water'. Current total: 13")

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_add_resource_invalid_quantity(self, mock_print, mock_save):
        # Mock rationale: Test input validation without side effects.
        with self.assertRaises(ValueError):
            self.tracker.add_resource("Ammo", -1)
        mock_save.assert_not_called()

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_add_resource_invalid_name(self, mock_print, mock_save):
        # Mock rationale: Test input validation without side effects.
        with self.assertRaises(ValueError):
            self.tracker.add_resource("", 5)
        with self.assertRaises(ValueError):
            self.tracker.add_resource("   ", 5)
        mock_save.assert_not_called()

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_update_quantity_existing_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the update_quantity logic from file I/O and console output.
        self.tracker.inventory = {"medkit": 2}
        self.tracker.update_quantity("Medkit", 5)
        self.assertEqual(self.tracker.inventory, {"medkit": 5})
        mock_save.assert_called_once()
        mock_print.assert_called_with("Updated 'medkit' to 5.")

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_update_quantity_non_existent_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the update_quantity logic from file I/O and console output.
        self.tracker.update_quantity("Rope", 10)
        self.assertEqual(self.tracker.inventory, {})
        mock_save.assert_not_called()
        mock_print.assert_called_with("Resource 'rope' not found. Use 'add' to create it.")

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_update_quantity_invalid_quantity(self, mock_print, mock_save):
        # Mock rationale: Test input validation without side effects.
        self.tracker.inventory = {"fuel": 10}
        with self.assertRaises(ValueError):
            self.tracker.update_quantity("Fuel", -5)
        self.assertEqual(self.tracker.inventory, {"fuel": 10}) # Should not change
        mock_save.assert_not_called()

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_remove_resource_existing_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O and console output.
        self.tracker.inventory = {"bullets": 50, "bandages": 10}
        self.tracker.remove_resource("Bullets")
        self.assertEqual(self.tracker.inventory, {"bandages": 10})
        mock_save.assert_called_once()
        mock_print.assert_called_with("Removed 'bullets' from inventory.")

    @patch('src.tracker.ResourceTracker._save')
    @patch('builtins.print')
    def test_remove_resource_non_existent_item(self, mock_print, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O and console output.
        self.tracker.inventory = {"water": 10}
        self.tracker.remove_resource("Gasoline")
        self.assertEqual(self.tracker.inventory, {"water": 10})
        mock_save.assert_not_called()
        mock_print.assert_called_with("Resource 'gasoline' not found in inventory.")

    def test_get_inventory(self):
        self.tracker.inventory = {"scrap metal": 100}
        inventory_copy = self.tracker.get_inventory()
        self.assertEqual(inventory_copy, {"scrap metal": 100})
        # Ensure it's a copy, not the original reference
        inventory_copy["scrap metal"] = 50
        self.assertEqual(self.tracker.inventory, {"scrap metal": 100})

    @patch('builtins.print')
    def test_display_inventory_empty(self, mock_print):
        # Mock rationale: Capture print output to verify display logic.
        self.tracker.inventory = {}
        self.tracker.display_inventory()
        mock_print.assert_called_with("Your inventory is empty. Time to scavenge!")

    @patch('builtins.print')
    def test_display_inventory_with_items(self, mock_print):
        # Mock rationale: Capture print output to verify display logic.
        self.tracker.inventory = {"water": 10, "canned food": 5}
        self.tracker.display_inventory()
        expected_calls = [
            unittest.mock.call("\n--- Current Inventory ---"),
            unittest.mock.call("  - Canned Food: 5"),
            unittest.mock.call("  - Water: 10"),
            unittest.mock.call("-------------------------")
        ]
        # Using assert_has_calls with any_order=True for robustness against minor print order changes
        # or if internal sorting changes, though current implementation sorts.
        mock_print.assert_has_calls(expected_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()
