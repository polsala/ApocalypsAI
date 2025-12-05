import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing reminder.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import reminder

class TestSnackpocalypseReminder(unittest.TestCase):

    def setUp(self):
        # Ensure we start with a clean slate for each test
        self.mock_config_data = {
            'interval_minutes': 1,
            'reminder_message': 'Test Snack Time!'
        }
        self.mock_state_data = {'last_reminded_timestamp': 0}

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('time.time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_first_run_triggers_reminder(self, mock_stdout, mock_time, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate no config or state files existing initially.
        # The paths are constructed in reminder.py, so we need to mock based on those.
        mock_exists.side_effect = lambda x: x not in [reminder.CONFIG_FILE, reminder.STATE_FILE]
        mock_time.return_value = 1000.0 # Current time

        # Mock rationale: get_config will use default, get_state will use default.
        # No need to mock json.load for config/state as exists() returns False.

        reminder.main()

        # Assert reminder message is printed (default message as no config file)
        self.assertIn('🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕', mock_stdout.getvalue())

        # Assert state is saved with current time
        mock_json_dump.assert_called_once()
        saved_state = mock_json_dump.call_args[0][0]
        self.assertAlmostEqual(saved_state['last_reminded_timestamp'], 1000.0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('time.time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_reminder_triggered_after_interval(self, mock_stdout, mock_time, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate config and state files existing, and enough time has passed.
        mock_exists.side_effect = lambda x: x in [reminder.CONFIG_FILE, reminder.STATE_FILE]

        # Mock rationale: Provide specific config and state data.
        mock_json_load.side_effect = [
            self.mock_config_data, # For get_config
            {'last_reminded_timestamp': 0} # For get_state, last reminded 0 seconds ago
        ]
        mock_time.return_value = 61.0 # Current time is 61 seconds (1 min + 1 sec) after last reminder

        reminder.main()

        # Assert custom reminder message is printed
        self.assertIn('Test Snack Time!', mock_stdout.getvalue())

        # Assert state is saved with current time
        mock_json_dump.assert_called_once()
        saved_state = mock_json_dump.call_args[0][0]
        self.assertAlmostEqual(saved_state['last_reminded_timestamp'], 61.0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('time.time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_no_reminder_before_interval(self, mock_stdout, mock_time, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate config and state files existing, but not enough time has passed.
        mock_exists.side_effect = lambda x: x in [reminder.CONFIG_FILE, reminder.STATE_FILE]

        # Mock rationale: Provide specific config and state data.
        mock_json_load.side_effect = [
            self.mock_config_data, # For get_config
            {'last_reminded_timestamp': 50.0} # For get_state, last reminded 50 seconds ago
        ]
        mock_time.return_value = 100.0 # Current time is 100 seconds. Interval is 60s. 100-50=50s passed. Not enough.

        reminder.main()

        # Assert no reminder message, but next reminder time is printed
        self.assertIn('Next snack-pocalypse reminder in 0m 10s.', mock_stdout.getvalue())

        # Assert state is NOT saved
        mock_json_dump.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('time.time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_config_uses_defaults(self, mock_stdout, mock_time, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an invalid config file. Only config.json exists.
        mock_exists.side_effect = lambda x: x == reminder.CONFIG_FILE

        # Mock rationale: Simulate JSONDecodeError for config. State file does not exist, so get_state returns default.
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        mock_time.return_value = 1000.0

        reminder.main()

        # Assert warning is printed and default reminder is triggered
        self.assertIn('Warning: Could not parse config.json. Using default configuration.', mock_stdout.getvalue())
        self.assertIn('🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕', mock_stdout.getvalue())
        mock_json_dump.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('time.time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_state_starts_fresh(self, mock_stdout, mock_time, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an invalid state file. Only state.json exists.
        mock_exists.side_effect = lambda x: x == reminder.STATE_FILE

        # Mock rationale: Simulate JSONDecodeError for state. Config file does not exist, so get_config returns default.
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        mock_time.return_value = 1000.0

        reminder.main()

        # Assert warning is printed and default reminder is triggered (as state starts fresh)
        self.assertIn('Warning: Could not parse state.json. Starting fresh.', mock_stdout.getvalue())
        self.assertIn('🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕', mock_stdout.getvalue())
        mock_json_dump.assert_called_once()
