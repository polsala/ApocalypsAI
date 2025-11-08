import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys

# Mock rationale: We need to test the tracker's logic without actually touching the filesystem.
# Mocking `os.path.exists`, `open`, `json.load`, and `json.dump` allows us to simulate
# file operations and control the data read from and written to the 'resources.json' file.
# This ensures tests are deterministic, fast, and don't leave artifacts.

# Import the functions directly for testing
from src.tracker import load_resources, save_resources, add_resource, consume_resource, list_resources, DATA_FILE

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Reset mocks for each test to ensure isolation
        pass

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_resources_existing_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing resources.json file with predefined content.
        # `os.path.exists` returns True, `json.load` returns the mock data.
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = {'food': 10, 'water': 5}
        
        resources = load_resources()
        
        self.assertEqual(resources, {'food': 10, 'water': 5})
        mock_os_path_exists.assert_called_once_with(DATA_FILE)
        mock_file_open.assert_called_once_with(DATA_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_resources_no_file(self, mock_os_path_exists):
        # Mock rationale: Simulate no resources.json file existing.
        # `os.path.exists` returns False, so `json.load` and `open` should not be called.
        mock_os_path_exists.return_value = False
        
        resources = load_resources()
        
        self.assertEqual(resources, {})
        mock_os_path_exists.assert_called_once_with(DATA_FILE)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate saving data to resources.json.
        # `open` is mocked to capture write calls, `json.dump` is mocked to ensure it's called with correct data.
        resources_to_save = {'food': 12, 'ammo': 3}
        
        save_resources(resources_to_save)
        
        mock_file_open.assert_called_once_with(DATA_FILE, 'w')
        mock_json_dump.assert_called_once_with(resources_to_save, mock_file_open(), indent=4)

    @patch('src.tracker.save_resources') # Mock rationale: Isolate add_resource from actual file saving during test.
    def test_add_resource_new(self, mock_save_resources):
        resources = {}
        with patch('builtins.print') as mock_print:
            add_resource(resources, 'food', 5)
            self.assertEqual(resources, {'food': 5})
            mock_print.assert_called_once_with('Added 5 of food. Current: 5')
            mock_save_resources.assert_called_once_with({'food': 5})

    @patch('src.tracker.save_resources') # Mock rationale: Isolate add_resource from actual file saving during test.
    def test_add_resource_existing(self, mock_save_resources):
        resources = {'food': 10}
        with patch('builtins.print') as mock_print:
            add_resource(resources, 'food', 3)
            self.assertEqual(resources, {'food': 13})
            mock_print.assert_called_once_with('Added 3 of food. Current: 13')
            mock_save_resources.assert_called_once_with({'food': 13})

    @patch('src.tracker.save_resources') # Mock rationale: Isolate consume_resource from actual file saving during test.
    def test_consume_resource_sufficient(self, mock_save_resources):
        resources = {'water': 10}
        with patch('builtins.print') as mock_print:
            consume_resource(resources, 'water', 3)
            self.assertEqual(resources, {'water': 7})
            mock_print.assert_called_once_with('Consumed 3 of water. Remaining: 7.')
            mock_save_resources.assert_called_once_with({'water': 7})

    @patch('src.tracker.save_resources') # Mock rationale: Isolate consume_resource from actual file saving during test.
    def test_consume_resource_insufficient(self, mock_save_resources):
        resources = {'ammo': 5}
        with patch('builtins.print') as mock_print:
            consume_resource(resources, 'ammo', 10)
            self.assertEqual(resources, {'ammo': 0})
            mock_print.assert_called_once_with('Consumed 5 of ammo. Remaining: 0. (Note: You only had 5)')
            mock_save_resources.assert_called_once_with({'ammo': 0})

    @patch('src.tracker.save_resources') # Mock rationale: Isolate consume_resource from actual file saving during test.
    def test_consume_resource_none_available(self, mock_save_resources):
        resources = {'meds': 0}
        with patch('builtins.print') as mock_print:
            consume_resource(resources, 'meds', 1)
            self.assertEqual(resources, {'meds': 0})
            mock_print.assert_called_once_with('No meds to consume. Current: 0.')
            mock_save_resources.assert_not_called() # No change, so no save needed

    @patch('src.tracker.save_resources') # Mock rationale: Isolate consume_resource from actual file saving during test.
    def test_consume_resource_non_existent(self, mock_save_resources):
        resources = {}
        with patch('builtins.print') as mock_print:
            consume_resource(resources, 'tools', 1)
            self.assertEqual(resources, {})
            mock_print.assert_called_once_with('No tools to consume. Current: 0.')
            mock_save_resources.assert_not_called() # No change, so no save needed

    def test_list_resources_empty(self):
        resources = {}
        with patch('builtins.print') as mock_print:
            list_resources(resources)
            mock_print.assert_called_once_with('No resources tracked yet. Start adding some!')

    def test_list_resources_populated(self):
        resources = {'food': 8, 'water': 15, 'sanity': 90}
        with patch('builtins.print') as mock_print:
            list_resources(resources)
            # Check that print was called with the correct lines
            mock_print.assert_any_call('Current Resources:')
            mock_print.assert_any_call('  food: 8')
            mock_print.assert_any_call('  water: 15')
            mock_print.assert_any_call('  sanity: 90')
            self.assertEqual(mock_print.call_count, 4)

    # Test main function with argparse
    @patch('src.tracker.load_resources')
    @patch('src.tracker.add_resource')
    @patch('src.tracker.consume_resource')
    @patch('src.tracker.list_resources')
    @patch('sys.argv', ['tracker.py', 'add', 'food', '5'])
    def test_main_add_command(self, mock_list, mock_consume, mock_add, mock_load):
        # Mock rationale: Simulate command-line arguments and ensure the correct functions are called.
        # `sys.argv` is patched to simulate CLI input. `load_resources`, `add_resource`, etc., are mocked
        # to verify their invocation without executing their full logic.
        mock_load.return_value = {}
        from src.tracker import main
        main()
        mock_load.assert_called_once()
        mock_add.assert_called_once_with({}, 'food', 5)
        mock_consume.assert_not_called()
        mock_list.assert_not_called()

    @patch('src.tracker.load_resources')
    @patch('src.tracker.add_resource')
    @patch('src.tracker.consume_resource')
    @patch('src.tracker.list_resources')
    @patch('sys.argv', ['tracker.py', 'consume', 'water', '2'])
    def test_main_consume_command(self, mock_list, mock_consume, mock_add, mock_load):
        mock_load.return_value = {'water': 10}
        from src.tracker import main
        main()
        mock_load.assert_called_once()
        mock_consume.assert_called_once_with({'water': 10}, 'water', 2)
        mock_add.assert_not_called()
        mock_list.assert_not_called()

    @patch('src.tracker.load_resources')
    @patch('src.tracker.add_resource')
    @patch('src.tracker.consume_resource')
    @patch('src.tracker.list_resources')
    @patch('sys.argv', ['tracker.py', 'list'])
    def test_main_list_command(self, mock_list, mock_consume, mock_add, mock_load):
        mock_load.return_value = {'food': 5}
        from src.tracker import main
        main()
        mock_load.assert_called_once()
        mock_list.assert_called_once_with({'food': 5})
        mock_add.assert_not_called()
        mock_consume.assert_not_called()

    @patch('src.tracker.load_resources')
    @patch('src.tracker.add_resource')
    @patch('src.tracker.consume_resource')
    @patch('src.tracker.list_resources')
    @patch('sys.argv', ['tracker.py'])
    @patch('argparse.ArgumentParser.print_help') # Mock rationale: Prevent actual help message printing during test.
    def test_main_no_command(self, mock_print_help, mock_list, mock_consume, mock_add, mock_load):
        from src.tracker import main
        main()
        mock_load.assert_not_called() # No command, so no resource loading needed
        mock_add.assert_not_called()
        mock_consume.assert_not_called()
        mock_list.assert_not_called()
        mock_print_help.assert_called_once()
