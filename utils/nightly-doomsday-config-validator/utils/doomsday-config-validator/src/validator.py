import json
import sys
import os

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please install it using 'pip install pyyaml'.", file=sys.stderr)
    sys.exit(1)

def validate_yaml_string(content: str) -> tuple[bool, str]:
    """Validates a YAML string for syntax errors."""
    try:
        yaml.safe_load(content)
        return True, "Syntax is pristine. The apocalypse can wait."
    except yaml.YAMLError as e:
        return False, f"YAML syntax error: {e}"

def validate_json_string(content: str) -> tuple[bool, str]:
    """Validates a JSON string for syntax errors."""
    try:
        json.loads(content)
        return True, "Syntax is pristine. The apocalypse can wait."
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error: {e}"

def validate_file(file_path: str) -> tuple[bool, str]:
    """Reads a file and validates its content based on file extension."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"

    if ext in ('.yaml', '.yml'):
        return validate_yaml_string(content)
    elif ext == '.json':
        return validate_json_string(content)
    else:
        return False, f"Unsupported file type: {ext}. Only .yaml, .yml, and .json are supported."


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/validator.py <path_to_config_file>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    is_valid, message = validate_file(file_path)

    status = "OK" if is_valid else "ERROR"
    print(f"{file_path}: {status} - {message}")
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
