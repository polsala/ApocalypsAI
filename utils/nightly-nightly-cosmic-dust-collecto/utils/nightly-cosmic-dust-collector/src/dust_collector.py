import os
import sys
import argparse
import yaml
import fnmatch
from datetime import datetime, timedelta

def load_config(config_path):
    """Loads the YAML configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        if 'rules' not in config or not isinstance(config['rules'], list):
            raise ValueError("Config file must contain a 'rules' list.")
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found at '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config file '{config_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error in config file format: {e}", file=sys.stderr)
        sys.exit(1)

def collect_dust(root_dir, config, dry_run=False):
    """Collects 'cosmic dust' (old files) based on config rules.

    Args:
        root_dir (str): The root directory to scan.
        config (dict): The loaded configuration dictionary.
        dry_run (bool): If True, only report actions, don't delete files.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{root_dir}' for cosmic dust... (Dry run: {dry_run})")
    now = datetime.now()
    files_cleaned_count = 0

    for rule in config['rules']:
        patterns = rule.get('patterns', [])
        max_age_days = rule.get('max_age_days')
        rule_name = rule.get('name', 'Unnamed Rule')

        if not patterns or max_age_days is None:
            print(f"Warning: Rule '{rule_name}' is missing 'patterns' or 'max_age_days'. Skipping.", file=sys.stderr)
            continue

        min_mtime = now - timedelta(days=max_age_days)

        print(f"\nApplying rule: '{rule_name}' (Patterns: {patterns}, Max Age: {max_age_days} days)")

        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, root_dir)

                # Check if file matches any pattern
                matches_pattern = False
                for pattern in patterns:
                    # fnmatch handles glob patterns, including directory separators for patterns like 'dist/*' or '__pycache__/*'
                    if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(filename, pattern):
                        matches_pattern = True
                        break

                if not matches_pattern:
                    continue

                # Check file age
                try:
                    mtime_timestamp = os.path.getmtime(full_path)
                    mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                    if mtime_datetime < min_mtime:
                        action = "Would remove" if dry_run else "Removing"
                        print(f"  {action}: {full_path} (Last modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                        if not dry_run:
                            os.remove(full_path)
                            files_cleaned_count += 1
                except OSError as e:
                    print(f"Warning: Could not access file '{full_path}': {e}", file=sys.stderr)

    print(f"\nCosmic dust collection complete. {'No files removed in dry run.' if dry_run else f'{files_cleaned_count} files removed.'}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans old files based on patterns and age."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start cleaning from."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to a YAML configuration file."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only report actions, don't delete files."
    )

    args = parser.parse_args()

    config = load_config(args.config)
    collect_dust(args.path, config, args.dry_run)

if __name__ == "__main__":
    main()
