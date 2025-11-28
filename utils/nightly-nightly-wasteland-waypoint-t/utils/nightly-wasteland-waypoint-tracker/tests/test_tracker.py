import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch
from datetime import datetime

# Import the WaypointTracker class from the src directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import WaypointTracker

class TestWaypointTracker(unittest.TestCase):

    # Mock rationale: Using a temporary directory and file ensures tests are isolated and don't interfere with actual user data or other tests.
    # It simulates real file system interactions without requiring complex patching of `open` or `json` functions, making the tests deterministic and offline.
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.test_dir, 'test_waypoints.json')
        self.tracker = WaypointTracker(self.data_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_waypoint(self):
        initial_count = len(self.tracker.waypoints)
        waypoint = self.tracker.add_waypoint(
            name="Test Config", 
            target="/path/to/config.ini", 
            tags="config,ini", 
            description="A test configuration file"
        )
        self.assertEqual(len(self.tracker.waypoints), initial_count + 1)
        self.assertIn(waypoint, self.tracker.waypoints)
        self.assertIsInstance(waypoint['id'], int)
        self.assertIsInstance(waypoint['created_at'], str)
        self.assertEqual(waypoint['name'], "Test Config")
        self.assertEqual(waypoint['target'], "/path/to/config.ini")
        self.assertEqual(waypoint['tags'], ['config', 'ini'])
        self.assertEqual(waypoint['description'], "A test configuration file")

    def test_list_waypoints_empty(self):
        # Capture stdout to check printed messages
        with patch('builtins.print') as mock_print:
            result = self.tracker.list_waypoints()
            self.assertEqual(result, [])
            mock_print.assert_called_with("No waypoints found. Start by adding one!")

    def test_list_waypoints_with_data(self):
        self.tracker.add_waypoint("W1", "/t1", "tag1", "desc1")
        self.tracker.add_waypoint("W2", "/t2", "tag2", "desc2")
        with patch('builtins.print') as mock_print:
            results = self.tracker.list_waypoints()
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]['name'], "W1")
            self.assertEqual(results[1]['name'], "W2")
            self.assertTrue(mock_print.called)

    def test_search_waypoints(self):
        wp1 = self.tracker.add_waypoint("API Endpoint", "https://api.example.com/v1", "api,external", "Main API endpoint")
        wp2 = self.tracker.add_waypoint("Local DB", "/var/data/db.sqlite", "db,local", "SQLite database file")
        wp3 = self.tracker.add_waypoint("Config File", "/etc/app/config.json", "config,json", "Application config")

        results = self.tracker.search_waypoints("api")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "API Endpoint")

        results = self.tracker.search_waypoints("db")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Local DB")

        results = self.tracker.search_waypoints("config")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Config File")

        results = self.tracker.search_waypoints("example") # Search by target
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "API Endpoint")

        results = self.tracker.search_waypoints("nonexistent")
        self.assertEqual(len(results), 0)

        results = self.tracker.search_waypoints("app") # Search by description
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Config File")

    def test_delete_waypoint(self):
        wp1 = self.tracker.add_waypoint("WP1", "/t1", "tag1", "desc1")
        wp2 = self.tracker.add_waypoint("WP2", "/t2", "tag2", "desc2")
        wp3 = self.tracker.add_waypoint("WP3", "/t3", "tag3", "desc3")

        self.assertTrue(self.tracker.delete_waypoint(wp2['id']))
        self.assertEqual(len(self.tracker.waypoints), 2)
        self.assertNotIn(wp2, self.tracker.waypoints)

        self.assertFalse(self.tracker.delete_waypoint(99999999999)) # Non-existent ID
        self.assertEqual(len(self.tracker.waypoints), 2)

        self.assertTrue(self.tracker.delete_waypoint(wp1['id']))
        self.assertTrue(self.tracker.delete_waypoint(wp3['id']))
        self.assertEqual(len(self.tracker.waypoints), 0)

    def test_persistence(self):
        self.tracker.add_waypoint("Persistent WP", "/data/persistent.txt", "data", "Should survive restart")
        self.tracker._save_data() # Ensure data is written

        # Create a new tracker instance, pointing to the same file
        new_tracker = WaypointTracker(self.data_file)
        self.assertEqual(len(new_tracker.waypoints), 1)
        self.assertEqual(new_tracker.waypoints[0]['name'], "Persistent WP")

    def test_empty_or_corrupted_data_file(self):
        # Test with non-existent file (handled by setUp)
        self.assertEqual(self.tracker.waypoints, [])

        # Create a corrupted file
        with open(self.data_file, 'w') as f:
            f.write("{\"invalid json")
        
        # Re-initialize tracker and check if it handles corruption
        with patch('builtins.print') as mock_print:
            corrupted_tracker = WaypointTracker(self.data_file)
            self.assertEqual(corrupted_tracker.waypoints, [])
            mock_print.assert_called_with(f"Warning: {self.data_file} is corrupted or empty. Starting with an empty waypoint list.")

    def test_add_waypoint_no_tags_or_description(self):
        waypoint = self.tracker.add_waypoint(
            name="Simple Link", 
            target="https://example.com"
        )
        self.assertEqual(waypoint['name'], "Simple Link")
        self.assertEqual(waypoint['target'], "https://example.com")
        self.assertEqual(waypoint['tags'], [])
        self.assertEqual(waypoint['description'], '')

    def test_search_case_insensitivity(self):
        self.tracker.add_waypoint("UPPERCASE TAG", "/path", "TAG", "")
        results = self.tracker.search_waypoints("tag")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "UPPERCASE TAG")

        results = self.tracker.search_waypoints("uppercase")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "UPPERCASE TAG")

if __name__ == '__main__':
    unittest.main()
