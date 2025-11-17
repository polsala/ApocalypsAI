import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Mock rationale: We need to simulate file system interactions (reading/writing resource data)
# without actually touching the disk. This ensures tests are fast, deterministic, and isolated
# from the host file system. `mock_open` allows us to control what `open()` returns and
# what gets written, while `os.path.exists` allows us to simulate file presence.

# Import the functions directly for testing
# We'll patch the global RESOURCE_FILE constant in tracker.py if needed, but for now
# we'll rely on patching open and os.path.exists which are used by the functions.
from src.tracker import _load_resources, _save_resources, add_resource, remove_resource, list_resources, RESOURCE_FILE

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Capture stdout for list_resources tests
        self.held_stdout = sys.stdout
        sys.stdout = self._devnull = open(os.devnull, 'w')

        # Store initial stderr to restore later
        self.original_stderr = sys.stderr
        sys.stderr = self._devnull # Redirect stderr to devnull during tests to avoid clutter

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout.close()
        sys.stdout = self.held_stdout
        sys.stderr = self.original_stderr

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_new_file(self, mock_file_open, mock_exists):
        add_resource("Water", 10)
        mock_exists.assert_called_with(RESOURCE_FILE)
        mock_file_open.assert_called_with(RESOURCE_FILE, 'w')
        mock_file_open().write.assert_called_once_with("Water=10\n")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Food=5\n")
    def test_add_resource_existing_item(self, mock_file_open, mock_exists):
        add_resource("Food", 3)
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        mock_file_open().write.assert_called_once_with("Food=8\n")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Food=5\n")
    def test_add_resource_new_item_to_existing_file(self, mock_file_open, mock_exists):
        add_resource("Water", 10)
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        # The order of items in the file might vary depending on dict iteration, but both should be present
        # We check if the content contains both lines
        written_content = "".join(call.args[0] for call in mock_file_open().write.call_args_list)
        self.assertIn("Food=5\n", written_content)
        self.assertIn("Water=10\n", written_content)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\nFood=5\n")
    def test_remove_resource_partial(self, mock_file_open, mock_exists):
        remove_resource("Water", 3)
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        written_content = "".join(call.args[0] for call in mock_file_open().write.call_args_list)
        self.assertIn("Water=7\n", written_content)
        self.assertIn("Food=5\n", written_content)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\nFood=5\n")
    def test_remove_resource_deplete(self, mock_file_open, mock_exists):
        remove_resource("Water", 10)
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        mock_file_open().write.assert_called_once_with("Food=5\n") # Water should be gone

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\nFood=5\n")
    def test_remove_resource_over_deplete(self, mock_file_open, mock_exists):
        remove_resource("Water", 15)
        mock_file_open.assert_any_call(RESOURCE_FILE, 'r')
        mock_file_open.assert_any_call(RESOURCE_FILE, 'w')
        mock_file_open().write.assert_called_once_with("Food=5\n") # Water should be gone

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\n")
    def test_remove_resource_not_found(self, mock_file_open, mock_exists):
        remove_resource("Food", 1)
        # Should not write anything back if item not found
        mock_file_open().write.assert_not_called()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\nFood=5\n")
    def test_list_resources(self, mock_file_open, mock_exists):
        with patch('sys.stdout', new=self.held_stdout) as mock_stdout:
            list_resources()
            output = mock_stdout.getvalue()
            self.assertIn("--- Current Resources ---", output)
            self.assertIn("Food: 5", output)
            self.assertIn("Water: 10", output)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_list_resources_empty(self, mock_file_open, mock_exists):
        with patch('sys.stdout', new=self.held_stdout) as mock_stdout:
            list_resources()
            output = mock_stdout.getvalue()
            self.assertIn("No resources tracked yet.", output)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="InvalidLine\nWater=10\n")
    def test_load_resources_with_invalid_line(self, mock_file_open, mock_exists):
        resources = _load_resources()
        self.assertIn("Water", resources)
        self.assertEqual(resources["Water"], 10)
        self.assertEqual(len(resources), 1)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=abc\nFood=5\n")
    def test_load_resources_with_invalid_quantity(self, mock_file_open, mock_exists):
        resources = _load_resources()
        self.assertIn("Food", resources)
        self.assertEqual(resources["Food"], 5)
        self.assertNotIn("Water", resources)
        self.assertEqual(len(resources), 1)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_add_resource_invalid_input(self, mock_file_open, mock_exists):
        # Test empty item name
        add_resource("", 5)
        mock_file_open().write.assert_not_called()

        # Test zero quantity
        add_resource("Item", 0)
        mock_file_open().write.assert_not_called()

        # Test negative quantity
        add_resource("Item", -5)
        mock_file_open().write.assert_not_called()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Water=10\n")
    def test_remove_resource_invalid_input(self, mock_file_open, mock_exists):
        # Test empty item name
        remove_resource("", 5)
        mock_file_open().write.assert_not_called()

        # Test zero quantity
        remove_resource("Water", 0)
        mock_file_open().write.assert_not_called()

        # Test negative quantity
        remove_resource("Water", -5)
        mock_file_open().write.assert_not_called()

if __name__ == '__main__':
    unittest.main()
