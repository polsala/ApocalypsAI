import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import sys

# Add the src directory to the Python path for importing logbook
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from logbook import add_entry, view_entries, _get_log_file_path, DEFAULT_LOG_FILENAME

class TestLogbook(unittest.TestCase):

    def setUp(self):
        # Ensure a consistent log file path for testing
        self.test_log_file = os.path.join(os.getcwd(), 'test_chronicle.log')

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_file_open, mock_dt):
        # Mock rationale: datetime.datetime.now() is mocked to ensure deterministic timestamps in log entries.
        # builtins.open is mocked to prevent actual file system interaction during tests, allowing inspection of written content.
        mock_dt.now.return_value = datetime.datetime(2077, 10, 23, 13, 37, 0)
        expected_timestamp = '2077-10-23 13:37:00'
        test_message = "Found a pristine Nuka-Cola Quantum!"
        expected_entry = f"[{expected_timestamp}] {test_message}\n"

        add_entry(test_message, self.test_log_file)

        mock_file_open.assert_called_once_with(self.test_log_file, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_entry)

    @patch('builtins.open', new_callable=mock_open, read_data="[2077-10-23 13:37:00] First entry\n[2077-10-24 08:00:00] Second entry\n")
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_entries_existing_file(self, mock_stdout, mock_file_open):
        # Mock rationale: builtins.open is mocked to simulate reading from a log file without actual file system interaction.
        # sys.stdout is mocked to capture printed output and assert its content.
        view_entries(self.test_log_file)

        mock_file_open.assert_called_once_with(self.test_log_file, 'r', encoding='utf-8')
        expected_output = (
            "\n--- Chronicle Logbook ---\n"
            "[2077-10-23 13:37:00] First entry\n"
            "[2077-10-24 08:00:00] Second entry\n"
            "-------------------------\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_entries_file_not_found(self, mock_stdout, mock_file_open):
        # Mock rationale: builtins.open is mocked to raise FileNotFoundError, simulating the case where the log file does not exist.
        # sys.stdout is mocked to capture printed output and assert its content.
        view_entries(self.test_log_file)

        mock_file_open.assert_called_once_with(self.test_log_file, 'r', encoding='utf-8')
        self.assertIn(f"Log file {self.test_log_file} not found. No entries yet.\n", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_view_entries_empty_file(self, mock_stdout, mock_file_open):
        # Mock rationale: builtins.open is mocked to simulate an empty log file.
        # sys.stdout is mocked to capture printed output and assert its content.
        view_entries(self.test_log_file)

        mock_file_open.assert_called_once_with(self.test_log_file, 'r', encoding='utf-8')
        self.assertIn(f"Log file {self.test_log_file} is empty.\n", mock_stdout.getvalue())

    def test_get_log_file_path(self):
        # This test does not require mocking as it only uses os.path.join and os.getcwd()
        # which are deterministic for a given test environment.
        expected_path = os.path.join(os.getcwd(), DEFAULT_LOG_FILENAME)
        self.assertEqual(_get_log_file_path(), expected_path)
        custom_filename = 'my_custom.log'
        expected_custom_path = os.path.join(os.getcwd(), custom_filename)
        self.assertEqual(_get_log_file_path(custom_filename), expected_custom_path)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.add_entry')
    @patch('logbook._get_log_file_path')
    def test_main_add_command(self, mock_get_path, mock_add_entry, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate command-line arguments.
        # logbook.add_entry is mocked to verify it's called with correct arguments without executing its full logic.
        # logbook._get_log_file_path is mocked to return a consistent path for testing.
        mock_parse_args.return_value = unittest.mock.Mock(command='add', message='Test message')
        mock_get_path.return_value = self.test_log_file

        from logbook import main
        main()

        mock_add_entry.assert_called_once_with('Test message', self.test_log_file)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('logbook.view_entries')
    @patch('logbook._get_log_file_path')
    def test_main_view_command(self, mock_get_path, mock_view_entries, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate command-line arguments.
        # logbook.view_entries is mocked to verify it's called with correct arguments without executing its full logic.
        # logbook._get_log_file_path is mocked to return a consistent path for testing.
        mock_parse_args.return_value = unittest.mock.Mock(command='view')
        mock_get_path.return_value = self.test_log_file

        from logbook import main
        main()

        mock_view_entries.assert_called_once_with(self.test_log_file)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate no command being provided.
        # argparse.ArgumentParser.print_help is mocked to verify that help is printed in this scenario.
        mock_parse_args.return_value = unittest.mock.Mock(command=None)

        from logbook import main
        main()

        mock_print_help.assert_called_once()
