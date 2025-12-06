import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust the import path for the tracker module
# Assuming test_tracker.py is in tests/ and tracker.py is in src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tracker import ResourceTracker, DATA_FILE

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test by mocking file operations
        self.mock_data = {}
        self.mock_file_content = json.dumps(self.mock_data)

        # Mock os.path.exists to control if the data file "exists"
        self.patcher_exists = patch('os.path.exists')
        self.mock_exists = self.patcher_exists.start()
        self.mock_exists.return_value = False # Default: file does not exist

        # Mock open for reading and writing
        self.patcher_open = patch('builtins.open', mock_open())
        self.mock_open = self.patcher_open.start()

        # Mock print to capture output
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()

        # Initialize tracker with a dummy data file path for isolation
        self.tracker = ResourceTracker(data_file="mock_resources.json")

    def tearDown(self):
        self.patcher_exists.stop()
        self.patcher_open.stop()
        self.patcher_print.stop()

    def _simulate_file_read(self, content: dict):
        # Mock rationale: Simulate reading existing JSON data from the file.
        self.mock_exists.return_value = True
        self.mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(content)
        self.tracker = ResourceTracker(data_file="mock_resources.json") # Re-initialize to load mocked data

    def _get_saved_data(self) -> dict:
        # Mock rationale: Retrieve the data that would have been written to the file.
        # The mock_open object records calls to write.
        handle = self.mock_open()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        return json.loads(written_content) if written_content else {}

    def test_initialization_no_file(self):
        # Mock rationale: Test behavior when the data file does not exist initially.
        self.mock_exists.return_value = False
        tracker = ResourceTracker(data_file="mock_resources.json")
        self.assertEqual(tracker.resources, {})
        self.mock_print.assert_not_called() # No warning if file doesn't exist

    def test_initialization_empty_file(self):
        # Mock rationale: Test behavior when the data file exists but is empty.
        self.mock_exists.return_value = True
        self.mock_open.return_value.__enter__.return_value.read.return_value = ""
        tracker = ResourceTracker(data_file="mock_resources.json")
        self.assertEqual(tracker.resources, {})
        self.mock_print.assert_called_with("Warning: Could not decode mock_resources.json. Starting with empty resources.")

    def test_initialization_corrupt_file(self):
        # Mock rationale: Test behavior when the data file contains invalid JSON.
        self.mock_exists.return_value = True
        self.mock_open.return_value.__enter__.return_value.read.return_value = "{invalid json"
        tracker = ResourceTracker(data_file="mock_resources.json")
        self.assertEqual(tracker.resources, {})
        self.mock_print.assert_called_with("Warning: Could not decode mock_resources.json. Starting with empty resources.")

    def test_add_resource(self):
        self.tracker.add_resource("Water", 10, 2)
        self.assertEqual(self.tracker.resources["water"], {"quantity": 10, "threshold": 2})
        saved_data = self._get_saved_data()
        self.assertEqual(saved_data["water"], {"quantity": 10, "threshold": 2})
        self.mock_print.assert_called_with("Added resource 'water' with quantity 10 and threshold 2.")

    def test_add_existing_resource(self):
        self._simulate_file_read({"water": {"quantity": 10, "threshold": 2}})
        self.tracker.add_resource("Water", 5, 1)
        # Should not change existing resource, just print warning
        self.assertEqual(self.tracker.resources["water"], {"quantity": 10, "threshold": 2})
        self.mock_print.assert_called_with("Resource 'water' already exists. Use 'replenish' or 'set-threshold' to update.")

    def test_remove_resource(self):
        self._simulate_file_read({"food": {"quantity": 5, "threshold": 1}})
        self.tracker.remove_resource("Food")
        self.assertNotIn("food", self.tracker.resources)
        saved_data = self._get_saved_data()
        self.assertNotIn("food", saved_data)
        self.mock_print.assert_called_with("Removed resource 'food'.")

    def test_remove_non_existent_resource(self):
        self.tracker.remove_resource("NonExistent")
        self.mock_print.assert_called_with("Resource 'nonexistent' not found.")

    def test_consume_resource(self):
        self._simulate_file_read({"ammo": {"quantity": 20, "threshold": 5}})
        self.tracker.update_quantity("Ammo", 5, "consume")
        self.assertEqual(self.tracker.resources["ammo"]["quantity"], 15)
        saved_data = self._get_saved_data()
        self.assertEqual(saved_data["ammo"]["quantity"], 15)
        self.mock_print.assert_any_call("Consumed 5 of 'ammo'. New quantity: 15.")

    def test_consume_more_than_available(self):
        self._simulate_file_read({"medkits": {"quantity": 3, "threshold": 1}})
        self.tracker.update_quantity("Medkits", 5, "consume")
        self.assertEqual(self.tracker.resources["medkits"]["quantity"], 0)
        saved_data = self._get_saved_data()
        self.assertEqual(saved_data["medkits"]["quantity"], 0)
        self.mock_print.assert_any_call("Warning: Trying to consume 5 of 'medkits', but only 3 available.")
        self.mock_print.assert_any_call("Consumed 5 of 'medkits'. New quantity: 0.")
        self.mock_print.assert_any_call("ALERT: 'Medkits' quantity (0) is at or below its critical threshold (1)!")


    def test_replenish_resource(self):
        self._simulate_file_read({"fuel": {"quantity": 10, "threshold": 2}})
        self.tracker.update_quantity("Fuel", 15, "replenish")
        self.assertEqual(self.tracker.resources["fuel"]["quantity"], 25)
        saved_data = self._get_saved_data()
        self.assertEqual(saved_data["fuel"]["quantity"], 25)
        self.mock_print.assert_any_call("Replenished 15 of 'fuel'. New quantity: 25.")

    def test_update_non_existent_resource(self):
        self.tracker.update_quantity("NonExistent", 1, "consume")
        self.mock_print.assert_called_with("Resource 'nonexistent' not found. Please add it first.")

    def test_set_threshold(self):
        self._simulate_file_read({"water": {"quantity": 10, "threshold": 2}})
        self.tracker.set_threshold("Water", 5)
        self.assertEqual(self.tracker.resources["water"]["threshold"], 5)
        saved_data = self._get_saved_data()
        self.assertEqual(saved_data["water"]["threshold"], 5)
        self.mock_print.assert_called_with("Set threshold for 'water' to 5.")

    def test_set_threshold_non_existent_resource(self):
        self.tracker.set_threshold("NonExistent", 5)
        self.mock_print.assert_called_with("Resource 'nonexistent' not found. Please add it first.")

    def test_get_status_empty(self):
        self.tracker.get_status()
        self.mock_print.assert_called_with("No resources tracked yet. Add some with 'add' command!")

    def test_get_status_with_resources(self):
        self._simulate_file_read({
            "water": {"quantity": 10, "threshold": 5},
            "food": {"quantity": 2, "threshold": 3}
        })
        self.tracker.get_status()
        expected_calls = [
            unittest.mock.call("\n--- Wasteland Resource Status ---"),
            unittest.mock.call("- Water: 10 (Threshold: 5)"),
            unittest.mock.call("- Food: 2 (Threshold: 3) [CRITICAL!]"),
            unittest.mock.call("---------------------------------\n")
        ]
        self.mock_print.assert_has_calls(expected_calls, any_order=True)

    def test_threshold_alert_on_consume(self):
        self._simulate_file_read({"berries": {"quantity": 10, "threshold": 8}})
        self.tracker.update_quantity("Berries", 3, "consume") # Quantity becomes 7
        self.mock_print.assert_any_call("Consumed 3 of 'berries'. New quantity: 7.")
        self.mock_print.assert_any_call("ALERT: 'Berries' quantity (7) is at or below its critical threshold (8)!")

    def test_threshold_alert_on_set_threshold(self):
        self._simulate_file_read({"scrap_metal": {"quantity": 10, "threshold": 5}})
        self.tracker.set_threshold("Scrap_Metal", 12) # Quantity 10, threshold 12
        self.mock_print.assert_any_call("Set threshold for 'scrap_metal' to 12.")
        self.mock_print.assert_any_call("ALERT: 'Scrap_Metal' quantity (10) is at or below its critical threshold (12)!")

    def test_no_threshold_alert_if_above(self):
        self._simulate_file_read({"medicine": {"quantity": 10, "threshold": 5}})
        self.tracker.update_quantity("Medicine", 2, "consume") # Quantity becomes 8
        self.mock_print.assert_any_call("Consumed 2 of 'medicine'. New quantity: 8.")
        # Ensure no alert is printed if quantity is still above threshold
        for call_args in self.mock_print.call_args_list:
            self.assertNotIn("ALERT", call_args.args[0])

if __name__ == '__main__':
    unittest.main()
