import unittest
import json
from unittest.mock import patch, mock_open
import sys
import os

# Mock rationale: We need to test the `debugger.py` script's `main` function
# which reads from a file and prints to stdout, and exits with a specific code.
# To make tests deterministic and offline, we mock `open` to simulate file content
# and `sys.argv` to simulate command-line arguments. We also capture `sys.stdout`
# to check printed output and `sys.exit` to check exit codes without actually exiting.

# Add the src directory to the Python path for importing the module
# Mock rationale: This allows the test file to import the utility's source code
# directly without relying on the package being installed or complex path configurations.
# It ensures the test is self-contained and runnable from within its utility folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from debugger import validate_config, main

class TestDoomsdayDeviceDebugger(unittest.TestCase):

    def setUp(self):
        # Store original sys.stdout and sys.argv
        self._original_stdout = sys.stdout
        self._original_argv = sys.argv
        # Create a mock for stdout
        self.mock_stdout = unittest.mock.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore original sys.stdout and sys.argv
        sys.stdout = self._original_stdout
        sys.argv = self._original_argv

    def _run_main_with_mocked_file(self, config_content, filename="test_config.json"):
        # Mock rationale: Simulate reading a file from disk without actual file I/O.
        # This ensures tests are offline and deterministic.
        mock_file_handle = mock_open(read_data=config_content)
        with patch('builtins.open', mock_file_handle),
             patch('os.path.exists', return_value=True),
             patch('sys.exit') as mock_exit:
            sys.argv = ['debugger.py', filename]
            main()
            return self.mock_stdout.getvalue(), mock_exit.call_args[0][0] if mock_exit.called else None

    def test_validate_config_valid(self):
        valid_config = {
            "device_name": "Apocalypse Initiator",
            "activation_code": "ALPHA123",
            "target_population_percentage": 99,
            "power_source": "Fusion Core",
            "countdown_timer_seconds": 600,
            "safety_protocols": ["Fingerprint scan", "Voice command"],
            "self_destruct_on_failure": False
        }
        errors, warnings = validate_config(valid_config)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)

    def test_validate_config_minimal_valid(self):
        minimal_config = {
            "device_name": "Minimal Destroyer",
            "activation_code": "MINIMAL",
            "target_population_percentage": 50,
            "power_source": "Solar",
            "countdown_timer_seconds": 10
        }
        errors, warnings = validate_config(minimal_config)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)

    def test_validate_config_missing_required_fields(self):
        invalid_config = {
            "activation_code": "CODE123",
            "power_source": "Dark Energy"
        }
        errors, warnings = validate_config(invalid_config)
        self.assertGreater(len(errors), 0)
        self.assertIn("Missing required field: 'device_name'.", errors)
        self.assertIn("Missing required field: 'target_population_percentage'.", errors)
        self.assertIn("Missing required field: 'countdown_timer_seconds'.", errors)

    def test_validate_config_invalid_types_and_values(self):
        invalid_config = {
            "device_name": 123, # Invalid type
            "activation_code": "short", # Too short
            "target_population_percentage": 101, # Out of range
            "power_source": "", # Empty string
            "countdown_timer_seconds": -5, # Negative
            "safety_protocols": ["protocol1", ""], # Empty protocol
            "self_destruct_on_failure": "not_a_bool" # Invalid type
        }
        errors, warnings = validate_config(invalid_config)
        self.assertGreater(len(errors), 0)
        self.assertIn("'device_name' must be a non-empty string.", errors)
        self.assertIn("'activation_code' must be an alphanumeric string of at least 6 characters.", errors)
        self.assertIn("'target_population_percentage' must be an integer between 0 and 100.", errors)
        self.assertIn("'power_source' must be a non-empty string.", errors)
        self.assertIn("'countdown_timer_seconds' must be a positive integer.", errors)
        self.assertIn("'safety_protocols' item 1 must be a non-empty string.", errors)
        self.assertIn("'self_destruct_on_failure' must be a boolean.", errors)

    def test_main_success(self):
        valid_config_json = json.dumps({
            "device_name": "Test Device",
            "activation_code": "TESTCODE",
            "target_population_percentage": 50,
            "power_source": "Test Power",
            "countdown_timer_seconds": 100
        })
        output, exit_code = self._run_main_with_mocked_file(valid_config_json)
        self.assertIn("Flawless and ready for deployment!", output)
        self.assertEqual(exit_code, 0)

    def test_main_failure_invalid_json(self):
        invalid_json_content = "{ 'device_name': 'Bad JSON' "
        output, exit_code = self._run_main_with_mocked_file(invalid_json_content)
        self.assertIn("Error: Invalid JSON format", output)
        self.assertEqual(exit_code, 1)

    def test_main_failure_validation_errors(self):
        invalid_config_json = json.dumps({
            "device_name": "", # Empty string
            "activation_code": "123", # Too short
            "countdown_timer_seconds": 0 # Not positive
        })
        output, exit_code = self._run_main_with_mocked_file(invalid_config_json)
        self.assertIn("Errors found (critical flaws!):", output)
        self.assertIn("'device_name' must be a non-empty string.", output)
        self.assertIn("'activation_code' must be an alphanumeric string of at least 6 characters.", output)
        self.assertIn("Missing required field: 'target_population_percentage'.", output) # Also checks for missing fields
        self.assertIn("Missing required field: 'power_source'.", output)
        self.assertIn("'countdown_timer_seconds' must be a positive integer.", output)
        self.assertIn("Status: Device configuration requires immediate attention!", output)
        self.assertEqual(exit_code, 1)

    def test_main_no_args(self):
        # Mock rationale: Simulate running the script without any command-line arguments.
        # This tests the argument parsing logic.
        with patch('sys.exit') as mock_exit:
            sys.argv = ['debugger.py']
            main()
            output = self.mock_stdout.getvalue()
            self.assertIn("Usage: python src/debugger.py <config_file.json>", output)
            self.assertEqual(mock_exit.call_args[0][0], 1)

    def test_main_file_not_found(self):
        # Mock rationale: Simulate a scenario where the specified config file does not exist.
        # This tests the file existence check.
        with patch('os.path.exists', return_value=False),
             patch('sys.exit') as mock_exit:
            sys.argv = ['debugger.py', 'non_existent_file.json']
            main()
            output = self.mock_stdout.getvalue()
            self.assertIn("Error: Configuration file not found at 'non_existent_file.json'", output)
            self.assertEqual(mock_exit.call_args[0][0], 1)

if __name__ == '__main__':
    unittest.main()
