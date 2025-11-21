import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# To make the import work when running tests from the tests/ directory
# we need to ensure the parent directory of manifest_manager.py is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import manifest_manager
sys.path.pop(0) # Clean up sys.path after import

class TestManifestManager(unittest.TestCase):

    def setUp(self):
        # Store original stdout to restore later
        self.original_stdout = sys.stdout
        # Redirect stdout to capture print statements
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

        # Define a temporary manifest file name for testing
        manifest_manager.MANIFEST_FILE = 'test_manifest.json' # Override for tests

    def tearDown(self):
        # Restore original stdout
        sys.stdout = self.original_stdout
        # Reset MANIFEST_FILE to its original value if needed, though tests should be isolated.
        manifest_manager.MANIFEST_FILE = 'manifest.json'

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_item_new(self, mock_dump, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate manifest file not existing initially, then adding an item.
        # mock_exists: Controls whether _load_manifest thinks the file exists.
        # mock_load: Provides initial data when _load_manifest is called.
        # mock_open_file: Captures file operations (read/write).
        # mock_dump: Captures data being written to the file.

        mock_exists.return_value = False # Manifest file does not exist initially
        mock_load.return_value = {"items": []} # _load_manifest returns empty manifest

        manifest_manager.add_item("Rusty Spanner", "Tools", 1)

        # Assert that json.dump was called with the correct data
        expected_manifest = {"items": [{"name": "Rusty Spanner", "category": "Tools", "quantity": 1}]}
        mock_dump.assert_called_once_with(expected_manifest, mock_open_file(), indent=4)
        self.assertIn("Added/Updated: Rusty Spanner (Tools, Qty: 1)", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_item_update_existing(self, mock_dump, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate manifest file existing with an item, then updating it.
        mock_exists.return_value = True
        initial_manifest = {"items": [{"name": "Canned Beans", "category": "Food", "quantity": 5}]}
        mock_load.return_value = initial_manifest

        manifest_manager.add_item("Canned Beans", "Food", 3) # Add 3 more beans

        expected_manifest = {"items": [{"name": "Canned Beans", "category": "Food", "quantity": 8}]}
        mock_dump.assert_called_once_with(expected_manifest, mock_open_file(), indent=4)
        self.assertIn("Added/Updated: Canned Beans (Food, Qty: 3)", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_items_empty(self, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty manifest file.
        mock_exists.return_value = False
        mock_load.return_value = {"items": []}

        manifest_manager.list_items()

        self.assertIn("Your manifest is currently empty. Go scavenge!", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_items_with_data(self, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a manifest file with data.
        mock_exists.return_value = True
        manifest_data = {
            "items": [
                {"name": "Rusty Spanner", "category": "Tools", "quantity": 1},
                {"name": "Canned Beans", "category": "Food", "quantity": 5}
            ]
        }
        mock_load.return_value = manifest_data

        manifest_manager.list_items()

        output = self.captured_output.getvalue()
        self.assertIn("--- Current Manifest ---", output)
        self.assertIn("Name: Rusty Spanner, Category: Tools, Quantity: 1", output)
        self.assertIn("Name: Canned Beans, Category: Food, Quantity: 5", output)
        self.assertIn("------------------------", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_search_items_found_by_name(self, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate searching for an item by name.
        mock_exists.return_value = True
        manifest_data = {
            "items": [
                {"name": "Rusty Spanner", "category": "Tools", "quantity": 1},
                {"name": "Canned Beans", "category": "Food", "quantity": 5}
            ]
        }
        mock_load.return_value = manifest_data

        manifest_manager.search_items("Spanner")

        output = self.captured_output.getvalue()
        self.assertIn("--- Search Results for 'Spanner' ---", output)
        self.assertIn("Name: Rusty Spanner, Category: Tools", output)
        self.assertNotIn("Canned Beans", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_search_items_found_by_category(self, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate searching for an item by category.
        mock_exists.return_value = True
        manifest_data = {
            "items": [
                {"name": "Rusty Spanner", "category": "Tools", "quantity": 1},
                {"name": "Canned Beans", "category": "Food", "quantity": 5},
                {"name": "Hammer", "category": "Tools", "quantity": 1}
            ]
        }
        mock_load.return_value = manifest_data

        manifest_manager.search_items("Tools")

        output = self.captured_output.getvalue()
        self.assertIn("--- Search Results for 'Tools' ---", output)
        self.assertIn("Name: Rusty Spanner, Category: Tools", output)
        self.assertIn("Name: Hammer, Category: Tools", output)
        self.assertNotIn("Canned Beans", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_search_items_not_found(self, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate searching for an item that doesn't exist.
        mock_exists.return_value = True
        manifest_data = {
            "items": [
                {"name": "Rusty Spanner", "category": "Tools", "quantity": 1}
            ]
        }
        mock_load.return_value = manifest_data

        manifest_manager.search_items("NonExistent")

        self.assertIn("No items found matching 'NonExistent'.", self.captured_output.getvalue())

    @patch('sys.argv', ['manifest_manager.py', 'add', 'New Item', 'Misc', '10'])
    @patch('manifest_manager.add_item')
    def test_main_add_command(self, mock_add_item):
        # Mock rationale: Test the main function's argument parsing for 'add' command.
        # sys.argv: Simulates command-line arguments.
        # manifest_manager.add_item: Mocks the actual function call to verify arguments.
        manifest_manager.main()
        mock_add_item.assert_called_once_with("New Item", "Misc", 10)

    @patch('sys.argv', ['manifest_manager.py', 'list'])
    @patch('manifest_manager.list_items')
    def test_main_list_command(self, mock_list_items):
        # Mock rationale: Test the main function's argument parsing for 'list' command.
        manifest_manager.main()
        mock_list_items.assert_called_once()

    @patch('sys.argv', ['manifest_manager.py', 'search', 'keyword'])
    @patch('manifest_manager.search_items')
    def test_main_search_command(self, mock_search_items):
        # Mock rationale: Test the main function's argument parsing for 'search' command.
        manifest_manager.main()
        mock_search_items.assert_called_once_with("keyword")

    @patch('sys.argv', ['manifest_manager.py', 'add', 'Invalid Item', 'Category', '0'])
    @patch('sys.exit')
    @patch('builtins.print') # Mock print to avoid actual stderr output in test logs
    def test_main_add_command_invalid_quantity(self, mock_print, mock_exit):
        # Mock rationale: Test handling of invalid quantity for 'add' command.
        # sys.exit: Mocks the exit call to prevent test termination.
        # builtins.print: Mocks print to capture stderr output.
        manifest_manager.main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Quantity must be a positive integer.", file=sys.stderr)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stderr', new_callable=StringIO) # Capture stderr
    def test_load_manifest_corrupted_json(self, mock_stderr, mock_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_exists.return_value = True
        mock_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        result = manifest_manager._load_manifest()
        self.assertEqual(result, {"items": []})
        self.assertIn("Warning: test_manifest.json is corrupted. Starting with an empty manifest.", mock_stderr.getvalue())
