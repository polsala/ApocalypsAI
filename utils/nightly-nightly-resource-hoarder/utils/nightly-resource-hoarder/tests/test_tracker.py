import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Adjust sys.path to allow importing tracker.py from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import tracker
sys.path.pop(0) # Clean up sys.path

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Reset the RESOURCE_FILE for each test to ensure isolation
        self.test_file = 'test_resources.json'
        tracker.RESOURCE_FILE = self.test_file
        self.initial_resources = {
            "Canned Beans": 10,
            "Water Bottles": 5,
        }

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_existing(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing resource file with content.
        mock_exists.return_value = True
        mock_json_load.return_value = self.initial_resources

        resources = tracker.load_resources()
        self.assertEqual(resources, self.initial_resources)
        mock_exists.assert_called_once_with(self.test_file)
        mock_open_file.assert_called_once_with(self.test_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_resources_non_existing(self, mock_exists):
        # Mock rationale: Simulate no resource file existing.
        mock_exists.return_value = False

        resources = tracker.load_resources()
        self.assertEqual(resources, {})
        mock_exists.assert_called_once_with(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stderr', new_callable=StringIO)
    def test_load_resources_corrupted(self, mock_stderr, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        resources = tracker.load_resources()
        self.assertEqual(resources, {})
        self.assertIn("Warning: test_resources.json is corrupted or empty.", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_open_file):
        # Mock rationale: Simulate saving resources to a file.
        tracker.save_resources(self.initial_resources)
        mock_open_file.assert_called_once_with(self.test_file, 'w')
        mock_json_dump.assert_called_once_with(self.initial_resources, mock_open_file(), indent=4)

    def test_add_resource_new_item(self):
        resources = {}
        with patch('builtins.print') as mock_print:
            result = tracker.add_resource(resources, "First Aid Kit", 1)
            self.assertTrue(result)
            self.assertEqual(resources, {"First Aid Kit": 1})
            mock_print.assert_called_once_with("Added 1x First Aid Kit. Total: 1")

    def test_add_resource_existing_item(self):
        resources = {"Canned Beans": 10}
        with patch('builtins.print') as mock_print:
            result = tracker.add_resource(resources, "Canned Beans", 5)
            self.assertTrue(result)
            self.assertEqual(resources, {"Canned Beans": 15})
            mock_print.assert_called_once_with("Added 5x Canned Beans. Total: 15")

    def test_add_resource_invalid_quantity(self):
        resources = {}
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = tracker.add_resource(resources, "Water", 0)
            self.assertFalse(result)
            self.assertEqual(resources, {})
            self.assertIn("Error: Quantity must be a positive integer.", mock_stderr.getvalue())

    def test_remove_resource_existing_item(self):
        resources = {"Canned Beans": 10}
        with patch('builtins.print') as mock_print:
            result = tracker.remove_resource(resources, "Canned Beans", 3)
            self.assertTrue(result)
            self.assertEqual(resources, {"Canned Beans": 7})
            mock_print.assert_called_once_with("Removed 3x Canned Beans. Remaining: 7")

    def test_remove_resource_item_fully_removed(self):
        resources = {"Water Bottles": 5}
        with patch('builtins.print') as mock_print:
            result = tracker.remove_resource(resources, "Water Bottles", 5)
            self.assertTrue(result)
            self.assertEqual(resources, {})
            mock_print.assert_called_once_with("Removed all 5x Water Bottles. Item removed from inventory.")

    def test_remove_resource_item_over_removed(self):
        resources = {"First Aid Kit": 2}
        with patch('builtins.print') as mock_print:
            result = tracker.remove_resource(resources, "First Aid Kit", 5)
            self.assertTrue(result)
            self.assertEqual(resources, {})
            mock_print.assert_called_once_with("Removed all 2x First Aid Kit. Item removed from inventory.")

    def test_remove_resource_non_existing_item(self):
        resources = {"Canned Beans": 10}
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = tracker.remove_resource(resources, "Non Existent Item", 1)
            self.assertFalse(result)
            self.assertEqual(resources, {"Canned Beans": 10})
            self.assertIn("Error: 'Non Existent Item' not found in resources.", mock_stderr.getvalue())

    def test_remove_resource_invalid_quantity(self):
        resources = {"Canned Beans": 10}
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = tracker.remove_resource(resources, "Canned Beans", 0)
            self.assertFalse(result)
            self.assertEqual(resources, {"Canned Beans": 10})
            self.assertIn("Error: Quantity to remove must be a positive integer.", mock_stderr.getvalue())

    def test_list_resources_empty(self):
        resources = {}
        with patch('builtins.print') as mock_print:
            tracker.list_resources(resources)
            mock_print.assert_called_once_with("Your resource inventory is empty. Time to start hoarding!")

    def test_list_resources_non_empty(self):
        resources = {"Canned Beans": 10, "Water Bottles": 5}
        expected_output = (
            "\n--- Current Resource Inventory ---\n"
            "- Canned Beans: 10\n"
            "- Water Bottles: 5\n"
            "----------------------------------"
        )
        with patch('builtins.print') as mock_print:
            tracker.list_resources(resources)
            # Join calls to print for comparison
            actual_output = "\n".join(call.args[0] for call in mock_print.call_args_list)
            self.assertEqual(actual_output, expected_output)

    @patch('tracker.load_resources')
    @patch('tracker.save_resources')
    @patch('sys.argv', ['tracker.py', 'add', 'Food Rations', '10'])
    @patch('builtins.print') # Mock print to avoid actual output during test
    def test_main_add_command(self, mock_print, mock_save_resources, mock_load_resources):
        # Mock rationale: Simulate CLI arguments and mock underlying functions.
        initial_resources = {}
        mock_load_resources.return_value = initial_resources # load_resources returns a mutable dict
        
        tracker.main()
        
        mock_load_resources.assert_called_once()
        # Verify that initial_resources was modified in place
        self.assertEqual(initial_resources, {'Food Rations': 10}) 
        mock_save_resources.assert_called_once_with({'Food Rations': 10}) # save_resources gets the modified dict

    @patch('tracker.load_resources')
    @patch('tracker.save_resources')
    @patch('sys.argv', ['tracker.py', 'remove', 'Water Bottles', '2'])
    @patch('builtins.print') # Mock print to avoid actual output during test
    def test_main_remove_command(self, mock_print, mock_save_resources, mock_load_resources):
        # Mock rationale: Simulate CLI arguments and mock underlying functions.
        initial_resources = {"Water Bottles": 5}
        mock_load_resources.return_value = initial_resources # load_resources returns a mutable dict
        
        tracker.main()
        
        mock_load_resources.assert_called_once()
        # Verify that initial_resources was modified in place
        self.assertEqual(initial_resources, {'Water Bottles': 3})
        mock_save_resources.assert_called_once_with({'Water Bottles': 3}) # save_resources gets the modified dict

    @patch('tracker.load_resources')
    @patch('tracker.list_resources')
    @patch('sys.argv', ['tracker.py', 'list'])
    def test_main_list_command(self, mock_list_resources, mock_load_resources):
        # Mock rationale: Simulate CLI arguments and mock underlying functions.
        mock_load_resources.return_value = {"Canned Food": 10}
        tracker.main()
        mock_load_resources.assert_called_once()
        mock_list_resources.assert_called_once_with({"Canned Food": 10})

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['tracker.py'])
    def test_main_no_command(self, mock_stdout):
        # Mock rationale: Test help message when no command is given.
        with self.assertRaises(SystemExit) as cm: # argparse exits on no command
            tracker.main()
        self.assertEqual(cm.exception.code, 2) # Exit code 2 for argument parsing error
        self.assertIn("usage: tracker.py", mock_stdout.getvalue())
        self.assertIn("Available commands:", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
