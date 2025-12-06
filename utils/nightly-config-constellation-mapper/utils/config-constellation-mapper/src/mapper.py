import os
import json
import yaml
import configparser
import argparse
from collections import defaultdict

def parse_yaml(content):
    """Parses YAML content."""
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError:
        return None

def parse_json(content):
    """Parses JSON content."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None

def parse_ini(content):
    """Parses INI content."""
    config = configparser.ConfigParser()
    try:
        # configparser expects a file-like object or list of lines
        config.read_string(content)
        # Convert to a dictionary for consistency
        ini_dict = {section: dict(config.items(section)) for section in config.sections()}
        return ini_dict
    except configparser.Error:
        return None

def flatten_dict(d, parent_key='', sep='.'):
    """Flattens a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def scan_and_map_configs(directory, supported_formats=None):
    """
    Scans a directory for configuration files and maps their contents.
    Returns a dictionary of {filename: flattened_config_dict}.
    """
    if supported_formats is None:
        supported_formats = ['yaml', 'json', 'ini']

    config_parsers = {
        'yaml': parse_yaml,
        'yml': parse_yaml, # Also support .yml
        'json': parse_json,
        'ini': parse_ini,
    }

    all_configs = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            name, ext = os.path.splitext(filename)
            ext = ext[1:].lower() # Remove dot and make lowercase

            if ext in supported_formats and ext in config_parsers:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    parsed_content = config_parsers[ext](content)
                    if parsed_content:
                        all_configs[filename] = flatten_dict(parsed_content)
                except Exception as e:
                    print(f"Warning: Could not process {file_path}: {e}")
                    continue
    return all_configs

def analyze_configs(all_configs):
    """
    Analyzes the mapped configurations for commonalities, differences, and missing keys.
    """
    analysis = {
        "shared_keys": defaultdict(lambda: defaultdict(list)),
        "inconsistent_values": [],
        "missing_keys": []
    }

    all_keys = set()
    for config_name, flat_config in all_configs.items():
        all_keys.update(flat_config.keys())

    # Analyze shared and inconsistent values
    for key in all_keys:
        values_for_key = defaultdict(list)
        for config_name, flat_config in all_configs.items():
            if key in flat_config:
                value = flat_config[key]
                values_for_key[str(value)].append(config_name) # Convert value to string for dict key

        if len(values_for_key) > 1: # Key exists with different values
            analysis["inconsistent_values"].append({
                "key": key,
                "values": dict(values_for_key)
            })
        elif len(values_for_key) == 1: # Key exists with same value across files it's present in
            first_value = next(iter(values_for_key))
            analysis["shared_keys"][key][first_value].extend(values_for_key[first_value])

    # Analyze missing keys
    for key in all_keys:
        present_in = []
        absent_from = []
        for config_name, flat_config in all_configs.items():
            if key in flat_config:
                present_in.append(config_name)
            else:
                absent_from.append(config_name)
        
        if absent_from: # If key is missing from at least one config
            analysis["missing_keys"].append({
                "key": key,
                "present_in": present_in,
                "absent_from": absent_from
            })

    return analysis

def main():
    parser = argparse.ArgumentParser(
        description="🌌 Config Constellation Mapper: Scans and analyzes configuration files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to scan for configuration files."
    )
    parser.add_argument(
        "--output",
        help="The filename to save the JSON report. If not provided, prints to stdout."
    )
    parser.add_argument(
        "--formats",
        default="yaml,json,ini",
        help="Comma-separated list of formats to include (e.g., 'yaml,json'). Defaults to all supported."
    )

    args = parser.parse_args()

    supported_formats = [f.strip().lower() for f in args.formats.split(',')]

    print(f"Scanning directory: {args.path}")
    all_configs_flat = scan_and_map_configs(args.path, supported_formats)

    if not all_configs_flat:
        print("No supported configuration files found or parsed successfully.")
        return

    full_configs_original = {}
    for root, _, files in os.walk(args.path):
        for filename in files:
            file_path = os.path.join(root, filename)
            name, ext = os.path.splitext(filename)
            ext = ext[1:].lower()
            if ext in supported_formats:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if ext in ['yaml', 'yml']:
                        parsed = parse_yaml(content)
                    elif ext == 'json':
                        parsed = parse_json(content)
                    elif ext == 'ini':
                        parsed = parse_ini(content)
                    else:
                        parsed = None
                    if parsed:
                        full_configs_original[filename] = parsed
                except Exception:
                    pass # Already warned in scan_and_map_configs

    analysis_results = analyze_configs(all_configs_flat)

    all_unique_keys_across_all_configs = set()
    for config_name, flat_config in all_configs_flat.items():
        all_unique_keys_across_all_configs.update(flat_config.keys())

    report = {
        "summary": {
            "total_files_scanned": len(all_configs_flat),
            "unique_keys_found": len(all_unique_keys_across_all_configs),
            "inconsistencies_detected": len(analysis_results["inconsistent_values"]) + len(analysis_results["missing_keys"])
        },
        "configurations": full_configs_original,
        "analysis": analysis_results
    }

    json_report = json.dumps(report, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_report)
        print(f"Cosmic Configuration Report saved to {args.output}")
    else:
        print("\n--- Cosmic Configuration Report ---")
        print(json_report)
        print("---------------------------------")

if __name__ == "__main__":
    main()
