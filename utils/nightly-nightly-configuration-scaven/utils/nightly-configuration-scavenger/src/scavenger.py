import argparse
import configparser
import json
import os
import sys
import yaml

def parse_ini(content: str) -> dict:
    """Parses INI content from a string."""
    config = configparser.ConfigParser()
    # configparser expects a file-like object or a list of lines
    # We can use io.StringIO to simulate a file
    import io
    config.read_string(content)
    parsed_data = {section: dict(config[section]) for section in config.sections()}
    return parsed_data

def parse_json(content: str) -> dict:
    """Parses JSON content from a string."""
    return json.loads(content)

def parse_yaml(content: str) -> dict:
    """Parses YAML content from a string."""
    return yaml.safe_load(content)

def scavenge_configs(directory: str, extensions: list[str]) -> dict:
    """
    Scavenges a directory for configuration files of specified extensions,
    parses them, and returns a dictionary of results.
    """
    results = {}
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, ext = os.path.splitext(file_name)
            ext = ext.lstrip('.') # Remove leading dot

            if ext in extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    parsed_content = None
                    if ext == 'ini':
                        parsed_content = parse_ini(content)
                    elif ext == 'json':
                        parsed_content = parse_json(content)
                    elif ext == 'yaml' or ext == 'yml': # Handle both .yaml and .yml
                        parsed_content = parse_yaml(content)
                    
                    results[file_path] = parsed_content
                except Exception as e:
                    results[file_path] = {"error": f"{type(e).__name__}: {e}"}
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Scavenge directories for configuration files and parse them."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start scavenging for configuration files."
    )
    parser.add_argument(
        "--extensions",
        nargs='+',
        default=['ini', 'json', 'yaml', 'yml'],
        help="A space-separated list of file extensions to look for (e.g., ini yaml json)."
    )
    parser.add_argument(
        "--output",
        help="Path to save the JSON output. If not provided, prints to stdout."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'", file=sys.stderr)
        sys.exit(1)

    scavenged_data = scavenge_configs(args.path, args.extensions)

    output_json = json.dumps(scavenged_data, indent=2)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"Scavenged data saved to '{args.output}'")
        except IOError as e:
            print(f"Error writing to output file '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_json)

if __name__ == "__main__":
    main()
