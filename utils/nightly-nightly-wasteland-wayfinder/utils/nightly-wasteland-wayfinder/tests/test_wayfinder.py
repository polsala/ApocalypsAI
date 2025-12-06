import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Temporarily add src to sys.path to import wayfinder.py
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import wayfinder
sys.path.pop(0) # Remove it after import

class TestWastelandWayfinder(unittest.TestCase):

    def setUp(self):
        # Reset the mocked file content before each test
        self.mock_file_content = "[]"
        self.mock_exists = False

    @patch('wayfinder._load_landmarks')
    @patch('wayfinder._save_landmarks')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_landmark(self, mock_stdout, mock_save, mock_load):
        # Mock rationale: `_load_landmarks` is mocked to control the initial state of the data.
        # `_save_landmarks` is mocked to verify that data is correctly persisted without actual file I/O.
        # `sys.stdout` is mocked to capture printed output for assertion.
        mock_load.return_value = []
        wayfinder.add_landmark("Test Bunker", "1,1", "safe_zone", "A cozy spot")
        mock_save.assert_called_once()
        self.assertIn("Landmark 'Test Bunker' added successfully.", mock_stdout.getvalue())

        # Test adding a duplicate
        mock_load.return_value = [{'name': 'Test Bunker', 'coords': '1,1', 'type': 'safe_zone', 'description': 'A cozy spot'}]
        mock_save.reset_mock() # Clear previous call
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        wayfinder.add_landmark("Test Bunker", "2,2", "danger_area")
        mock_save.assert_not_called()
        self.assertIn("Error: Landmark 'Test Bunker' already exists.", mock_stdout.getvalue())

    @patch('wayfinder._load_landmarks')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_landmarks(self, mock_stdout, mock_load):
        # Mock rationale: `_load_landmarks` is mocked to control the data being listed.
        # `sys.stdout` is mocked to capture printed output for assertion.
        # Test empty list
        mock_load.return_value = []
        wayfinder.list_landmarks()
        self.assertIn("No landmarks recorded yet.", mock_stdout.getvalue())

        # Test with data
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        mock_load.return_value = [
            {'name': 'Test Bunker', 'coords': '1,1', 'type': 'safe_zone', 'description': 'A cozy spot'},
            {'name': 'Mutant Lair', 'coords': '2,2', 'type': 'danger_area', 'description': None}
        ]
        wayfinder.list_landmarks()
        output = mock_stdout.getvalue()
        self.assertIn("Test Bunker", output)
        self.assertIn("Mutant Lair", output)
        self.assertIn("safe_zone (A cozy spot)", output)
        self.assertIn("danger_area", output)

    @patch('wayfinder._load_landmarks')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_landmarks(self, mock_stdout, mock_load):
        # Mock rationale: `_load_landmarks` is mocked to control the data being searched.
        # `sys.stdout` is mocked to capture printed output for assertion.
        mock_load.return_value = [
            {'name': 'Test Bunker', 'coords': '1,1', 'type': 'safe_zone', 'description': 'A cozy spot'},
            {'name': 'Mutant Lair', 'coords': '2,2', 'type': 'danger_area', 'description': None},
            {'name': 'Old Bunker', 'coords': '3,3', 'type': 'resource_cache', 'description': 'Empty'}
        ]

        # Find by name (partial)
        wayfinder.find_landmarks("bunker")
        output = mock_stdout.getvalue()
        self.assertIn("Test Bunker", output)
        self.assertIn("Old Bunker", output)
        self.assertNotIn("Mutant Lair", output)

        # Find by type
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        wayfinder.find_landmarks("danger_area")
        output = mock_stdout.getvalue()
        self.assertIn("Mutant Lair", output)
        self.assertNotIn("Test Bunker", output)

        # No match
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        wayfinder.find_landmarks("non_existent")
        self.assertIn("No landmarks found matching 'non_existent'.", mock_stdout.getvalue())

    @patch('wayfinder._load_landmarks')
    @patch('wayfinder._save_landmarks')
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_landmark(self, mock_stdout, mock_save, mock_load):
        # Mock rationale: `_load_landmarks` is mocked to control the initial data state.
        # `_save_landmarks` is mocked to verify the updated data is correctly persisted.
        # `sys.stdout` is mocked to capture printed output for assertion.
        initial_landmarks = [
            {'name': 'Test Bunker', 'coords': '1,1', 'type': 'safe_zone', 'description': 'A cozy spot'},
            {'name': 'Mutant Lair', 'coords': '2,2', 'type': 'danger_area', 'description': None}
        ]
        mock_load.return_value = list(initial_landmarks) # Use list() to ensure a copy

        # Remove existing
        wayfinder.remove_landmark("Test Bunker")
        mock_save.assert_called_once_with([{'name': 'Mutant Lair', 'coords': '2,2', 'type': 'danger_area', 'description': None}])
        self.assertIn("Landmark 'Test Bunker' removed successfully.", mock_stdout.getvalue())

        # Remove non-existent
        mock_load.return_value = list(initial_landmarks) # Reset for next test
        mock_save.reset_mock()
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        wayfinder.remove_landmark("Non Existent")
        mock_save.assert_not_called()
        self.assertIn("Error: Landmark 'Non Existent' not found.", mock_stdout.getvalue())

    @patch('wayfinder.sys.argv', ['wayfinder.py', 'add', 'New Spot', '4,4', 'resource_cache'])
    @patch('wayfinder.add_landmark')
    def test_main_add(self, mock_add_landmark):
        # Mock rationale: `sys.argv` is patched to simulate command-line arguments.
        # `add_landmark` is mocked to verify that `main` correctly parses arguments and calls the right function.
        wayfinder.main()
        mock_add_landmark.assert_called_once_with('New Spot', '4,4', 'resource_cache', None)

    @patch('wayfinder.sys.argv', ['wayfinder.py', 'list'])
    @patch('wayfinder.list_landmarks')
    def test_main_list(self, mock_list_landmarks):
        # Mock rationale: `sys.argv` is patched to simulate command-line arguments.
        # `list_landmarks` is mocked to verify that `main` correctly calls the right function.
        wayfinder.main()
        mock_list_landmarks.assert_called_once()

    @patch('wayfinder.sys.argv', ['wayfinder.py', 'find', 'bunker'])
    @patch('wayfinder.find_landmarks')
    def test_main_find(self, mock_find_landmarks):
        # Mock rationale: `sys.argv` is patched to simulate command-line arguments.
        # `find_landmarks` is mocked to verify that `main` correctly parses arguments and calls the right function.
        wayfinder.main()
        mock_find_landmarks.assert_called_once_with('bunker')

    @patch('wayfinder.sys.argv', ['wayfinder.py', 'remove', 'Old Spot'])
    @patch('wayfinder.remove_landmark')
    def test_main_remove(self, mock_remove_landmark):
        # Mock rationale: `sys.argv` is patched to simulate command-line arguments.
        # `remove_landmark` is mocked to verify that `main` correctly parses arguments and calls the right function.
        wayfinder.main()
        mock_remove_landmark.assert_called_once_with('Old Spot')

    @patch('wayfinder.sys.argv', ['wayfinder.py', 'unknown_command'])
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unknown_command(self, mock_stdout, mock_exit):
        # Mock rationale: `sys.argv` is patched to simulate an unknown command.
        # `sys.exit` is mocked to prevent the test from terminating prematurely.
        # `sys.stdout` is mocked to capture printed output for assertion.
        wayfinder.main()
        self.assertIn("Unknown command: unknown_command", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('wayfinder.sys.argv', ['wayfinder.py'])
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_command(self, mock_stdout, mock_exit):
        # Mock rationale: `sys.argv` is patched to simulate no command-line arguments.
        # `sys.exit` is mocked to prevent the test from terminating prematurely.
        # `sys.stdout` is mocked to capture printed output for assertion.
        wayfinder.main()
        self.assertIn("Usage: python wayfinder.py <command> [arguments]", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('wayfinder.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_landmarks_file_not_exists(self, mock_file_open, mock_path_exists):
        # Mock rationale: Simulate the scenario where DATA_FILE does not exist.
        # `os.path.exists` is mocked to return False, and `open` should not be called.
        mock_path_exists.return_value = False
        landmarks = wayfinder._load_landmarks()
        self.assertEqual(landmarks, [])
        mock_file_open.assert_not_called()

    @patch('wayfinder.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "A", "coords": "0,0", "type": "safe"}]')
    def test_load_landmarks_file_exists(self, mock_file_open, mock_path_exists):
        # Mock rationale: Simulate reading valid JSON data from DATA_FILE.
        # `os.path.exists` returns True, and `open` is mocked to return a file-like object
        # with predefined JSON content.
        mock_path_exists.return_value = True
        landmarks = wayfinder._load_landmarks()
        self.assertEqual(landmarks, [{"name": "A", "coords": "0,0", "type": "safe"}])
        mock_file_open.assert_called_once_with(wayfinder.DATA_FILE, 'r')

    @patch('wayfinder.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"corrupt": "json"')
    def test_load_landmarks_corrupt_file(self, mock_file_open, mock_path_exists):
        # Mock rationale: Simulate reading invalid JSON data from DATA_FILE.
        # `os.path.exists` returns True, and `open` is mocked to return corrupt JSON.
        # The function should handle `json.JSONDecodeError` gracefully.
        mock_path_exists.return_value = True
        landmarks = wayfinder._load_landmarks()
        self.assertEqual(landmarks, [])
        mock_file_open.assert_called_once_with(wayfinder.DATA_FILE, 'r')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_landmarks(self, mock_file_open):
        # Mock rationale: Simulate writing JSON data to DATA_FILE.
        # `open` is mocked to capture the written content.
        test_data = [{"name": "B", "coords": "1,1", "type": "danger"}]
        wayfinder._save_landmarks(test_data)
        mock_file_open.assert_called_once_with(wayfinder.DATA_FILE, 'w')
        mock_file_open().write.assert_called_once_with(json.dumps(test_data, indent=4))


if __name__ == '__main__':
    unittest.main()
