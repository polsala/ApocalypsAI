import argparse
import json
import sys
import os

# Conditional import for YAML and TOML
try:
    import yaml
except ImportError:
    yaml = None

try:
    import tomli
    import tomli_w # tomli_w is for writing, tomli is for reading
except ImportError:
    tomli = None
    tomli_w = None


def load_json(file_content: str) -> dict:
    """Loads data from a JSON string."""
    return json.loads(file_content)

def dump_json(data: dict) -> str:
    """Dumps data to a JSON string."""
    return json.dumps(data, indent=2)

def load_yaml(file_content: str) -> dict:
    """Loads data from a YAML string."""
    if yaml is None:
        raise ImportError("PyYAML library not found. Please install it with 'pip install PyYAML'.")
    return yaml.safe_load(file_content)

def dump_yaml(data: dict) -> str:
    """Dumps data to a YAML string."""
    if yaml is None:
        raise ImportError("PyYAML library not found. Please install it with 'pip install PyYAML'.")
    # default_flow_style=False for block style, sort_keys=False to preserve order (Python 3.7+)
    return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

def load_toml(file_content: str) -> dict:
    """Loads data from a TOML string."""
    if tomli is None:
        raise ImportError("tomli library not found. Please install it with 'pip install tomli'.")
    return tomli.loads(file_content)

def dump_toml(data: dict) -> str:
    """Dumps data to a TOML string."""
    if tomli_w is None:
        raise ImportError("tomli_w library not found. Please install it with 'pip install tomli_w'.")
    return tomli_w.dumps(data)

FORMAT_HANDLERS = {
    'json': {'load': load_json, 'dump': dump_json},
    'yaml': {'load': load_yaml, 'dump': dump_yaml},
    'toml': {'load': load_toml, 'dump': dump_toml},
}

def convert_data(input_path: str, output_path: str, input_format: str, output_format: str):
    """Reads data from input_path, converts it, and writes to output_path."""
    if input_format not in FORMAT_HANDLERS:
        raise ValueError(f"Unsupported input format: {input_format}. Supported are: {', '.join(FORMAT_HANDLERS.keys())}")
    if output_format not in FORMAT_HANDLERS:
        raise ValueError(f"Unsupported output format: {output_format}. Supported are: {', '.join(FORMAT_HANDLERS.keys())}")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_path}")
    except Exception as e:
        raise IOError(f"Error reading input file {input_path}: {e}")

    try:
        loaded_data = FORMAT_HANDLERS[input_format]['load'](input_content)
    except Exception as e:
        raise ValueError(f"Error parsing input file as {input_format}: {e}")

    try:
        output_content = FORMAT_HANDLERS[output_format]['dump'](loaded_data)
    except Exception as e:
        raise ValueError(f"Error converting data to {output_format}: {e}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
    except Exception as e:
        raise IOError(f"Error writing output file {output_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert data between JSON, YAML, and TOML formats."
    )
    parser.add_argument('--input-file', '-i', required=True, help='Path to the input file.')
    parser.add_argument('--output-file', '-o', required=True, help='Path to the output file.')
    parser.add_argument('--input-format', '-if', required=True, choices=FORMAT_HANDLERS.keys(), help='Format of the input file.')
    parser.add_argument('--output-format', '-of', required=True, choices=FORMAT_HANDLERS.keys(), help='Format for the output file.')

    args = parser.parse_args()

    try:
        convert_data(args.input_file, args.output_file, args.input_format, args.output_format)
        print(f"Successfully converted '{args.input_file}' ({args.input_format}) to '{args.output_file}' ({args.output_format}).")
    except (FileNotFoundError, ValueError, IOError, ImportError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
