import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import datetime

# Add the src directory to the path to allow importing journal.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import journal

class TestJournal(unittest.TestCase):

    @patch('journal.os.makedirs')
    @patch('journal.open', new_callable=mock_open)
    @patch('journal.datetime')
    def test_add_entry(self, mock_dt, mock_file_open, mock_makedirs):
        # Mock rationale:
        # - journal.os.makedirs: Prevent actual directory creation during tests.
        # - journal.open: Simulate file writing without touching the filesystem.
        # - journal.datetime: Ensure deterministic timestamps for testing.

        mock_dt.datetime.now.return_value = datetime.datetime(2024, 7, 26, 10, 30, 0)
        mock_dt.datetime.strftime.return_value = "2024-07-26 10:30:00"

        test_entry = "Grateful for the quiet hum of the last generator."
        journal.add_entry(test_entry)

        mock_makedirs.assert_called_once_with(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'), exist_ok=True)
        mock_file_open.assert_called_once_with(
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'journal.txt'), "a"
        )
        mock_file_open().write.assert_called_once_with(
            "[2024-07-26 10:30:00] - Grateful for the quiet hum of the last generator.\n"
        )

    @patch('journal.os.path.exists')
    @patch('journal.open', new_callable=mock_open)
    def test_get_entries_no_file(self, mock_file_open, mock_exists):
        # Mock rationale:
        # - journal.os.path.exists: Simulate the journal file not existing.
        # - journal.open: Ensure file is not opened if it doesn't exist.

        mock_exists.return_value = False
        with patch('builtins.print') as mock_print:
            entries = journal.get_entries()
            self.assertEqual(entries, [])
            mock_print.assert_called_once_with("No entries found yet. Start by adding one!")
        mock_exists.assert_called_once()
        mock_file_open.assert_not_called()

    @patch('journal.os.path.exists')
    @patch('journal.open', new_callable=mock_open, read_data="[2024-07-26 10:00:00] - Entry 1\n[2024-07-26 11:00:00] - Entry 2\n[2024-07-27 09:00:00] - Entry 3\n")
    def test_get_all_entries(self, mock_file_open, mock_exists):
        # Mock rationale:
        # - journal.os.path.exists: Simulate the journal file existing.
        # - journal.open: Simulate reading predefined journal content.

        mock_exists.return_value = True
        entries = journal.get_entries()
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0], "[2024-07-26 10:00:00] - Entry 1")
        self.assertEqual(entries[1], "[2024-07-26 11:00:00] - Entry 2")
        self.assertEqual(entries[2], "[2024-07-27 09:00:00] - Entry 3")
        mock_exists.assert_called_once()
        mock_file_open.assert_called_once()

    @patch('journal.os.path.exists')
    @patch('journal.open', new_callable=mock_open, read_data="[2024-07-26 10:00:00] - Entry 1\n[2024-07-26 11:00:00] - Entry 2\n[2024-07-27 09:00:00] - Entry 3\n")
    def test_get_entries_by_date(self, mock_file_open, mock_exists):
        # Mock rationale:
        # - journal.os.path.exists: Simulate the journal file existing.
        # - journal.open: Simulate reading predefined journal content.

        mock_exists.return_value = True
        entries = journal.get_entries(date_filter="2024-07-26")
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], "[2024-07-26 10:00:00] - Entry 1")
        self.assertEqual(entries[1], "[2024-07-26 11:00:00] - Entry 2")
        mock_exists.assert_called_once()
        mock_file_open.assert_called_once()

    @patch('journal.os.path.exists')
    @patch('journal.open', new_callable=mock_open, read_data="[2024-07-26 10:00:00] - Entry 1\n")
    def test_get_entries_by_date_no_match(self, mock_file_open, mock_exists):
        # Mock rationale:
        # - journal.os.path.exists: Simulate the journal file existing.
        # - journal.open: Simulate reading predefined journal content.

        mock_exists.return_value = True
        entries = journal.get_entries(date_filter="2024-07-28")
        self.assertEqual(entries, [])
        mock_exists.assert_called_once()
        mock_file_open.assert_called_once()

    @patch('journal.argparse.ArgumentParser')
    @patch('journal.add_entry')
    @patch('journal.get_entries')
    def test_main_add_command(self, mock_get_entries, mock_add_entry, mock_argparse):
        # Mock rationale:
        # - journal.argparse.ArgumentParser: Control command-line arguments for testing.
        # - journal.add_entry: Isolate and test the 'add' command's logic.
        # - journal.get_entries: Ensure 'view' is not called during 'add' test.

        mock_args = MagicMock()
        mock_args.command = "add"
        mock_args.text = "Test gratitude"
        mock_argparse.return_value.parse_args.return_value = mock_args

        journal.main()
        mock_add_entry.assert_called_once_with("Test gratitude")
        mock_get_entries.assert_not_called()

    @patch('journal.argparse.ArgumentParser')
    @patch('journal.add_entry')
    @patch('journal.get_entries', return_value=["[2024-07-26 12:00:00] - Test entry"])
    def test_main_view_command(self, mock_get_entries, mock_add_entry, mock_argparse):
        # Mock rationale:
        # - journal.argparse.ArgumentParser: Control command-line arguments for testing.
        # - journal.add_entry: Ensure 'add' is not called during 'view' test.
        # - journal.get_entries: Isolate and test the 'view' command's logic, providing mock data.

        mock_args = MagicMock()
        mock_args.command = "view"
        mock_args.date = None
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            journal.main()
            mock_get_entries.assert_called_once_with(None)
            mock_add_entry.assert_not_called()
            self.assertIn("Test entry", mock_print.call_args_list[1].args[0]) # Check if the entry was printed

    @patch('journal.argparse.ArgumentParser')
    @patch('journal.add_entry')
    @patch('journal.get_entries', return_value=[])
    def test_main_view_command_no_entries(self, mock_get_entries, mock_add_entry, mock_argparse):
        # Mock rationale:
        # - journal.argparse.ArgumentParser: Control command-line arguments for testing.
        # - journal.add_entry: Ensure 'add' is not called.
        # - journal.get_entries: Simulate no entries found.

        mock_args = MagicMock()
        mock_args.command = "view"
        mock_args.date = None
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            journal.main()
            mock_get_entries.assert_called_once_with(None)
            mock_add_entry.assert_not_called()
            mock_print.assert_called_once_with("No entries found yet. Start by adding one!")

    @patch('journal.argparse.ArgumentParser')
    @patch('journal.add_entry')
    @patch('journal.get_entries', return_value=["[2024-07-26 12:00:00] - Test entry"])
    def test_main_view_command_with_date(self, mock_get_entries, mock_add_entry, mock_argparse):
        # Mock rationale:
        # - journal.argparse.ArgumentParser: Control command-line arguments for testing.
        # - journal.add_entry: Ensure 'add' is not called.
        # - journal.get_entries: Simulate entries found for a specific date.

        mock_args = MagicMock()
        mock_args.command = "view"
        mock_args.date = "2024-07-26"
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            journal.main()
            mock_get_entries.assert_called_once_with("2024-07-26")
            mock_add_entry.assert_not_called()
            self.assertIn("Test entry", mock_print.call_args_list[1].args[0])

    @patch('journal.argparse.ArgumentParser')
    @patch('journal.add_entry')
    @patch('journal.get_entries', return_value=[])
    def test_main_view_command_with_date_no_match(self, mock_get_entries, mock_add_entry, mock_argparse):
        # Mock rationale:
        # - journal.argparse.ArgumentParser: Control command-line arguments for testing.
        # - journal.add_entry: Ensure 'add' is not called.
        # - journal.get_entries: Simulate no entries found for a specific date.

        mock_args = MagicMock()
        mock_args.command = "view"
        mock_args.date = "2024-07-28"
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            journal.main()
            mock_get_entries.assert_called_once_with("2024-07-28")
            mock_add_entry.assert_not_called()
            mock_print.assert_called_once_with("No entries found for 2024-07-28.")


if __name__ == '__main__':
    unittest.main()
