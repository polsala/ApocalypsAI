import unittest
from unittest.mock import patch, mock_open
import json
import os
import io
from src.tracker import ResourceTracker, DEFAULT_INVENTORY_FILE, main

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.test_file = "test_inventory.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_existing(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing inventory file with content.
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = {"Water": 10, "Food": 5}

        tracker = ResourceTracker(self.test_file)
        self.assertEqual(tracker.inventory, {"Water": 10, "Food": 5})
        mock_os_path_exists.assert_called_once_with(self.test_file)
        mock_file_open.assert_called_once_with(self.test_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_inventory_non_existing(self, mock_os_path_exists):
        # Mock rationale: Simulate no existing inventory file.
        mock_os_path_exists.return_value = False

        tracker = ResourceTracker(self.test_file)
        self.assertEqual(tracker.inventory, {})
        mock_os_path_exists.assert_called_once_with(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_load_inventory_corrupted(self, mock_stdout, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_os_path_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        tracker = ResourceTracker(self.test_file)
        self.assertEqual(tracker.inventory, {})
        self.assertIn(f"Warning: Inventory file '{self.test_file}' is corrupted.", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_inventory(self, mock_json_dump, mock_file_open):
        # Mock rationale: Verify that inventory is correctly saved to file.
        tracker = ResourceTracker(self.test_file)
        tracker.inventory = {"Medkit": 2}
        tracker._save_inventory()
        mock_file_open.assert_called_once_with(self.test_file, 'w')
        mock_json_dump.assert_called_once_with({"Medkit": 2}, mock_file_open(), indent=4)

    @patch('src.tracker.ResourceTracker._save_inventory')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_resource(self, mock_stdout, mock_save_inventory):
        # Mock rationale: Test adding a resource and ensure save is called and output is correct.
        tracker = ResourceTracker(self.test_file)
        tracker.add_resource("Water", 10)
        self.assertEqual(tracker.inventory, {"Water": 10})
        mock_save_inventory.assert_called_once()
        self.assertIn("Added/Updated 'Water': 10 units.", mock_stdout.getvalue())

        tracker.add_resource("Water", 5)
        self.assertEqual(tracker.inventory, {"Water": 15})
        self.assertEqual(mock_save_inventory.call_count, 2)
        self.assertIn("Added/Updated 'Water': 15 units.", mock_stdout.getvalue())

    @patch('src.tracker.ResourceTracker._save_inventory')
    def test_add_resource_negative_quantity(self, mock_save_inventory):
        # Mock rationale: Ensure negative quantities are rejected.
        tracker = ResourceTracker(self.test_file)
        with self.assertRaises(ValueError):
            tracker.add_resource("Water", -5)
        mock_save_inventory.assert_not_called()

    @patch('src.tracker.ResourceTracker._save_inventory')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_resource(self, mock_stdout, mock_save_inventory):
        # Mock rationale: Test updating a resource and ensure save is called and output is correct.
        tracker = ResourceTracker(self.test_file)
        tracker.inventory = {"Water": 10}
        tracker.update_resource("Water", 7)
        self.assertEqual(tracker.inventory, {"Water": 7})
        mock_save_inventory.assert_called_once()
        self.assertIn("Added/Updated 'Water': 7 units.", mock_stdout.getvalue())

        tracker.update_resource("Food", 3) # Update non-existent resource
        self.assertEqual(tracker.inventory, {"Water": 7, "Food": 3})
        self.assertEqual(mock_save_inventory.call_count, 2)
        self.assertIn("Added/Updated 'Food': 3 units.", mock_stdout.getvalue())

    @patch('src.tracker.ResourceTracker._save_inventory')
    def test_update_resource_negative_quantity(self, mock_save_inventory):
        # Mock rationale: Ensure negative quantities are rejected.
        tracker = ResourceTracker(self.test_file)
        with self.assertRaises(ValueError):
            tracker.update_resource("Water", -5)
        mock_save_inventory.assert_not_called()

    @patch('src.tracker.ResourceTracker._save_inventory')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_resource(self, mock_stdout, mock_save_inventory):
        # Mock rationale: Test removing a resource and ensure save is called and output is correct.
        tracker = ResourceTracker(self.test_file)
        tracker.inventory = {"Water": 10, "Food": 5}
        tracker.remove_resource("Water")
        self.assertEqual(tracker.inventory, {"Food": 5})
        mock_save_inventory.assert_called_once()
        self.assertIn("Removed 'Water' from inventory.", mock_stdout.getvalue())

    @patch('src.tracker.ResourceTracker._save_inventory')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_non_existent_resource(self, mock_stdout, mock_save_inventory):
        # Mock rationale: Test removing a non-existent resource.
        tracker = ResourceTracker(self.test_file)
        tracker.inventory = {"Food": 5}
        tracker.remove_resource("Water")
        self.assertEqual(tracker.inventory, {"Food": 5}) # Inventory should be unchanged
        mock_save_inventory.assert_not_called() # No save should happen
        self.assertIn("Resource 'Water' not found in inventory.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_resources_empty(self, mock_stdout):
        # Mock rationale: Test listing when inventory is empty.
        tracker = ResourceTracker(self.test_file)
        tracker.list_resources()
        self.assertIn("Inventory is empty. Time to scavenge!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_resources_populated(self, mock_stdout):
        # Mock rationale: Test listing when inventory has items, ensuring sorted output.
        tracker = ResourceTracker(self.test_file)
        tracker.inventory = {"Water": 10, "Food": 5, "Medkit": 2}
        tracker.list_resources()
        expected_output = (
            "--- Current Inventory ---\n"
            "Food: 5\n"
            "Medkit: 2\n"
            "Water: 10\n"
            "-------------------------\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_add_command(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'add' command and verify tracker method calls.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", name="Canned Beans", quantity=5, file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        main()
        MockResourceTracker.assert_called_once_with(DEFAULT_INVENTORY_FILE)
        mock_tracker_instance.add_resource.assert_called_once_with("Canned Beans", 5)
        mock_tracker_instance.update_resource.assert_not_called()
        mock_tracker_instance.remove_resource.assert_not_called()
        mock_tracker_instance.list_resources.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_update_command(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'update' command and verify tracker method calls.
        mock_parse_args.return_value = argparse.Namespace(
            command="update", name="Canned Beans", quantity=3, file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        main()
        MockResourceTracker.assert_called_once_with(DEFAULT_INVENTORY_FILE)
        mock_tracker_instance.update_resource.assert_called_once_with("Canned Beans", 3)
        mock_tracker_instance.add_resource.assert_not_called()
        mock_tracker_instance.remove_resource.assert_not_called()
        mock_tracker_instance.list_resources.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_remove_command(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'remove' command and verify tracker method calls.
        mock_parse_args.return_value = argparse.Namespace(
            command="remove", name="Canned Beans", file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        main()
        MockResourceTracker.assert_called_once_with(DEFAULT_INVENTORY_FILE)
        mock_tracker_instance.remove_resource.assert_called_once_with("Canned Beans")
        mock_tracker_instance.add_resource.assert_not_called()
        mock_tracker_instance.update_resource.assert_not_called()
        mock_tracker_instance.list_resources.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_list_command(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'list' command and verify tracker method calls.
        mock_parse_args.return_value = argparse.Namespace(
            command="list", file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        main()
        MockResourceTracker.assert_called_once_with(DEFAULT_INVENTORY_FILE)
        mock_tracker_instance.list_resources.assert_called_once()
        mock_tracker_instance.add_resource.assert_not_called()
        mock_tracker_instance.update_resource.assert_not_called()
        mock_tracker_instance.remove_resource.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_add_command_error_handling(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate an error during 'add' command and check error output.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", name="Water", quantity=-5, file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        mock_tracker_instance.add_resource.side_effect = ValueError("Quantity cannot be negative.")
        main()
        self.assertIn("Error: Quantity cannot be negative.", mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.ResourceTracker')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_update_command_error_handling(self, mock_stdout, MockResourceTracker, mock_parse_args):
        # Mock rationale: Simulate an error during 'update' command and check error output.
        mock_parse_args.return_value = argparse.Namespace(
            command="update", name="Water", quantity=-5, file=DEFAULT_INVENTORY_FILE
        )
        mock_tracker_instance = MockResourceTracker.return_value
        mock_tracker_instance.update_resource.side_effect = ValueError("Quantity cannot be negative.")
        main()
        self.assertIn("Error: Quantity cannot be negative.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
