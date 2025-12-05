import os
import re
import configparser
import argparse
import sys
from typing import List, Dict, Tuple

class ConfigChaosChecker:
    def __init__(self):
        self.issues: List[Tuple[str, str, str]] = [] # (filepath, level, message)

    def _parse_env_file(self, filepath: str) -> Dict[str, str]:
        config = {}
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    match = re.match(r'^([^=]+?)\s*=\s*(.*)$', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip().strip('"\'') # Remove quotes
                        config[key] = value
        except Exception as e:
            self.issues.append((filepath, 'ERROR', f'Failed to parse .env file: {e}'))
        return config

    def _parse_ini_file(self, filepath: str) -> Dict[str, Dict[str, str]]:
        parser = configparser.ConfigParser()
        config = {}
        try:
            parser.read(filepath)
            for section in parser.sections():
                config[section] = {k: v for k, v in parser.items(section)}
        except Exception as e:
            self.issues.append((filepath, 'ERROR', f'Failed to parse .ini file: {e}'))
        return config

    def _check_sensitive_data(self, filepath: str, config_data: Dict[str, str]):
        sensitive_patterns = re.compile(r'(API_KEY|SECRET|PASSWORD|TOKEN|AUTH_KEY|DB_PASS|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)', re.IGNORECASE)
        for key, value in config_data.items():
            if sensitive_patterns.search(key) and value and len(value) > 8: # Heuristic: value exists and is reasonably long
                self.issues.append((filepath, 'CRITICAL', f"Sensitive data detected for '{key}'. Consider using environment variables or a secret management system."))

    def _check_empty_values(self, filepath: str, config_data: Dict[str, str]):
        critical_keys = ['DATABASE_URL', 'HOST', 'PORT', 'USERNAME', 'DB_NAME', 'APP_ENV']
        for key, value in config_data.items():
            # Check if the key itself is a critical key, or if it's a 'section.key' that contains a critical key
            if key in critical_keys or any(ck in key for ck in critical_keys) and not value:
                self.issues.append((filepath, 'WARNING', f"Empty value for '{key}'. This might cause unexpected behavior."))

    def _check_duplicate_keys_in_file(self, filepath: str):
        # This requires re-reading the file line by line to detect duplicates as parsers might silently overwrite
        keys_found = set()
        duplicate_keys = set()
        current_section = None # For INI files
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if line.startswith('[') and line.endswith(']'): # INI section
                        current_section = line[1:-1].strip()
                        keys_found = set() # Reset keys for new section in INI
                        continue

                    match = re.match(r'^([^=:]+?)\s*[=:]\s*(.*)$', line) # For .env or INI key-value
                    if match:
                        key = match.group(1).strip()
                        # For INI, prepend section to key for uniqueness across sections
                        full_key = f"{current_section}.{key}" if current_section else key

                        if full_key in keys_found:
                            duplicate_keys.add(key) # Report the original key, not the full_key
                        keys_found.add(full_key)

            for key in duplicate_keys:
                self.issues.append((filepath, 'WARNING', f"Duplicate key '{key}' found. The last definition will likely be used, but this indicates a potential error."))
        except Exception as e:
            self.issues.append((filepath, 'ERROR', f'Failed to check for duplicate keys in {filepath}: {e}'))

    def scan_directory(self, root_dir: str):
        print(f"Scanning for config chaos in: {root_dir}")
        self.issues = [] # Reset issues for a new scan

        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filename.endswith('.env'):
                    config_data = self._parse_env_file(filepath)
                    if config_data:
                        self._check_sensitive_data(filepath, config_data)
                        self._check_empty_values(filepath, config_data)
                        self._check_duplicate_keys_in_file(filepath)
                elif filename.endswith('.ini'):
                    ini_config_data = self._parse_ini_file(filepath)
                    if ini_config_data:
                        # For .ini, sensitive/empty checks apply to each section's items
                        flat_ini_data = {f'{section}.{k}': v for section, items in ini_config_data.items() for k, v in items.items()}
                        self._check_sensitive_data(filepath, flat_ini_data)
                        self._check_empty_values(filepath, flat_ini_data)
                        self._check_duplicate_keys_in_file(filepath)

        self.report_issues()

    def report_issues(self):
        if not self.issues:
            print("\nNo chaos detected. Your configurations are in pristine order!")
            return

        print("\n--- Chaos Report ---")
        current_file = None
        # Sort issues by filepath, then level (CRITICAL, WARNING, ERROR)
        level_order = {'CRITICAL': 0, 'WARNING': 1, 'ERROR': 2}
        sorted_issues = sorted(self.issues, key=lambda x: (x[0], level_order.get(x[1], 99)))

        for filepath, level, message in sorted_issues:
            if filepath != current_file:
                if current_file is not None:
                    print()
                print(f"File: {filepath}")
                current_file = filepath
            print(f"  [{level}] {message}")
        print("\n--- Scan Complete ---")


def main():
    parser = argparse.ArgumentParser(description='Scan configuration files for chaos points.')
    parser.add_argument('--path', type=str, required=True, help='The root directory to start scanning for configuration files.')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        sys.exit(1)

    checker = ConfigChaosChecker()
    checker.scan_directory(args.path)

if __name__ == '__main__':
    main()
