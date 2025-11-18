import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime

# Mock rationale: We need to ensure that file I/O operations are deterministic and do not affect the actual filesystem.
# `mock_open` allows us to simulate reading from and writing to a file in memory.
# `patch('os.path.exists')` allows us to control whether the simulated data file appears to exist.
# `patch('datetime.now')` ensures that timestamps are consistent across test runs, preventing flaky tests due to time variations.

# Define a consistent mock timestamp
MOCK_TIMESTAMP_STR = "2023-10-27T10:00:00.000000"
MOCK_DATETIME = datetime.fromisoformat(MOCK_TIMESTAMP_STR)

class TestMoraleMonitor(unittest.TestCase):

    def setUp(self):
        # Reset the mock file content before each test
        self.mock_file_content = []

    def _mock_load_data(self):
        return self.mock_file_content

    def _mock_save_data(self, data):
        self.mock_file_content = data

    @patch('morale_monitor._save_data')
    @patch('morale_monitor._load_data')
    @patch('datetime.datetime')
    def test_add_entry_new_data(self, mock_dt, mock_load, mock_save):
        mock_dt.now.return_value = MOCK_DATETIME
        mock_load.return_value = []
        
        import morale_monitor
        morale_monitor.add_entry(4, "Feeling good after a system patch.")

        expected_entry = {
            'timestamp': MOCK_TIMESTAMP_STR,
            'mood': 4,
            'note': "Feeling good after a system patch."
        }
        mock_save.assert_called_once_with([expected_entry])
        self.assertEqual(mock_load.call_count, 1)

    @patch('morale_monitor._save_data')
    @patch('morale_monitor._load_data')
    @patch('datetime.datetime')
    def test_add_entry_existing_data(self, mock_dt, mock_load, mock_save):
        mock_dt.now.return_value = MOCK_DATETIME
        initial_data = [
            {'timestamp': '2023-10-26T09:00:00.000000', 'mood': 3, 'note': 'Initial entry'}
        ]
        mock_load.return_value = initial_data

        import morale_monitor
        morale_monitor.add_entry(5, "Exhilarated by new energy source.")

        expected_entry = {
            'timestamp': MOCK_TIMESTAMP_STR,
            'mood': 5,
            'note': "Exhilarated by new energy source."
        }
        mock_save.assert_called_once_with(initial_data + [expected_entry])
        self.assertEqual(mock_load.call_count, 1)

    @patch('morale_monitor._save_data')
    @patch('morale_monitor._load_data')
    @patch('datetime.datetime')
    def test_add_entry_invalid_mood(self, mock_dt, mock_load, mock_save):
        mock_dt.now.return_value = MOCK_DATETIME
        mock_load.return_value = []

        import morale_monitor
        with patch('builtins.print') as mock_print:
            morale_monitor.add_entry(6, "Too happy.")
            mock_print.assert_called_with("Error: Mood must be an integer between 1 and 5.")
            mock_save.assert_not_called()

    @patch('morale_monitor._load_data')
    @patch('builtins.print')
    def test_view_entries_empty(self, mock_print, mock_load):
        mock_load.return_value = []

        import morale_monitor
        morale_monitor.view_entries()

        mock_print.assert_called_with("No morale entries found. Start by adding one!")

    @patch('morale_monitor._load_data')
    @patch('builtins.print')
    def test_view_entries_with_data(self, mock_print, mock_load):
        mock_load.return_value = [
            {'timestamp': '2023-10-26T09:00:00.000000', 'mood': 3, 'note': 'Initial entry'},
            {'timestamp': '2023-10-27T10:00:00.000000', 'mood': 5, 'note': 'Another entry'}
        ]

        import morale_monitor
        morale_monitor.view_entries()

        mock_print.assert_any_call("\n--- Morale History ---")
        mock_print.assert_any_call("[2023-10-26 09:00:00] Mood: ⭐⭐⭐ (3/5)")
        mock_print.assert_any_call("  Note: Initial entry")
        mock_print.assert_any_call("[2023-10-27 10:00:00] Mood: ⭐⭐⭐⭐⭐ (5/5)")
        mock_print.assert_any_call("  Note: Another entry")
        mock_print.assert_any_call("----------------------\n")

    @patch('morale_monitor._load_data')
    @patch('builtins.print')
    def test_get_summary_empty(self, mock_print, mock_load):
        mock_load.return_value = []

        import morale_monitor
        morale_monitor.get_summary()

        mock_print.assert_called_with("No morale entries to summarize.")

    @patch('morale_monitor._load_data')
    @patch('builtins.print')
    def test_get_summary_with_data(self, mock_print, mock_load):
        mock_load.return_value = [
            {'timestamp': '2023-10-26T09:00:00.000000', 'mood': 3, 'note': 'Entry 1'},
            {'timestamp': '2023-10-26T10:00:00.000000', 'mood': 4, 'note': 'Entry 2'},
            {'timestamp': '2023-10-27T11:00:00.000000', 'mood': 4, 'note': 'Entry 3'},
            {'timestamp': '2023-10-27T12:00:00.000000', 'mood': 5, 'note': 'Entry 4'}
        ]

        import morale_monitor
        morale_monitor.get_summary()

        mock_print.assert_any_call("\n--- Morale Summary ---")
        mock_print.assert_any_call("Total Entries: 4")
        mock_print.assert_any_call("Average Mood: 4.00/5")
        mock_print.assert_any_call("Mood Distribution:")
        mock_print.assert_any_call("  3/5 (⭐⭐⭐): 1 entries")
        mock_print.assert_any_call("  4/5 (⭐⭐⭐⭐): 2 entries")
        mock_print.assert_any_call("  5/5 (⭐⭐⭐⭐⭐): 1 entries")
        mock_print.assert_any_call("----------------------\n")

    # Test CLI commands using patch for argparse and main function
    @patch('morale_monitor.add_entry')
    @patch('argparse.ArgumentParser')
    def test_cli_add_command(self, MockArgumentParser, mock_add_entry):
        mock_args = MockArgumentParser.return_value.parse_args.return_value
        mock_args.command = 'add'
        mock_args.mood = 4
        mock_args.note = "CLI test note"

        import morale_monitor
        morale_monitor.main()

        mock_add_entry.assert_called_once_with(4, "CLI test note")

    @patch('morale_monitor.view_entries')
    @patch('argparse.ArgumentParser')
    def test_cli_view_command(self, MockArgumentParser, mock_view_entries):
        mock_args = MockArgumentParser.return_value.parse_args.return_value
        mock_args.command = 'view'

        import morale_monitor
        morale_monitor.main()

        mock_view_entries.assert_called_once()

    @patch('morale_monitor.get_summary')
    @patch('argparse.ArgumentParser')
    def test_cli_summary_command(self, MockArgumentParser, mock_get_summary):
        mock_args = MockArgumentParser.return_value.parse_args.return_value
        mock_args.command = 'summary'

        import morale_monitor
        morale_monitor.main()

        mock_get_summary.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_data_file_not_exists(self, mock_json_load, mock_file_open, mock_exists):
        mock_exists.return_value = False
        
        import morale_monitor
        data = morale_monitor._load_data()
        
        self.assertEqual(data, [])
        mock_file_open.assert_not_called()
        mock_json_load.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_data_empty_json(self, mock_json_load, mock_file_open, mock_exists):
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        
        import morale_monitor
        data = morale_monitor._load_data()
        
        self.assertEqual(data, [])
        mock_file_open.assert_called_once_with(morale_monitor.DATA_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_data(self, mock_json_dump, mock_file_open):
        test_data = [{'mood': 3}]
        
        import morale_monitor
        morale_monitor._save_data(test_data)
        
        mock_file_open.assert_called_once_with(morale_monitor.DATA_FILE, 'w')
        mock_json_dump.assert_called_once_with(test_data, mock_file_open(), indent=2)

if __name__ == '__main__':
    unittest.main()
