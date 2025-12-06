import unittest
from unittest.mock import patch, mock_open
import json
import os
import argparse
from io import StringIO

# Import the main module from src
from src.mapper import WaypointManager, main

class TestWaypointManager(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test by removing any potential test file
        self.test_file = "test_waypoints.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_waypoints_existing_file(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing file with valid JSON content.
        mock_os_exists.return_value = True
        mock_json_load.return_value = [{"name": "Base", "coords": "0,0", "description": "Home"}]

        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "Base")
        mock_file_open.assert_called_with(self.test_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_waypoints_no_file(self, mock_os_exists):
        # Mock rationale: Simulate the scenario where no data file exists.
        mock_os_exists.return_value = False

        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 0)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_waypoints_malformed_json(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a data file containing invalid JSON, which should result in an empty waypoint list.
        manager = WaypointManager(self.test_file)
        self.assertEqual(len(manager.waypoints), 0)
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False) # Ensure no file exists initially for a clean add
    def test_add_waypoint(self, mock_os_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate file write operations without actually touching the disk.
        manager = WaypointManager(self.test_file)
        success, message = manager.add_waypoint("Oasis", "N10,E20", "Water source")
        self.assertTrue(success)
        self.assertEqual(message, "Waypoint 'Oasis' added.")
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "Oasis")
        mock_json_dump.assert_called_once_with(
            [{"name": "Oasis", "coords": "N10,E20", "description": "Water source"}],
            mock_file_open(), indent=4
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[{"name": "Oasis", "coords": "N10,E20", "description": "Water source"}])
    def test_add_waypoint_duplicate(self, mock_json_load, mock_os_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate an existing waypoint to test the duplicate handling logic.
        manager = WaypointManager(self.test_file)
        success, message = manager.add_waypoint("Oasis", "N11,E21", "Another water source")
        self.assertFalse(success)
        self.assertEqual(message, "Waypoint 'Oasis' already exists.")
        self.assertEqual(len(manager.waypoints), 1) # Should not add duplicate
        mock_json_dump.assert_not_called() # Should not save if no new waypoint was added

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Oasis", "coords": "N10,E20", "description": "Water source"},
        {"name": "Ruins", "coords": "N5,E15", "description": "Old city ruins"}
    ])
    def test_list_waypoints(self, mock_json_load, mock_os_exists):
        # Mock rationale: Provide pre-loaded waypoints to test the listing functionality.
        manager = WaypointManager(self.test_file)
        waypoints = manager.list_waypoints()
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[0]['name'], "Oasis")
        self.assertEqual(waypoints[1]['name'], "Ruins")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Oasis", "coords": "N10,E20", "description": "Water source"},
        {"name": "Ruins", "coords": "N5,E15", "description": "Old city ruins"}
    ])
    def test_find_waypoint_exists(self, mock_json_load, mock_os_exists):
        # Mock rationale: Provide pre-loaded waypoints to test finding an existing one.
        manager = WaypointManager(self.test_file)
        waypoint = manager.find_waypoint("Oasis")
        self.assertIsNotNone(waypoint)
        self.assertEqual(waypoint['coords'], "N10,E20")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Oasis", "coords": "N10,E20", "description": "Water source"}
    ])
    def test_find_waypoint_not_exists(self, mock_json_load, mock_os_exists):
        # Mock rationale: Provide pre-loaded waypoints to test finding a non-existent waypoint.
        manager = WaypointManager(self.test_file)
        waypoint = manager.find_waypoint("NonExistent")
        self.assertIsNone(waypoint)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Oasis", "coords": "N10,E20", "description": "Water source"},
        {"name": "Ruins", "coords": "N5,E15", "description": "Old city ruins"}
    ])
    def test_delete_waypoint_exists(self, mock_json_load, mock_os_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate deleting an existing waypoint and verify the save operation.
        manager = WaypointManager(self.test_file)
        success, message = manager.delete_waypoint("Oasis")
        self.assertTrue(success)
        self.assertEqual(message, "Waypoint 'Oasis' deleted.")
        self.assertEqual(len(manager.waypoints), 1)
        self.assertEqual(manager.waypoints[0]['name'], "Ruins")
        mock_json_dump.assert_called_once_with(
            [{"name": "Ruins", "coords": "N5,E15", "description": "Old city ruins"}],
            mock_file_open(), indent=4
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Oasis", "coords": "N10,E20", "description": "Water source"}
    ])
    def test_delete_waypoint_not_exists(self, mock_json_load, mock_os_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate attempting to delete a waypoint that does not exist.
        manager = WaypointManager(self.test_file)
        success, message = manager.delete_waypoint("NonExistent")
        self.assertFalse(success)
        self.assertEqual(message, "Waypoint 'NonExistent' not found.")
        self.assertEqual(len(manager.waypoints), 1) # Should not change the list
        mock_json_dump.assert_not_called() # Should not save if nothing was deleted

    # --- Tests for the main CLI function ---

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_add_command(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for the 'add' command and verify manager methods are called correctly.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", name="NewBase", coords="N1,E1", description="New home", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.add_waypoint.return_value = (True, "Waypoint 'NewBase' added.")

        main()
        MockWaypointManager.assert_called_once_with("test.json")
        mock_manager_instance.add_waypoint.assert_called_once_with("NewBase", "N1,E1", "New home")
        mock_print.assert_called_once_with("Waypoint 'NewBase' added.")

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_list_command(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for the 'list' command and verify manager methods and output.
        mock_parse_args.return_value = argparse.Namespace(
            command="list", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.list_waypoints.return_value = [
            {"name": "Base", "coords": "0,0", "description": "Home"}
        ]

        main()
        MockWaypointManager.assert_called_once_with("test.json")
        mock_manager_instance.list_waypoints.assert_called_once()
        # Check if print was called with expected output parts
        self.assertIn("--- Wasteland Waypoints ---", mock_print.call_args_list[0].args[0])
        self.assertIn("Name: Base", mock_print.call_args_list[1].args[0])

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_list_command_empty(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for 'list' when no waypoints are present.
        mock_parse_args.return_value = argparse.Namespace(
            command="list", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.list_waypoints.return_value = []

        main()
        mock_print.assert_called_once_with("No waypoints recorded yet. Add some!")

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_find_command(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for the 'find' command and verify manager methods and output.
        mock_parse_args.return_value = argparse.Namespace(
            command="find", name="Base", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.find_waypoint.return_value = {
            "name": "Base", "coords": "0,0", "description": "Home"
        }

        main()
        MockWaypointManager.assert_called_once_with("test.json")
        mock_manager_instance.find_waypoint.assert_called_once_with("Base")
        self.assertIn("--- Waypoint Found: Base ---", mock_print.call_args_list[0].args[0])

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_find_command_not_found(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for 'find' when the waypoint is not found.
        mock_parse_args.return_value = argparse.Namespace(
            command="find", name="NonExistent", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.find_waypoint.return_value = None

        main()
        mock_print.assert_called_once_with("Waypoint 'NonExistent' not found.")

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_delete_command(self, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate CLI arguments for the 'delete' command and verify manager methods and output.
        mock_parse_args.return_value = argparse.Namespace(
            command="delete", name="Base", data_file="test.json"
        )
        mock_manager_instance = MockWaypointManager.return_value
        mock_manager_instance.delete_waypoint.return_value = (True, "Waypoint 'Base' deleted.")

        main()
        MockWaypointManager.assert_called_once_with("test.json")
        mock_manager_instance.delete_waypoint.assert_called_once_with("Base")
        mock_print.assert_called_once_with("Waypoint 'Base' deleted.")

    @patch('src.mapper.WaypointManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help, mock_print, mock_parse_args, MockWaypointManager):
        # Mock rationale: Simulate running the script with no command, which should print help.
        mock_parse_args.return_value = argparse.Namespace(command=None, data_file="test.json")

        main()
        mock_print_help.assert_called_once()
        MockWaypointManager.assert_called_once_with("test.json") # Manager is still initialized

if __name__ == '__main__':
    unittest.main()
