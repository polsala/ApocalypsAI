import argparse
import yaml
import json
import os
from typing import Any, Dict, List, Union

class DoomsdayConfigValidator:
    def __init__(self, config_data: Dict[str, Any], schema_data: Dict[str, Any], config_name: str = "unknown_config"):
        self.config_data = config_data
        self.schema_data = schema_data
        self.config_name = config_name
        self.errors = []

    def _add_error(self, message: str):
        self.errors.append(f"[INTEGRATOR] ERROR: Doomsday device configuration '{self.config_name}' has critical structural anomalies! ({message})")

    def validate_required_keys(self):
        required_keys = self.schema_data.get('required_keys', [])
        for key in required_keys:
            if key not in self.config_data:
                self._add_error(f"Missing key: '{key}'")

    def validate_key_types(self):
        key_types = self.schema_data.get('key_types', {})
        for key, expected_type_str in key_types.items():
            if key in self.config_data:
                value = self.config_data[key]
                expected_type = self._get_python_type(expected_type_str)
                if not isinstance(value, expected_type):
                    self._add_error(f"Key '{key}' has incorrect type. Expected {expected_type_str}, got {type(value).__name__}")

    def validate_list_item_types(self):
        list_item_types = self.schema_data.get('list_item_types', {})
        for key, expected_item_type_str in list_item_types.items():
            if key in self.config_data:
                value = self.config_data[key]
                if isinstance(value, list):
                    expected_item_type = self._get_python_type(expected_item_type_str)
                    for i, item in enumerate(value):
                        if not isinstance(item, expected_item_type):
                            self._add_error(f"List '{key}' at index {i} has item of incorrect type. Expected {expected_item_type_str}, got {type(item).__name__}")
                elif value is not None:
                    self._add_error(f"Key '{key}' is expected to be a list but is {type(value).__name__}")

    def _get_python_type(self, type_str: str) -> type:
        type_map = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'any': Any # For schema flexibility
        }
        return type_map.get(type_str.lower(), Any)

    def validate(self) -> bool:
        self.validate_required_keys()
        self.validate_key_types()
        self.validate_list_item_types()
        return not bool(self.errors)

    def get_errors(self) -> List[str]:
        return self.errors

def load_config_file(file_path: str) -> Dict[str, Any]:
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        if ext in ('.yaml', '.yml'):
            return yaml.safe_load(f)
        elif ext == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported configuration file type: {ext}. Only .yaml, .yml, and .json are supported.")

def main():
    parser = argparse.ArgumentParser(description="Validate doomsday device configuration files.")
    parser.add_argument('--config-file', required=True, help="Path to the configuration file (YAML or JSON).")
    parser.add_argument('--schema-file', required=True, help="Path to the schema definition file (YAML or JSON).")

    args = parser.parse_args()

    try:
        config_data = load_config_file(args.config_file)
        schema_data = load_config_file(args.schema_file)

        config_name = os.path.basename(args.config_file)
        validator = DoomsdayConfigValidator(config_data, schema_data, config_name)

        if validator.validate():
            print(f"[INTEGRATOR] Doomsday device configuration '{config_name}' is structurally sound. The end is nigh, but at least it's configured correctly.")
            exit(0)
        else:
            for error in validator.get_errors():
                print(error)
            exit(1)
    except FileNotFoundError as e:
        print(f"[INTEGRATOR] ERROR: Critical file not found: {e}")
        exit(1)
    except ValueError as e:
        print(f"[INTEGRATOR] ERROR: Configuration parsing failed: {e}")
        exit(1)
    except yaml.YAMLError as e:
        print(f"[INTEGRATOR] ERROR: YAML parsing failed for '{args.config_file}': {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"[INTEGRATOR] ERROR: JSON parsing failed for '{args.config_file}': {e}")
        exit(1)
    except Exception as e:
        print(f"[INTEGRATOR] An unexpected catastrophe occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
