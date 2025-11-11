import pytest
import os
from unittest.mock import patch, mock_open
from src.validator import DoomsdayConfigValidator, load_config_file, main

# Mock rationale: We need to simulate file system interactions (reading config and schema files)
# without actually creating files on disk or relying on external file paths during tests.
# `mock_open` allows us to provide predefined content for file reads, making tests deterministic and isolated.
# `patch` is used to intercept calls to `argparse`, `sys.exit`, and `print` to control CLI behavior
# and capture output without affecting the actual system during testing.

# --- Fixture Data for Mocks ---
VALID_YAML_CONFIG = """
device_name: "Chronos Disruptor"
activation_sequence:
  - "Initiate temporal flux capacitor"
  - "Calibrate quantum entanglement field"
power_source: "Dark Matter Reactor"
debug_mode: false
"""

VALID_JSON_CONFIG = """
{
  "device_name": "Quantum Stabilizer",
  "activation_sequence": [
    "Stabilize quantum field",
    "Engage temporal lock"
  ],
  "power_source": "Zero-Point Energy",
  "debug_mode": true
}
"""

VALID_SCHEMA = """
required_keys:
  - device_name
  - activation_sequence
  - power_source
optional_keys:
  - debug_mode
key_types:
  device_name: str
  activation_sequence: list
  power_source: str
  debug_mode: bool
list_item_types:
  activation_sequence: str
"""

INVALID_YAML_MISSING_KEY = """
device_name: "Chronos Disruptor"
activation_sequence:
  - "Initiate temporal flux capacitor"
  - "Calibrate quantum entanglement field"
debug_mode: false
"""

INVALID_YAML_WRONG_TYPE = """
device_name: 123 # Should be str
activation_sequence:
  - "Initiate temporal flux capacitor"
  - "Calibrate quantum entanglement field"
power_source: "Dark Matter Reactor"
debug_mode: false
"""

INVALID_YAML_LIST_ITEM_TYPE = """
device_name: "Chronos Disruptor"
activation_sequence:
  - "Initiate temporal flux capacitor"
  - 123 # Should be str
power_source: "Dark Matter Reactor"
debug_mode: false
"""

INVALID_JSON_MISSING_KEY = """
{
  "device_name": "Quantum Stabilizer",
  "activation_sequence": [
    "Stabilize quantum field"
  ]
}
"""

INVALID_JSON_WRONG_TYPE = """
{
  "device_name": "Quantum Stabilizer",
  "activation_sequence": [
    "Stabilize quantum field"
  ],
  "power_source": 12345, # Should be str
  "debug_mode": true
}
"""

# --- Test Cases for DoomsdayConfigValidator class ---

def test_validator_valid_yaml_config():
    config_data = DoomsdayConfigValidator(yaml.safe_load(VALID_YAML_CONFIG), yaml.safe_load(VALID_SCHEMA))
    assert config_data.validate() is True
    assert not config_data.get_errors()

def test_validator_valid_json_config():
    config_data = DoomsdayConfigValidator(json.loads(VALID_JSON_CONFIG), yaml.safe_load(VALID_SCHEMA))
    assert config_data.validate() is True
    assert not config_data.get_errors()

def test_validator_missing_required_key():
    config_data = DoomsdayConfigValidator(yaml.safe_load(INVALID_YAML_MISSING_KEY), yaml.safe_load(VALID_SCHEMA), "missing_key.yaml")
    assert config_data.validate() is False
    assert "Missing key: 'power_source'" in config_data.get_errors()[0]

def test_validator_wrong_key_type():
    config_data = DoomsdayConfigValidator(yaml.safe_load(INVALID_YAML_WRONG_TYPE), yaml.safe_load(VALID_SCHEMA), "wrong_type.yaml")
    assert config_data.validate() is False
    assert "Key 'device_name' has incorrect type. Expected str, got int" in config_data.get_errors()[0]

def test_validator_wrong_list_item_type():
    config_data = DoomsdayConfigValidator(yaml.safe_load(INVALID_YAML_LIST_ITEM_TYPE), yaml.safe_load(VALID_SCHEMA), "wrong_list_item_type.yaml")
    assert config_data.validate() is False
    assert "List 'activation_sequence' at index 1 has item of incorrect type. Expected str, got int" in config_data.get_errors()[0]

# --- Test Cases for load_config_file function ---

@patch("builtins.open", new_callable=mock_open, read_data=VALID_YAML_CONFIG)
@patch("os.path.splitext", return_value=("config", ".yaml"))
def test_load_yaml_config(mock_split, mock_file):
    data = load_config_file("dummy.yaml")
    assert data == yaml.safe_load(VALID_YAML_CONFIG)

@patch("builtins.open", new_callable=mock_open, read_data=VALID_JSON_CONFIG)
@patch("os.path.splitext", return_value=("config", ".json"))
def test_load_json_config(mock_split, mock_file):
    data = load_config_file("dummy.json")
    assert data == json.loads(VALID_JSON_CONFIG)

