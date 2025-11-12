import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Add the src directory to the Python path to allow importing validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from validator import validate_config, main

class TestDoomsdayConfigValidator(unittest.TestCase):

    def test_valid_config(self):
        config = {
            'activation_code': 'ALPHA-OMEGA-1',
            'target_coordinates': [40.7128, -74.0060],
            'power_source': 'fusion',
            'countdown_timer_seconds': 120,
            'safety_override': False,
            'self_destruct_on_failure': True,
            'message_on_activation': 'Greetings, Earthlings!'
        }
        errors = validate_config(config)
        self.assertEqual(len(errors), 0, f"Expected no errors, but got: {errors}")

    def test_missing_activation_code(self):
        config = {
            'target_coordinates': [40.7128, -74.0060],
            'power_source': 'dark_matter',
            'countdown_timer_seconds': 300
        }
        errors = validate_config(config)
        self.assertIn("Missing critical parameter: 'activation_code'.", errors)

    def test_invalid_activation_code_type(self):
        config = {
            'activation_code': 12345,
            'target_coordinates': [40.7128, -74.0060],
            'power_source': 'dark_matter',
            'countdown_timer_seconds': 300
        }
        errors = validate_config(config)
        self.assertIn("'activation_code' must be a string.", errors)

    def test_missing_target_coordinates(self):
        config = {
            'activation_code': 'CODE-RED',
            'power_source': 'solar',
            'countdown_timer_seconds': 600
        }
        errors = validate_config(config)
        self.assertIn("Missing critical parameter: 'target_coordinates'.", errors)

    def test_invalid_target_coordinates_format(self):
        config = {
            'activation_code': 'CODE-RED',
            'target_coordinates': [40.7128],
            'power_source': 'solar',
            'countdown_timer_seconds': 600
        }
        errors = validate_config(config)
        self.assertIn("'target_coordinates' must be a list of two numbers (latitude, longitude).", errors)

        config_str = {
            'activation_code': 'CODE-RED',
            'target_coordinates': ['40.7128', '-74.0060'],
            'power_source': 'solar',
            'countdown_timer_seconds': 600
        }
        errors_str = validate_config(config_str)
        self.assertIn("'target_coordinates' must be a list of two numbers (latitude, longitude).", errors_str)

    def test_invalid_power_source(self):
        config = {
            'activation_code': 'CODE-GREEN',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'unobtainium',
            'countdown_timer_seconds': 900
        }
        errors = validate_config(config)
        self.assertIn("Invalid 'power_source': 'unobtainium'. Must be one of 'solar', 'fusion', 'dark_matter', 'antimatter'.", errors)

    def test_missing_countdown_timer(self):
        config = {
            'activation_code': 'CODE-YELLOW',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'fusion'
        }
        errors = validate_config(config)
        self.assertIn("Missing critical parameter: 'countdown_timer_seconds'.", errors)

    def test_invalid_countdown_timer_value(self):
        config_zero = {
            'activation_code': 'CODE-YELLOW',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'fusion',
            'countdown_timer_seconds': 0
        }
        errors_zero = validate_config(config_zero)
        self.assertIn("'countdown_timer_seconds' must be a positive integer.", errors_zero)

        config_negative = {
            'activation_code': 'CODE-YELLOW',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'fusion',
            'countdown_timer_seconds': -10
        }
        errors_negative = validate_config(config_negative)
        self.assertIn("'countdown_timer_seconds' must be a positive integer.", errors_negative)

        config_float = {
            'activation_code': 'CODE-YELLOW',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'fusion',
            'countdown_timer_seconds': 10.5
        }
        errors_float = validate_config(config_float)
        self.assertIn("'countdown_timer_seconds' must be a positive integer.", errors_float)

    def test_conflicting_safety_and_self_destruct(self):
        config = {
            'activation_code': 'CODE-BLUE',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'antimatter',
            'countdown_timer_seconds': 100,
            'safety_override': True,
            'self_destruct_on_failure': True
        }
        errors = validate_config(config)
        self.assertIn("Conflicting settings: 'safety_override' and 'self_destruct_on_failure' cannot both be true. Choose your fate!", errors)

    def test_invalid_safety_override_type(self):
        config = {
            'activation_code': 'CODE-BLUE',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'antimatter',
            'countdown_timer_seconds': 100,
            'safety_override': "yes"
        }
        errors = validate_config(config)
        self.assertIn("'safety_override' must be a boolean.", errors)

    def test_invalid_self_destruct_type(self):
        config = {
            'activation_code': 'CODE-BLUE',
            'target_coordinates': [1.0, 2.0],
            'power_source': 'antimatter',
            'countdown_timer_seconds': 100,
            'self_destruct_on_failure': "no"
        }
        errors = validate_config(config)
        self.assertIn("'self_destruct_on_failure' must be a boolean.", errors)

    def test_empty_config(self):
        config = {}
        errors = validate_config(config)
        self.assertGreater(len(errors), 0)
        self.assertIn("Missing critical parameter: 'activation_code'.", errors)
        self.assertIn("Missing critical parameter: 'target_coordinates'.", errors)
        self.assertIn("Missing critical parameter: 'power_source'.", errors)
        self.assertIn("Missing critical parameter: 'countdown_timer_seconds'.", errors)

    @patch('builtins.open', new_callable=mock_open, read_data='activation_code: "TEST"\n') # Mock rationale: Avoid actual file system interaction for deterministic tests.
    @patch('sys.argv', ['validator.py', 'config.yaml']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output for assertions instead of printing to console.
    def test_main_valid_yaml(self, mock_print, mock_exit, mock_argv, mock_file_open):
        # Mock rationale: Ensure yaml.safe_load is called correctly.
        with patch('yaml.safe_load', return_value={'activation_code': 'TEST', 'target_coordinates': [1.0, 2.0], 'power_source': 'fusion', 'countdown_timer_seconds': 100}):
            main()
            mock_exit.assert_called_once_with(0)
            mock_print.assert_any_call("\nDoomsday Configuration for 'config.yaml' is VALID! Proceed with caution... or don't.")

    @patch('builtins.open', new_callable=mock_open, read_data='{\"activation_code\": \"TEST\"}') # Mock rationale: Avoid actual file system interaction for deterministic tests.
    @patch('sys.argv', ['validator.py', 'config.json']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output for assertions instead of printing to console.
    def test_main_valid_json(self, mock_print, mock_exit, mock_argv, mock_file_open):
        # Mock rationale: Ensure json.load is called correctly.
        with patch('json.load', return_value={'activation_code': 'TEST', 'target_coordinates': [1.0, 2.0], 'power_source': 'fusion', 'countdown_timer_seconds': 100}):
            main()
            mock_exit.assert_called_once_with(0)
            mock_print.assert_any_call("\nDoomsday Configuration for 'config.json' is VALID! Proceed with caution... or don't.")

    @patch('builtins.open', new_callable=mock_open, read_data='activation_code: 123\n') # Mock rationale: Avoid actual file system interaction for deterministic tests.
    @patch('sys.argv', ['validator.py', 'config.yaml']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output for assertions instead of printing to console.
    def test_main_invalid_config(self, mock_print, mock_exit, mock_argv, mock_file_open):
        # Mock rationale: Simulate an invalid config being loaded.
        invalid_config = {
            'activation_code': 123, # Invalid type
            'target_coordinates': [1.0],
            'power_source': 'bad_source',
            'countdown_timer_seconds': -5
        }
        with patch('yaml.safe_load', return_value=invalid_config):
            main()
            mock_exit.assert_called_once_with(1)
            mock_print.assert_any_call("\nDoomsday Configuration for 'config.yaml' is INVALID! Detected the following anomalies:")
            mock_print.assert_any_call("- 'activation_code' must be a string.")
            mock_print.assert_any_call("- 'target_coordinates' must be a list of two numbers (latitude, longitude).")
            mock_print.assert_any_call("- Invalid 'power_source': 'bad_source'. Must be one of 'solar', 'fusion', 'dark_matter', 'antimatter'.")
            mock_print.assert_any_call("- 'countdown_timer_seconds' must be a positive integer.")

    @patch('builtins.open', side_effect=FileNotFoundError) # Mock rationale: Simulate a file not found error.
    @patch('sys.argv', ['validator.py', 'non_existent.yaml']) # Mock rationale: Simulate command-line arguments.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_main_file_not_found(self, mock_print, mock_exit, mock_argv, mock_file_open):
        main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Error: Configuration file not found at 'non_existent.yaml'.")

    @patch('builtins.open', new_callable=mock_open, read_data='invalid yaml content: -') # Mock rationale: Simulate malformed YAML.
    @patch('sys.argv', ['validator.py', 'malformed.yaml']) # Mock rationale: Simulate command-line arguments.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_main_yaml_parse_error(self, mock_print, mock_exit, mock_argv, mock_file_open):
        main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call(unittest.mock.ANY) # Check for error message, content might vary by yaml version
        self.assertTrue(any("Error parsing configuration file" in call_arg[0][0] for call_arg in mock_print.call_args_list))

    @patch('builtins.open', new_callable=mock_open, read_data='not a dict') # Mock rationale: Simulate a config that's not a dictionary.
    @patch('sys.argv', ['validator.py', 'not_a_dict.yaml']) # Mock rationale: Simulate command-line arguments.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_main_config_not_dict(self, mock_print, mock_exit, mock_argv, mock_file_open):
        with patch('yaml.safe_load', return_value='not a dict'): # Mock rationale: Simulate yaml.safe_load returning a non-dict.
            main()
            mock_exit.assert_called_once_with(1)
            mock_print.assert_any_call("Error: Configuration file must contain a dictionary/object at its root.")

    @patch('sys.argv', ['validator.py']) # Mock rationale: Simulate missing argument.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_main_no_args(self, mock_print, mock_exit, mock_argv):
        main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Usage: python src/validator.py <config_file.yaml|json>")

    @patch('builtins.open', new_callable=mock_open, read_data='content') # Mock rationale: Avoid actual file system interaction.
    @patch('sys.argv', ['validator.py', 'unsupported.txt']) # Mock rationale: Simulate unsupported file type.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_main_unsupported_file_type(self, mock_print, mock_exit, mock_argv, mock_file_open):
        main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Error: Unsupported file type for unsupported.txt. Must be .yaml, .yml, or .json.")


if __name__ == '__main__':
    unittest.main()
