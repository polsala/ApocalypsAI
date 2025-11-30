import unittest
import json
import os
from unittest.mock import patch, mock_open
from io import StringIO
import sys

# Adjusting sys.path to allow importing the module from src/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, os.path.join(project_root, 'src'))

from waypoint_weaver import WaypointManager, main, WAYPOINTS_FILE

class TestWaypointManager(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.test_file = "test_waypoints.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = WaypointManager(self.test_file)

    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_waypoints_existing_file(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing waypoints file with content.
        mock_exists.return_value = True
        mock_json_load.return_value = [{"name": "Test", "description": "Desc", "coordinates": "0,0"}]
        
        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "Test")
        mock_exists.assert_called_with(self.test_file)
        mock_open_file.assert_called_with(self.test_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_waypoints_no_file(self, mock_exists):
        # Mock rationale: Simulate no existing waypoints file.
        mock_exists.return_value = False
        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 0)
        mock_exists.assert_called_with(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stderr', new_callable=StringIO)
    def test_load_waypoints_corrupted_file(self, mock_stderr, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        
        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 0)
        self.assertIn("Warning: test_waypoints.json is corrupted.", mock_stderr.getvalue())

    @patch('src.waypoint_weaver.WaypointManager._save_waypoints') # Mock internal save
    def test_add_waypoint(self, mock_save):
        # Mock rationale: Prevent actual file writes during add operation.
        self.assertTrue(self.manager.add_waypoint("Bunker A", "Safe zone", "10,20"))
        self.assertEqual(len(self.manager.waypoints), 1)
        self.assertEqual(self.manager.waypoints[0]['name'], "Bunker A")
        mock_save.assert_called_once()

    @patch('src.waypoint_weaver.WaypointManager._save_waypoints')
    @patch('sys.stderr', new_callable=StringIO)
    def test_add_duplicate_waypoint(self, mock_stderr, mock_save):
        # Mock rationale: Prevent actual file writes and capture stderr.
        self.manager.add_waypoint("Bunker A", "Safe zone")
        self.assertFalse(self.manager.add_waypoint("Bunker A", "Another desc"))
        self.assertEqual(len(self.manager.waypoints), 1) # Should not add duplicate
        self.assertIn("Error: Waypoint 'Bunker A' already exists.", mock_stderr.getvalue())
        mock_save.assert_called_once() # Only called for the first successful add

    def test_list_waypoints(self):
        self.manager.add_waypoint("Bunker A", "Safe zone")
        self.manager.add_waypoint("Rubble Pile", "Scavenge point")
        waypoints = self.manager.list_waypoints()
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[0]['name'], "Bunker A")
        self.assertEqual(waypoints[1]['name'], "Rubble Pile")

    @patch('src.waypoint_weaver.WaypointManager._save_waypoints')
    def test_remove_waypoint(self, mock_save):
        # Mock rationale: Prevent actual file writes during remove operation.
        self.manager.add_waypoint("Bunker A", "Safe zone")
        self.manager.add_waypoint("Rubble Pile", "Scavenge point")
        self.assertTrue(self.manager.remove_waypoint("Bunker A"))
        self.assertEqual(len(self.manager.waypoints), 1)
        self.assertEqual(self.manager.waypoints[0]['name'], "Rubble Pile")
        mock_save.assert_called_once()

    @patch('src.waypoint_weaver.WaypointManager._save_waypoints')
    @patch('sys.stderr', new_callable=StringIO)
    def test_remove_non_existent_waypoint(self, mock_stderr, mock_save):
        # Mock rationale: Prevent actual file writes and capture stderr.
        self.manager.add_waypoint("Bunker A", "Safe zone")
        self.assertFalse(self.manager.remove_waypoint("NonExistent"))
        self.assertEqual(len(self.manager.waypoints), 1) # Should not change
        self.assertIn("Error: Waypoint 'NonExistent' not found.", mock_stderr.getvalue())
        mock_save.assert_not_called() # No save if nothing removed

    @patch('src.waypoint_weaver.WaypointManager') # Mock the entire manager for main function tests
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_add_command(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Isolate the main function from actual WaypointManager behavior and file I/O.
        # Capture stdout/stderr and prevent sys.exit from terminating the test.
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.add_waypoint.return_value = True

        sys.argv = ["waypoint_weaver.py", "add", "New Camp", "Fresh water source"]
        main()
        mock_manager_instance.add_waypoint.assert_called_with("New Camp", "Fresh water source", None)
        self.assertIn("Waypoint 'New Camp' added.", mock_stdout.getvalue())
        mock_exit.assert_not_called()

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_list_command(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Isolate the main function from actual WaypointManager behavior and file I/O.
        # Capture stdout/stderr and prevent sys.exit from terminating the test.
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.list_waypoints.return_value = [
            {"name": "Old Bunker", "description": "Abandoned military bunker", "coordinates": "N/A"}
        ]

        sys.argv = ["waypoint_weaver.py", "list"]
        main()
        mock_manager_instance.list_waypoints.assert_called_once()
        self.assertIn("Name: Old Bunker", mock_stdout.getvalue())
        self.assertIn("Description: Abandoned military bunker", mock_stdout.getvalue())
        mock_exit.assert_not_called()

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_remove_command(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Isolate the main function from actual WaypointManager behavior and file I/O.
        # Capture stdout/stderr and prevent sys.exit from terminating the test.
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.remove_waypoint.return_value = True

        sys.argv = ["waypoint_weaver.py", "remove", "Old Bunker"]
        main()
        mock_manager_instance.remove_waypoint.assert_called_with("Old Bunker")
        self.assertIn("Waypoint 'Old Bunker' removed.", mock_stdout.getvalue())
        mock_exit.assert_not_called()

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_invalid_command(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Capture stderr and prevent sys.exit from terminating the test.
        sys.argv = ["waypoint_weaver.py", "unknown_command"]
        main()
        self.assertIn("Unknown command: unknown_command", mock_stderr.getvalue())
        mock_exit.assert_called_with(1)

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_add_missing_args(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Capture stderr and prevent sys.exit from terminating the test.
        sys.argv = ["waypoint_weaver.py", "add", "NameOnly"]
        main()
        self.assertIn("Usage: python waypoint_weaver.py add <name> <description> [coordinates]", mock_stderr.getvalue())
        mock_exit.assert_called_with(1)

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_remove_missing_args(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Capture stderr and prevent sys.exit from terminating the test.
        sys.argv = ["waypoint_weaver.py", "remove"]
        main()
        self.assertIn("Usage: python waypoint_weaver.py remove <name>", mock_stderr.getvalue())
        mock_exit.assert_called_with(1)

    @patch('src.waypoint_weaver.WaypointManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_stderr, mock_stdout, MockWaypointManager):
        # Mock rationale: Capture stdout/stderr and prevent sys.exit from terminating the test.
        sys.argv = ["waypoint_weaver.py"]
        main()
        self.assertIn("Usage:", mock_stdout.getvalue())
        mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
