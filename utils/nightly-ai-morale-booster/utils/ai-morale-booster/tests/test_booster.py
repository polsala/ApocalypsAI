import unittest
import sys
import os
import io
import datetime
from unittest.mock import patch, mock_open
from src.booster import generate_message, log_message, main, MESSAGES

class TestMoraleBooster(unittest.TestCase):

    def test_generate_message_returns_string(self):
        """Test that generate_message returns a string."""
        message = generate_message()
        self.assertIsInstance(message, str)

    def test_generate_message_is_from_list(self):
        """Test that generate_message returns a message from the predefined list."""
        message = generate_message()
        self.assertIn(message, MESSAGES)

    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_log_message_writes_to_file(self, mock_dt, mock_file_open):
        """Test that log_message correctly writes a timestamped message to a file."""
        # Mock rationale: We need to ensure that `log_message` attempts to open a file
        # in append mode and writes the correct content. Mocking `open` allows us to
        # inspect the calls made to the file system without actually creating files.
        # Mocking `datetime.datetime` ensures deterministic timestamps for testing.
        
        mock_dt.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_dt.strftime.return_value = "2023-10-27 10:00:00"
        
        test_message = "Test message for logging."
        test_log_file = "test_log.txt"

        log_message(test_message, test_log_file)

        mock_file_open.assert_called_once_with(test_log_file, 'a')
        mock_file_open().write.assert_called_once_with(f"2023-10-27 10:00:00 - {test_message}\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.booster.generate_message', return_value="Mocked message.")
    @patch('src.booster.log_message')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_prints_message(self, mock_parse_args, mock_log_message, mock_generate_message, mock_stdout):
        """Test that main function prints the generated message to stdout."""
        # Mock rationale: We want to test the `main` function's output and behavior
        # without actual side effects like random message generation, file I/O,
        # or parsing real command-line arguments.
        # - `sys.stdout` is mocked to capture printed output.
        # - `generate_message` is mocked to return a fixed string for determinism.
        # - `log_message` is mocked to prevent actual file writes.
        # - `parse_args` is mocked to control CLI arguments programmatically.

        mock_parse_args.return_value = argparse.Namespace(log_file=None)

        main()

        self.assertIn("[ApocalypsAI Morale Booster] Mocked message.", mock_stdout.getvalue())
        mock_generate_message.assert_called_once()
        mock_log_message.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.booster.generate_message', return_value="Another mocked message.")
    @patch('src.booster.log_message')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_logs_message_when_log_file_specified(self, mock_parse_args, mock_log_message, mock_generate_message, mock_stdout):
        """Test that main function calls log_message when --log-file is provided."""
        # Mock rationale: Similar to the above, ensuring `main` behaves correctly
        # when the `--log-file` argument is present, without actual file operations.

        test_log_file = "test_cli_log.txt"
        mock_parse_args.return_value = argparse.Namespace(log_file=test_log_file)

        main()

        self.assertIn("[ApocalypsAI Morale Booster] Another mocked message.", mock_stdout.getvalue())
        mock_generate_message.assert_called_once()
        mock_log_message.assert_called_once_with("Another mocked message.", test_log_file)

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('src.booster.generate_message', return_value="Error message.")
    @patch('src.booster.log_message', side_effect=IOError("Permission denied"))
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_handles_log_file_error(self, mock_parse_args, mock_log_message, mock_generate_message, mock_exit, mock_stderr):
        """Test that main function handles IOError during logging and exits with code 1."""
        # Mock rationale: Simulate an IOError during file logging (e.g., permission denied)
        # to ensure the `main` function catches it, prints an error to stderr,
        # and exits with the correct status code (1).

        test_log_file = "/no/permission/log.txt"
        mock_parse_args.return_value = argparse.Namespace(log_file=test_log_file)

        main()

        self.assertIn(f"Error logging message to {test_log_file}: Permission denied", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
