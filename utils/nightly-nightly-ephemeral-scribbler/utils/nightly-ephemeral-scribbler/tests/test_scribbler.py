import unittest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO
import argparse

# Adjust sys.path to allow importing scribbler from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import scribbler

class TestEphemeralScribbler(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = StringIO()
        sys.stdout = self.held_stdout
        # Capture stderr for testing error messages
        self.held_stderr = StringIO()
        sys.stderr = self.held_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_note_new_file(self, mock_exists, mock_file):
        # Mock rationale: We don't want to create actual files during tests.
        # `mock_open` simulates file I/O, and `os.path.exists` ensures we simulate a new file.
        test_file = "test_scribbles.txt"
        test_note = "First note for the day."
        scribbler.add_note(test_note, test_file)
        mock_file.assert_called_once_with(test_file, 'a', encoding='utf-8')
        mock_file().write.assert_called_once_with(test_note + '\n')
        self.assertIn(f"Note added: '{test_note}'", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="Existing note 1\nExisting note 2\n")
    @patch('os.path.exists', return_value=True)
    def test_add_note_existing_file(self, mock_exists, mock_file):
        # Mock rationale: Simulate appending to an existing file without actual disk writes.
        test_file = "test_scribbles.txt"
        test_note = "Another important reminder."
        scribbler.add_note(test_note, test_file)
        mock_file.assert_called_once_with(test_file, 'a', encoding='utf-8')
        mock_file().write.assert_called_once_with(test_note + '\n')
        self.assertIn(f"Note added: '{test_note}'", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="Note A\nNote B\n")
    @patch('os.path.exists', return_value=True)
    def test_list_notes_with_content(self, mock_exists, mock_file):
        # Mock rationale: Simulate reading from a file with predefined content.
        test_file = "test_scribbles.txt"
        scribbler.list_notes(test_file)
        mock_file.assert_called_once_with(test_file, 'r', encoding='utf-8')
        output = self.held_stdout.getvalue()
        self.assertIn("--- Your Ephemeral Scribbles ---", output)
        self.assertIn("1. Note A", output)
        self.assertIn("2. Note B", output)

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('os.path.exists', return_value=True)
    def test_list_notes_empty_file(self, mock_exists, mock_file):
        # Mock rationale: Simulate reading from an empty file.
        test_file = "test_scribbles.txt"
        scribbler.list_notes(test_file)
        mock_file.assert_called_once_with(test_file, 'r', encoding='utf-8')
        self.assertIn("No notes found yet. Start scribbling!", self.held_stdout.getvalue())

    @patch('os.path.exists', return_value=False)
    def test_list_notes_no_file(self, mock_exists):
        # Mock rationale: Simulate the absence of a notes file.
        test_file = "non_existent_scribbles.txt"
        scribbler.list_notes(test_file)
        mock_exists.assert_called_once_with(test_file)
        self.assertIn("No notes found yet. Start scribbling!", self.held_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_clear_notes_existing_file(self, mock_exists, mock_file):
        # Mock rationale: Simulate clearing an existing file without actual disk writes.
        test_file = "test_scribbles.txt"
        scribbler.clear_notes(test_file)
        mock_file.assert_called_once_with(test_file, 'w', encoding='utf-8')
        mock_file().truncate.assert_called_once_with(0)
        self.assertIn(f"All notes cleared from '{test_file}'.", self.held_stdout.getvalue())

    @patch('os.path.exists', return_value=False)
    def test_clear_notes_no_file(self, mock_exists):
        # Mock rationale: Simulate clearing when no notes file exists.
        test_file = "non_existent_scribbles.txt"
        scribbler.clear_notes(test_file)
        mock_exists.assert_called_once_with(test_file)
        self.assertIn("No notes file to clear.", self.held_stdout.getvalue())

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_add_note_io_error(self, mock_exit, mock_exists, mock_file):
        # Mock rationale: Simulate an IOError during file write operations.
        test_file = "protected_scribbles.txt"
        test_note = "This note will fail."
        scribbler.add_note(test_note, test_file)
        self.assertIn(f"Error adding note to '{test_file}': Permission denied", self.held_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', side_effect=IOError("Disk full"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_list_notes_io_error(self, mock_exit, mock_exists, mock_file):
        # Mock rationale: Simulate an IOError during file read operations.
        test_file = "corrupt_scribbles.txt"
        scribbler.list_notes(test_file)
        self.assertIn(f"Error listing notes from '{test_file}': Disk full", self.held_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', side_effect=IOError("Read-only filesystem"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_clear_notes_io_error(self, mock_exit, mock_exists, mock_file):
        # Mock rationale: Simulate an IOError during file clear operations.
        test_file = "read_only_scribbles.txt"
        scribbler.clear_notes(test_file)
        self.assertIn(f"Error clearing notes from '{test_file}': Read-only filesystem", self.held_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scribbler.add_note')
    def test_main_add_command(self, mock_add_note, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", note="Test note content", file="custom.txt"
        )
        scribbler.main()
        mock_add_note.assert_called_once_with("Test note content", "custom.txt")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scribbler.list_notes')
    def test_main_list_command(self, mock_list_notes, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        mock_parse_args.return_value = argparse.Namespace(
            command="list", file="custom.txt"
        )
        scribbler.main()
        mock_list_notes.assert_called_once_with("custom.txt")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scribbler.clear_notes')
    def test_main_clear_command(self, mock_clear_notes, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and verify the correct function is called.
        mock_parse_args.return_value = argparse.Namespace(
            command="clear", file="custom.txt"
        )
        scribbler.main()
        mock_clear_notes.assert_called_once_with("custom.txt")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.print_help')
    @patch('sys.exit')
    def test_main_no_command(self, mock_exit, mock_print_help, mock_parse_args):
        # Mock rationale: Simulate no command being provided and verify help is printed and exit code is 1.
        mock_parse_args.return_value = argparse.Namespace(command=None, file="default.txt")
        scribbler.main()
        mock_print_help.assert_called_once()
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scribbler.add_note')
    def test_main_default_file(self, mock_add_note, mock_parse_args):
        # Mock rationale: Verify that the default file path is used when --file is not specified.
        mock_parse_args.return_value = argparse.Namespace(
            command="add", note="Default file test", file=scribbler.DEFAULT_NOTES_FILE
        )
        scribbler.main()
        mock_add_note.assert_called_once_with("Default file test", scribbler.DEFAULT_NOTES_FILE)


if __name__ == '__main__':
    unittest.main()
