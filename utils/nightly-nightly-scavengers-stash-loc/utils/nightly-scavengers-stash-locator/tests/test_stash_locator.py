import unittest
import json
import os
from unittest.mock import patch, mock_open
from src.stash_locator import StashLocator

class TestStashLocator(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test by setting a dummy data file name
        self.test_data_file = "test_stashes.json"

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_stashes_existing_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: We need to simulate file system interactions (reading/writing JSON)
        # without actually touching the disk to ensure deterministic and isolated tests.
        # os.path.exists: To make StashLocator believe the file exists.
        # builtins.open: To intercept file opening and provide mock content.
        # json.load: To control the data returned when the mock file is "read".
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = [{"name": "Old Stash", "description": "Old", "coordinates": "0,0"}]

        locator = StashLocator(self.test_data_file)
        self.assertEqual(len(locator.stashes), 1)
        self.assertEqual(locator.stashes[0]['name'], "Old Stash")
        mock_file_open.assert_called_with(self.test_data_file, 'r')

    @patch('os.path.exists')
    def test_load_stashes_no_file(self, mock_os_path_exists):
        # Mock rationale: Simulate no existing data file.
        # os.path.exists: To make StashLocator believe the file does not exist.
        mock_os_path_exists.return_value = False

        locator = StashLocator(self.test_data_file)
        self.assertEqual(len(locator.stashes), 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Test Error", "", 0))
    @patch('builtins.print') # Mock print to avoid actual output during test
    def test_load_stashes_corrupted_file(self, mock_print, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate a corrupted JSON file.
        # json.load: To raise a JSONDecodeError.
        # builtins.print: To capture the warning message.
        mock_os_path_exists.return_value = True

        locator = StashLocator(self.test_data_file)
        self.assertEqual(len(locator.stashes), 0)
        mock_print.assert_called_with(f"Warning: {self.test_data_file} is corrupted. Starting with an empty stash list.")


    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False) # Ensure no file exists initially
    def test_add_stash(self, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate adding a stash and saving it to a new file.
        # builtins.open: To intercept file writing.
        # json.dump: To check if the correct data is being saved.
        locator = StashLocator(self.test_data_file)
        success, message = locator.add_stash("Hidden Cache", "Emergency supplies", "X:100,Y:200")
        self.assertTrue(success)
        self.assertEqual(message, "Stash 'Hidden Cache' added.")
        self.assertEqual(len(locator.stashes), 1)
        self.assertEqual(locator.stashes[0]['name'], "Hidden Cache")
        mock_json_dump.assert_called_once()
        mock_file_open.assert_called_with(self.test_data_file, 'w')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[{"name": "Hidden Cache", "description": "Old", "coordinates": "0,0"}])
    def test_add_stash_duplicate(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate adding a stash that already exists.
        # json.load: To provide initial stash data.
        locator = StashLocator(self.test_data_file)
        success, message = locator.add_stash("Hidden Cache", "New supplies", "X:101,Y:201")
        self.assertFalse(success)
        self.assertEqual(message, "Stash 'Hidden Cache' already exists.")
        self.assertEqual(len(locator.stashes), 1) # Should not add duplicate
        mock_json_dump.assert_not_called() # Should not save if not added

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Stash A", "description": "Desc A", "coordinates": "1,1"},
        {"name": "Stash B", "description": "Desc B", "coordinates": "2,2"}
    ])
    def test_list_stashes(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate loading existing stashes and then listing them.
        locator = StashLocator(self.test_data_file)
        stashes = locator.list_stashes()
        self.assertEqual(len(stashes), 2)
        self.assertEqual(stashes[0]['name'], "Stash A")
        self.assertEqual(stashes[1]['name'], "Stash B")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Stash A", "description": "Desc A", "coordinates": "1,1"},
        {"name": "Stash B", "description": "Desc B", "coordinates": "2,2"}
    ])
    def test_find_stash_exists(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate finding an existing stash.
        locator = StashLocator(self.test_data_file)
        stash = locator.find_stash("Stash A")
        self.assertIsNotNone(stash)
        self.assertEqual(stash['description'], "Desc A")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Stash A", "description": "Desc A", "coordinates": "1,1"}
    ])
    def test_find_stash_not_exists(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate trying to find a non-existent stash.
        locator = StashLocator(self.test_data_file)
        stash = locator.find_stash("Stash C")
        self.assertIsNone(stash)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Stash A", "description": "Desc A", "coordinates": "1,1"},
        {"name": "Stash B", "description": "Desc B", "coordinates": "2,2"}
    ])
    def test_remove_stash_exists(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate removing an existing stash.
        locator = StashLocator(self.test_data_file)
        success, message = locator.remove_stash("Stash A")
        self.assertTrue(success)
        self.assertEqual(message, "Stash 'Stash A' removed.")
        self.assertEqual(len(locator.stashes), 1)
        self.assertEqual(locator.stashes[0]['name'], "Stash B")
        mock_json_dump.assert_called_once()
        mock_file_open.assert_called_with(self.test_data_file, 'w')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value=[
        {"name": "Stash A", "description": "Desc A", "coordinates": "1,1"}
    ])
    def test_remove_stash_not_exists(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate trying to remove a non-existent stash.
        locator = StashLocator(self.test_data_file)
        success, message = locator.remove_stash("Stash C")
        self.assertFalse(success)
        self.assertEqual(message, "Stash 'Stash C' not found.")
        self.assertEqual(len(locator.stashes), 1) # Should remain unchanged
        mock_json_dump.assert_not_called() # Should not save if nothing was removed

if __name__ == '__main__':
    unittest.main()
