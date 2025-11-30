import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
import sys
from io import StringIO

# Add parent directory to path to allow importing src.stash_tracker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.stash_tracker import (
    load_stash, save_stash, add_item, list_items, remove_item, clear_stash,
    get_default_stash_path, STASH_FILENAME
)
sys.path.pop(0) # Clean up sys.path

class TestStashTracker(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "/mock/path/test_stash.json"
        self.initial_stash_data = {
            "water": {"name": "Water", "quantity": 10},
            "food rations": {"name": "Food Rations", "quantity": 5}
        }

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_stash_existing_file(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing stash file with valid JSON content.
        mock_exists.return_value = True
        mock_json_load.return_value = self.initial_stash_data
        stash = load_stash(self.test_file_path)
        self.assertEqual(stash, self.initial_stash_data)
        mock_file_open.assert_called_once_with(self.test_file_path, 'r')

    @patch('os.path.exists')
    def test_load_stash_non_existing_file(self, mock_exists):
        # Mock rationale: Simulate a non-existent stash file, expecting an empty stash.
        mock_exists.return_value = False
        stash = load_stash(self.test_file_path)
        self.assertEqual(stash, {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stderr', new_callable=StringIO)
    def test_load_stash_corrupted_file(self, mock_stderr, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate a corrupted JSON file, expecting an empty stash and a warning.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        stash = load_stash(self.test_file_path)
        self.assertEqual(stash, {})
        self.assertIn("Warning: Stash file", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_stash(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate saving stash data to a file.
        save_stash(self.test_file_path, self.initial_stash_data)
        mock_file_open.assert_called_once_with(self.test_file_path, 'w')
        mock_json_dump.assert_called_once_with(self.initial_stash_data, mock_file_open(), indent=4)

    @patch('src.stash_tracker.load_stash')
    @patch('src.stash_tracker.save_stash')
    @patch('builtins.print')
    def test_add_item_new(self, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate adding a new item to an empty stash.
        mock_load.return_value = {}
        add_item("Bandages", 3, self.test_file_path)
        mock_load.assert_called_once_with(self.test_file_path)
        mock_save.assert_called_once_with(self.test_file_path, {"bandages": {"name": "Bandages", "quantity": 3}})
        mock_print.assert_called_once_with("Added 'Bandages' with quantity 3")

    @patch('src.stash_tracker.load_stash')
    @patch('src.stash_tracker.save_stash')
    @patch('builtins.print')
    def test_add_item_update_existing(self, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate updating the quantity of an existing item.
        mock_load.return_value = {"water": {"name": "Water", "quantity": 10}}
        add_item("Water", 5, self.test_file_path)
        mock_load.assert_called_once_with(self.test_file_path)
        mock_save.assert_called_once_with(self.test_file_path, {"water": {"name": "Water", "quantity": 15}})
        mock_print.assert_called_once_with("Updated 'Water': new quantity is 15")

    @patch('src.stash_tracker.load_stash')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_items_empty(self, mock_stdout, mock_load):
        # Mock rationale: Simulate listing items when the stash is empty.
        mock_load.return_value = {}
        list_items(self.test_file_path)
        self.assertIn("Your scavenger's stash is empty.", mock_stdout.getvalue())

    @patch('src.stash_tracker.load_stash')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_items_populated(self, mock_stdout, mock_load):
        # Mock rationale: Simulate listing items from a populated stash.
        mock_load.return_value = self.initial_stash_data
        list_items(self.test_file_path)
        output = mock_stdout.getvalue()
        self.assertIn("--- Your Scavenger's Stash ---", output)
        self.assertIn("- Water: 10", output)
        self.assertIn("- Food Rations: 5", output)

    @patch('src.stash_tracker.load_stash')
    @patch('src.stash_tracker.save_stash')
    @patch('builtins.print')
    def test_remove_item_existing(self, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate removing an existing item from the stash.
        mock_load.return_value = self.initial_stash_data.copy() # Use copy to avoid modifying original
        expected_stash = {"food rations": {"name": "Food Rations", "quantity": 5}}
        remove_item("Water", self.test_file_path)
        mock_load.assert_called_once_with(self.test_file_path)
        mock_save.assert_called_once_with(self.test_file_path, expected_stash)
        mock_print.assert_called_once_with("Removed 'Water' from your stash.")

    @patch('src.stash_tracker.load_stash')
    @patch('src.stash_tracker.save_stash')
    @patch('builtins.print')
    def test_remove_item_non_existing(self, mock_print, mock_save, mock_load):
        # Mock rationale: Simulate attempting to remove a non-existent item.
        mock_load.return_value = self.initial_stash_data.copy()
        remove_item("Medkit", self.test_file_path)
        mock_load.assert_called_once_with(self.test_file_path)
        mock_save.assert_not_called() # Should not save if item not found
        mock_print.assert_called_once_with("'Medkit' not found in your stash.")

    @patch('src.stash_tracker.save_stash')
    @patch('builtins.print')
    def test_clear_stash(self, mock_print, mock_save):
        # Mock rationale: Simulate clearing the entire stash.
        clear_stash(self.test_file_path)
        mock_save.assert_called_once_with(self.test_file_path, {})
        mock_print.assert_called_once_with("Your scavenger's stash has been cleared. A fresh start!")

    @patch('os.getcwd', return_value='/mock/current/dir')
    def test_get_default_stash_path(self, mock_getcwd):
        # Mock rationale: Ensure the default path is constructed correctly based on the current working directory.
        expected_path = os.path.join('/mock/current/dir', STASH_FILENAME)
        self.assertEqual(get_default_stash_path(), expected_path)

    # Test main function with various commands
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.stash_tracker.add_item')
    def test_main_add_command(self, mock_add_item, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for the 'add' command.
        mock_parse_args.return_value = MagicMock(
            command='add', item='Rope', quantity=2, stash_file=self.test_file_path
        )
        from src.stash_tracker import main
        main()
        mock_add_item.assert_called_once_with('Rope', 2, self.test_file_path)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.stash_tracker.list_items')
    def test_main_list_command(self, mock_list_items, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for the 'list' command.
        mock_parse_args.return_value = MagicMock(
            command='list', stash_file=self.test_file_path
        )
        from src.stash_tracker import main
        main()
        mock_list_items.assert_called_once_with(self.test_file_path)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.stash_tracker.remove_item')
    def test_main_remove_command(self, mock_remove_item, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for the 'remove' command.
        mock_parse_args.return_value = MagicMock(
            command='remove', item='Water', stash_file=self.test_file_path
        )
        from src.stash_tracker import main
        main()
        mock_remove_item.assert_called_once_with('Water', self.test_file_path)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.stash_tracker.clear_stash')
    def test_main_clear_command(self, mock_clear_stash, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for the 'clear' command.
        mock_parse_args.return_value = MagicMock(
            command='clear', stash_file=self.test_file_path
        )
        from src.stash_tracker import main
        main()
        mock_clear_stash.assert_called_once_with(self.test_file_path)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help, mock_parse_args):
        # Mock rationale: Simulate running the script without a command, expecting help message.
        mock_parse_args.return_value = MagicMock(command=None)
        from src.stash_tracker import main
        main()
        mock_print_help.assert_called_once()
