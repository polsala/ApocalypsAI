import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Add the src directory to the Python path to allow importing validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import validator

class TestDoomsdayConfigValidator(unittest.TestCase):

    def test_valid_config_global_annihilation(self):
        # Mock rationale: We need to simulate reading a YAML file without actually creating one on disk.
        # `mock_open` allows us to provide a string as the file content.
        mock_yaml_content = """
device_name: "World-Ender 9000"
activation_code: "ZETA-GAMMA-3"
target_mode: "global_annihilation"
payload_yield: 5000
safety_protocols_active: false
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stdout') as mock_stdout:
                        validator.main()
                        mock_exit.assert_called_once_with(0)
                        mock_stdout.write.assert_any_call("Configuration is VALID.\n")

    def test_valid_config_peaceful_coexistence(self):
        # Mock rationale: Simulate reading a valid peaceful config.
        mock_yaml_content = """
device_name: "Harmony Spreader"
activation_code: "PEACE-LOVE-9"
target_mode: "peaceful_coexistence"
safety_protocols_active: true
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stdout') as mock_stdout:
                        validator.main()
                        mock_exit.assert_called_once_with(0)
                        mock_stdout.write.assert_any_call("Configuration is VALID.\n")

    def test_valid_config_with_self_destruct(self):
        # Mock rationale: Simulate reading a valid config including self-destruct sequence.
        mock_yaml_content = """
device_name: "Temporal Discombobulator"
activation_code: "TIMEZ-WARPZ-5"
target_mode: "localized_disruption"
payload_yield: 100
safety_protocols_active: true
self_destruct_sequence:
  enabled: true
  countdown_hours: 72
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stdout') as mock_stdout:
                        validator.main()
                        mock_exit.assert_called_once_with(0)
                        mock_stdout.write.assert_any_call("Configuration is VALID.\n")

    def test_invalid_config_missing_device_name(self):
        # Mock rationale: Simulate reading a config with a missing required field.
        mock_yaml_content = """
activation_code: "ZETA-GAMMA-3"
target_mode: "global_annihilation"
payload_yield: 5000
safety_protocols_active: false
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Configuration is INVALID:\n")
                        mock_stderr.write.assert_any_call("- Missing required field: 'device_name'.\n")

    def test_invalid_config_bad_activation_code(self):
        # Mock rationale: Simulate reading a config with an invalid activation code format.
        mock_yaml_content = """
device_name: "World-Ender 9000"
activation_code: "BADCODE"
target_mode: "global_annihilation"
payload_yield: 5000
safety_protocols_active: false
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Configuration is INVALID:\n")
                        mock_stderr.write.assert_any_call("- 'activation_code' must be a string matching pattern 'AAAAA-BBBBB-C'.\n")

    def test_invalid_config_payload_yield_peaceful_mode(self):
        # Mock rationale: Simulate reading a config where payload_yield is present for peaceful mode.
        mock_yaml_content = """
device_name: "The Pacifier"
activation_code: "PEACE-LOVE-9"
target_mode: "peaceful_coexistence"
payload_yield: 100 # Not allowed for peaceful mode
safety_protocols_active: true
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Configuration is INVALID:\n")
                        mock_stderr.write.assert_any_call("- 'payload_yield' is not allowed for 'peaceful_coexistence' mode.\n")

    def test_invalid_config_missing_payload_yield_destructive_mode(self):
        # Mock rationale: Simulate reading a config where payload_yield is missing for a destructive mode.
        mock_yaml_content = """
device_name: "Local Disruptor"
activation_code: "DISRU-PTOR-1"
target_mode: "localized_disruption"
safety_protocols_active: true
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Configuration is INVALID:\n")
                        mock_stderr.write.assert_any_call("- 'payload_yield' is required for 'localized_disruption' mode.\n")

    def test_invalid_config_self_destruct_enabled_missing_countdown(self):
        # Mock rationale: Simulate reading a config where self-destruct is enabled but countdown is missing.
        mock_yaml_content = """
device_name: "Self-Destruct Test"
activation_code: "TESTS-FAILZ-0"
target_mode: "peaceful_coexistence"
safety_protocols_active: true
self_destruct_sequence:
  enabled: true
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'dummy_path.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Configuration is INVALID:\n")
                        mock_stderr.write.assert_any_call("- Missing required field in 'self_destruct_sequence': 'countdown_hours' when enabled is true.\n")

    def test_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the config file.
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('sys.argv', ['validator.py', 'non_existent.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Error: Configuration file not found at 'non_existent.yaml'.\n")

    def test_yaml_parse_error(self):
        # Mock rationale: Simulate a YAML parsing error (e.g., malformed YAML).
        mock_yaml_content = """
device_name: "Bad YAML"
  activation_code: "INDEN-TATION-1"
  # This is malformed YAML due to incorrect indentation
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'malformed.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        # Check for error message prefix, specific content might vary by yaml version
                        mock_stderr.write.assert_any_call(unittest.mock.ANY)
                        mock_stderr.write.assert_any_call("Error parsing YAML file: ")

    def test_no_arguments(self):
        # Mock rationale: Simulate running the script without any arguments.
        with patch('sys.argv', ['validator.py']):
            with patch('sys.exit') as mock_exit:
                with patch('sys.stderr') as mock_stderr:
                    validator.main()
                    mock_exit.assert_called_once_with(1)
                    mock_stderr.write.assert_any_call("Usage: python validator.py <config_file.yaml>\n")

    def test_yaml_not_dict(self):
        # Mock rationale: Simulate a YAML file that contains a list or scalar, not a dictionary.
        mock_yaml_content = """
- item1
- item2
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('sys.argv', ['validator.py', 'list_config.yaml']):
                with patch('sys.exit') as mock_exit:
                    with patch('sys.stderr') as mock_stderr:
                        validator.main()
                        mock_exit.assert_called_once_with(1)
                        mock_stderr.write.assert_any_call("Error: YAML content must be a dictionary.\n")
