import unittest
import json
import os
from unittest.mock import patch, mock_open
import io
import sys

# Add src directory to sys.path for importing the utility module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from waypoint_weaver import WaypointManager, main
sys.path.pop(0)

class TestWaypointManager(unittest.TestCase):

    def setUp(self):
        # Mock the data file path to ensure tests are isolated and don't touch real files
        self.mock_data_file = 'mock_waypoints.json'
        # Ensure no real file exists from previous runs
        if os.path.exists(self.mock_data_file):
            os.remove(self.mock_data_file)

    def tearDown(self):
        # Clean up mock file if it was created during a test
        if os.path.exists(self.mock_data_file):
            os.remove(self.mock_data_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_loads_existing_waypoints(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing waypoints file with content.
        # `os.path.exists` is mocked to return True, and `builtins.open` is mocked
        # to return a file-like object with predefined JSON content.
        mock_os_exists.return_value = True
        mock_file_open.return_value.read.return_value = json.dumps([
            {"name": "Test1", "lat": 1.0, "lon": 2.0, "description": "Desc1", "danger_level": "Safe"}
        ])

        manager = WaypointManager(self.mock_data_file)
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "Test1")
        mock_os_exists.assert_called_with(self.mock_data_file)
        mock_file_open.assert_called_with(self.mock_data_file, 'r')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_handles_no_existing_waypoints(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate no existing waypoints file.
        # `os.path.exists` is mocked to return False, so `open` should not be called for reading.
        mock_os_exists.return_value = False

        manager = WaypointManager(self.mock_data_file)
        self.assertEqual(len(manager.waypoints), 0)
        mock_os_exists.assert_called_with(self.mock_data_file)
        mock_file_open.assert_not_called()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_init_handles_corrupted_json(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        # `os.path.exists` returns True, but `open` provides invalid JSON, leading to JSONDecodeError.
        mock_file_open.return_value.read.return_value = "{invalid json"

        manager = WaypointManager(self.mock_data_file)
        self.assertEqual(len(manager.waypoints), 0)
        self.assertEqual(manager.waypoints, [])

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_waypoint_success(self, mock_os_exists, mock_file_open):
        # Mock rationale: Simulate adding a new waypoint to an empty state.
        # `os.path.exists` returns False initially, and `open` is mocked for writing the new state.
        manager = WaypointManager(self.mock_data_file)
        result = manager.add_waypoint("New Spot", 10.0, 20.0, "A fresh start", "Safe")
        self.assertTrue(result)
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "New Spot")
        mock_file_open.assert_called_with(self.mock_data_file, 'w')
        handle = mock_file_open()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        self.assertEqual(written_data[0]['name'], "New Spot")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_waypoint_duplicate_name(self, mock_os_exists, mock_file_open):
        # Mock rationale: Simulate adding a waypoint with a name that already exists.
        # The manager is initialized with one waypoint, then an attempt is made to add another with the same name.
        manager = WaypointManager(self.mock_data_file)
        manager.waypoints.append({"name": "Existing", "lat": 1.0, "lon": 2.0, "description": "Desc", "danger_level": "Safe"})
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            result = manager.add_waypoint("Existing", 10.0, 20.0, "Another Desc", "Caution")
            self.assertFalse(result)
            self.assertEqual(len(manager.waypoints), 1) # Should not add a duplicate
            self.assertIn("Error: Waypoint 'Existing' already exists.", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_waypoint_invalid_danger_level(self, mock_os_exists, mock_file_open):
        # Mock rationale: Simulate adding a waypoint with an invalid danger level.
        manager = WaypointManager(self.mock_data_file)
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            result = manager.add_waypoint("Invalid Spot", 10.0, 20.0, "Bad level", "Apocalypse Now")
            self.assertFalse(result)
            self.assertEqual(len(manager.waypoints), 0)
            self.assertIn("Error: Invalid danger level 'Apocalypse Now'.", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_remove_waypoint_success(self, mock_os_exists, mock_file_open):
        # Mock rationale: Simulate removing an existing waypoint.
        # The manager is initialized with two waypoints, then one is removed.
        manager = WaypointManager(self.mock_data_file)
        manager.waypoints.extend([
            {"name": "To Remove", "lat": 1.0, "lon": 2.0, "description": "Desc1", "danger_level": "Safe"},
            {"name": "Keep Me", "lat": 3.0, "lon": 4.0, "description": "Desc2", "danger_level": "Dangerous"}
        ])
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            result = manager.remove_waypoint("To Remove")
            self.assertTrue(result)
            self.assertEqual(len(manager.waypoints), 1)
            self.assertEqual(manager.waypoints[0]['name'], "Keep Me")
            self.assertIn("Waypoint 'To Remove' removed successfully.", mock_stdout.getvalue())
            mock_file_open.assert_called_with(self.mock_data_file, 'w')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_remove_waypoint_not_found(self, mock_os_exists, mock_file_open):
        # Mock rationale: Simulate attempting to remove a non-existent waypoint.
        manager = WaypointManager(self.mock_data_file)
        manager.waypoints.append({"name": "Existing", "lat": 1.0, "lon": 2.0, "description": "Desc", "danger_level": "Safe"})

        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            result = manager.remove_waypoint("Non Existent")
            self.assertFalse(result)
            self.assertEqual(len(manager.waypoints), 1) # Should not change
            self.assertIn("Error: Waypoint 'Non Existent' not found.", mock_stdout.getvalue())
            # Ensure save was not called as no change occurred
            mock_file_open.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_list_waypoints_empty(self, mock_file_open, mock_os_exists, mock_stdout):
        # Mock rationale: Simulate listing waypoints when none are recorded.
        manager = WaypointManager(self.mock_data_file)
        manager.list_waypoints()
        self.assertIn("No waypoints recorded yet.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_list_waypoints_with_data(self, mock_file_open, mock_os_exists, mock_stdout):
        # Mock rationale: Simulate listing waypoints with pre-existing data.
        manager = WaypointManager(self.mock_data_file)
        manager.waypoints.extend([
            {"name": "Alpha", "lat": 10.12345, "lon": -20.6789, "description": "First point", "danger_level": "Safe"},
            {"name": "Beta Long Name", "lat": 30.0, "lon": 40.0, "description": "Second point with a longer description", "danger_level": "Death Trap"}
        ])
        manager.list_waypoints()
        output = mock_stdout.getvalue()
        self.assertIn("Name", output)
        self.assertIn("Alpha", output)
        self.assertIn("10.1235", output) # Rounded lat
        self.assertIn("-20.6789", output) # Rounded lon
        self.assertIn("Beta Long Name", output)
        self.assertIn("Death Trap", output)
        self.assertIn("Second point with a longer description", output)

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.mock_data_file = 'mock_waypoints.json'
        if os.path.exists(self.mock_data_file):
            os.remove(self.mock_data_file)

    def tearDown(self):
        if os.path.exists(self.mock_data_file):
            os.remove(self.mock_data_file)

    @patch('sys.argv', ['waypoint_weaver.py', 'add', '--name', 'TestPoint', '--lat', '1.0', '--lon', '2.0', '--desc', 'A test', '--danger', 'Safe'])
    @patch('waypoint_weaver.WaypointManager')
    def test_main_add_command(self, MockWaypointManager):
        # Mock rationale: Simulate command-line arguments for the 'add' command.
        # `sys.argv` is patched to provide the arguments, and `WaypointManager` is mocked
        # to verify its `add_waypoint` method is called correctly.
        mock_manager_instance = MockWaypointManager.return_value
        main()
        mock_manager_instance.add_waypoint.assert_called_once_with('TestPoint', 1.0, 2.0, 'A test', 'Safe')

    @patch('sys.argv', ['waypoint_weaver.py', 'list'])
    @patch('waypoint_weaver.WaypointManager')
    def test_main_list_command(self, MockWaypointManager):
        # Mock rationale: Simulate command-line arguments for the 'list' command.
        # `sys.argv` is patched, and `WaypointManager` is mocked to verify `list_waypoints` call.
        mock_manager_instance = MockWaypointManager.return_value
        main()
        mock_manager_instance.list_waypoints.assert_called_once()

    @patch('sys.argv', ['waypoint_weaver.py', 'remove', '--name', 'OldPoint'])
    @patch('waypoint_weaver.WaypointManager')
    def test_main_remove_command(self, MockWaypointManager):
        # Mock rationale: Simulate command-line arguments for the 'remove' command.
        # `sys.argv` is patched, and `WaypointManager` is mocked to verify `remove_waypoint` call.
        mock_manager_instance = MockWaypointManager.return_value
        main()
        mock_manager_instance.remove_waypoint.assert_called_once_with('OldPoint')

    @patch('sys.argv', ['waypoint_weaver.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        # Mock rationale: Simulate running the script with no command, which should print help.
        # `sys.argv` is patched to be just the script name, and `print_help` is mocked to verify it's called.
        main()
        mock_print_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
