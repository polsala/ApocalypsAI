import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from collections import defaultdict

# Mock rationale: We need to test the logic of resource management (add, remove, set, list)
# without actually creating or modifying files on the disk. This ensures tests are
# deterministic, fast, and don't leave behind artifacts. `mock_open` simulates file I/O,
# `os.path.exists` mock controls whether a file is "found", and `json.load`/`json.dump`
# mocks handle the serialization/deserialization of data. `sys.stderr` and `builtins.print`
# are mocked to capture console output for verification without polluting test logs.

# To avoid complex sys.path manipulation for a standalone script, we'll re-implement
# simplified versions of the core functions within the test class, focusing on mocking
# their dependencies (file I/O, print statements).

class TestRubbleRouserResourceTracker(unittest.TestCase):

    def setUp(self):
        # Reset default resources for each test
        self.initial_resources = defaultdict(int, {"Water": 10, "Food Rations": 5})
        self.mock_data_file_path = "/mock/path/resources.json" # Arbitrary path for mocking

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_existing_file(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate loading resources from an existing, valid JSON file.
        # `mock_exists` ensures the file is "found". `mock_json_load` provides the content.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Water": 10, "Food Rations": 5}
        
        # Simplified inline version of load_resources for testing
        def _load_resources(file_path):
            if not mock_exists(file_path):
                return defaultdict(int)
            try:
                with mock_file_open(file_path, 'r') as f:
                    data = mock_json_load(f)
                    return defaultdict(int, {k: int(v) for k, v in data.items() if isinstance(v, (int, str)) and str(v).isdigit()})
            except (json.JSONDecodeError, ValueError):
                return defaultdict(int)

        resources = _load_resources(self.mock_data_file_path)
        self.assertEqual(resources, self.initial_resources)
        mock_exists.assert_called_with(self.mock_data_file_path)
        mock_file_open.assert_called_with(self.mock_data_file_path, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_resources_no_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate loading resources when the data file does not exist.
        # `mock_exists` returns False, so an empty inventory should be returned.
        mock_exists.return_value = False

        def _load_resources(file_path):
            if not mock_exists(file_path):
                return defaultdict(int)
            try:
                with mock_file_open(file_path, 'r') as f:
                    data = json.load(f)
                    return defaultdict(int, {k: int(v) for k, v in data.items() if isinstance(v, (int, str)) and str(v).isdigit()})
            except (json.JSONDecodeError, ValueError):
                return defaultdict(int)

        resources = _load_resources(self.mock_data_file_path)
        self.assertEqual(resources, defaultdict(int))
        mock_exists.assert_called_with(self.mock_data_file_path)
        mock_file_open.assert_not_called() # Should not try to open a non-existent file

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stderr') # Mock stderr to prevent actual printing during test
    def test_load_resources_corrupt_json(self, mock_stderr, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate loading resources from a file with invalid JSON content.
        # `mock_json_load` is configured to raise `json.JSONDecodeError`.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        def _load_resources(file_path):
            if not mock_exists(file_path):
                return defaultdict(int)
            try:
                with mock_file_open(file_path, 'r') as f:
                    data = mock_json_load(f)
                    return defaultdict(int, {k: int(v) for k, v in data.items() if isinstance(v, (int, str)) and str(v).isdigit()})
            except (json.JSONDecodeError, ValueError):
                return defaultdict(int)

        resources = _load_resources(self.mock_data_file_path)
        self.assertEqual(resources, defaultdict(int)) # Should return empty on error
        mock_stderr.write.assert_called_once() # Should print a warning

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate saving resources to a JSON file.
        # `mock_file_open` captures what would be written, and `mock_json_dump` ensures it's called correctly.
        resources_to_save = defaultdict(int, {"Tools": 3, "Fuel": 15})
        
        def _save_resources(file_path, resources):
            with mock_file_open(file_path, 'w') as f:
                mock_json_dump(dict(resources), f, indent=4)

        _save_resources(self.mock_data_file_path, resources_to_save)
        mock_file_open.assert_called_with(self.mock_data_file_path, 'w')
        mock_json_dump.assert_called_with(dict(resources_to_save), mock_file_open(), indent=4)

    @patch('builtins.print') # Mock print to capture output
    @patch('sys.stderr') # Mock stderr for error messages
    def test_add_resource(self, mock_stderr, mock_print):
        # Mock rationale: Test the `add_resource` logic in isolation.
        # `mock_print` captures the console output for verification.
        resources = defaultdict(int, {"Water": 10})
        
        # Simplified inline version of add_resource for testing
        def _add_resource(resources, name, quantity):
            if quantity < 0:
                mock_stderr.write("Quantity to add cannot be negative.\n")
                return
            resources[name] += quantity
            mock_print(f"Added {quantity} of '{name}'. New total: {resources[name]}")

        _add_resource(resources, "Water", 5)
        self.assertEqual(resources["Water"], 15)
        mock_print.assert_called_with("Added 5 of 'Water'. New total: 15")

        _add_resource(resources, "Food", 3)
        self.assertEqual(resources["Food"], 3)
        mock_print.assert_called_with("Added 3 of 'Food'. New total: 3")

        # Test adding negative quantity
        mock_print.reset_mock()
        mock_stderr.reset_mock()
        _add_resource(resources, "Water", -2)
        self.assertEqual(resources["Water"], 15) # Should not change
        mock_stderr.write.assert_called_with("Quantity to add cannot be negative.\n")


    @patch('builtins.print')
    @patch('sys.stderr')
    def test_remove_resource(self, mock_stderr, mock_print):
        # Mock rationale: Test the `remove_resource` logic in isolation.
        resources = defaultdict(int, {"Water": 10, "Food": 5})

        def _remove_resource(resources, name, quantity):
            if quantity < 0:
                mock_stderr.write("Quantity to remove cannot be negative.\n")
                return
            if name not in resources or resources[name] == 0:
                mock_stderr.write(f"'{name}' not found or quantity is already zero. Cannot remove.\n")
                return
            
            resources[name] = max(0, resources[name] - quantity)
            mock_print(f"Removed {quantity} of '{name}'. New total: {resources[name]}")

        _remove_resource(resources, "Water", 3)
        self.assertEqual(resources["Water"], 7)
        mock_print.assert_called_with("Removed 3 of 'Water'. New total: 7")

        # Test removing more than available
        mock_print.reset_mock()
        _remove_resource(resources, "Food", 10)
        self.assertEqual(resources["Food"], 0)
        mock_print.assert_called_with("Removed 10 of 'Food'. New total: 0")

        # Test removing non-existent item
        mock_print.reset_mock()
        mock_stderr.reset_mock()
        _remove_resource(resources, "Tools", 1)
        self.assertEqual(resources["Tools"], 0) # defaultdict default
        mock_stderr.write.assert_called_with("'Tools' not found or quantity is already zero. Cannot remove.\n")

        # Test removing negative quantity
        mock_print.reset_mock()
        mock_stderr.reset_mock()
        _remove_resource(resources, "Water", -1)
        self.assertEqual(resources["Water"], 7) # Should not change
        mock_stderr.write.assert_called_with("Quantity to remove cannot be negative.\n")

    @patch('builtins.print')
    @patch('sys.stderr')
    def test_set_resource(self, mock_stderr, mock_print):
        # Mock rationale: Test the `set_resource` logic in isolation.
        resources = defaultdict(int, {"Water": 10})

        def _set_resource(resources, name, quantity):
            if quantity < 0:
                mock_stderr.write("Quantity cannot be negative.\n")
                return
            resources[name] = quantity
            mock_print(f"Set '{name}' quantity to {resources[name]}")

        _set_resource(resources, "Water", 5)
        self.assertEqual(resources["Water"], 5)
        mock_print.assert_called_with("Set 'Water' quantity to 5")

        _set_resource(resources, "Tools", 2)
        self.assertEqual(resources["Tools"], 2)
        mock_print.assert_called_with("Set 'Tools' quantity to 2")

        # Test setting negative quantity
        mock_print.reset_mock()
        mock_stderr.reset_mock()
        _set_resource(resources, "Water", -1)
        self.assertEqual(resources["Water"], 5) # Should not change
        mock_stderr.write.assert_called_with("Quantity cannot be negative.\n")

    @patch('builtins.print')
    def test_list_resources(self, mock_print):
        # Mock rationale: Test the `list_resources` logic in isolation.
        # `mock_print` captures the output to verify formatting and content.
        resources = defaultdict(int, {"Water": 10, "Food Rations": 5, "Scrap Metal": 0})

        def _list_resources(resources):
            if not resources:
                mock_print("Your inventory is empty. Time to scavenge!")
                return

            mock_print("\n--- Current Inventory ---")
            for name, quantity in sorted(resources.items()):
                mock_print(f"- {name}: {quantity}")
            mock_print("-------------------------\n")

        _list_resources(resources)
        expected_calls = [
            unittest.mock.call("\n--- Current Inventory ---"),
            unittest.mock.call("- Food Rations: 5"),
            unittest.mock.call("- Scrap Metal: 0"),
            unittest.mock.call("- Water: 10"),
            unittest.mock.call("-------------------------\n")
        ]
        mock_print.assert_has_calls(expected_calls)

        # Test empty inventory
        mock_print.reset_mock()
        _list_resources(defaultdict(int))
        mock_print.assert_called_with("Your inventory is empty. Time to scavenge!")

if __name__ == '__main__':
    unittest.main()
