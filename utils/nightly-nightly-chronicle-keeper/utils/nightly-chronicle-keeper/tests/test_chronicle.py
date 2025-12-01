import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
from pathlib import Path
import sys
import io # Required for capturing stdout/stderr in tests

# Adjust path to import chronicle.py from the src directory
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from chronicle import ChronicleKeeper

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Use a dummy log file path for testing, relative to the test script
        self.test_log_file = Path("test_chronicle.log")
        self.keeper = ChronicleKeeper(log_file=self.test_log_file)

    @patch('builtins.open', new_callable=mock_open)
    @patch('chronicle.datetime') # Mock datetime from the chronicle module
    def test_add_entry(self, mock_dt, mock_file_open):
        # Mock rationale: We need to control the timestamp for deterministic tests
        # and prevent actual file system writes. By patching 'chronicle.datetime',
        # we ensure that calls to datetime.now() within the ChronicleKeeper class
        # return our fixed_datetime, making the timestamp predictable.
        fixed_datetime = datetime(2077, 10, 23, 13, 37, 0)
        mock_dt.now.return_value = fixed_datetime

        entry_text = "Discovered a new species of glowing fungi."
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.keeper.add_entry(entry_text)
            self.assertIn("Chronicle added:", mock_stdout.getvalue())

        # Ensure open was called with 'a' (append) mode and correct path
        mock_file_open.assert_called_once_with(self.test_log_file, "a", encoding="utf-8")
        # Ensure the correct content was written. strftime is called on fixed_datetime.
        mock_file_open().write.assert_called_once_with("[2077-10-23 13:37:00] Discovered a new species of glowing fungi.\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists', return_value=True)
    def test_view_entries_with_content(self, mock_exists, mock_file_open):
        # Mock rationale: We need to simulate a log file existing with specific content
        # without actually creating files. 'mock_exists' ensures the keeper thinks
        # the file is there, and 'mock_file_open' provides the content.
        mock_file_open.return_value.__enter__.return_value.read.return_value = (
            "[2077-10-23 13:37:00] First entry.\n"
            "[2077-10-24 08:00:00] Second entry.\n"
        )

        # Capture stdout to check printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.keeper.view_entries()
            output = mock_stdout.getvalue()

            self.assertIn("--- Your Chronicles ---", output)
            self.assertIn("[2077-10-23 13:37:00] First entry.", output)
            self.assertIn("[2077-10-24 08:00:00] Second entry.", output)
            self.assertIn("-----------------------", output)

        mock_file_open.assert_called_once_with(self.test_log_file, "r", encoding="utf-8")

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists', return_value=False)
    def test_view_entries_no_file(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate the scenario where the log file does not exist yet.
        # 'mock_exists' returns False, preventing 'open' from being called.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.keeper.view_entries()
            output = mock_stdout.getvalue()
            self.assertIn("No chronicles found yet. Start by adding an entry!", output)
        mock_file_open.assert_not_called() # Ensure open is not called if file doesn't exist

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists', return_value=True)
    def test_view_entries_empty_file(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate an empty log file. 'mock_exists' returns True,
        # and 'mock_file_open' provides an empty string as content.
        mock_file_open.return_value.__enter__.return_value.read.return_value = ""

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.keeper.view_entries()
            output = mock_stdout.getvalue()
            self.assertIn("Chronicle log is empty. Time to make some history!", output)
        mock_file_open.assert_called_once_with(self.test_log_file, "r", encoding="utf-8")

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('chronicle.datetime')
    def test_add_entry_io_error(self, mock_dt, mock_file_open):
        # Mock rationale: Simulate an IOError during file writing. 'mock_file_open'
        # is configured to raise an IOError when called, and 'mock_dt' provides
        # a fixed timestamp for consistency.
        fixed_datetime = datetime(2077, 10, 23, 13, 37, 0)
        mock_dt.now.return_value = fixed_datetime

        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                self.keeper.add_entry("Test entry with error.")
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error writing to chronicle log: Permission denied", mock_stderr.getvalue())

    @patch('builtins.open', side_effect=IOError("File corrupted"))
    @patch('pathlib.Path.exists', return_value=True)
    def test_view_entries_io_error(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate an IOError during file reading. 'mock_file_open'
        # is configured to raise an IOError when called, and 'mock_exists' ensures
        # the file is considered present before the read attempt.
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                self.keeper.view_entries()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error reading chronicle log: File corrupted", mock_stderr.getvalue())
