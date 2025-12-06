import argparse
import json
import yaml
import configparser
import sys
import os

def validate_json(file_path):
    """Validates a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "JSON file is valid."
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def validate_yaml(file_path):
    """Validates a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True, "YAML file is valid."
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def validate_ini(file_path):
    """Validates an INI file."""
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config.read_string(f.read()) # read_string is safer for testing content directly
        return True, "INI file is valid."
    except configparser.Error as e:
        return False, f"Invalid INI: {e}"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Config Quirk Quencher: Validate JSON, YAML, or INI configuration files."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the configuration file."
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=['json', 'yaml', 'ini'],
        required=True,
        help="Type of the configuration file (json, yaml, ini)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found at '{args.file}'", file=sys.stderr)
        sys.exit(1)

    is_valid, message = False, "Unknown error."

    if args.type == 'json':
        is_valid, message = validate_json(args.file)
    elif args.type == 'yaml':
        is_valid, message = validate_yaml(args.file)
    elif args.type == 'ini':
        is_valid, message = validate_ini(args.file)

    if is_valid:
        print(f"✅ Success: {message}")
        sys.exit(0)
    else:
        print(f"❌ Failure: {message}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
