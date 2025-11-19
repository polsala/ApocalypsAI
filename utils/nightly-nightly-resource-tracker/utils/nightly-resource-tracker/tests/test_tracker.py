import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust sys.path to allow importing the tracker module from src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker

class TestTracker(unittest.TestCase):

    def setUp(self):
        self.inventory_file_name = "inventory.json"
        self.mock_inventory_path = os.path.join("/mock/path/src", self.inventory_file_name)
        self.empty_inventory_json = "[]"
        self.sample_inventory_data = [
            {"name": "Canned Beans", "quantity": 5, "location": "Pantry"},
            {"name": "Water Bottle", "quantity": 2, "location": "Backpack"}
        ]
        self.sample_inventory_json = json.dumps(self.sample_inventory_data, indent=4)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    @patch('os.path.dirname', return_value='/mock/path/src') # Mock rationale: Ensure consistent base path for inventory file.
    @patch('os.path.abspath', return_value='/mock/path/src/tracker.py') # Mock rationale: Ensure consistent absolute path for tracker.py.
    def test_load_inventory_empty(self, mock_abspath, mock_dirname, mock_join, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty or non-existent inventory file.
        mock_exists.return_value = False
        mock_join.return_value = self.mock_inventory_path
        
        inventory = tracker.load_inventory()
        self.assertEqual(inventory, [])
        mock_exists.assert_called_with(self.mock_inventory_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    @patch('os.path.dirname', return_value='/mock/path/src') # Mock rationale: Ensure consistent base path for inventory file.
    @patch('os.path.abspath', return_value='/mock/path/src/tracker.py') # Mock rationale: Ensure consistent absolute path for tracker.py.
    def test_load_inventory_existing(self, mock_abspath, mock_dirname, mock_join, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing inventory file with data.
        mock_exists.return_value = True
        mock_open_file.return_value.read.return_value = self.sample_inventory_json
        mock_join.return_value = self.mock_inventory_path

        inventory = tracker.load_inventory()
        self.assertEqual(inventory, self.sample_inventory_data)
        mock_exists.assert_called_with(self.mock_inventory_path)
        mock_open_file.assert_called_with(self.mock_inventory_path, 'r', encoding='utf-8')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    @patch('os.path.dirname', return_value='/mock/path/src') # Mock rationale: Ensure consistent base path for inventory file.
    @patch('os.path.abspath', return_value='/mock/path/src/tracker.py') # Mock rationale: Ensure consistent absolute path for tracker.py.
    def test_save_inventory(self, mock_abspath, mock_dirname, mock_join, mock_open_file, mock_exists):
        # Mock rationale: Verify that inventory data is correctly serialized and written to file.
        mock_join.return_value = self.mock_inventory_path
        
        tracker.save_inventory(self.sample_inventory_data)
        mock_open_file.assert_called_with(self.mock_inventory_path, 'w', encoding='utf-8')
        mock_open_file().write.assert_called_once_with(self.sample_inventory_json)

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_add_resource_new(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate adding a new resource to an empty inventory.
        mock_load.return_value = []
        
        tracker.add_resource("First Aid Kit", 1, "Medical Box")
        mock_load.assert_called_once()
        mock_save.assert_called_once_with([{"name": "First Aid Kit", "quantity": 1, "location": "Medical Box"}])
        self.assertIn("Added 1x First Aid Kit at Medical Box.", mock_stdout.getvalue())

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_add_resource_existing(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate adding more quantity to an existing resource, and updating its location.
        mock_load.return_value = [{"name": "Canned Beans", "quantity": 5, "location": "Pantry"}]
        
        tracker.add_resource("Canned Beans", 3, "Kitchen Shelf") # Location should update
        mock_load.assert_called_once()
        mock_save.assert_called_once_with([{"name": "Canned Beans", "quantity": 8, "location": "Kitchen Shelf"}])
        self.assertIn("Added 3x Canned Beans at Kitchen Shelf.", mock_stdout.getvalue())

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_remove_resource_partial(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate removing a partial quantity of an existing resource.
        mock_load.return_value = [{"name": "Canned Beans", "quantity": 5, "location": "Pantry"}]
        
        tracker.remove_resource("Canned Beans", 2)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with([{"name": "Canned Beans", "quantity": 3, "location": "Pantry"}])
        self.assertIn("Removed 2x Canned Beans. Remaining: 3.", mock_stdout.getvalue())

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_remove_resource_all(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate removing all quantity of an existing resource, leading to its removal from inventory.
        mock_load.return_value = [{"name": "Water Bottle", "quantity": 2, "location": "Backpack"}]
        
        tracker.remove_resource("Water Bottle", 2)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with([])
        self.assertIn("Removed all Water Bottle (quantity dropped to 0 or less).", mock_stdout.getvalue())

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_remove_resource_more_than_available(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate attempting to remove more quantity than available, leading to removal.
        mock_load.return_value = [{"name": "Water Bottle", "quantity": 1, "location": "Backpack"}]
        
        tracker.remove_resource("Water Bottle", 5)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with([])
        self.assertIn("Removed all Water Bottle (quantity dropped to 0 or less).", mock_stdout.getvalue())

    @patch('tracker.save_inventory')
    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_remove_resource_not_found(self, mock_stdout, mock_load, mock_save):
        # Mock rationale: Simulate attempting to remove a resource that doesn't exist.
        mock_load.return_value = self.sample_inventory_data
        
        tracker.remove_resource("NonExistent Item", 1)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with(self.sample_inventory_data) # Inventory should not change
        self.assertIn("Resource 'NonExistent Item' not found in inventory.", mock_stdout.getvalue())

    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_list_resources_empty(self, mock_stdout, mock_load):
        # Mock rationale: Simulate an empty inventory when listing.
        mock_load.return_value = []
        
        tracker.list_resources()
        mock_load.assert_called_once()
        self.assertIn("Inventory is empty. Time to start scavenging!", mock_stdout.getvalue())

    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_list_resources_existing(self, mock_stdout, mock_load):
        # Mock rationale: Simulate an existing inventory when listing.
        mock_load.return_value = self.sample_inventory_data
        
        tracker.list_resources()
        mock_load.assert_called_once()
        output = mock_stdout.getvalue()
        self.assertIn("--- Current Inventory ---", output)
        self.assertIn("- Canned Beans (x5) at Pantry", output)
        self.assertIn("- Water Bottle (x2) at Backpack", output)

    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_search_resources_found_name(self, mock_stdout, mock_load):
        # Mock rationale: Simulate searching for a resource by name.
        mock_load.return_value = self.sample_inventory_data
        
        tracker.search_resources("beans")
        mock_load.assert_called_once()
        output = mock_stdout.getvalue()
        self.assertIn("--- Search Results for 'beans' ---", output)
        self.assertIn("- Canned Beans (x5) at Pantry", output)
        self.assertNotIn("- Water Bottle (x2) at Backpack", output)

    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_search_resources_found_location(self, mock_stdout, mock_load):
        # Mock rationale: Simulate searching for a resource by location.
        mock_load.return_value = self.sample_inventory_data
        
        tracker.search_resources("backpack")
        mock_load.assert_called_once()
        output = mock_stdout.getvalue()
        self.assertIn("--- Search Results for 'backpack' ---", output)
        self.assertIn("- Water Bottle (x2) at Backpack", output)
        self.assertNotIn("- Canned Beans (x5) at Pantry", output)

    @patch('tracker.load_inventory')
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print statements for verification.
    def test_search_resources_not_found(self, mock_stdout, mock_load):
        # Mock rationale: Simulate searching for a resource that doesn't exist.
        mock_load.return_value = self.sample_inventory_data
        
        tracker.search_resources("flashlight")
        mock_load.assert_called_once()
        self.assertIn("No resources found matching 'flashlight'. Keep looking!", mock_stdout.getvalue())

    @patch('tracker.add_resource')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_add_command(self, mock_parse_args, mock_add_resource):
        # Mock rationale: Simulate CLI argument parsing for the 'add' command.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", name="Rope", quantity=10, location="Garage"
        )
        tracker.main()
        mock_add_resource.assert_called_once_with("Rope", 10, "Garage")

    @patch('tracker.remove_resource')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_remove_command(self, mock_parse_args, mock_remove_resource):
        # Mock rationale: Simulate CLI argument parsing for the 'remove' command.
        mock_parse_args.return_value = argparse.Namespace(
            command="remove", name="Rope", quantity=5
        )
        tracker.main()
        mock_remove_resource.assert_called_once_with("Rope", 5)

    @patch('tracker.list_resources')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_command(self, mock_parse_args, mock_list_resources):
        # Mock rationale: Simulate CLI argument parsing for the 'list' command.
        mock_parse_args.return_value = argparse.Namespace(
            command="list"
        )
        tracker.main()
        mock_list_resources.assert_called_once()

    @patch('tracker.search_resources')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_search_command(self, mock_parse_args, mock_search_resources):
        # Mock rationale: Simulate CLI argument parsing for the 'search' command.
        mock_parse_args.return_value = argparse.Namespace(
            command="search", query="water"
        )
        tracker.main()
        mock_search_resources.assert_called_once_with("water")

    @patch('argparse.ArgumentParser.print_help')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_command(self, mock_parse_args, mock_print_help):
        # Mock rationale: Simulate running the script without any command.
        mock_parse_args.return_value = argparse.Namespace(command=None)
        tracker.main()
        mock_print_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
