import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing cache_coordinator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cache_coordinator

class TestCacheCoordinator(unittest.TestCase):

    def setUp(self):
        # Ensure CACHE_FILE is set to a test-specific name to avoid conflicts
        self.test_cache_file = 'test_caches.json'
        cache_coordinator.CACHE_FILE = self.test_cache_file

    def tearDown(self):
        # Clean up the test cache file if it was created
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)
        # Reset CACHE_FILE to its original name if necessary (though not strictly needed for this test setup)
        cache_coordinator.CACHE_FILE = 'caches.json'

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_add_cache_new(self, mock_json_load, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty cache file existing, then adding a new cache.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns an empty dict, simulating an empty file.
        # `mock_json_dump` captures the data that would be written.
        # `mock_open_file` is used for file operations.
        mock_exists.return_value = True
        mock_json_load.return_value = {}

        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.add_cache("Water Purifier", "Abandoned Well", "Under the mossy stone.")

        sys.stdout = sys.__stdout__ # Restore stdout

        mock_json_dump.assert_called_once_with(
            {"Water Purifier": {"location": "Abandoned Well", "hint": "Under the mossy stone."}},
            mock_open_file(),
            indent=4
        )
        self.assertIn("Cache 'Water Purifier' added successfully.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_add_cache_existing(self, mock_json_load, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate adding a cache that already exists.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns a dict with an existing cache.
        # `mock_json_dump` should not be called as no change is made.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Existing Cache": {"location": "Loc", "hint": "Hint"}}

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.add_cache("Existing Cache", "New Loc", "New Hint")

        sys.stdout = sys.__stdout__

        mock_json_dump.assert_not_called()
        self.assertIn("Error: Cache 'Existing Cache' already exists.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_caches_empty(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty cache file when listing.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns an empty dict.
        mock_exists.return_value = True
        mock_json_load.return_value = {}

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.list_caches()

        sys.stdout = sys.__stdout__

        self.assertIn("No caches found.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_caches_with_data(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a cache file with data when listing.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns a dict with multiple caches.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Cache A": {"location": "Loc A", "hint": "Hint A"},
            "Cache B": {"location": "Loc B", "hint": "Hint B"}
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.list_caches()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("- Cache A", output)
        self.assertIn("- Cache B", output)
        self.assertIn("--- Your Cryptic Caches ---", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_view_cache_found(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate viewing an existing cache.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns a dict with the target cache.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "Secret Stash": {"location": "Under the old oak", "hint": "Follow the raven's flight."}
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.view_cache("Secret Stash")

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("--- Cache Details for 'Secret Stash' ---", output)
        self.assertIn("Location: Under the old oak", output)
        self.assertIn("Hint: Follow the raven's flight.", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_view_cache_not_found(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate viewing a non-existent cache.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns an empty dict.
        mock_exists.return_value = True
        mock_json_load.return_value = {}

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.view_cache("Non Existent Cache")

        sys.stdout = sys.__stdout__

        self.assertIn("Error: Cache 'Non Existent Cache' not found.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_delete_cache_found(self, mock_json_load, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate deleting an existing cache.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns a dict with the target cache.
        # `mock_json_dump` captures the data that would be written (without the deleted cache).
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "ToDelete": {"location": "Loc", "hint": "Hint"},
            "ToKeep": {"location": "Loc2", "hint": "Hint2"}
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.delete_cache("ToDelete")

        sys.stdout = sys.__stdout__

        mock_json_dump.assert_called_once_with(
            {"ToKeep": {"location": "Loc2", "hint": "Hint2"}},
            mock_open_file(),
            indent=4
        )
        self.assertIn("Cache 'ToDelete' deleted successfully.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_delete_cache_not_found(self, mock_json_load, mock_json_dump, mock_open_file, mock_exists):
        # Mock rationale: Simulate deleting a non-existent cache.
        # `mock_exists` ensures `_load_caches` thinks the file exists.
        # `mock_json_load` returns an empty dict.
        # `mock_json_dump` should not be called.
        mock_exists.return_value = True
        mock_json_load.return_value = {}

        captured_output = StringIO()
        sys.stdout = captured_output

        cache_coordinator.delete_cache("Non Existent")

        sys.stdout = sys.__stdout__

        mock_json_dump.assert_not_called()
        self.assertIn("Error: Cache 'Non Existent' not found.", captured_output.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_caches_file_not_exists(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate the cache file not existing.
        # `mock_exists` returns False, so `_load_caches` should return an empty dict.
        mock_exists.return_value = False
        caches = cache_coordinator._load_caches()
        self.assertEqual(caches, {})
        mock_open_file.assert_not_called() # No file opened if it doesn't exist

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_caches_corrupted_json(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        # `mock_exists` returns True.
        # `mock_json_load` raises a JSONDecodeError.
        # `_load_caches` should catch this and return an empty dict, printing a warning.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        captured_output = StringIO()
        sys.stdout = captured_output

        caches = cache_coordinator._load_caches()

        sys.stdout = sys.__stdout__

        self.assertEqual(caches, {})
        self.assertIn(f"Warning: {self.test_cache_file} is corrupted.", captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
