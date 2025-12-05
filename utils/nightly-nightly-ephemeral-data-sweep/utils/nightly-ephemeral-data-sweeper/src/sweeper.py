import os
import yaml
import argparse
import datetime
import fnmatch
import time

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    mod_time = os.path.getmtime(filepath)
    mod_datetime = datetime.datetime.fromtimestamp(mod_time)
    now = datetime.datetime.now()
    return (now - mod_datetime).days

def sweep_ephemeral_data(config_path, dry_run=True):
    """Sweeps ephemeral data based on the provided configuration.

    Args:
        config_path (str): Path to the YAML configuration file.
        dry_run (bool): If True, only reports files to be removed, does not delete.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        return

    ephemeral_paths = config.get('ephemeral_paths', [])
    if not ephemeral_paths:
        print("No ephemeral paths defined in the configuration.")
        return

    print(f"{'DRY RUN: ' if dry_run else ''}Starting Ephemeral Data Sweep...")
    total_files_processed = 0
    total_files_removed = 0
    total_space_freed = 0

    for entry in ephemeral_paths:
        path = entry.get('path')
        max_age_days = entry.get('max_age_days')
        patterns = entry.get('patterns', ['*']) # Default to all files

        if not path or max_age_days is None:
            print(f"Warning: Skipping entry due to missing 'path' or 'max_age_days': {entry}")
            continue

        if not os.path.exists(path):
            print(f"Info: Path '{path}' does not exist. Skipping.")
            continue

        print(f"\nScanning '{path}' for files older than {max_age_days} days with patterns {patterns}...")

        for root, _, files in os.walk(path):
            for filename in files:
                total_files_processed += 1
                filepath = os.path.join(root, filename)

                # Check if file matches any pattern
                if not any(fnmatch.fnmatch(filename, p) for p in patterns):
                    continue

                try:
                    file_age = get_file_age_days(filepath)
                    if file_age > max_age_days:
                        file_size = os.path.getsize(filepath)
                        print(f"  - {'[DRY RUN] ' if dry_run else ''}Found old file: {filepath} (Age: {file_age} days, Size: {file_size / (1024*1024):.2f} MB)")
                        if not dry_run:
                            os.remove(filepath)
                            total_files_removed += 1
                            total_space_freed += file_size
                except OSError as e:
                    print(f"  - Error processing file {filepath}: {e}")

    print("\nSweep complete.")
    print(f"Total files processed: {total_files_processed}")
    print(f"Total files {'would be ' if dry_run else ''}removed: {total_files_removed}")
    print(f"Total space {'would be ' if dry_run else ''}freed: {total_space_freed / (1024*1024):.2f} MB")

def main():
    parser = argparse.ArgumentParser(description="Sweep ephemeral data based on configuration.")
    parser.add_argument('--config', required=True, help='Path to the YAML configuration file.')
    parser.add_argument('--dry-run', action='store_true', help='Only report files, do not delete them.')
    args = parser.parse_args()

    sweep_ephemeral_data(args.config, args.dry_run)

if __name__ == '__main__':
    main()
