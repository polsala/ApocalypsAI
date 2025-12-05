import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Import the functions from the tracker script
# We need to adjust the import path for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker
sys.path.pop(0)

class TestTracker(unittest.TestCase):

    def setUp(self):
        # Ensure DATA_FILE points to a test-specific path or is mocked
        self.test_data_file = 'test_resources.json'
        tracker.DATA_FILE = self.test_data_file
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def tearDown(self):
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('json.load', return_value={})
    def test_load_resources_empty_file(self, mock_json_load, mock_file_open):
        # Mock rationale: We want to test loading from an empty or non-existent file without
        # actually creating/reading files. `mock_open` simulates file existence, and `json.load`
        # simulates the content.
        resources = tracker.load_resources()
        self.assertEqual(resources, {})
        mock_file_open.assert_called_once_with(self.test_data_file, 'r', encoding='utf-8')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='{"Water": 5}')
    @patch('json.load', return_value={"Water": 5})
    def test_load_resources_existing_file(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate loading existing data from a file.
        resources = tracker.load_resources()
        self.assertEqual(resources, {"Water": 5})
        mock_file_open.assert_called_once_with(self.test_data_file, 'r', encoding='utf-8')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_file_open):
        # Mock rationale: Test saving data without actual file writes.
        # `mock_open` captures the file handle, `json.dump` captures the data.
        test_data = {"Food": 10, "Tools": 2}
        tracker.save_resources(test_data)
        mock_file_open.assert_called_once_with(self.test_data_file, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(test_data, mock_file_open(), indent=4)

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={})
    @patch('builtins.print')
    def test_add_resource_new_item(self, mock_print, mock_load, mock_save):
        # Mock rationale: Isolate the `add_resource` logic. `load_resources` provides initial state,
        # `save_resources` confirms the new state is persisted, `print` captures output.
        tracker.add_resource("Medkit", 3)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"Medkit": 3})
        mock_print.assert_called_once_with("Added 3x Medkit. Total: 3x.")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Water": 5})
    @patch('builtins.print')
    def test_add_resource_existing_item(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test adding to an existing item.
        tracker.add_resource("Water", 2)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"Water": 7})
        mock_print.assert_called_once_with("Added 2x Water. Total: 7x.")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Food": 10})
    @patch('builtins.print')
    def test_remove_resource_partial(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test removing part of an item's quantity.
        tracker.remove_resource("Food", 3)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"Food": 7})
        mock_print.assert_called_once_with("Removed 3x Food. Remaining: 7x.")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Food": 5})
    @patch('builtins.print')
    def test_remove_resource_all(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test removing all of an item, leading to its deletion.
        tracker.remove_resource("Food", 5)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({})
        mock_print.assert_called_once_with("Used up all Food. It's gone, survivor!")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Food": 5})
    @patch('builtins.print')
    def test_remove_resource_more_than_available(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test attempting to remove more than available. Should remove all.
        tracker.remove_resource("Food", 10)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({})
        mock_print.assert_called_once_with("Used up all Food. It's gone, survivor!")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Water": 5})
    @patch('builtins.print')
    def test_remove_resource_non_existent(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test removing an item that isn't in inventory.
        tracker.remove_resource("Tools", 1)
        mock_load.assert_called_once()
        mock_save.assert_not_called() # Should not save if nothing changed
        mock_print.assert_called_once_with("Can't remove Tools. You don't seem to have any, survivor!")

    @patch('tracker.load_resources', return_value={"Water": 5, "Food": 10})
    @patch('builtins.print')
    def test_list_resources_populated(self, mock_print, mock_load):
        # Mock rationale: Test listing resources without actual file I/O.
        # `load_resources` provides the data, `print` captures the output.
        tracker.list_resources()
        mock_load.assert_called_once()
        expected_calls = [
            unittest.mock.call("\n--- Current Inventory ---"),
            unittest.mock.call("- Food: 10x"),
            unittest.mock.call("- Water: 5x"),
            unittest.mock.call("-------------------------\n")
        ]
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(mock_print.call_count, len(expected_calls))

    @patch('tracker.load_resources', return_value={})
    @patch('builtins.print')
    def test_list_resources_empty(self, mock_print, mock_load):
        # Mock rationale: Test listing when inventory is empty.
        tracker.list_resources()
        mock_load.assert_called_once()
        mock_print.assert_called_once_with("Your inventory is empty, survivor. Time to scavenge!")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={})
    @patch('builtins.print')
    def test_add_resource_zero_quantity(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test adding with zero quantity.
        tracker.add_resource("Medkit", 0)
        mock_load.assert_not_called()
        mock_save.assert_not_called()
        mock_print.assert_called_once_with("Quantity must be a positive number, survivor!")

    @patch('tracker.save_resources')
    @patch('tracker.load_resources', return_value={"Food": 10})
    @patch('builtins.print')
    def test_remove_resource_zero_quantity(self, mock_print, mock_load, mock_save):
        # Mock rationale: Test removing with zero quantity.
        tracker.remove_resource("Food", 0)
        mock_load.assert_not_called()
        mock_save.assert_not_called()
        mock_print.assert_called_once_with("Quantity to remove must be a positive number, survivor!")

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('builtins.print')
    def test_load_resources_invalid_json(self, mock_print, mock_file_open):
        # Mock rationale: Simulate a corrupted data file.
        resources = tracker.load_resources()
        self.assertEqual(resources, {})
        mock_print.assert_called_once_with(f"Warning: Could not decode {self.test_data_file}. Starting with empty inventory.")

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('builtins.print')
    def test_load_resources_io_error(self, mock_print, mock_file_open):
        # Mock rationale: Simulate a file permission error during loading.
        resources = tracker.load_resources()
        self.assertEqual(resources, {})
        mock_print.assert_called_once_with(f"Error loading resources: Permission denied. Starting with empty inventory.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump', side_effect=IOError("Disk full"))
    @patch('builtins.print')
    def test_save_resources_io_error(self, mock_print, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate a file permission error during saving.
        test_data = {"Food": 10}
        tracker.save_resources(test_data)
        mock_print.assert_called_once_with(f"Error saving resources: Disk full")

if __name__ == '__main__':
    unittest.main()
