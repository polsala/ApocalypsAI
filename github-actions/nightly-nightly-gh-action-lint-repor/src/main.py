import sys
import os
import yaml
from typing import List, Dict, Any

def lint_yaml_file(file_path: str) -> List[str]:
    """Lints a single YAML file for basic syntax errors."""
    errors = []
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"Syntax error in {file_path}: {e}")
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(f"Unexpected error processing {file_path}: {e}")
    return errors

def find_yaml_files(search_path: str) -> List[str]:
    """Finds all .yaml and .yml files recursively from a given path."""
    yaml_files = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

def main():
    search_path = os.environ.get('INPUT_SEARCH_PATH', '.')
    fail_on_error = os.environ.get('INPUT_FAIL_ON_ERROR', 'false').lower() == 'true'

    all_errors: List[str] = []
    yaml_files = find_yaml_files(search_path)

    if not yaml_files:
        print("No YAML files found to lint.")
        sys.exit(0)

    for file_path in yaml_files:
        errors = lint_yaml_file(file_path)
        all_errors.extend(errors)

    summary = "YAML Linting Report:\n"
    if all_errors:
        summary += f"Found {len(all_errors)} errors:\n"
        for error in all_errors:
            summary += f"- {error}\n"
    else:
        summary += "All YAML files linted successfully with no errors found."

    print(f"::set-output name=lint_summary::{summary}")
    print(f"::set-output name=has_errors::{'true' if all_errors else 'false'}")

    if fail_on_error and all_errors:
        print("::error::YAML linting failed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
