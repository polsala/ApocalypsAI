import unittest
from unittest.mock import patch, mock_open
import json
import os
from collections import defaultdict

# Import functions from the ledger script
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ledger import load_ledger, save_ledger, add_resource, remove_resource, list_resources, show_resource, LEDGER_FILE

class TestLedger(unittest.TestCase):

    def setUp(self):
        # Ensure LEDGER_FILE is set to a test-specific name to avoid conflicts
        self.test_ledger_file = "test_resources.json"
        # Mock os.path.exists to control file existence for tests
        self.patcher_exists = patch('os.path.exists')
        self.mock_exists = self.patcher_exists.start()
        self.mock_exists.return_value = False # Default: file does not exist

        # Mock open for file I/O
        self.patcher_open = patch('builtins.open', new_callable=mock_open)
        self.mock_open = self.patcher_open.start()

        # Mock json.dump and json.load
        self.patcher_json_dump = patch('json.dump')
        self.mock_json_dump = self.patcher_json_dump.start()
        self.patcher_json_load = patch('json.load')
        self.mock_json_load = self.patcher_json_load.start()

        # Mock print for capturing output
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_exists.stop()
        self.patcher_open.stop()
        self.patcher_json_dump.stop()
        self.patcher_json_load.stop()
        self.patcher_print.stop()

    def test_load_ledger_empty_file(self):
        # Mock rationale: Simulate an empty or non-existent ledger file.
        self.mock_exists.return_value = False
        ledger = load_ledger(self.test_ledger_file)
        self.assertEqual(ledger, defaultdict(int))
        self.mock_exists.assert_called_once_with(self.test_ledger_file)

    def test_load_ledger_existing_file(self):
        # Mock rationale: Simulate an existing ledger file with content.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 5, "Water Bottle": 2}
        ledger = load_ledger(self.test_ledger_file)
        self.assertEqual(ledger, defaultdict(int, {"Canned Beans": 5, "Water Bottle": 2}))
        self.mock_exists.assert_called_once_with(self.test_ledger_file)
        self.mock_open.assert_called_once_with(self.test_ledger_file, 'r')
        self.mock_json_load.assert_called_once()

    def test_load_ledger_corrupted_file(self):
        # Mock rationale: Simulate a corrupted JSON file.
        self.mock_exists.return_value = True
        self.mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        ledger = load_ledger(self.test_ledger_file)
        self.assertEqual(ledger, defaultdict(int))
        self.mock_print.assert_called_once_with(f"Warning: {self.test_ledger_file} is corrupted or empty. Starting with an empty ledger.")

    def test_save_ledger(self):
        # Mock rationale: Verify that save_ledger correctly writes to file.
        ledger_data = defaultdict(int, {"Canned Beans": 7})
        save_ledger(ledger_data, self.test_ledger_file)
        self.mock_open.assert_called_once_with(self.test_ledger_file, 'w')
        self.mock_json_dump.assert_called_once_with(dict(ledger_data), self.mock_open(), indent=4)

    def test_add_resource_new(self):
        # Mock rationale: Simulate adding a new resource to an empty ledger.
        self.mock_exists.return_value = False # No existing file
        add_resource("First Aid Kit", 1, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({"First Aid Kit": 1}, self.mock_open(), indent=4)
        self.mock_print.assert_called_once_with("Added 1 unit(s) of 'First Aid Kit' to your stash. Total: 1.")

    def test_add_resource_existing(self):
        # Mock rationale: Simulate adding to an existing resource.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 5}
        add_resource("Canned Beans", 3, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({"Canned Beans": 8}, self.mock_open(), indent=4)
        self.mock_print.assert_called_once_with("Added 3 unit(s) of 'Canned Beans' to your stash. Total: 8.")

    def test_add_resource_with_location(self):
        # Mock rationale: Simulate adding a resource with a location.
        self.mock_exists.return_value = False
        add_resource("Water Bottle", 2, location="Abandoned Gas Station", file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({"Water Bottle": 2}, self.mock_open(), indent=4)
        self.mock_print.assert_called_once_with("Added 2 unit(s) of 'Water Bottle' to your stash (found at Abandoned Gas Station). Total: 2.")

    def test_add_resource_zero_quantity(self):
        # Mock rationale: Test adding zero quantity.
        self.mock_exists.return_value = False
        add_resource("First Aid Kit", 0, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_not_called() # Should not save
        self.mock_print.assert_called_once_with("Scavenger's wisdom: Quantity must be positive to add a resource, not 0.")

    def test_remove_resource_existing(self):
        # Mock rationale: Simulate removing some quantity of an existing resource.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 5, "Duct Tape": 1}
        remove_resource("Canned Beans", 2, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({"Canned Beans": 3, "Duct Tape": 1}, self.mock_open(), indent=4)
        self.mock_print.assert_called_once_with("Removed 2 unit(s) of 'Canned Beans'. Remaining: 3.")

    def test_remove_resource_all(self):
        # Mock rationale: Simulate removing all quantity of an existing resource.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 2, "Duct Tape": 1}
        remove_resource("Canned Beans", 2, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({"Duct Tape": 1}, self.mock_open(), indent=4)
        self.mock_print.assert_called_once_with("All 'Canned Beans' consumed. It's gone.")

    def test_remove_resource_more_than_available(self):
        # Mock rationale: Simulate trying to remove more than available.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 2}
        remove_resource("Canned Beans", 5, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_called_once_with({}, self.mock_open(), indent=4)
        self.mock_print.assert_any_call("Warning: You only have 2 unit(s) of 'Canned Beans'. Removing all of them.")
        self.mock_print.assert_any_call("All 'Canned Beans' consumed. It's gone.")

    def test_remove_resource_not_found(self):
        # Mock rationale: Simulate trying to remove a resource that doesn't exist.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Duct Tape": 1}
        remove_resource("Canned Beans", 1, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_not_called() # Should not save
        self.mock_print.assert_called_once_with("No 'Canned Beans' found in your ledger to remove. Perhaps it was already consumed?")

    def test_remove_resource_zero_quantity(self):
        # Mock rationale: Test removing zero quantity.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 5}
        remove_resource("Canned Beans", 0, file_path=self.test_ledger_file)
        self.mock_json_dump.assert_not_called() # Should not save
        self.mock_print.assert_called_once_with("Scavenger's wisdom: Quantity must be positive to remove a resource, not 0.")

    def test_list_resources_empty(self):
        # Mock rationale: Simulate an empty ledger when listing.
        self.mock_exists.return_value = False
        list_resources(file_path=self.test_ledger_file)
        self.mock_print.assert_called_once_with("Your ledger is empty. Time to scavenge!")

    def test_list_resources_with_items(self):
        # Mock rationale: Simulate a ledger with items when listing.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Water Bottle": 2, "Canned Beans": 5}
        list_resources(file_path=self.test_ledger_file)
        expected_calls_sorted = [
            unittest.mock.call("\n--- Your Wasteland Stash ---"),
            unittest.mock.call("- Canned Beans: 5 unit(s)"),
            unittest.mock.call("- Water Bottle: 2 unit(s)"),
            unittest.mock.call("---------------------------\n")
        ]
        self.mock_print.assert_has_calls(expected_calls_sorted)

    def test_show_resource_existing(self):
        # Mock rationale: Simulate showing an existing resource.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Canned Beans": 5}
        show_resource("Canned Beans", file_path=self.test_ledger_file)
        self.mock_print.assert_called_once_with("You have 5 unit(s) of 'Canned Beans'.")

    def test_show_resource_not_found(self):
        # Mock rationale: Simulate showing a resource that doesn't exist.
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {"Duct Tape": 1}
        show_resource("Canned Beans", file_path=self.test_ledger_file)
        self.mock_print.assert_called_once_with("No 'Canned Beans' found in your ledger. Keep an eye out!")

    def test_show_resource_empty_ledger(self):
        # Mock rationale: Simulate showing a resource when the ledger is empty.
        self.mock_exists.return_value = False
        show_resource("Canned Beans", file_path=self.test_ledger_file)
        self.mock_print.assert_called_once_with("No 'Canned Beans' found in your ledger. Keep an eye out!")


if __name__ == '__main__':
    unittest.main()
