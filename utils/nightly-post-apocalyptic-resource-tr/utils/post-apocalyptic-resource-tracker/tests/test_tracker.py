import unittest
from unittest.mock import patch, mock_open
import json
import io
import os
import sys

# Mock rationale: We need to isolate the tracker logic from actual file system operations.
# Mocking `open` allows us to simulate reading from and writing to `resources.json`
# without creating or modifying real files. This ensures tests are deterministic,
# fast, and don't leave artifacts.

# Mock rationale: `json.load` and `json.dump` are directly tied to file I/O.
# By mocking them, we control the data that is 'read' from the file and verify
# the data that is 'written' to it, ensuring the core logic of the tracker
# functions correctly with its data structures.

# Mock rationale: `os.path.exists` is used to check if the data file exists.
# Mocking it allows us to simulate scenarios where the file is present or absent
# without actual file system checks.

# Mock rationale: `os.path.dirname` and `os.path.abspath` are used to construct
# the path to the data file. Mocking them ensures that the `_get_data_path`
# function returns a predictable, test-controlled path, preventing reliance
# on the actual script location during tests.

class TestResourceTracker(unittest.TestCase):

    @patch('os.path.abspath', return_value='/mock/path/src/tracker.py')
    @patch('os.path.dirname', return_value='/mock/path/src')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def setUp(self, mock_json_dump, mock_json_load, mock_open_file, mock_exists, mock_dirname, mock_abspath):
        super().setUp()
        # Add the parent directory of 'tests' (which is the util root) to sys.path
        # so 'src.tracker' can be imported.
        self.original_sys_path = sys.path[:]
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        # Import tracker here to ensure mocks are active when it's loaded
        # and its _get_data_path is called.
        global tracker
        import src.tracker as tracker # Changed import path to be relative to util root
        self.tracker_module = tracker # Store reference for tearDown

        self.mock_json_dump = mock_json_dump
        self.mock_json_load = mock_json_load
        self.mock_open_file = mock_open_file
        self.mock_exists = mock_exists
        self.mock_dirname = mock_dirname
        self.mock_abspath = mock_abspath

        # Reset mocks for each test
        self.mock_json_dump.reset_mock()
        self.mock_json_load.reset_mock()
        self.mock_open_file.reset_mock()
        self.mock_exists.reset_mock()

        # Default behavior: file exists, contains empty data
        self.mock_exists.return_value = True
        self.mock_json_load.return_value = {}

        # Capture print output
        self.held_output = io.StringIO()
        self.patcher_stdout = patch('sys.stdout', self.held_output)
        self.patcher_stdout.start()

    def tearDown(self):
        self.patcher_stdout.stop()
        # Restore original sys.path
        sys.path = self.original_sys_path
        # Clean up the imported module to avoid state leakage between tests
        if 'src.tracker' in sys.modules:
            del sys.modules['src.tracker']
        # Remove global reference
        global tracker
        if 'tracker' in globals():
            del globals()['tracker']

    def test_add_resource_new(self):
        tracker.add_resource("Water", 10)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_called_once_with({"Water": 10}, self.mock_open_file(), indent=4)
        self.assertIn("Added 10 of 'Water'. Current total: 10", self.held_output.getvalue())

    def test_add_resource_existing(self):
        self.mock_json_load.return_value = {"Water": 5}
        tracker.add_resource("Water", 3)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_called_once_with({"Water": 8}, self.mock_open_file(), indent=4)
        self.assertIn("Added 3 of 'Water'. Current total: 8", self.held_output.getvalue())

    def test_add_resource_zero_quantity(self):
        tracker.add_resource("Food", 0)
        self.mock_json_load.assert_not_called()
        self.mock_json_dump.assert_not_called()
        self.assertIn("Quantity must be positive.", self.held_output.getvalue())

    def test_consume_resource_success(self):
        self.mock_json_load.return_value = {"Food": 10, "Water": 5}
        result = tracker.consume_resource("Food", 3)
        self.assertTrue(result)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_called_once_with({"Food": 7, "Water": 5}, self.mock_open_file(), indent=4)
        self.assertIn("Consumed 3 of 'Food'. Remaining: 7", self.held_output.getvalue())

    def test_consume_resource_not_enough(self):
        self.mock_json_load.return_value = {"Food": 2}
        result = tracker.consume_resource("Food", 5)
        self.assertFalse(result)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_not_called()
        self.assertIn("Error: Not enough 'Food' to consume 5. Available: 2", self.held_output.getvalue())

    def test_consume_resource_not_exist(self):
        self.mock_json_load.return_value = {}
        result = tracker.consume_resource("Medicine", 1)
        self.assertFalse(result)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_not_called()
        self.assertIn("Error: Not enough 'Medicine' to consume 1. Available: 0", self.held_output.getvalue())

    def test_consume_resource_zero_quantity(self):
        self.mock_json_load.return_value = {"Food": 5}
        result = tracker.consume_resource("Food", 0)
        self.assertIsNone(result) # Function returns None if quantity is invalid
        self.mock_json_load.assert_not_called()
        self.mock_json_dump.assert_not_called()
        self.assertIn("Quantity must be positive.", self.held_output.getvalue())

    def test_consume_resource_to_zero(self):
        self.mock_json_load.return_value = {"Food": 5, "Water": 10}
        result = tracker.consume_resource("Food", 5)
        self.assertTrue(result)
        self.mock_json_load.assert_called_once()
        self.mock_json_dump.assert_called_once_with({"Water": 10}, self.mock_open_file(), indent=4)
        self.assertIn("Consumed 5 of 'Food'. Remaining: 0", self.held_output.getvalue())

    def test_list_resources_empty(self):
        self.mock_json_load.return_value = {}
        tracker.list_resources()
        self.mock_json_load.assert_called_once()
        self.assertIn("No resources currently tracked. Time to scavenge!", self.held_output.getvalue())

    def test_list_resources_with_items(self):
        self.mock_json_load.return_value = {"Water": 5, "Food": 10, "Medicine": 2}
        tracker.list_resources()
        self.mock_json_load.assert_called_once()
        expected_output = (
            "--- Current Resources ---\n"
            "- Food: 10\n"
            "- Medicine: 2\n"
            "- Water: 5\n"
            "-------------------------"
        )
        self.assertIn(expected_output, self.held_output.getvalue())

    def test_load_data_file_not_exists(self):
        self.mock_exists.return_value = False
        resources = tracker._load_data()
        self.assertEqual(resources, {})
        self.mock_exists.assert_called_once()
        self.mock_open_file.assert_not_called()
        self.mock_json_load.assert_not_called()

    def test_load_data_corrupted_json(self):
        self.mock_exists.return_value = True
        # Simulate a corrupted file by making json.load raise an error
        self.mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        resources = tracker._load_data()
        self.assertEqual(resources, {})
        self.mock_exists.assert_called_once()
        self.mock_open_file.assert_called_once_with(tracker._get_data_path(), 'r')
        self.mock_json_load.assert_called_once()
        self.assertIn("Warning: resources.json is corrupted. Starting with empty resources.", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()
