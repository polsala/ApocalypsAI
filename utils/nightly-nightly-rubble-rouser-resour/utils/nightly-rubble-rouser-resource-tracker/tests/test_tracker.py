import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Mock rationale: We need to mock the file system interactions (os.path.exists, open, json.load, json.dump)
# to ensure tests are deterministic, offline, and don't create actual files.

# Adjust path to import tracker.py from src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import ResourceTracker
sys.path.pop(0)

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Common setup for tests
        self.data_file = 'resources.json'

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_existing_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing data file with content.
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = {'water': 10, 'food': 5}

        tracker = ResourceTracker(self.data_file)
        self.assertEqual(tracker.resources, {'water': 10, 'food': 5})
        mock_os_path_exists.assert_called_once_with(self.data_file)
        mock_file_open.assert_called_once_with(self.data_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_resources_no_file(self, mock_os_path_exists):
        # Mock rationale: Simulate no existing data file.
        mock_os_path_exists.return_value = False

        tracker = ResourceTracker(self.data_file)
        self.assertEqual(tracker.resources, {})
        mock_os_path_exists.assert_called_once_with(self.data_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError('Expecting value', 'doc', 0))
    def test_load_resources_malformed_json(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate a malformed JSON file.
        mock_os_path_exists.return_value = True

        tracker = ResourceTracker(self.data_file)
        self.assertEqual(tracker.resources, {})
        mock_os_path_exists.assert_called_once_with(self.data_file)
        mock_file_open.assert_called_once_with(self.data_file, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False)
    def test_add_resource(self, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Test adding a resource without actual file I/O.
        tracker = ResourceTracker(self.data_file)
        tracker.add_resource('water', 5)
        self.assertEqual(tracker.resources, {'water': 5})
        mock_json_dump.assert_called_once_with({'water': 5}, mock_file_open(), indent=2)

        mock_json_dump.reset_mock() # Reset mock call count for subsequent calls
        tracker.add_resource('water', 3)
        self.assertEqual(tracker.resources, {'water': 8})
        mock_json_dump.assert_called_once_with({'water': 8}, mock_file_open(), indent=2)

        mock_json_dump.reset_mock()
        tracker.add_resource('food', 2)
        self.assertEqual(tracker.resources, {'water': 8, 'food': 2})
        mock_json_dump.assert_called_once_with({'water': 8, 'food': 2}, mock_file_open(), indent=2)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'water': 10, 'food': 5})
    def test_remove_resource(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Test removing a resource without actual file I/O.
        tracker = ResourceTracker(self.data_file)
        tracker.remove_resource('water', 3)
        self.assertEqual(tracker.resources, {'water': 7, 'food': 5})
        mock_json_dump.assert_called_once_with({'water': 7, 'food': 5}, mock_file_open(), indent=2)

        mock_json_dump.reset_mock()
        tracker.remove_resource('food', 5)
        self.assertEqual(tracker.resources, {'water': 7})
        mock_json_dump.assert_called_once_with({'water': 7}, mock_file_open(), indent=2)

        # Try to remove non-existent resource
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            tracker.remove_resource('scrap', 1)
            self.assertIn("Resource 'scrap' not found", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {'water': 7})
        mock_json_dump.assert_not_called() # No save on non-existent resource removal attempt

        # Remove more than available, should deplete and remove
        mock_json_dump.reset_mock()
        tracker.remove_resource('water', 10)
        self.assertEqual(tracker.resources, {})
        mock_json_dump.assert_called_once_with({}, mock_file_open(), indent=2)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'water': 10, 'food': 5})
    def test_set_resource(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Test setting a resource without actual file I/O.
        tracker = ResourceTracker(self.data_file)
        tracker.set_resource('water', 20)
        self.assertEqual(tracker.resources, {'water': 20, 'food': 5})
        mock_json_dump.assert_called_once_with({'water': 20, 'food': 5}, mock_file_open(), indent=2)

        mock_json_dump.reset_mock()
        tracker.set_resource('food', 0)
        self.assertEqual(tracker.resources, {'water': 20})
        mock_json_dump.assert_called_once_with({'water': 20}, mock_file_open(), indent=2)

        mock_json_dump.reset_mock()
        tracker.set_resource('new_item', 7)
        self.assertEqual(tracker.resources, {'water': 20, 'new_item': 7})
        mock_json_dump.assert_called_once_with({'water': 20, 'new_item': 7}, mock_file_open(), indent=2)

        # Set existing item to 0
        mock_json_dump.reset_mock()
        tracker.set_resource('water', 0)
        self.assertEqual(tracker.resources, {'new_item': 7})
        mock_json_dump.assert_called_once_with({'new_item': 7}, mock_file_open(), indent=2)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'water': 10, 'food': 5, 'scrap': 20})
    def test_list_resources(self, mock_json_load, mock_os_path_exists, mock_stdout):
        # Mock rationale: Capture stdout to verify printed output without actual file I/O.
        tracker = ResourceTracker(self.data_file)
        tracker.list_resources()
        # Resources are sorted alphabetically for consistent output
        expected_output = "Current Resources:\n  food: 5\n  scrap: 20\n  water: 10\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.path.exists', return_value=False)
    def test_list_resources_empty(self, mock_os_path_exists, mock_stdout):
        # Mock rationale: Capture stdout to verify printed output for an empty inventory.
        tracker = ResourceTracker(self.data_file)
        tracker.list_resources()
        expected_output = "Your inventory is currently empty. Time to scavenge!\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False)
    def test_add_resource_invalid_quantity(self, mock_os_path_exists, mock_json_dump, mock_file_open, mock_stdout):
        # Mock rationale: Test input validation for add_resource.
        tracker = ResourceTracker(self.data_file)
        tracker.add_resource('water', 0)
        self.assertIn("Quantity for 'water' must be positive to add.", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {})
        mock_json_dump.assert_not_called()

        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        tracker.add_resource('water', -5)
        self.assertIn("Quantity for 'water' must be positive to add.", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {})
        mock_json_dump.assert_not_called()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'water': 10})
    def test_remove_resource_invalid_quantity(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open, mock_stdout):
        # Mock rationale: Test input validation for remove_resource.
        tracker = ResourceTracker(self.data_file)
        tracker.remove_resource('water', 0)
        self.assertIn("Quantity for 'water' must be positive to remove.", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {'water': 10})
        mock_json_dump.assert_not_called()

        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        tracker.remove_resource('water', -5)
        self.assertIn("Quantity for 'water' must be positive to remove.", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {'water': 10})
        mock_json_dump.assert_not_called()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'water': 10})
    def test_set_resource_invalid_quantity(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open, mock_stdout):
        # Mock rationale: Test input validation for set_resource.
        tracker = ResourceTracker(self.data_file)
        tracker.set_resource('water', -5)
        self.assertIn("Quantity for 'water' cannot be negative.", mock_stdout.getvalue())
        self.assertEqual(tracker.resources, {'water': 10})
        mock_json_dump.assert_not_called()

if __name__ == '__main__':
    unittest.main()
