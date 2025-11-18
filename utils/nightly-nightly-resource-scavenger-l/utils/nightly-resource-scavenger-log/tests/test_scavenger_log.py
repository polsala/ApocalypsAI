import unittest
from unittest.mock import patch, mock_open
import json
import os
from collections import defaultdict

# Mock rationale: Adjusting sys.path to allow importing from a sibling directory
# is a common pattern for self-contained utilities. For testing, we need to ensure
# the module under test is discoverable.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scavenger_log import ScavengerLog
sys.path.pop(0)

class TestScavengerLog(unittest.TestCase):

    def setUp(self):
        # Mock rationale: We want to test the ScavengerLog class in isolation
        # without actually creating or modifying files on the disk. This ensures
        # tests are deterministic, fast, and don't leave artifacts.
        self.mock_data = defaultdict(lambda: defaultdict(int))
        self.data_file = 'test_scavenger_log.json'

        # Patch os.path.exists to simulate file existence
        # Mock rationale: Control whether the 'data_file' appears to exist for _load_log.
        self.patch_exists = patch('os.path.exists', return_value=False)
        self.mock_exists = self.patch_exists.start()

        # Patch open for file I/O operations
        # Mock rationale: Intercept file read/write operations to use an in-memory dict.
        self.patch_open = patch('builtins.open', mock_open())
        self.mock_file_open = self.patch_open.start()

        # Patch json.load and json.dump
        # Mock rationale: Directly control the data loaded and saved, bypassing actual JSON parsing/serialization to disk.
        self.patch_json_load = patch('json.load', side_effect=lambda f: self.mock_data)
        self.mock_json_load = self.patch_json_load.start()

        self.patch_json_dump = patch('json.dump', side_effect=lambda obj, f, indent: self._mock_json_dump(obj))
        self.mock_json_dump = self.patch_json_dump.start()

        # Initialize ScavengerLog with the mocked data file
        self.log_manager = ScavengerLog(data_file=self.data_file)

    def tearDown(self):
        self.patch_exists.stop()
        self.patch_open.stop()
        self.patch_json_load.stop()
        self.patch_json_dump.stop()

    def _mock_json_dump(self, obj):
        # This method simulates saving the log by updating our in-memory mock_data
        # Mock rationale: When json.dump is called, we want to update our internal
        # representation of the file content so subsequent json.load calls reflect it.
        self.mock_data.clear()
        for loc, items in obj.items():
            for item, qty in items.items():
                self.mock_data[loc][item] = qty

    def test_add_resource_new_item_location(self):
        # Mock rationale: Ensure _load_log starts with an empty state.
        self.mock_exists.return_value = False
        self.log_manager = ScavengerLog(data_file=self.data_file) # Re-init to ensure empty state

        self.log_manager.add_resource("Canned Beans", 5, "Kitchen Stash")
        self.assertEqual(self.mock_data["Kitchen Stash"]["Canned Beans"], 5)
        self.mock_json_dump.assert_called_once() # Mock rationale: Verify data was attempted to be saved.

    def test_add_resource_existing_item_location(self):
        # Mock rationale: Simulate a pre-existing log state.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 3
        self.mock_exists.return_value = True # Simulate file exists
        self.log_manager = ScavengerLog(data_file=self.data_file) # Re-init to load mock_data
        self.mock_json_dump.reset_mock() # Reset dump call count after init load

        self.log_manager.add_resource("Canned Beans", 2, "Kitchen Stash")
        self.assertEqual(self.mock_data["Kitchen Stash"]["Canned Beans"], 5)
        self.mock_json_dump.assert_called_once()

    def test_add_resource_negative_quantity(self):
        # Mock rationale: Ensure validation prevents invalid operations.
        with patch('builtins.print') as mock_print:
            self.log_manager.add_resource("Water Bottle", -1, "Backpack")
            mock_print.assert_called_with("Quantity must be positive.")
            self.mock_json_dump.assert_not_called() # Mock rationale: No save should occur for invalid input.

    def test_remove_resource_existing_item(self):
        # Mock rationale: Simulate a pre-existing log state.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 5
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        self.log_manager.remove_resource("Canned Beans", 2, "Kitchen Stash")
        self.assertEqual(self.mock_data["Kitchen Stash"]["Canned Beans"], 3)
        self.mock_json_dump.assert_called_once()

    def test_remove_resource_all_items(self):
        # Mock rationale: Simulate a pre-existing log state and verify item deletion.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 2
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        self.log_manager.remove_resource("Canned Beans", 2, "Kitchen Stash")
        self.assertNotIn("Canned Beans", self.mock_data["Kitchen Stash"])
        self.mock_json_dump.assert_called_once()

    def test_remove_resource_location_becomes_empty(self):
        # Mock rationale: Verify that an empty location is removed from the log.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 1
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        self.log_manager.remove_resource("Canned Beans", 1, "Kitchen Stash")
        self.assertNotIn("Kitchen Stash", self.mock_data)
        self.mock_json_dump.assert_called_once()

    def test_remove_resource_not_enough(self):
        # Mock rationale: Ensure validation prevents removing more than available.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 1
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        with patch('builtins.print') as mock_print:
            self.log_manager.remove_resource("Canned Beans", 5, "Kitchen Stash")
            mock_print.assert_called_with("Not enough Canned Beans in Kitchen Stash to remove 5. Current: 1")
            self.assertEqual(self.mock_data["Kitchen Stash"]["Canned Beans"], 1) # Should remain unchanged
            self.mock_json_dump.assert_not_called()

    def test_remove_resource_item_not_found(self):
        # Mock rationale: Ensure graceful handling of non-existent items.
        self.mock_data["Kitchen Stash"]["Water Bottle"] = 1
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        with patch('builtins.print') as mock_print:
            self.log_manager.remove_resource("Canned Beans", 1, "Kitchen Stash")
            mock_print.assert_called_with("Not enough Canned Beans in Kitchen Stash to remove 1. Current: 0")
            self.mock_json_dump.assert_not_called()

    def test_remove_resource_negative_quantity(self):
        # Mock rationale: Ensure validation prevents invalid operations.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 5
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)
        self.mock_json_dump.reset_mock()

        with patch('builtins.print') as mock_print:
            self.log_manager.remove_resource("Canned Beans", -1, "Kitchen Stash")
            mock_print.assert_called_with("Quantity must be positive.")
            self.assertEqual(self.mock_data["Kitchen Stash"]["Canned Beans"], 5)
            self.mock_json_dump.assert_not_called()

    def test_list_resources_empty_log(self):
        # Mock rationale: Test behavior when no resources are logged.
        self.mock_exists.return_value = False
        self.log_manager = ScavengerLog(data_file=self.data_file)

        with patch('builtins.print') as mock_print:
            self.log_manager.list_resources()
            mock_print.assert_called_with("The scavenger log is empty.")

    def test_list_resources_all(self):
        # Mock rationale: Simulate a log with multiple items and locations.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 5
        self.mock_data["Garage Cache"]["Duct Tape"] = 2
        self.mock_data["Kitchen Stash"]["Water Bottle"] = 3
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)

        expected_output = [
            "\nAll Scavenged Resources:",
            "\nLocation: Garage Cache",
            "  - Duct Tape: 2",
            "\nLocation: Kitchen Stash",
            "  - Canned Beans: 5",
            "  - Water Bottle: 3"
        ]
        with patch('builtins.print') as mock_print:
            self.log_manager.list_resources()
            # Check if all expected calls are present, order might vary for items within a location if not sorted
            # We sort the items in the actual implementation, so the order should be deterministic.
            mock_print.assert_has_calls([unittest.mock.call(line) for line in expected_output])
            self.assertEqual(mock_print.call_count, len(expected_output))

    def test_list_resources_by_location(self):
        # Mock rationale: Simulate a log with multiple items and locations.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 5
        self.mock_data["Garage Cache"]["Duct Tape"] = 2
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)

        expected_output = [
            "\nResources in Kitchen Stash:",
            "  - Canned Beans: 5",
            "  - Water Bottle: 3"
        ]
        with patch('builtins.print') as mock_print:
            self.log_manager.list_resources(location="Kitchen Stash")
            mock_print.assert_has_calls([unittest.mock.call(line) for line in expected_output])
            self.assertEqual(mock_print.call_count, len(expected_output))

    def test_list_resources_non_existent_location(self):
        # Mock rationale: Test behavior for querying a location that doesn't exist.
        self.mock_data["Kitchen Stash"]["Canned Beans"] = 5
        self.mock_exists.return_value = True
        self.log_manager = ScavengerLog(data_file=self.data_file)

        with patch('builtins.print') as mock_print:
            self.log_manager.list_resources(location="Basement Bunker")
            mock_print.assert_called_with("No resources found in location: Basement Bunker")

    def test_load_log_corrupted_json(self):
        # Mock rationale: Simulate a corrupted JSON file to ensure graceful handling.
        self.mock_exists.return_value = True
        # Mock open to return invalid JSON content
        self.mock_file_open.return_value.__enter__.return_value.read.return_value = "{invalid json"
        self.mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        with patch('builtins.print') as mock_print:
            log_manager = ScavengerLog(data_file=self.data_file)
            mock_print.assert_called_with(f"Warning: Could not decode {self.data_file}. Starting with an empty log.")
            self.assertTrue(not log_manager.log) # Log should be empty

    def test_load_log_empty_file(self):
        # Mock rationale: Simulate an empty file to ensure graceful handling.
        self.mock_exists.return_value = True
        self.mock_file_open.return_value.__enter__.return_value.read.return_value = ""
        self.mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        with patch('builtins.print') as mock_print:
            log_manager = ScavengerLog(data_file=self.data_file)
            mock_print.assert_called_with(f"Warning: Could not decode {self.data_file}. Starting with an empty log.")
            self.assertTrue(not log_manager.log) # Log should be empty
