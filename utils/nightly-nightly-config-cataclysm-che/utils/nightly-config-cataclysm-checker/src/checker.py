import os
import json
import yaml # Using pyyaml, which is allowed by AGENTS.md for optional deps
import argparse
from typing import List, Dict, Any, Tuple

class ConfigCataclysmChecker:
    def __init__(self, config_spec_path: str):
        self.config_spec_path = config_spec_path
        self.errors: List[str] = []

    def _load_spec(self) -> Dict[str, Any]:
        """Loads the configuration specification from a JSON file."""
        if not os.path.exists(self.config_spec_path):
            raise FileNotFoundError(f"Config specification file not found: {self.config_spec_path}")
        with open(self.config_spec_path, 'r') as f:
            return json.load(f)

    def _check_file_or_dir(self, item: Dict[str, Any]) -> None:
        path = item['path']
        required = item.get('required', True)
        item_type = item.get('type', 'file') # 'file', 'directory', 'json', 'yaml'

        exists = os.path.exists(path)

        if required and not exists:
            self.errors.append(f"MISSING: Required {item_type} '{path}' does not exist.")
            return

        if exists:
            if item_type == 'directory' and not os.path.isdir(path):
                self.errors.append(f"TYPE MISMATCH: Expected '{path}' to be a directory, but it's not.")
            elif item_type == 'file' and not os.path.isfile(path):
                self.errors.append(f"TYPE MISMATCH: Expected '{path}' to be a file, but it's not.")
            elif item_type == 'json' and os.path.isfile(path):
                try:
                    with open(path, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    self.errors.append(f"INVALID FORMAT: File '{path}' is not valid JSON.")
            elif item_type == 'yaml' and os.path.isfile(path):
                try:
                    with open(path, 'r') as f:
                        yaml.safe_load(f)
                except yaml.YAMLError:
                    self.errors.append(f"INVALID FORMAT: File '{path}' is not valid YAML.")

    def _check_env_var(self, item: Dict[str, Any]) -> None:
        name = item['name']
        required = item.get('required', True)
        var_type = item.get('type', 'string') # 'string', 'int', 'boolean'

        value = os.environ.get(name)

        if required and value is None:
            self.errors.append(f"MISSING: Required environment variable '{name}' is not set.")
            return

        if value is not None:
            if var_type == 'int':
                try:
                    int(value)
                except ValueError:
                    self.errors.append(f"TYPE MISMATCH: Environment variable '{name}' ('{value}') is not a valid integer.")
            elif var_type == 'boolean':
                if value.lower() not in ['true', 'false', '1', '0']:
                    self.errors.append(f"TYPE MISMATCH: Environment variable '{name}' ('{value}') is not a valid boolean (true/false/1/0).")

    def run_checks(self) -> bool:
        """Runs all checks defined in the specification."""
        self.errors = [] # Reset errors for each run
        try:
            spec = self._load_spec()
        except FileNotFoundError as e:
            self.errors.append(str(e))
            return False
        except json.JSONDecodeError:
            self.errors.append(f"INVALID FORMAT: Config specification file '{self.config_spec_path}' is not valid JSON.")
            return False

        for item in spec.get('files', []):
            self._check_file_or_dir(item)

        for item in spec.get('env_vars', []):
            self._check_env_var(item)

        return not self.errors

    def get_errors(self) -> List[str]:
        return self.errors

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Config Cataclysm Checker: Ensures critical configurations are present and valid."
    )
    parser.add_argument(
        "config_spec",
        help="Path to the JSON file containing the configuration specification."
    )
    args = parser.parse_args()

    checker = ConfigCataclysmChecker(args.config_spec)
    if checker.run_checks():
        print("✅ All configurations are present and valid. No cataclysm detected!")
        exit(0)
    else:
        print("❌ Configuration cataclysm detected! The following issues were found:")
        for error in checker.get_errors():
            print(f"- {error}")
        exit(1)

if __name__ == "__main__":
    main()
