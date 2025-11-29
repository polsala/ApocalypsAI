import unittest
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime

# Add the src directory to the path to allow importing chronicle_keeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Ensure the CHRONICLE_FILE constant is set for testing purposes
        self.test_chronicle_file = "test_chronicle.log"
        self.original_chronicle_file = chronicle_keeper.CHRONICLE_FILE
        chronicle_keeper.CHRONICLE_FILE = self.test_chronicle_file
        self.test_chronicle_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src', self.test_chronicle_file)

    def tearDown(self):
        # Restore original CHRONICLE_FILE constant
        chronicle_keeper.CHRONICLE_FILE = self.original_chronicle_file
        # Clean up any created test files if they somehow escape mocks
        if os.path.exists(self.test_chronicle_path):
            os.remove(self.test_chronicle_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle_keeper.datetime')
    @patch('builtins.print')
    def test_init_chronicle_creates_file_if_not_exists(self, mock_print, mock_datetime, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file not existing.
        # builtins.open is mocked to prevent actual file system interaction.
        # chronicle_keeper.datetime is mocked to control the timestamp for deterministic output.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = False
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now().strftime.return_value = "2023-10-27 10:00:00"

        chronicle_keeper.init_chronicle()

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_file_open.assert_called_once_with(self.test_chronicle_path, 'w')
        mock_file_open().write.assert_called_once_with("[2023-10-27 10:00:00] Chronicle initialized.\n")
        mock_print.assert_called_once_with(f"Chronicle initialized at: {self.test_chronicle_path}")

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_init_chronicle_does_not_create_if_exists(self, mock_print, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file already existing.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = True

        chronicle_keeper.init_chronicle()

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_print.assert_called_once_with(f"Chronicle already exists at: {self.test_chronicle_path}")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle_keeper.datetime')
    @patch('builtins.print')
    def test_add_entry_appends_message(self, mock_print, mock_datetime, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file existing.
        # builtins.open is mocked to prevent actual file system interaction.
        # chronicle_keeper.datetime is mocked to control the timestamp for deterministic output.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = True
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 5, 0)
        mock_datetime.now().strftime.return_value = "2023-10-27 10:05:00"
        message = "Found a shiny new wrench."

        chronicle_keeper.add_entry(message)

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_file_open.assert_called_once_with(self.test_chronicle_path, 'a')
        mock_file_open().write.assert_called_once_with(f"[2023-10-27 10:05:00] {message}\n")
        mock_print.assert_called_once_with(f"Entry added: {message}")

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_add_entry_handles_file_not_found(self, mock_print, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file not existing.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = False
        message = "Attempted to add entry without chronicle."

        chronicle_keeper.add_entry(message)

        mock_print.assert_called_once_with("Chronicle file not found. Please run 'init' first.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] Initialized.\n[2023-10-27 10:05:00] Entry 1.\n")
    @patch('builtins.print')
    def test_view_chronicle_displays_content(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file existing.
        # builtins.open is mocked to provide specific content for reading.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = True

        chronicle_keeper.view_chronicle()

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_file_open.assert_called_once_with(self.test_chronicle_path, 'r')
        expected_output = [
            "\n--- Chronicle Entries ---",
            "[2023-10-27 10:00:00] Initialized.",
            "[2023-10-27 10:05:00] Entry 1.",
            "-------------------------"
        ]
        mock_print.assert_has_calls([
            unittest.mock.call(line) for line in expected_output
        ])

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_view_chronicle_handles_file_not_found(self, mock_print, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file not existing.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = False

        chronicle_keeper.view_chronicle()

        mock_print.assert_called_once_with("Chronicle file not found. Please run 'init' first.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] Initialized.\n[2023-10-27 10:05:00] Found a shiny wrench.\n[2023-10-27 10:10:00] Repaired the robot arm.\n")
    @patch('builtins.print')
    def test_search_chronicle_finds_keyword(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file existing.
        # builtins.open is mocked to provide specific content for reading.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = True
        keyword = "wrench"

        chronicle_keeper.search_chronicle(keyword)

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_file_open.assert_called_once_with(self.test_chronicle_path, 'r')
        expected_output = [
            f"\n--- Search Results for '{keyword}' ---",
            "[2023-10-27 10:05:00] Found a shiny wrench.",
            "------------------------------------"
        ]
        mock_print.assert_has_calls([
            unittest.mock.call(line) for line in expected_output
        ])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] Initialized.\n")
    @patch('builtins.print')
    def test_search_chronicle_no_keyword_found(self, mock_print, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file existing.
        # builtins.open is mocked to provide specific content for reading.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = True
        keyword = "nonexistent"

        chronicle_keeper.search_chronicle(keyword)

        mock_exists.assert_called_once_with(self.test_chronicle_path)
        mock_file_open.assert_called_once_with(self.test_chronicle_path, 'r')
        mock_print.assert_called_once_with(f"No entries found containing '{keyword}'.")

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_search_chronicle_handles_file_not_found(self, mock_print, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate the file not existing.
        # builtins.print is mocked to capture output for assertions.
        mock_exists.return_value = False
        keyword = "any"

        chronicle_keeper.search_chronicle(keyword)

        mock_print.assert_called_once_with("Chronicle file not found. Please run 'init' first.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('chronicle_keeper.init_chronicle')
    @patch('chronicle_keeper.add_entry')
    @patch('chronicle_keeper.view_chronicle')
    @patch('chronicle_keeper.search_chronicle')
    def test_main_dispatch(self, mock_search, mock_view, mock_add, mock_init, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate command-line input.
        # All chronicle_keeper functions are mocked to check if they are called correctly.

        # Test 'init' command
        mock_parse_args.return_value = unittest.mock.Mock(command="init")
        chronicle_keeper.main()
        mock_init.assert_called_once()
        mock_init.reset_mock() # Reset for next test

        # Test 'add' command
        mock_parse_args.return_value = unittest.mock.Mock(command="add", message="Test message")
        chronicle_keeper.main()
        mock_add.assert_called_once_with("Test message")
        mock_add.reset_mock()

        # Test 'view' command
        mock_parse_args.return_value = unittest.mock.Mock(command="view")
        chronicle_keeper.main()
        mock_view.assert_called_once()
        mock_view.reset_mock()

        # Test 'search' command
        mock_parse_args.return_value = unittest.mock.Mock(command="search", keyword="TestKeyword")
        chronicle_keeper.main()
        mock_search.assert_called_once_with("TestKeyword")
        mock_search.reset_mock()

if __name__ == '__main__':
    unittest.main()
