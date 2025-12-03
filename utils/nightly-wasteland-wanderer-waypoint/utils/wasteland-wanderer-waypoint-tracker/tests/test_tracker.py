import unittest
import os
import json
from unittest.mock import patch, mock_open
import io
import sys

# Mock rationale: We need to prevent the tracker from actually reading/writing to the filesystem
# during tests to ensure determinism and isolation. `mock_open` and `patch('os.path.exists')`
# allow us to simulate file operations and content without touching real files.
# `patch('sys.stdout')` and `patch('sys.stderr')` capture printed output for verification.

# Import the functions from the tracker script
# We need to adjust the import path for testing.
# For self-contained utility, it's often easier to import directly if the test is in the same folder,
# or adjust sys.path. Given the structure, let's assume `tracker.py` is in `src/` and tests are in `tests/`.
# A common way is to temporarily add the src directory to the path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker
sys.path.pop(0) # Clean up path after import

class TestWaypointTracker(unittest.TestCase):

    def setUp(self):
        # Reset WAYPOINTS_FILE for each test to ensure isolation
        self.waypoints_data = {}
        tracker.WAYPOINTS_FILE = 'test_waypoints.json' # Use a different file name for testing

    def _mock_file_operations(self, initial_data=None):
        """Helper to set up mocks for file operations."""
        if initial_data is None:
            initial_data = {}
        
        # Mock rationale: Simulate the file existing or not, and its content.
        # This prevents actual file system interaction.
        mock_file_content = json.dumps(initial_data)
        
        # Mock rationale: `os.path.exists` needs to return True if we want to simulate a file existing.
        # We'll control this based on whether initial_data is empty or not.
        mock_exists = patch('os.path.exists', return_value=bool(initial_data))
        mock_exists.start()
        self.addCleanup(mock_exists.stop)

        # Mock rationale: `open` is used for reading and writing. `mock_open` handles both.
        # We capture what's written and provide what's read.
        m_open = mock_open(read_data=mock_file_content)
        patch('builtins.open', m_open).start()
        self.addCleanup(patch.stopall) # Stop all patches started in this method

        return m_open

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_add_waypoint_success(self, mock_stderr, mock_stdout):
        m_open = self._mock_file_operations()
        
        result = tracker.add_waypoint("TestPoint", "10.0", "20.0", "Some notes")
        self.assertTrue(result)
        self.assertIn("Waypoint 'TestPoint' added successfully.", mock_stdout.getvalue())
        
        # Mock rationale: Verify that `json.dump` was called with the correct data.
        # The `mock_open` object's `write` method captures what was written.
        written_data = json.loads(m_open().write.call_args[0][0])
        self.assertIn("TestPoint", written_data)
        self.assertEqual(written_data["TestPoint"]["latitude"], 10.0)
        self.assertEqual(written_data["TestPoint"]["longitude"], 20.0)
        self.assertEqual(written_data["TestPoint"]["notes"], "Some notes")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_add_waypoint_duplicate(self, mock_stderr, mock_stdout):
        initial_data = {"ExistingPoint": {"latitude": 1.0, "longitude": 2.0, "notes": "Old notes"}}
        self._mock_file_operations(initial_data)

        result = tracker.add_waypoint("ExistingPoint", "10.0", "20.0", "New notes")
        self.assertFalse(result)
        self.assertIn("Error: Waypoint 'ExistingPoint' already exists.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_add_waypoint_invalid_coords(self, mock_stderr, mock_stdout):
        self._mock_file_operations()
        result = tracker.add_waypoint("BadPoint", "not_a_number", "20.0")
        self.assertFalse(result)
        self.assertIn("Error: Latitude and Longitude must be valid numbers.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_list_waypoints_empty(self, mock_stderr, mock_stdout):
        self._mock_file_operations({}) # Simulate empty file
        tracker.list_waypoints()
        self.assertIn("No waypoints tracked yet.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_list_waypoints_with_data(self, mock_stderr, mock_stdout):
        initial_data = {
            "PointA": {"latitude": 1.1, "longitude": 2.2, "notes": "Short note."},
            "PointB": {"latitude": 3.3, "longitude": 4.4, "notes": "A very very very very very very very very very very very very long note that should be truncated."}
        }
        self._mock_file_operations(initial_data)
        tracker.list_waypoints()
        output = mock_stdout.getvalue()
        self.assertIn("--- Tracked Waypoints ---", output)
        self.assertIn("Name: PointA", output)
        self.assertIn("Coords: 1.1000, 2.2000", output)
        self.assertIn("Notes: Short note.", output)
        self.assertIn("Name: PointB", output)
        self.assertIn("Coords: 3.3000, 4.4000", output)
        self.assertIn("Notes: A very very very very very very very very very...", output) # Check truncation

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_get_waypoint_success(self, mock_stderr, mock_stdout):
        initial_data = {"PointC": {"latitude": 5.5, "longitude": 6.6, "notes": "Detailed notes here."}}
        self._mock_file_operations(initial_data)
        tracker.get_waypoint("PointC")
        output = mock_stdout.getvalue()
        self.assertIn("--- Waypoint Details: PointC ---", output)
        self.assertIn("Latitude: 5.500000", output)
        self.assertIn("Longitude: 6.600000", output)
        self.assertIn("Notes: Detailed notes here.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_get_waypoint_not_found(self, mock_stderr, mock_stdout):
        self._mock_file_operations({})
        tracker.get_waypoint("NonExistent")
        self.assertIn("Error: Waypoint 'NonExistent' not found.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_delete_waypoint_success(self, mock_stderr, mock_stdout):
        initial_data = {"PointD": {"latitude": 7.7, "longitude": 8.8, "notes": "To be deleted."}}
        m_open = self._mock_file_operations(initial_data)
        
        result = tracker.delete_waypoint("PointD")
        self.assertTrue(result)
        self.assertIn("Waypoint 'PointD' deleted successfully.", mock_stdout.getvalue())
        
        # Mock rationale: Verify that `json.dump` was called with the updated (deleted) data.
        written_data = json.loads(m_open().write.call_args[0][0])
        self.assertNotIn("PointD", written_data)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_delete_waypoint_not_found(self, mock_stderr, mock_stdout):
        self._mock_file_operations({})
        result = tracker.delete_waypoint("NonExistent")
        self.assertFalse(result)
        self.assertIn("Error: Waypoint 'NonExistent' not found.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate file exists
    def test_load_waypoints_corrupted_json(self, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a corrupted JSON file by providing invalid JSON string.
        m_open = mock_open(read_data="{'bad_json'")
        with patch('builtins.open', m_open):
            waypoints = tracker._load_waypoints()
            self.assertEqual(waypoints, {})
            self.assertIn("Warning: test_waypoints.json is corrupted.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate file does not exist
    def test_load_waypoints_no_file(self, mock_exists, mock_stderr, mock_stdout):
        waypoints = tracker._load_waypoints()
        self.assertEqual(waypoints, {})
        self.assertEqual(mock_stderr.getvalue(), "") # No error if file doesn't exist, just empty dict

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_add_command(self, mock_stderr, mock_stdout):
        m_open = self._mock_file_operations()
        
        # Mock rationale: Simulate command-line arguments.
        with patch.object(sys, 'argv', ['tracker.py', 'add', 'NewPlace', '1.0', '2.0', 'First', 'Last']):
            tracker.main()
            self.assertIn("Waypoint 'NewPlace' added successfully.", mock_stdout.getvalue())
            written_data = json.loads(m_open().write.call_args[0][0])
            self.assertEqual(written_data['NewPlace']['notes'], 'First Last')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_list_command(self, mock_stderr, mock_stdout):
        initial_data = {"ListTest": {"latitude": 1.0, "longitude": 2.0, "notes": "List notes"}}
        self._mock_file_operations(initial_data)
        
        with patch.object(sys, 'argv', ['tracker.py', 'list']):
            tracker.main()
            self.assertIn("Name: ListTest", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_get_command(self, mock_stderr, mock_stdout):
        initial_data = {"GetTest": {"latitude": 1.0, "longitude": 2.0, "notes": "Get notes"}}
        self._mock_file_operations(initial_data)
        
        with patch.object(sys, 'argv', ['tracker.py', 'get', 'GetTest']):
            tracker.main()
            self.assertIn("Waypoint Details: GetTest", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_delete_command(self, mock_stderr, mock_stdout):
        initial_data = {"DeleteTest": {"latitude": 1.0, "longitude": 2.0, "notes": "Delete notes"}}
        m_open = self._mock_file_operations(initial_data)
        
        with patch.object(sys, 'argv', ['tracker.py', 'delete', 'DeleteTest']):
            tracker.main()
            self.assertIn("Waypoint 'DeleteTest' deleted successfully.", mock_stdout.getvalue())
            written_data = json.loads(m_open().write.call_args[0][0])
            self.assertNotIn("DeleteTest", written_data)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_no_command(self, mock_stderr, mock_stdout):
        # Mock rationale: `sys.exit` is called on error, so we need to catch it.
        with patch.object(sys, 'argv', ['tracker.py']), \
             self.assertRaises(SystemExit) as cm:
            tracker.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python tracker.py <command> [args...]", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_unknown_command(self, mock_stderr, mock_stdout):
        with patch.object(sys, 'argv', ['tracker.py', 'unknown_cmd']), \
             self.assertRaises(SystemExit) as cm:
            tracker.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Unknown command: unknown_cmd", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_add_missing_args(self, mock_stderr, mock_stdout):
        with patch.object(sys, 'argv', ['tracker.py', 'add', 'name', 'lat']), \
             self.assertRaises(SystemExit) as cm:
            tracker.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python tracker.py add <name> <latitude> <longitude> [notes...]", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_get_missing_args(self, mock_stderr, mock_stdout):
        with patch.object(sys, 'argv', ['tracker.py', 'get']), \
             self.assertRaises(SystemExit) as cm:
            tracker.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python tracker.py get <name>", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_delete_missing_args(self, mock_stderr, mock_stdout):
        with patch.object(sys, 'argv', ['tracker.py', 'delete']), \
             self.assertRaises(SystemExit) as cm:
            tracker.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python tracker.py delete <name>", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
