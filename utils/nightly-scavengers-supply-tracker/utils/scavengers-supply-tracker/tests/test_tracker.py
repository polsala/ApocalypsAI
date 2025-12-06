import unittest
from unittest.mock import patch, mock_open
import json
import os
from io import StringIO

# Adjust sys.path to allow importing tracker.py from the src directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import load_data, save_data, add_supply, list_supplies, remove_supply, _get_data_path, DATA_FILE

class TestScavengersSupplyTracker(unittest.TestCase):

    def setUp(self):
        # Mock the data file path to ensure tests don't interfere with real files
        # Mock rationale: Prevent actual file system interaction during tests.
        # This ensures tests are deterministic and don't leave artifacts.
        self.mock_data_path = "/mock/path/supplies.json"
        patcher = patch('tracker._get_data_path', return_value=self.mock_data_path)
        self.mock_get_data_path = patcher.start()
        self.addCleanup(patcher.stop)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_data_empty_file(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a non-existent data file.
        mock_os_exists.return_value = False
        data = load_data()
        self.assertEqual(data, {"locations": {}})
        mock_os_exists.assert_called_once_with(self.mock_data_path)
        mock_file_open.assert_not_called()
        mock_json_load.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_data_existing_file(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing data file with content.
        mock_os_exists.return_value = True
        mock_json_load.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        data = load_data()
        self.assertEqual(data, {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}})
        mock_os_exists.assert_called_once_with(self.mock_data_path)
        mock_file_open.assert_called_once_with(self.mock_data_path, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_load_data_corrupted_file(self, mock_print, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_os_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        data = load_data()
        self.assertEqual(data, {"locations": {}})
        mock_print.assert_called_once_with(f"Warning: {DATA_FILE} is corrupted. Starting with empty data.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_data(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate saving data to a file.
        test_data = {"locations": {"Zone B": [{"item": "Food", "quantity": 5}]}}
        save_data(test_data)
        mock_file_open.assert_called_once_with(self.mock_data_path, 'w')
        mock_json_dump.assert_called_once_with(test_data, mock_file_open(), indent=4)

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_add_supply_new_location_item(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate adding a new item to a new location.
        mock_load_data.return_value = {"locations": {}}
        add_supply("Zone C", "Medkit", 2)
        expected_data = {"locations": {"Zone C": [{"item": "Medkit", "quantity": 2}]}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Added 2x Medkit to Zone C.")

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_add_supply_existing_location_new_item(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate adding a new item to an existing location.
        mock_load_data.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        add_supply("Zone A", "Food", 5)
        expected_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}, {"item": "Food", "quantity": 5}]}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Added 5x Food to Zone A.")

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_add_supply_existing_location_existing_item(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate adding to an existing item's quantity.
        mock_load_data.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        add_supply("Zone A", "Water", 3)
        expected_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 13}]}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Added 3x Water to Zone A.")

    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_list_supplies_empty(self, mock_print, mock_load_data):
        # Mock rationale: Simulate an empty data set for listing.
        mock_load_data.return_value = {"locations": {}}
        list_supplies()
        mock_print.assert_called_once_with("No supplies tracked yet. Go scavenge!")

    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_list_supplies_all(self, mock_print, mock_load_data):
        # Mock rationale: Simulate a populated data set for listing all supplies.
        mock_load_data.return_value = {
            "locations": {
                "Zone B": [{"item": "Food", "quantity": 5}],
                "Zone A": [{"item": "Water", "quantity": 10}, {"item": "Batteries", "quantity": 2}]
            }
        }
        list_supplies()
        expected_calls = [
            unittest.mock.call("\n--- Zone A ---"),
            unittest.mock.call("  - Batteries: 2"),
            unittest.mock.call("  - Water: 10"),
            unittest.mock.call("\n--- Zone B ---"),
            unittest.mock.call("  - Food: 5")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_print.call_count, 5) # 2 headers + 3 items

    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_list_supplies_specific_location(self, mock_print, mock_load_data):
        # Mock rationale: Simulate listing supplies for a specific location.
        mock_load_data.return_value = {
            "locations": {
                "Zone B": [{"item": "Food", "quantity": 5}],
                "Zone A": [{"item": "Water", "quantity": 10}, {"item": "Batteries", "quantity": 2}]
            }
        }
        list_supplies("Zone A")
        expected_calls = [
            unittest.mock.call("\n--- Zone A ---"),
            unittest.mock.call("  - Batteries: 2"),
            unittest.mock.call("  - Water: 10")
        ]
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(mock_print.call_count, 3)

    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_list_supplies_non_existent_location(self, mock_print, mock_load_data):
        # Mock rationale: Simulate listing supplies for a non-existent location.
        mock_load_data.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        list_supplies("Zone X")
        mock_print.assert_called_once_with("Location 'Zone X' not found.")

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_remove_supply_all(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate removing all of a specific item.
        initial_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}, {"item": "Food", "quantity": 5}]}}
        mock_load_data.return_value = initial_data.copy()
        remove_supply("Zone A", "Water")
        expected_data = {"locations": {"Zone A": [{"item": "Food", "quantity": 5}]}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Removed all 10x Water from Zone A.")

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_remove_supply_partial(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate removing a partial quantity of an item.
        initial_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        mock_load_data.return_value = initial_data.copy()
        remove_supply("Zone A", "Water", 3)
        expected_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 7}]}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Removed 3x Water from Zone A. Remaining: 7x.")

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_remove_supply_non_existent_location(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate attempting to remove from a non-existent location.
        mock_load_data.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        remove_supply("Zone X", "Water")
        mock_print.assert_called_once_with("Location 'Zone X' not found.")
        mock_save_data.assert_not_called()

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_remove_supply_non_existent_item(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate attempting to remove a non-existent item.
        mock_load_data.return_value = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        remove_supply("Zone A", "Food")
        mock_print.assert_called_once_with("Item 'Food' not found in 'Zone A'.")
        mock_save_data.assert_not_called()

    @patch('tracker.save_data')
    @patch('tracker.load_data')
    @patch('builtins.print')
    def test_remove_supply_cleans_empty_location(self, mock_print, mock_load_data, mock_save_data):
        # Mock rationale: Simulate removing the last item from a location, which should then remove the location itself.
        initial_data = {"locations": {"Zone A": [{"item": "Water", "quantity": 10}]}}
        mock_load_data.return_value = initial_data.copy()
        remove_supply("Zone A", "Water")
        expected_data = {"locations": {}}
        mock_save_data.assert_called_once_with(expected_data)
        mock_print.assert_called_once_with("Removed all 10x Water from Zone A.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py', 'add', 'Old Supermarket', 'Canned Beans', '5'])
    @patch('tracker.add_supply')
    def test_main_add_command(self, mock_add_supply, mock_stdout):
        # Mock rationale: Simulate command-line arguments for the 'add' command.
        # Also mock stdout to capture print output if needed, and mock add_supply to isolate main logic.
        from tracker import main
        main()
        mock_add_supply.assert_called_once_with("Old Supermarket", "Canned Beans", 5)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py', 'list', '--location', 'Old Supermarket'])
    @patch('tracker.list_supplies')
    def test_main_list_command_with_location(self, mock_list_supplies, mock_stdout):
        # Mock rationale: Simulate command-line arguments for the 'list' command with a location.
        from tracker import main
        main()
        mock_list_supplies.assert_called_once_with("Old Supermarket")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py', 'remove', 'Old Supermarket', 'Canned Beans', '--quantity', '2'])
    @patch('tracker.remove_supply')
    def test_main_remove_command_with_quantity(self, mock_remove_supply, mock_stdout):
        # Mock rationale: Simulate command-line arguments for the 'remove' command with a quantity.
        from tracker import main
        main()
        mock_remove_supply.assert_called_once_with("Old Supermarket", "Canned Beans", 2)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py', 'add', 'Location', 'Item', '0'])
    @patch('builtins.print')
    def test_main_add_invalid_quantity(self, mock_print, mock_stdout):
        # Mock rationale: Test input validation for add command.
        from tracker import main
        main()
        mock_print.assert_called_once_with("Quantity must be a positive integer.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py', 'remove', 'Location', 'Item', '--quantity', '-1'])
    @patch('builtins.print')
    def test_main_remove_invalid_quantity(self, mock_print, mock_stdout):
        # Mock rationale: Test input validation for remove command.
        from tracker import main
        main()
        mock_print.assert_called_once_with("Quantity to remove must be a positive integer.")


if __name__ == '__main__':
    unittest.main()
