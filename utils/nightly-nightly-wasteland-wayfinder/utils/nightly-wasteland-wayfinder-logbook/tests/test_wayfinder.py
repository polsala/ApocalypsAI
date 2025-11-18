import unittest
import os
import datetime
from unittest.mock import patch, mock_open
import io
import sys

# Mock the current working directory for consistent log file path resolution
# Mock rationale: Ensures that _get_log_path always returns a predictable path
# relative to the script, regardless of where the test is run from.
@patch('os.path.dirname', return_value='/mock/path/src')
@patch('os.path.abspath', return_value='/mock/path/src/wayfinder.py')
class TestWayfinder(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    # Mock rationale: Ensures deterministic timestamps for log entries.
    @patch('datetime.datetime')
    def test_add_entry(self, mock_dt):
        mock_dt.now.return_value = datetime.datetime(2024, 1, 1, 10, 0, 0)
        mock_dt.strftime.return_value = '2024-01-01 10:00:00'

        # Mock rationale: Simulates file writing without touching the actual filesystem.
        # This allows testing the content written to the log file.
        m_open = mock_open()
        with patch('builtins.open', m_open):
            from src.wayfinder import add_entry
            add_entry('POI', 'Old Shack', 'Found rusty tools.')

            m_open.assert_called_once_with('/mock/path/src/wayfinder_log.txt', 'a', encoding='utf-8')
            m_open().write.assert_called_once_with('2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.\n')
            self.assertIn("Entry added: 2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.", self.mock_stdout.getvalue())

    # Mock rationale: Simulates reading from an existing log file.
    # This allows testing the parsing and display of log entries without actual file I/O.
    @patch('builtins.open', new_callable=mock_open, read_data='2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.\n2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.\n')
    @patch('os.path.exists', return_value=True)
    def test_get_entries(self, mock_exists, mock_file):
        from src.wayfinder import get_entries
        entries = get_entries()
        self.assertEqual(len(entries), 2)
        self.assertIn('2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.', entries)
        self.assertIn('2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.', entries)

    # Mock rationale: Simulates an empty log file scenario.
    @patch('os.path.exists', return_value=False)
    def test_get_entries_empty(self, mock_exists):
        from src.wayfinder import get_entries
        entries = get_entries()
        self.assertEqual(len(entries), 0)

    # Mock rationale: Simulates reading from a log file and capturing printed output.
    @patch('builtins.open', new_callable=mock_open, read_data='2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.\n2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.\n')
    @patch('os.path.exists', return_value=True)
    def test_list_entries(self, mock_exists, mock_file):
        from src.wayfinder import list_entries
        list_entries()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Wasteland Wayfinder Logbook ---", output)
        self.assertIn("2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.", output)
        self.assertIn("2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.", output)

    # Mock rationale: Simulates an empty log file for the list command.
    @patch('os.path.exists', return_value=False)
    def test_list_entries_empty(self, mock_exists):
        from src.wayfinder import list_entries
        list_entries()
        output = self.mock_stdout.getvalue()
        self.assertIn("No entries found in the logbook.", output)

    # Mock rationale: Simulates reading from a log file and capturing printed output for search.
    @patch('builtins.open', new_callable=mock_open, read_data='2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.\n2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.\n2024-01-02 12:00:00 | HAZARD | River Crossing | Bridge collapsed, dangerous currents.\n')
    @patch('os.path.exists', return_value=True)
    def test_search_entries(self, mock_exists, mock_file):
        from src.wayfinder import search_entries
        search_entries('tools')
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Search Results for 'tools' ---", output)
        self.assertIn("2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.", output)
        self.assertNotIn("Forest Path", output)

        # Reset stdout for next search within the same test method
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

        search_entries('path')
        output = self.mock_stdout.getvalue()
        self.assertIn("2024-01-01 11:00:00 | ROUTE | Forest Path | Clear path.", output)
        self.assertNotIn("Old Shack", output)

    # Mock rationale: Simulates searching an empty log file.
    @patch('os.path.exists', return_value=False)
    def test_search_entries_empty_log(self, mock_exists):
        from src.wayfinder import search_entries
        search_entries('anything')
        output = self.mock_stdout.getvalue()
        self.assertIn("No entries found to search.", output)

    # Mock rationale: Simulates searching a log file with no matches.
    @patch('builtins.open', new_callable=mock_open, read_data='2024-01-01 10:00:00 | POI | Old Shack | Found rusty tools.\n')
    @patch('os.path.exists', return_value=True)
    def test_search_entries_no_match(self, mock_exists, mock_file):
        from src.wayfinder import search_entries
        search_entries('nonexistent')
        output = self.mock_stdout.getvalue()
        self.assertIn("No entries found matching 'nonexistent'.", output)

    # Mock rationale: Simulates command-line argument parsing and execution flow.
    # This allows testing the main CLI logic without actually invoking the script via subprocess.
    @patch('sys.argv', ['wayfinder.py', 'add', '--type', 'NOTE', '--location', 'Test Loc', '--description', 'Test Desc'])
    @patch('src.wayfinder.add_entry')
    def test_main_add_command(self, mock_add_entry):
        from src.wayfinder import main
        main()
        mock_add_entry.assert_called_once_with('NOTE', 'Test Loc', 'Test Desc')

    @patch('sys.argv', ['wayfinder.py', 'list'])
    @patch('src.wayfinder.list_entries')
    def test_main_list_command(self, mock_list_entries):
        from src.wayfinder import main
        main()
        mock_list_entries.assert_called_once()

    @patch('sys.argv', ['wayfinder.py', 'search', '--query', 'test_query'])
    @patch('src.wayfinder.search_entries')
    def test_main_search_command(self, mock_search_entries):
        from src.wayfinder import main
        main()
        mock_search_entries.assert_called_once_with('test_query')

    @patch('sys.argv', ['wayfinder.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        from src.wayfinder import main
        main()
        mock_print_help.assert_called_once()
