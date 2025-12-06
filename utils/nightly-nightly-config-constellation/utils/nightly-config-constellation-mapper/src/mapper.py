import os
import yaml
import json
import argparse
from collections import defaultdict

def map_config_constellation(directory: str, extension: str) -> dict:
    """
    Scans a directory for configuration files of a given extension,
    parses them, and maps all unique top-level keys to the files they appear in.

    Args:
        directory (str): The root directory to scan.
        extension (str): The file extension to look for (e.g., '.yaml', '.json').
                         Note: '.yaml' will also match '.yml' files.

    Returns:
        dict: A dictionary where keys are top-level config keys and values are
              lists of file paths where those keys were found.
    """
    key_occurrences = defaultdict(set)
    target_extensions = {extension.lower()}
    if extension.lower() == '.yaml':
        target_extensions.add('.yml')

    for root, _, files in os.walk(directory):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in target_extensions):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    config_data = None
                    if extension.lower() in ('.yaml', '.yml'):
                        config_data = yaml.safe_load(content)
                    elif extension.lower() == '.json':
                        config_data = json.loads(content)
                    # Add more parsers here for other extensions if needed

                    if isinstance(config_data, dict):
                        for key in config_data.keys():
                            key_occurrences[key].add(filepath)
                except (yaml.YAMLError, json.JSONDecodeError) as e:
                    print(f"Warning: Could not parse {filepath} (invalid {extension} format): {e}")
                except Exception as e:
                    print(f"Warning: An unexpected error occurred while processing {filepath}: {e}")

    # Convert sets to sorted lists for consistent output
    return {key: sorted(list(paths)) for key, paths in key_occurrences.items()}

def main():
    parser = argparse.ArgumentParser(
        description="Map top-level keys across configuration files in a directory."
    )
    parser.add_argument(
        "--directory",
        required=True,
        help="The root directory to start scanning for configuration files."
    )
    parser.add_argument(
        "--extension",
        required=True,
        help="The file extension of the configuration files to map (e.g., .yaml, .json)."
    )

    args = parser.parse_args()

    print(f"\nConfig Constellation Map for '{args.extension}' files in '{args.directory}':\n")
    constellation_map = map_config_constellation(args.directory, args.extension)

    if not constellation_map:
        print("No configuration files found or no top-level keys extracted.")
        return

    for key, paths in sorted(constellation_map.items()):
        print(f"- {key}:")
        for path in paths:
            print(f"  - {path}")
    print("\n")

if __name__ == "__main__":
    main()
