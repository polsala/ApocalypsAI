import argparse
import json
import os
import sys

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def load_config(filepath, config_type='auto'):
    """Loads and parses a configuration file (JSON or YAML)."""
    if not os.path.exists(filepath):
        return None, f"Error: File not found at '{filepath}'"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if config_type == 'auto':
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ('.json',):
            config_type = 'json'
        elif ext in ('.yaml', '.yml'):
            config_type = 'yaml'
        else:
            return None, "Error: Could not determine config type. Use --type argument."

    if config_type == 'json':
        try:
            return json.loads(content), None
        except json.JSONDecodeError as e:
            return None, f"Error: Invalid JSON syntax in '{filepath}': {e}"
    elif config_type == 'yaml':
        if not HAS_YAML:
            return None, "Error: PyYAML not installed. Please run 'pip install PyYAML'."
        try:
            return yaml.safe_load(content), None
        except yaml.YAMLError as e:
            return None, f"Error: Invalid YAML syntax in '{filepath}': {e}"
    else:
        return None, f"Error: Unsupported config type '{config_type}'. Must be 'json' or 'yaml'."

def validate_config(filepath, required_keys=None, config_type='auto'):
    """Validates a configuration file for syntax and required keys."""
    config, error = load_config(filepath, config_type)
    if error:
        return False, error

    if config is None:
        return False, f"Error: Configuration file '{filepath}' is empty or could not be parsed."

    if not isinstance(config, dict):
        return False, f"Error: Configuration file '{filepath}' must contain a dictionary at its root."

    if required_keys:
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            return False, f"Error: Missing required keys: {', '.join(missing_keys)}"

    return True, "Configuration is valid."

def main():
    parser = argparse.ArgumentParser(
        description="Validate JSON or YAML configuration files for syntax and required keys."
    )
    parser.add_argument(
        "filepath",
        help="Path to the configuration file."
    )
    parser.add_argument(
        "--required-keys",
        nargs='*', # 0 or more arguments
        default=[],
        help="Space-separated list of top-level keys that must be present."
    )
    parser.add_argument(
        "--type",
        choices=['json', 'yaml'],
        default='auto',
        help="Explicitly specify config type (json or yaml). Auto-detects by default."
    )

    args = parser.parse_args()

    is_valid, message = validate_config(
        args.filepath,
        required_keys=args.required_keys,
        config_type=args.type
    )

    print(message)
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