@patch("builtins.open", new_callable=mock_open, read_data="<invalid content>")
@patch("os.path.splitext", return_value=("config", ".txt"))
def test_load_unsupported_type(mock_split, mock_file):
    with pytest.raises(ValueError, match="Unsupported configuration file type"):
        load_config_file("dummy.txt")

@patch("builtins.open", new_callable=mock_open, read_data="invalid yaml: - ")
@patch("os.path.splitext", return_value=("config", ".yaml"))
def test_load_invalid_yaml(mock_split, mock_file):
    with pytest.raises(yaml.YAMLError):
        load_config_file("invalid.yaml")

@patch("builtins.open", new_callable=mock_open, read_data="{invalid json}")
@patch("os.path.splitext", return_value=("config", ".json"))
def test_load_invalid_json(mock_split, mock_file):
    with pytest.raises(json.JSONDecodeError):
        load_config_file("invalid.json")

# --- Test Cases for main function (CLI) ---

@patch('argparse.ArgumentParser.parse_args')
@patch('src.validator.load_config_file')
@patch('src.validator.DoomsdayConfigValidator')
@patch('builtins.print')
@patch('sys.exit')
def test_main_success(mock_exit, mock_print, MockValidator, mock_load_config, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        config_file='path/to/valid_config.yaml',
        schema_file='path/to/valid_schema.yaml'
    )
    mock_load_config.side_effect = [yaml.safe_load(VALID_YAML_CONFIG), yaml.safe_load(VALID_SCHEMA)]
    
    mock_validator_instance = MockValidator.return_value
    mock_validator_instance.validate.return_value = True
    mock_validator_instance.get_errors.return_value = []

    main()
    mock_print.assert_called_with("[INTEGRATOR] Doomsday device configuration 'valid_config.yaml' is structurally sound. The end is nigh, but at least it's configured correctly.")
    mock_exit.assert_called_with(0)

@patch('argparse.ArgumentParser.parse_args')
@patch('src.validator.load_config_file')
@patch('src.validator.DoomsdayConfigValidator')
@patch('builtins.print')
@patch('sys.exit')
def test_main_failure(mock_exit, mock_print, MockValidator, mock_load_config, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        config_file='path/to/invalid_config.yaml',
        schema_file='path/to/valid_schema.yaml'
    )
    mock_load_config.side_effect = [yaml.safe_load(INVALID_YAML_MISSING_KEY), yaml.safe_load(VALID_SCHEMA)]
    
    mock_validator_instance = MockValidator.return_value
    mock_validator_instance.validate.return_value = False
    mock_validator_instance.get_errors.return_value = ["[INTEGRATOR] ERROR: Doomsday device configuration 'invalid_config.yaml' has critical structural anomalies! (Missing key: 'power_source')"]

    main()
    mock_print.assert_called_with("[INTEGRATOR] ERROR: Doomsday device configuration 'invalid_config.yaml' has critical structural anomalies! (Missing key: 'power_source')")
    mock_exit.assert_called_with(1)

@patch('argparse.ArgumentParser.parse_args')
@patch('src.validator.load_config_file')
@patch('builtins.print')
@patch('sys.exit')
def test_main_file_not_found(mock_exit, mock_print, mock_load_config, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        config_file='path/to/non_existent.yaml',
        schema_file='path/to/valid_schema.yaml'
    )
    mock_load_config.side_effect = FileNotFoundError("No such file")

    main()
    mock_print.assert_called_with("[INTEGRATOR] ERROR: Critical file not found: No such file")
    mock_exit.assert_called_with(1)

@patch('argparse.ArgumentParser.parse_args')
@patch('src.validator.load_config_file')
@patch('builtins.print')
@patch('sys.exit')
def test_main_yaml_error(mock_exit, mock_print, mock_load_config, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        config_file='path/to/invalid.yaml',
        schema_file='path/to/valid_schema.yaml'
    )
    mock_load_config.side_effect = yaml.YAMLError("Invalid YAML")

    main()
    mock_print.assert_called_with("[INTEGRATOR] ERROR: YAML parsing failed for 'path/to/invalid.yaml': Invalid YAML")
    mock_exit.assert_called_with(1)

@patch('argparse.ArgumentParser.parse_args')
@patch('src.validator.load_config_file')
@patch('builtins.print')
@patch('sys.exit')
def test_main_unsupported_type_error(mock_exit, mock_print, mock_load_config, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        config_file='path/to/config.txt',
        schema_file='path/to/schema.yaml'
    )
    mock_load_config.side_effect = ValueError("Unsupported configuration file type")

    main()
    mock_print.assert_called_with("[INTEGRATOR] ERROR: Configuration parsing failed: Unsupported configuration file type")
    mock_exit.assert_called_with(1)
