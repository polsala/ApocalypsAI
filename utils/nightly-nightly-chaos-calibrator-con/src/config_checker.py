import yaml
import json
import os
import sys

class ConfigChecker:
    def __init__(self, config_path, rules_path=None):
        self.config_path = config_path
        self.rules_path = rules_path
        self.errors = []
        self.config_data = None
        self.rules_data = None

    def _load_file(self, file_path):
        if not os.path.exists(file_path):
            self.errors.append(f"Error: File not found at {file_path}")
            return None
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(f)
                elif file_path.endswith('.json'):
                    return json.load(f)
                else:
                    self.errors.append(f"Error: Unsupported file type for {file_path}. Only .yaml, .yml, and .json are supported.")
                    return None
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            self.errors.append(f"Error parsing {file_path}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"An unexpected error occurred while loading {file_path}: {e}")
            return None

    def _validate_required_keys(self, data, required_keys, path=""):
        if not isinstance(data, dict):
            return
        for key in required_keys:
            current_path = f"{path}{key}"
            if key not in data:
                self.errors.append(f"Missing required key: '{current_path}'")
            elif isinstance(required_keys[key], dict): # Nested required keys
                self._validate_required_keys(data.get(key, {}), required_keys[key], path=f"{current_path}.")

    def _validate_types(self, data, type_rules, path=""):
        if not isinstance(data, dict):
            return
        for key, expected_type_str in type_rules.items():
            current_path = f"{path}{key}"
            if key in data:
                value = data[key]
                if isinstance(expected_type_str, dict): # Nested type rules
                    self._validate_types(value, expected_type_str, path=f"{current_path}.")
                else:
                    # Map string type names to Python types
                    type_map = {
                        'string': str,
                        'integer': int,
                        'boolean': bool,
                        'list': list,
                        'dict': dict,
                        'float': float
                    }
                    expected_type = type_map.get(expected_type_str)

                    if expected_type is None:
                        self.errors.append(f"Unknown type rule '{expected_type_str}' for '{current_path}'")
                    elif not isinstance(value, expected_type):
                        self.errors.append(f"Incorrect type for '{current_path}': Expected {expected_type.__name__}, got {type(value).__name__}")

    def _validate_values(self, data, value_rules, path=""):
        if not isinstance(data, dict):
            return
        for key, rule in value_rules.items():
            current_path = f"{path}{key}"
            if key in data:
                value = data[key]
                if isinstance(rule, dict): # Nested value rules
                    self._validate_values(value, rule, path=f"{current_path}.")
                else:
                    if 'enum' in rule and value not in rule['enum']:
                        self.errors.append(f"Invalid value for '{current_path}': '{value}' not in allowed list {rule['enum']}")
                    if 'min' in rule and isinstance(value, (int, float)) and value < rule['min']:
                        self.errors.append(f"Value for '{current_path}' is too low: {value} (min: {rule['min']})")
                    if 'max' in rule and isinstance(value, (int, float)) and value > rule['max']:
                        self.errors.append(f"Value for '{current_path}' is too high: {value} (max: {rule['max']})")

    def check(self):
        self.config_data = self._load_file(self.config_path)
        if self.config_data is None and not self.errors: # If load failed but no specific error, it means file not found or empty
             self.errors.append(f"Failed to load configuration from {self.config_path}")
             return self.errors

        if self.rules_path:
            self.rules_data = self._load_file(self.rules_path)
            if self.rules_data is None and not self.errors:
                self.errors.append(f"Failed to load rules from {self.rules_path}")
                return self.errors

        if self.config_data is None or (self.rules_path and self.rules_data is None):
            return self.errors # Errors already populated by _load_file

        if self.rules_data:
            if 'required_keys' in self.rules_data:
                self._validate_required_keys(self.config_data, self.rules_data['required_keys'])
            if 'type_rules' in self.rules_data:
                self._validate_types(self.config_data, self.rules_data['type_rules'])
            if 'value_rules' in self.rules_data:
                self._validate_values(self.config_data, self.rules_data['value_rules'])

        return self.errors

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Nightly Chaos Calibrator Config Checker")
    parser.add_argument("config_file", help="Path to the configuration file (YAML or JSON)")
    parser.add_argument("--rules-file", help="Optional path to a rules file (YAML or JSON) for validation")
    args = parser.parse_args()

    checker = ConfigChecker(args.config_file, args.rules_file)
    errors = checker.check()

    if errors:
        print(f"Configuration check failed for {args.config_file}:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print(f"Configuration for {args.config_file} is perfectly calibrated. All systems nominal!")
        sys.exit(0)

if __name__ == "__main__":
    main()
