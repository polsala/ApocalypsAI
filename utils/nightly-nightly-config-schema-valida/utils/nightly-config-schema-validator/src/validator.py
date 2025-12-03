import argparse
import json
import sys
import yaml
from jsonschema import validate, ValidationError

def load_file(filepath):
    """Loads a YAML or JSON file based on its extension."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if filepath.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif filepath.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError(f"Unsupported file type for {filepath}. Must be .yaml, .yml, or .json.")
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print(f"Error: Malformed file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def validate_config(config_data, schema_data):
    """Validates configuration data against a schema."""
    try:
        validate(instance=config_data, schema=schema_data)
        return True, None
    except ValidationError as e:
        return False, e
    except Exception as e:
        return False, f"An unexpected error occurred during validation: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Schema Shaman's Scrutiny: Validate configuration files against a schema."
    )
    parser.add_argument('--config', required=True, help='Path to the configuration file (YAML or JSON).')
    parser.add_argument('--schema', required=True, help='Path to the schema file (YAML or JSON).')

    args = parser.parse_args()

    config_data = load_file(args.config)
    schema_data = load_file(args.schema)

    is_valid, error = validate_config(config_data, schema_data)

    if is_valid:
        print(f"✅ Configuration '{args.config}' is valid according to schema '{args.schema}'. The spirits are pleased!")
        sys.exit(0)
    else:
        print(f"❌ Configuration '{args.config}' failed validation against schema '{args.schema}':", file=sys.stderr)
        if isinstance(error, ValidationError):
            print(error.message, file=sys.stderr)
            if error.path:
                print(f"Path: {' -> '.join(map(str, error.path))}", file=sys.stderr)
            if error.validator and error.validator_value:
                print(f"Validator: {error.validator} with value {error.validator_value}", file=sys.stderr)
        else:
            print(error, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
