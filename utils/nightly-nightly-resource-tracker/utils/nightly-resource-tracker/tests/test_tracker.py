import unittest
from unittest.mock import patch, mock_open
import json
import os
from src.tracker import ResourceTracker

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.test_data_file = "test_resources.json"

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_empty_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an empty or non-existent data file.
        mock_os_path_exists.return_value = False
        tracker = ResourceTracker(self.test_data_file)
        self.assertEqual(tracker.resources, {})
        mock_os_path_exists.assert_called_with(self.test_data_file)
        mock_file_open.assert_not_called()
        mock_json_load.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_existing_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing data file with content.
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = {
            "Water": {"quantity": 10, "threshold": 5},
            "Food Rations": {"quantity": 20, "threshold": 10}
        }
        
        tracker = ResourceTracker(self.test_data_file)
        self.assertEqual(tracker.resources, {
            "Water": {"quantity": 10, "threshold": 5},
            "Food Rations": {"quantity": 20, "threshold": 10}
        })
        mock_os_path_exists.assert_called_with(self.test_data_file)
        mock_file_open.assert_called_with(self.test_data_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists', return_value=False) # Mock rationale: Start with no existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_add_resource(self, mock_json_dump, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate adding a new resource and saving it.
        tracker = ResourceTracker(self.test_data_file)
        tracker.add_resource("Batteries", 50, 10)
        self.assertEqual(tracker.resources, {"Batteries": {"quantity": 50, "threshold": 10}})
        mock_file_open.assert_called_with(self.test_data_file, 'w')
        mock_json_dump.assert_called_with({"Batteries": {"quantity": 50, "threshold": 10}}, mock_file_open(), indent=4)

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={"Water": {"quantity": 10, "threshold": 5}}) # Mock rationale: Pre-load resources.
    @patch('json.dump')
    def test_update_quantity(self, mock_json_dump, mock_file_open, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate updating an existing resource's quantity.
        tracker = ResourceTracker(self.test_data_file)
        tracker.update_quantity("Water", -3) # Use -3 for removal
        self.assertEqual(tracker.resources["Water"]["quantity"], 7)
        mock_json_dump.assert_called_with({"Water": {"quantity": 7, "threshold": 5}}, mock_file_open(), indent=4)
        
        tracker.update_quantity("Water", 5) # Add 5
        self.assertEqual(tracker.resources["Water"]["quantity"], 12)
        # json.dump called twice, so check the last call
        mock_json_dump.assert_called_with({"Water": {"quantity": 12, "threshold": 5}}, mock_file_open(), indent=4)

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={"Water": {"quantity": 10, "threshold": 5}}) # Mock rationale: Pre-load resources.
    @patch('json.dump')
    def test_update_quantity_below_zero(self, mock_json_dump, mock_file_open, mock_json_load, mock_os_path_exists):
        # Mock rationale: Test that quantity doesn't go below zero.
        tracker = ResourceTracker(self.test_data_file)
        tracker.update_quantity("Water", -15)
        self.assertEqual(tracker.resources["Water"]["quantity"], 0)
        mock_json_dump.assert_called_with({"Water": {"quantity": 0, "threshold": 5}}, mock_file_open(), indent=4)

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={"Water": {"quantity": 10, "threshold": 5}}) # Mock rationale: Pre-load resources.
    @patch('json.dump')
    def test_set_threshold(self, mock_json_dump, mock_file_open, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate setting a new threshold for a resource.
        tracker = ResourceTracker(self.test_data_file)
        tracker.set_threshold("Water", 2)
        self.assertEqual(tracker.resources["Water"]["threshold"], 2)
        mock_json_dump.assert_called_with({"Water": {"quantity": 10, "threshold": 2}}, mock_file_open(), indent=4)

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={
        "Water": {"quantity": 10, "threshold": 5},
        "Food Rations": {"quantity": 8, "threshold": 10},
        "Medkits": {"quantity": 2, "threshold": 2}
    }) # Mock rationale: Pre-load resources with various statuses.
    def test_get_status(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Test the status determination logic.
        tracker = ResourceTracker(self.test_data_file)
        self.assertEqual(tracker.get_status("Water"), "OK")
        self.assertEqual(tracker.get_status("Food Rations"), "LOW")
        self.assertEqual(tracker.get_status("Medkits"), "LOW") # Equal to threshold is LOW
        self.assertEqual(tracker.get_status("NonExistent"), "Not Found")

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={
        "Water": {"quantity": 10, "threshold": 5},
        "Food Rations": {"quantity": 8, "threshold": 10}
    }) # Mock rationale: Pre-load resources for listing.
    def test_list_resources(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Test the formatted output for listing resources.
        tracker = ResourceTracker(self.test_data_file)
        expected_output = (
            "- Water: 10 (Threshold: 5) - Status: OK\n"
            "- Food Rations: 8 (Threshold: 10) - Status: LOW"
        )
        self.assertEqual(tracker.list_resources(), expected_output)

    @patch('os.path.exists', return_value=False) # Mock rationale: Start with no existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_list_empty_resources(self, mock_json_dump, mock_file_open, mock_os_path_exists):
        # Mock rationale: Test listing when no resources are tracked.
        tracker = ResourceTracker(self.test_data_file)
        self.assertEqual(tracker.list_resources(), "No resources tracked yet.")

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0)) # Mock rationale: Simulate corrupted JSON.
    def test_load_corrupted_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Test handling of corrupted JSON data file.
        with patch('builtins.print') as mock_print: # Mock rationale: Capture print statements.
            tracker = ResourceTracker(self.test_data_file)
            self.assertEqual(tracker.resources, {})
            mock_print.assert_called_with(f"Warning: Could not decode JSON from {self.test_data_file}. Starting with empty resources.")

    def test_add_resource_invalid_input(self):
        # Mock rationale: Test input validation for add_resource.
        tracker = ResourceTracker(self.test_data_file) # No need to mock file ops for these specific value errors
        with self.assertRaises(ValueError):
            tracker.add_resource("", 10)
        with self.assertRaises(ValueError):
            tracker.add_resource("Water", -5)
        with self.assertRaises(ValueError):
            tracker.add_resource("Water", 10, -1)

    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate an existing file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={"Water": {"quantity": 10, "threshold": 5}}) # Mock rationale: Pre-load resources.
    @patch('json.dump')
    def test_set_threshold_invalid_input(self, mock_json_dump, mock_file_open, mock_json_load, mock_os_path_exists):
        # Mock rationale: Test input validation for set_threshold.
        tracker = ResourceTracker(self.test_data_file)
        with self.assertRaises(ValueError):
            tracker.set_threshold("Water", -5)

if __name__ == '__main__':
    unittest.main()
