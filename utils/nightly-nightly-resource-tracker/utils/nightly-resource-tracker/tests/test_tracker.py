import unittest
from unittest.mock import patch, mock_open
import os
import sys
from io import StringIO

# Mock rationale: We need to prevent the tracker from interacting with the actual file system
# during tests to ensure determinism and isolation. Mocking `os.path.exists` and `builtins.open`
# allows us to simulate file presence and content without creating or modifying real files.

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_new_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a scenario where resources.txt does not exist initially.
        # `mock_exists` returns False, and `mock_file_open` will be used for writing.
        mock_exists.return_value = False
        from src.tracker import add_resource, RESOURCE_FILE

        add_resource('water', 10)

        mock_exists.assert_called_once_with(RESOURCE_FILE)
        mock_file_open.assert_called_once_with(RESOURCE_FILE, 'w')
        mock_file_open().write.assert_called_once_with('water,10\n')
        self.assertIn("Added 10 of 'water'. New total: 10", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_existing_file_new_item(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing resources.txt with content, then adding a new item.
        # `mock_exists` returns True. `mock_file_open` is configured to return initial content on 'r'
        # and capture new content on 'w'.
        mock_exists.return_value = True
        initial_content = "food,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import add_resource, RESOURCE_FILE

        add_resource('water', 10)

        # Assert 'r' call and 'w' call
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        # Check content written. Order might vary for dict iteration, so check for both lines.
        written_content = mock_file_open().write.call_args_list[0].args[0]
        self.assertIn('food,5\n', written_content)
        self.assertIn('water,10\n', written_content)
        self.assertIn("Added 10 of 'water'. New total: 10", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_existing_item(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing resources.txt with content, then updating an existing item.
        mock_exists.return_value = True
        initial_content = "water,10\nfood,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import add_resource, RESOURCE_FILE

        add_resource('water', 5)

        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        written_content = mock_file_open().write.call_args_list[0].args[0]
        self.assertIn('water,15\n', written_content)
        self.assertIn('food,5\n', written_content)
        self.assertIn("Added 5 of 'water'. New total: 15", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_resource_existing_item(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate removing a portion of an existing resource.
        mock_exists.return_value = True
        initial_content = "water,10\nfood,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import remove_resource, RESOURCE_FILE

        remove_resource('water', 3)

        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        written_content = mock_file_open().write.call_args_list[0].args[0]
        self.assertIn('water,7\n', written_content)
        self.assertIn('food,5\n', written_content)
        self.assertIn("Removed 3 of 'water'. Remaining: 7", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_resource_all_of_item(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate removing all of an existing resource, leading to its removal from the file.
        mock_exists.return_value = True
        initial_content = "water,10\nfood,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import remove_resource, RESOURCE_FILE

        remove_resource('water', 10)

        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        written_content = mock_file_open().write.call_args_list[0].args[0]
        self.assertNotIn('water', written_content)
        self.assertIn('food,5\n', written_content)
        self.assertIn("Removed 10 of 'water'. Remaining: 0", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_resource_not_found(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate attempting to remove a resource that doesn't exist.
        mock_exists.return_value = True
        initial_content = "food,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import remove_resource, RESOURCE_FILE

        remove_resource('water', 1)

        mock_file_open.assert_called_once_with(RESOURCE_FILE, 'r') # Only read, no write attempt
        self.assertIn("Error: Resource 'water' not found.", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_resource_insufficient_quantity(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate attempting to remove more of a resource than available.
        mock_exists.return_value = True
        initial_content = "water,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import remove_resource, RESOURCE_FILE

        remove_resource('water', 10)

        mock_file_open.assert_called_once_with(RESOURCE_FILE, 'r') # Only read, no write attempt
        self.assertIn("Error: Not enough 'water' to remove. Available: 5, trying to remove: 10", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_resources_empty(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty resources.txt file.
        mock_exists.return_value = False
        from src.tracker import list_resources

        list_resources()

        mock_exists.assert_called_once()
        self.assertIn("No resources tracked yet.", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_list_resources_populated(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a populated resources.txt file and verify its output.
        mock_exists.return_value = True
        initial_content = "water,10\nfood,5\nbatteries,2\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import list_resources

        list_resources()

        mock_exists.assert_called_once()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Current Resources ---", output)
        self.assertIn("batteries: 2", output)
        self.assertIn("food: 5", output)
        self.assertIn("water: 10", output)
        self.assertIn("-------------------------", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_negative_quantity_input(self, mock_file_open, mock_exists):
        # Mock rationale: Test input validation for negative quantities.
        mock_exists.return_value = False
        from src.tracker import add_resource

        add_resource('water', -5)

        mock_exists.assert_not_called() # Should not attempt to load/save
        mock_file_open.assert_not_called()
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_resource_negative_quantity_input(self, mock_file_open, mock_exists):
        # Mock rationale: Test input validation for negative quantities.
        mock_exists.return_value = False
        from src.tracker import remove_resource

        remove_resource('water', -5)

        mock_exists.assert_not_called() # Should not attempt to load/save
        mock_file_open.assert_not_called()
        self.assertIn("Error: Quantity must be a positive integer.", self.mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_resources_malformed_line(self, mock_file_open, mock_exists):
        # Mock rationale: Test handling of malformed lines in the resource file.
        mock_exists.return_value = True
        initial_content = "water,10\nmalformed_line\nfood,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import _load_resources

        resources = _load_resources()

        self.assertIn("Warning: Malformed line in resources.txt: 'malformed_line'. Skipping.", self.mock_stdout.getvalue())
        self.assertEqual(resources, {'water': 10, 'food': 5})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_resources_negative_quantity_in_file(self, mock_file_open, mock_exists):
        # Mock rationale: Test handling of negative quantities found in the resource file.
        mock_exists.return_value = True
        initial_content = "water,10\nbad_item,-5\nfood,5\n"
        mock_file_open.return_value.read.return_value = initial_content
        from src.tracker import _load_resources

        resources = _load_resources()

        self.assertIn("Warning: Negative quantity found for 'bad_item'. Skipping.", self.mock_stdout.getvalue())
        self.assertEqual(resources, {'water': 10, 'food': 5})

    @patch('sys.argv', ['tracker.py', 'add', 'medkit', '3'])
    @patch('src.tracker.add_resource')
    def test_main_add_command(self, mock_add_resource):
        # Mock rationale: Test the main CLI entry point for the 'add' command.
        # We mock `sys.argv` to simulate command-line arguments and `add_resource`
        # to verify it's called correctly without executing its full logic.
        from src.tracker import main
        main()
        mock_add_resource.assert_called_once_with('medkit', 3)

    @patch('sys.argv', ['tracker.py', 'remove', 'medkit', '1'])
    @patch('src.tracker.remove_resource')
    def test_main_remove_command(self, mock_remove_resource):
        # Mock rationale: Test the main CLI entry point for the 'remove' command.
        from src.tracker import main
        main()
        mock_remove_resource.assert_called_once_with('medkit', 1)

    @patch('sys.argv', ['tracker.py', 'list'])
    @patch('src.tracker.list_resources')
    def test_main_list_command(self, mock_list_resources):
        # Mock rationale: Test the main CLI entry point for the 'list' command.
        from src.tracker import main
        main()
        mock_list_resources.assert_called_once()
