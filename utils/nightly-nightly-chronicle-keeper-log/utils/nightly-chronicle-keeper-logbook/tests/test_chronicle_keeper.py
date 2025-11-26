import unittest
import unittest.mock
import os
import sys
from io import StringIO
from datetime import datetime

# Add the src directory to the Python path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper
sys.path.pop(0) # Clean up sys.path

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()
        self.mock_log_file = "test_chronicle.log"

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout
        # Clean up any potential files created by tests (though mocks should prevent this)
        if os.path.exists(self.mock_log_file):
            os.remove(self.mock_log_file)

    @unittest.mock.patch('chronicle_keeper.datetime')
    @unittest.mock.patch('builtins.open', unittest.mock.mock_open())
    @unittest.mock.patch('os.path.exists', return_value=False) # Mock file not existing initially
    def test_add_entry(self, mock_exists, mock_open, mock_datetime):
        # Mock rationale:
        # - datetime: Ensures deterministic timestamps for log entries.
        # - builtins.open: Prevents actual file system interaction, making tests isolated and fast.
        # - os.path.exists: Controls the perceived existence of the log file for 'view_log' tests.

        # Set a fixed datetime for deterministic testing
        fixed_time = datetime(2077, 10, 23, 13, 37, 0)
        mock_datetime.datetime.now.return_value = fixed_time
        mock_datetime.datetime.strftime = datetime.strftime # Ensure strftime works on the mock

        test_message = "Found a shiny bottlecap."
        chronicle_keeper.add_entry(test_message, self.mock_log_file)

        # Check if open was called correctly
        mock_open.assert_called_once_with(self.mock_log_file, "a")
        # Check if write was called with the correct content
        expected_entry = "[2077-10-23 13:37:00] Found a shiny bottlecap.\n"
        mock_open().write.assert_called_once_with(expected_entry)

        # Check stdout message
        self.assertIn(f"Entry added to {self.mock_log_file}", sys.stdout.getvalue())

    @unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data="[2077-10-23 13:37:00] First entry.\n[2077-10-23 13:38:00] Second entry.\n"))
    @unittest.mock.patch('os.path.exists', return_value=True)
    def test_view_log_with_content(self, mock_exists, mock_open):
        # Mock rationale:
        # - builtins.open: Provides predefined content for the log file without actual file I/O.
        # - os.path.exists: Simulates the log file existing.

        chronicle_keeper.view_log(self.mock_log_file)
        output = sys.stdout.getvalue()

        self.assertIn(f"--- Contents of {self.mock_log_file} ---", output)
        self.assertIn("[2077-10-23 13:37:00] First entry.", output)
        self.assertIn("[2077-10-23 13:38:00] Second entry.", output)
        self.assertIn(f"--- End of {self.mock_log_file} ---", output)
        mock_open.assert_called_once_with(self.mock_log_file, "r")

    @unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=""))
    @unittest.mock.patch('os.path.exists', return_value=True)
    def test_view_log_empty(self, mock_exists, mock_open):
        # Mock rationale:
        # - builtins.open: Simulates an empty log file.
        # - os.path.exists: Simulates the log file existing.

        chronicle_keeper.view_log(self.mock_log_file)
        output = sys.stdout.getvalue()

        self.assertIn(f"Log file '{self.mock_log_file}' is empty.", output)
        mock_open.assert_called_once_with(self.mock_log_file, "r")

    @unittest.mock.patch('os.path.exists', return_value=False)
    def test_view_log_not_found(self, mock_exists):
        # Mock rationale:
        # - os.path.exists: Simulates the log file not existing.

        chronicle_keeper.view_log(self.mock_log_file)
        output = sys.stdout.getvalue()

        self.assertIn(f"Log file '{self.mock_log_file}' not found.", output)
        mock_exists.assert_called_once_with(self.mock_log_file)

    @unittest.mock.patch('chronicle_keeper.add_entry')
    @unittest.mock.patch('chronicle_keeper.view_log')
    @unittest.mock.patch('argparse.ArgumentParser.parse_args')
    def test_main_add_message(self, mock_parse_args, mock_view_log, mock_add_entry):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: Controls the command-line arguments passed to main.
        # - chronicle_keeper.add_entry: Mocks the function being tested to ensure it's called correctly.
        # - chronicle_keeper.view_log: Mocks the other function to ensure it's NOT called.

        mock_parse_args.return_value = argparse.Namespace(
            message="Test message for main",
            log_file="main_test.log",
            view=False
        )
        chronicle_keeper.main()
        mock_add_entry.assert_called_once_with("Test message for main", "main_test.log")
        mock_view_log.assert_not_called()

    @unittest.mock.patch('chronicle_keeper.add_entry')
    @unittest.mock.patch('chronicle_keeper.view_log')
    @unittest.mock.patch('argparse.ArgumentParser.parse_args')
    def test_main_view_log(self, mock_parse_args, mock_view_log, mock_add_entry):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: Controls the command-line arguments passed to main.
        # - chronicle_keeper.view_log: Mocks the function being tested to ensure it's called correctly.
        # - chronicle_keeper.add_entry: Mocks the other function to ensure it's NOT called.

        mock_parse_args.return_value = argparse.Namespace(
            message=None,
            log_file="main_test.log",
            view=True
        )
        chronicle_keeper.main()
        mock_view_log.assert_called_once_with("main_test.log")
        mock_add_entry.assert_not_called()

    @unittest.mock.patch('chronicle_keeper.add_entry')
    @unittest.mock.patch('chronicle_keeper.view_log')
    @unittest.mock.patch('argparse.ArgumentParser.parse_args')
    @unittest.mock.patch('argparse.ArgumentParser.print_help')
    def test_main_no_args(self, mock_print_help, mock_parse_args, mock_view_log, mock_add_entry):
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: Simulates no relevant arguments being passed.
        # - argparse.ArgumentParser.print_help: Ensures the help message is printed when no action is specified.
        # - chronicle_keeper.add_entry/view_log: Ensures no action functions are called.

        mock_parse_args.return_value = argparse.Namespace(
            message=None,
            log_file="main_test.log",
            view=False
        )
        chronicle_keeper.main()
        mock_print_help.assert_called_once()
        mock_add_entry.assert_not_called()
        mock_view_log.assert_not_called()

if __name__ == '__main__':
    unittest.main()
