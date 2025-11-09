import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the src directory to the path to allow importing validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from validator import validate_config
sys.path.pop(0)

class TestDoomsdayConfigValidator(unittest.TestCase):

    def test_file_not_found(self):
        # Mock rationale: Simulate a non-existent file without touching the actual filesystem.
        with patch('os.path.exists', return_value=False):
            errors = validate_config('non_existent_file.json')
            self.assertIn("Configuration file not found", errors[0])
            self.assertEqual(len(errors), 1)

    def test_invalid_json_format(self):
        invalid_json_content = "{ 'device_name': 'test', " # Malformed JSON
        # Mock rationale: Simulate reading a file with malformed JSON content.
        with patch('builtins.open', mock_open(read_data=invalid_json_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('invalid.json')
            self.assertIn("Invalid JSON format", errors[0])
            self.assertEqual(len(errors), 1)

    def test_valid_config(self):
        valid_config_content = json.dumps({
            "device_name": "Omega Protocol Initiator",
            "activation_sequence": [1, 3, 5, 7, 9],
            "target_coordinates": [40.7128, -74.0060],
            "safety_override_code": "ALPHA-OMEGA-7",
            "power_level": 9000,
            "status": "standby"
        })
        # Mock rationale: Simulate reading a perfectly valid configuration file.
        with patch('builtins.open', mock_open(read_data=valid_config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('valid.json')
            self.assertEqual(len(errors), 0)

    def test_missing_device_name(self):
        config_content = json.dumps({
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config missing a critical key.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('missing_device_name.json')
            self.assertIn("'device_name' must be a non-empty string.", errors)

    def test_invalid_activation_sequence_type(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": "not a list",
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with incorrect data type for 'activation_sequence'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('invalid_seq_type.json')
            self.assertIn("'activation_sequence' must be a list.", errors)

    def test_short_activation_sequence(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with too few elements in 'activation_sequence'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('short_seq.json')
            self.assertIn("'activation_sequence' must contain at least 3 elements.", errors)

    def test_non_integer_activation_sequence(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, "three"],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with non-integer elements in 'activation_sequence'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('non_int_seq.json')
            self.assertIn("All elements in 'activation_sequence' must be integers.", errors)

    def test_invalid_target_coordinates_length(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with incorrect number of elements in 'target_coordinates'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('invalid_coords_len.json')
            self.assertIn("'target_coordinates' must contain exactly 2 elements.", errors)

    def test_non_numeric_target_coordinates(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0, "two"],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with non-numeric elements in 'target_coordinates'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('non_numeric_coords.json')
            self.assertIn("Both elements in 'target_coordinates' must be numbers", errors)

    def test_empty_safety_override_code(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "",
            "power_level": 100,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with an empty 'safety_override_code'.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('empty_code.json')
            self.assertIn("'safety_override_code' must be a non-empty string.", errors)

    def test_power_level_out_of_range(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 0,
            "status": "standby"
        })
        # Mock rationale: Simulate a config with 'power_level' outside the allowed range.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('low_power.json')
            self.assertIn("'power_level' must be between 1 and 10000.", errors)

    def test_invalid_status(self):
        config_content = json.dumps({
            "device_name": "Test",
            "activation_sequence": [1, 2, 3],
            "target_coordinates": [1.0, 2.0],
            "safety_override_code": "CODE",
            "power_level": 100,
            "status": "unknown"
        })
        # Mock rationale: Simulate a config with an invalid 'status' value.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('invalid_status.json')
            self.assertIn("'status' must be one of ['standby', 'armed', 'disarmed'].", errors)

    def test_multiple_errors(self):
        config_content = json.dumps({
            "device_name": "", # Error 1: empty string
            "activation_sequence": [1, "two"], # Error 2: too short, Error 3: non-integer
            "target_coordinates": [1.0], # Error 4: incorrect length
            "safety_override_code": "", # Error 5: empty string
            "power_level": 10001, # Error 6: out of range
            "status": "invalid" # Error 7: invalid value
        })
        # Mock rationale: Simulate a config with multiple validation errors.
        with patch('builtins.open', mock_open(read_data=config_content)), \
             patch('os.path.exists', return_value=True):
            errors = validate_config('multiple_errors.json')
            self.assertGreater(len(errors), 1)
            self.assertIn("'device_name' must be a non-empty string.", errors)
            self.assertIn("'activation_sequence' must contain at least 3 elements.", errors)
            self.assertIn("All elements in 'activation_sequence' must be integers.", errors)
            self.assertIn("'target_coordinates' must contain exactly 2 elements.", errors)
            self.assertIn("'safety_override_code' must be a non-empty string.", errors)
            self.assertIn("'power_level' must be between 1 and 10000.", errors)
            self.assertIn("'status' must be one of ['standby', 'armed', 'disarmed'].", errors)

if __name__ == '__main__':
    unittest.main()
