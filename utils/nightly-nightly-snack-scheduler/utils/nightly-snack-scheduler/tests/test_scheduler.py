import unittest
from unittest.mock import patch, mock_open
import datetime
import json
import sys
import os

# Adjust sys.path to allow importing scheduler from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scheduler import load_config, check_snacks, main, CONFIG_FILE

class TestSnackScheduler(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_load_config_success(self, mock_exists, mock_file):
        # Mock rationale: Simulate a valid config.json file existing and being readable.
        mock_file.return_value.read.return_value = json.dumps({"snacks": [{"name": "Apple", "time": "10:00"}]})
        config = load_config(CONFIG_FILE)
        self.assertIn('snacks', config)
        self.assertEqual(len(config['snacks']), 1)
        self.assertEqual(config['snacks'][0]['name'], 'Apple')

    @patch('os.path.exists', return_value=False)
    def test_load_config_file_not_found(self, mock_exists):
        # Mock rationale: Simulate the config.json file not existing.
        with self.assertRaises(FileNotFoundError):
            load_config(CONFIG_FILE)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_load_config_invalid_json(self, mock_exists, mock_file):
        # Mock rationale: Simulate a config.json file with invalid JSON content.
        mock_file.return_value.read.return_value = "{invalid json"
        with self.assertRaises(json.JSONDecodeError):
            load_config(CONFIG_FILE)

    def test_check_snacks_no_snacks_due(self):
        # Mock rationale: Simulate a current time where no snacks are scheduled.
        current_time = datetime.datetime(2023, 10, 27, 9, 0) # 9:00 AM
        config = {"snacks": [{"name": "Coffee", "time": "08:00"}, {"name": "Lunch", "time": "12:00"}]}
        reminders = check_snacks(current_time, config)
        self.assertEqual(len(reminders), 0)

    def test_check_snacks_one_snack_due(self):
        # Mock rationale: Simulate a current time where one snack is scheduled.
        current_time = datetime.datetime(2023, 10, 27, 10, 30) # 10:30 AM
        config = {"snacks": [{"name": "Power Bar", "time": "10:30"}, {"name": "Lunch", "time": "12:00"}]}
        reminders = check_snacks(current_time, config)
        self.assertEqual(len(reminders), 1)
        self.assertIn("It's time for your Power Bar!", reminders[0])

    def test_check_snacks_multiple_snacks_due(self):
        # Mock rationale: Simulate a current time where multiple snacks are scheduled for the same minute.
        current_time = datetime.datetime(2023, 10, 27, 11, 0) # 11:00 AM
        config = {
            "snacks": [
                {"name": "Hydration Break", "time": "11:00"},
                {"name": "Emergency Ration", "time": "11:00"},
                {"name": "Lunch", "time": "12:00"}
            ]
        }
        reminders = check_snacks(current_time, config)
        self.assertEqual(len(reminders), 2)
        self.assertIn("Hydration Break", reminders[0])
        self.assertIn("Emergency Ration", reminders[1])

    def test_check_snacks_malformed_entry(self):
        # Mock rationale: Simulate a config with a malformed snack entry (missing 'time').
        current_time = datetime.datetime(2023, 10, 27, 10, 0)
        config = {"snacks": [{"name": "Good Snack", "time": "10:00"}, {"name": "Bad Snack"}]}
        
        # Capture stderr to check for warnings
        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            reminders = check_snacks(current_time, config)
            self.assertEqual(len(reminders), 1)
            self.assertIn("Good Snack", reminders[0])
            self.assertIn("Warning: Malformed snack entry found", mock_stderr.getvalue())

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('scheduler.load_config')
    @patch('datetime.datetime')
    def test_main_snacks_due(self, mock_datetime, mock_load_config, mock_print, mock_exit):
        # Mock rationale: Simulate a scenario where snacks are due, verifying print output and exit code.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0)
        mock_load_config.return_value = {"snacks": [{"name": "Morning Fuel", "time": "10:00"}]}
        
        main()
        mock_print.assert_called_with("It's time for your Morning Fuel! Stay strong, survivor!")
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('scheduler.load_config')
    @patch('datetime.datetime')
    def test_main_no_snacks_due(self, mock_datetime, mock_load_config, mock_print, mock_exit):
        # Mock rationale: Simulate a scenario where no snacks are due, verifying print output and exit code.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 9, 0)
        mock_load_config.return_value = {"snacks": [{"name": "Morning Fuel", "time": "10:00"}]}
        
        main()
        mock_print.assert_called_with("No snacks due at 09:00. Keep vigilant!")
        mock_exit.assert_called_with(2)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('scheduler.load_config', side_effect=FileNotFoundError("Config not found"))
    def test_main_config_not_found(self, mock_load_config, mock_print, mock_exit):
        # Mock rationale: Simulate a FileNotFoundError during config loading, verifying error message and exit code.
        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            main()
            self.assertIn("Error: Config not found", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('scheduler.load_config', side_effect=json.JSONDecodeError("Invalid JSON", doc="{}", pos=1))
    def test_main_invalid_json_config(self, mock_load_config, mock_print, mock_exit):
        # Mock rationale: Simulate a JSONDecodeError during config loading, verifying error message and exit code.
        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            main()
            self.assertIn("Error parsing config file", mock_stderr.getvalue())
            self.assertIn("Invalid JSON", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('scheduler.load_config')
    @patch('scheduler.check_snacks', side_effect=Exception("Unexpected error"))
    def test_main_unexpected_error(self, mock_check_snacks, mock_load_config, mock_print, mock_exit):
        # Mock rationale: Simulate an unexpected error during snack checking, verifying error message and exit code.
        mock_load_config.return_value = {"snacks": []}
        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            main()
            self.assertIn("An unexpected error occurred: Unexpected error", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
