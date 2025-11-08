import unittest
import json
from unittest.mock import patch, mock_open
import os
import sys

# Mock rationale: The ResourceTracker class itself is pure logic and doesn't have external dependencies.
# The CLI part (main function) interacts with the file system to save/load state and prints to stdout.
# For testing the CLI, we need to mock file operations (os.path.exists, builtins.open) to ensure
# determinism and offline execution, and mock sys.argv to control command-line arguments.
# We also mock builtins.print to capture and verify console output.

from src.tracker import ResourceTracker, main

class TestResourceTracker(unittest.TestCase):

    def test_initialization(self):
        tracker = ResourceTracker()
        self.assertEqual(tracker.resources, {})

        initial = {'food': 100, 'water': 50.0}
        tracker = ResourceTracker(initial)
        self.assertEqual(tracker.resources, {'food': 100.0, 'water': 50.0})

    def test_add_resource(self):
        tracker = ResourceTracker({'food': 100.0})
        self.assertTrue(tracker.add_resource('food', 20.0))
        self.assertEqual(tracker.get_resource_level('food'), 120.0)
        self.assertTrue(tracker.add_resource('ammo', 10))
        self.assertEqual(tracker.get_resource_level('ammo'), 10.0)

    def test_add_resource_invalid_quantity(self):
        tracker = ResourceTracker()
        with self.assertRaises(ValueError):
            tracker.add_resource('food', -10.0)
        with self.assertRaises(ValueError):
            tracker.add_resource('food', 'abc')

    def test_consume_resource_success(self):
        tracker = ResourceTracker({'food': 100.0, 'water': 50.0})
        self.assertTrue(tracker.consume_resource('food', 30.0))
        self.assertEqual(tracker.get_resource_level('food'), 70.0)
        self.assertTrue(tracker.consume_resource('water', 50))
        self.assertEqual(tracker.get_resource_level('water'), 0.0)

    def test_consume_resource_not_enough(self):
        tracker = ResourceTracker({'food': 10.0})
        self.assertFalse(tracker.consume_resource('food', 20.0))
        self.assertEqual(tracker.get_resource_level('food'), 10.0) # Should remain unchanged
        self.assertFalse(tracker.consume_resource('nonexistent', 5.0))

    def test_consume_resource_invalid_quantity(self):
        tracker = ResourceTracker({'food': 100.0})
        with self.assertRaises(ValueError):
            tracker.consume_resource('food', -10.0)
        with self.assertRaises(ValueError):
            tracker.consume_resource('food', 'xyz')

    def test_get_resource_level(self):
        tracker = ResourceTracker({'food': 100.0, 'water': 0.0})
        self.assertEqual(tracker.get_resource_level('food'), 100.0)
        self.assertEqual(tracker.get_resource_level('water'), 0.0)
        self.assertEqual(tracker.get_resource_level('ammo'), 0.0) # Non-existent resource

    def test_estimate_survival_days(self):
        tracker = ResourceTracker({'food': 100.0, 'water': 50.0, 'ammo': 20.0})
        daily_consumption = {'food': 10.0, 'water': 5.0, 'ammo': 2.0, 'energy': 1.0}
        estimates = tracker.estimate_survival_days(daily_consumption)
        self.assertAlmostEqual(estimates['food'], 10.0)
        self.assertAlmostEqual(estimates['water'], 10.0)
        self.assertAlmostEqual(estimates['ammo'], 10.0)
        self.assertAlmostEqual(estimates['energy'], 0.0) # No energy resource, so 0 days

    def test_estimate_survival_days_zero_consumption(self):
        tracker = ResourceTracker({'food': 100.0})
        daily_consumption = {'food': 0.0, 'water': 5.0}
        estimates = tracker.estimate_survival_days(daily_consumption)
        self.assertEqual(estimates['food'], float('inf'))
        self.assertAlmostEqual(estimates['water'], 0.0) # Water not present, so 0 days

    def test_estimate_survival_days_invalid_consumption(self):
        tracker = ResourceTracker({'food': 100.0})
        with self.assertRaises(ValueError):
            tracker.estimate_survival_days({'food': -10.0})
        with self.assertRaises(ValueError):
            tracker.estimate_survival_days({'food': 'abc'})

    def test_to_json_from_json(self):
        initial = {'food': 100.5, 'water': 50.0}
        tracker = ResourceTracker(initial)
        json_string = tracker.to_json()
        loaded_tracker = ResourceTracker.from_json(json_string)
        self.assertEqual(loaded_tracker.resources, initial)

