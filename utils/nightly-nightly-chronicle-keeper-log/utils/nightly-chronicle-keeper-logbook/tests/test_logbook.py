import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os
import sys
from io import StringIO

# Add the src directory to the Python path to allow importing logbook
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import logbook

class TestLogbook(unittest.TestCase):

    @patch('datetime.datetime')
    def test_get_timestamp(self, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for testing.
        fixed_time = datetime.datetime(2023, 10, 27, 10, 30, 0)
        mock_dt.now.return_value = fixed_time
        # Allow actual datetime object methods to be called on the mocked object
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        timestamp = logbook._get_timestamp()
        self.assertEqual(timestamp, "2023-10-27 10:30:00")

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate directory not existing initially.
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_add_entry_new_file_and_dir(self, mock_dt, mock_file_open, mock_path_exists, mock_makedirs):
        # Mock rationale: Ensure deterministic timestamp for testing.
        fixed_time = datetime.datetime(2023, 10, 27, 10, 30, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        test_message = "Found a shiny new wrench."
        test_log_path = "test_logs/chronicle.log"

        # Capture print output
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            logbook.add_entry(test_message, test_log_path)
            self.assertIn(f"Entry added to {test_log_path}", fake_stdout.getvalue())

        mock_makedirs.assert_called_once_with("test_logs") # Mock rationale: Verify directory creation.
        mock_file_open.assert_called_once_with(test_log_path, 'a', encoding='utf-8') # Mock rationale: Verify file opened in append mode.
        mock_file_open().write.assert_called_once_with(f"[2023-10-27 10:30:00] {test_message}\n") # Mock rationale: Verify content written.

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate directory already existing.
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_add_entry_existing_file_no_dir_creation(self, mock_dt, mock_path_exists, mock_file_open, mock_makedirs):
        # Mock rationale: Ensure deterministic timestamp for testing.
        fixed_time = datetime.datetime(2023, 10, 27, 10, 30, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        test_message = "Traded some canned beans for a map."
        test_log_path = "test_logs/chronicle.log"

        with patch('sys.stdout', new=StringIO()):
            logbook.add_entry(test_message, test_log_path)

        mock_makedirs.assert_not_called() # Mock rationale: No directory creation if it already exists.
        mock_file_open.assert_called_once_with(test_log_path, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(f"[2023-10-27 10:30:00] {test_message}\n")

    @patch('logbook.add_entry')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_invocation(self, mock_parse_args, mock_add_entry):
        # Mock rationale: Simulate command-line arguments without actual sys.argv manipulation.
        # Mock rationale: Prevent actual file operations during CLI test.
        
        mock_args = MagicMock()
        mock_args.message = "Scavenged some useful parts."
        mock_args.output = "custom_logs/my_chronicle.log"
        mock_parse_args.return_value = mock_args

        logbook.main()

        mock_add_entry.assert_called_once_with(
            "Scavenged some useful parts.",
            "custom_logs/my_chronicle.log"
        )

    @patch('logbook.add_entry')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_invocation_default_output(self, mock_parse_args, mock_add_entry):
        # Mock rationale: Simulate command-line arguments without actual sys.argv manipulation.
        # Mock rationale: Prevent actual file operations during CLI test.

        mock_args = MagicMock()
        mock_args.message = "Found a new safe zone."
        mock_args.output = os.path.join("logs", "chronicle.log") # Default value
        mock_parse_args.return_value = mock_args

        logbook.main()

        mock_add_entry.assert_called_once_with(
            "Found a new safe zone.",
            os.path.join("logs", "chronicle.log")
        )

    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_cli_no_message_exits(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate command-line invocation without a message,
        # and capture argparse's error output and exit behavior.
        
        # Simulate no message argument by patching sys.argv
        with patch('sys.argv', ['logbook.py']):
            with self.assertRaises(SystemExit) as cm:
                logbook.main()
            
            self.assertEqual(cm.exception.code, 2) # argparse exits with code 2 for argument errors
            mock_exit.assert_called_once_with(2) # Verify sys.exit was called
            self.assertIn("the following arguments are required: message", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
