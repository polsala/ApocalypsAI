import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os
import sys

# Add the src directory to the path to allow importing journal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import journal

class TestJournal(unittest.TestCase):

    def setUp(self):
        # Ensure the journal file path is consistent for testing
        self.mock_journal_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../src',
            journal.JOURNAL_FILE
        )
        # Mock rationale: We need to control the path resolution for the journal file
        # to ensure tests are deterministic and don't rely on the actual file system.
        # This prevents `_get_journal_path()` from creating real files or looking in unexpected places.
        self.patch_abspath = patch('os.path.abspath', return_value=self.mock_journal_path)
        self.mock_abspath = self.patch_abspath.start()
        self.patch_dirname = patch('os.path.dirname', return_value=os.path.dirname(self.mock_journal_path))
        self.mock_dirname = self.patch_dirname.start()
        # Use real os.path.join but with mocked dirname/abspath to ensure correct path construction
        self.patch_join = patch('os.path.join', side_effect=os.path.join)
        self.mock_join = self.patch_join.start()


    def tearDown(self):
        self.patch_abspath.stop()
        self.patch_dirname.stop()
        self.patch_join.stop()

    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_add_entry(self, mock_datetime, mock_file):
        # Mock rationale: We need to control the current time for deterministic timestamps
        # in the journal entries. `datetime.datetime.now()` is mocked to return a fixed time.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.strftime.return_value = "2023-10-27 10:00:00"
        # Mock rationale: We need to simulate file writing without actually touching the disk.
        # `mock_open` allows us to inspect what would have been written to the file.
        
        entry_text = "Found a perfectly good can of beans."
        journal.add_entry(entry_text)

        mock_file.assert_called_once_with(self.mock_journal_path, "a")
        mock_file().write.assert_called_once_with(f"[2023-10-27 10:00:00] {entry_text}\n")

    @patch('builtins.open', new_callable=mock_open, read_data="[2023-10-27 10:00:00] First entry\n[2023-10-28 11:00:00] Second entry\n")
    @patch('sys.stdout', new_callable=MagicMock)
    def test_view_entries_with_data(self, mock_stdout, mock_file):
        # Mock rationale: We need to simulate reading from a journal file with predefined content.
        # `mock_open` allows us to provide the data that would be read from the file.
        # Mock rationale: We need to capture the output printed to stdout to verify it matches
        # the expected display of journal entries. `sys.stdout` is mocked to capture `write` calls.
        
        journal.view_entries()

        mock_file.assert_called_once_with(self.mock_journal_path, "r")
        expected_output = (
            "--- Your Gratitude Journal ---\n"
            "[2023-10-27 10:00:00] First entry\n"
            "[2023-10-28 11:00:00] Second entry\n"
            "-----------------------------\n"
        )
        # Check if the expected output was part of the calls to stdout.write
        # We use assert_any_call because print() might make multiple calls to write.
        mock_stdout.write.assert_any_call(expected_output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_view_entries_empty(self, mock_stdout, mock_file):
        # Mock rationale: Simulate an empty journal file by making `open` raise `FileNotFoundError`.
        # This tests the handling of a non-existent journal file.
        # Mock rationale: Capture stdout to verify the "empty" message is printed.
        
        mock_file.side_effect = FileNotFoundError # Simulate file not existing
        journal.view_entries()

        mock_stdout.write.assert_any_call("Your gratitude journal is empty. Start adding entries!\n")

    @patch('random.choice', return_value="What small comfort did you find today?")
    def test_get_silver_lining_prompt(self, mock_random_choice):
        # Mock rationale: We need to ensure a specific prompt is returned for deterministic testing,
        # rather than relying on random selection. `random.choice` is mocked to return a fixed value.
        
        prompt = journal.get_silver_lining_prompt()
        self.assertEqual(prompt, "What small comfort did you find today?")
        mock_random_choice.assert_called_once_with(journal.SILVER_LINING_PROMPTS)

    @patch('sys.argv', ['journal.py', 'add', 'Grateful for clean water.'])
    @patch('journal.add_entry')
    @patch('builtins.print')
    def test_main_add_command(self, mock_print, mock_add_entry):
        # Mock rationale: Control `sys.argv` to simulate command-line arguments passed to the script.
        # Mock rationale: Prevent actual file operations by mocking `journal.add_entry`.
        # Mock rationale: Capture `print` statements to verify output messages.
        
        journal.main()
        mock_add_entry.assert_called_once_with('Grateful for clean water.')
        mock_print.assert_called_once_with("Entry added: 'Grateful for clean water.'")

    @patch('sys.argv', ['journal.py', 'view'])
    @patch('journal.view_entries')
    def test_main_view_command(self, mock_view_entries):
        # Mock rationale: Control `sys.argv` to simulate command-line arguments.
        # Mock rationale: Prevent actual file operations by mocking `journal.view_entries`.
        
        journal.main()
        mock_view_entries.assert_called_once()

    @patch('sys.argv', ['journal.py', 'prompt'])
    @patch('journal.get_silver_lining_prompt', return_value="Test prompt.")
    @patch('builtins.print')
    def test_main_prompt_command(self, mock_print, mock_get_prompt):
        # Mock rationale: Control `sys.argv` to simulate command-line arguments.
        # Mock rationale: Control the returned prompt for deterministic testing.
        # Mock rationale: Capture `print` statements to verify output messages.
        
        journal.main()
        mock_get_prompt.assert_called_once()
        mock_print.assert_any_call("Silver Lining Prompt:")
        mock_print.assert_any_call("Test prompt.")

    @patch('sys.argv', ['journal.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_print):
        # Mock rationale: Control `sys.argv` to simulate no command-line arguments.
        # Mock rationale: Capture `print` statements to verify the usage message.
        # Mock rationale: Prevent actual program exit during testing by mocking `sys.exit`.
        
        journal.main()
        mock_print.assert_any_call("Usage:")
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['journal.py', 'add'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_add_no_entry_text(self, mock_exit, mock_print):
        # Mock rationale: Control `sys.argv` to simulate missing entry text for the 'add' command.
        # Mock rationale: Capture `print` statements to verify the error message.
        # Mock rationale: Prevent actual program exit during testing.
        
        journal.main()
        mock_print.assert_any_call("Error: 'add' command requires an entry text.")
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['journal.py', 'unknown_command'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_unknown_command(self, mock_exit, mock_print):
        # Mock rationale: Control `sys.argv` to simulate an unknown command.
        # Mock rationale: Capture `print` statements to verify the error message.
        # Mock rationale: Prevent actual program exit during testing.
        
        journal.main()
        mock_print.assert_any_call("Unknown command: unknown_command")
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_add_entry_io_error(self, mock_exit, mock_print, mock_datetime, mock_file):
        # Mock rationale: Simulate an `IOError` during file writing to test error handling.
        # `mock_file.side_effect` is used to raise the error when `open` is called.
        # Mock rationale: Capture `print` statements to verify the error message.
        # Mock rationale: Prevent actual program exit during testing.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.strftime.return_value = "2023-10-27 10:00:00"
        mock_file.side_effect = IOError("Disk full")

        journal.add_entry("Test entry")
        mock_print.assert_any_call("Error writing to journal: Disk full")
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_view_entries_io_error(self, mock_exit, mock_print, mock_file):
        # Mock rationale: Simulate an `IOError` during file reading to test error handling.
        # `mock_file.side_effect` is used to raise the error when `open` is called.
        # Mock rationale: Capture `print` statements to verify the error message.
        # Mock rationale: Prevent actual program exit during testing.
        mock_file.side_effect = IOError("Permission denied")

        journal.view_entries()
        mock_print.assert_any_call("Error reading journal: Permission denied")
        mock_exit.assert_called_once_with(1)