class TestTrackerCLI(unittest.TestCase):

    def setUp(self):
        self.state_file = 'test_tracker_state.json'
        # Ensure no state file exists before each test
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        self.original_argv = sys.argv
        self.original_exit = sys.exit
        sys.exit = self._mock_exit # Mock sys.exit to prevent actual exit during tests
        self.exit_called_with = None

    def tearDown(self):
        # Clean up state file after each test
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        sys.argv = self.original_argv
        sys.exit = self.original_exit

    def _mock_exit(self, code):
        self.exit_called_with = code
        raise SystemExit(code) # Raise to break out of main, but allow test to catch

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'init', 'food=100', 'water=50'])
    def test_cli_init(self, mock_exists, mock_open_file):
        # Mock rationale: We mock os.path.exists to simulate no existing state file
        # and builtins.open to capture the written state without actual file I/O.
        main()
        mock_open_file.assert_called_once_with(self.state_file, 'w')
        written_content = mock_open_file().write.call_args[0][0]
        self.assertEqual(json.loads(written_content), {'food': 100.0, 'water': 50.0})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'food': 100.0}))
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'add', 'food=20', 'ammo=10'])
    def test_cli_add(self, mock_exists, mock_open_file):
        # Mock rationale: We mock os.path.exists to simulate an existing state file
        # and builtins.open to provide initial state and capture the updated state.
        main()
        # The first call to open is for reading, the second for writing
        mock_open_file.assert_any_call(self.state_file, 'r')
        mock_open_file.assert_any_call(self.state_file, 'w')
        written_content = mock_open_file().write.call_args[0][0]
        self.assertEqual(json.loads(written_content), {'food': 120.0, 'ammo': 10.0})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'food': 100.0, 'water': 50.0}))
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'consume', 'food=30', 'water=10'])
    def test_cli_consume(self, mock_exists, mock_open_file):
        # Mock rationale: Similar to add, mock file operations for state management.
        main()
        mock_open_file.assert_any_call(self.state_file, 'r')
        mock_open_file.assert_any_call(self.state_file, 'w')
        written_content = mock_open_file().write.call_args[0][0]
        self.assertEqual(json.loads(written_content), {'food': 70.0, 'water': 40.0})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'food': 10.0}))
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'consume', 'food=20'])
    @patch('builtins.print') # Mock print to capture output
    def test_cli_consume_not_enough(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Mock file operations and print to verify warning message.
        main()
        mock_print.assert_any_call('Warning: Not enough food to consume 20.00. Current: 10.00')
        # State should not be changed if consumption failed, so the written content should be the original.
        mock_open_file.assert_any_call(self.state_file, 'r')
        written_content = mock_open_file().write.call_args[0][0]
        self.assertEqual(json.loads(written_content), {'food': 10.0})

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'food': 100.0, 'water': 50.0}))
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'levels'])
    @patch('builtins.print')
    def test_cli_levels(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Mock file read and print to verify output without modifying state.
        main()
        mock_print.assert_any_call('Current Resource Levels:')
        mock_print.assert_any_call('  food: 100.00')
        mock_print.assert_any_call('  water: 50.00')
        # Ensure state is not saved for 'levels' command
        self.assertNotIn('w', [call.args[1] for call in mock_open_file.call_args_list])

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'food': 100.0, 'water': 50.0}))
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'estimate', 'food=10', 'water=5'])
    @patch('builtins.print')
    def test_cli_estimate(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Mock file read and print to verify output without modifying state.
        main()
        mock_print.assert_any_call('Survival Estimates (Days Remaining):')
        mock_print.assert_any_call('  food: 10.00 days')
        mock_print.assert_any_call('  water: 10.00 days')
        # Ensure state is not saved for 'estimate' command
        self.assertNotIn('w', [call.args[1] for call in mock_open_file.call_args_list])

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'levels'])
    @patch('builtins.print')
    def test_cli_load_invalid_json(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Simulate a corrupted state file and verify graceful handling.
        main()
        mock_print.assert_any_call('Warning: Could not load state from test_tracker_state.json. File might be corrupted. Starting fresh.')
        mock_print.assert_any_call('No resources tracked yet.')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'add', 'food=invalid'])
    @patch('builtins.print')
    def test_cli_invalid_quantity_arg(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Test argument parsing for invalid quantities.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Invalid quantity for 'food'. Must be a number.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['tracker.py', '--state-file', 'test_tracker_state.json', 'add', 'food:10'])
    @patch('builtins.print')
    def test_cli_invalid_format_arg(self, mock_print, mock_exists, mock_open_file):
        # Mock rationale: Test argument parsing for invalid key=value format.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Invalid format for 'food:10'. Expected key=value.")

if __name__ == '__main__':
    unittest.main()
