import argparse
import os
import time
from datetime import datetime, timedelta
import fnmatch

def collect_cosmic_dust(directory, age_days, pattern=None, dry_run=False):
    """
    Scans a directory for files older than a specified age and optionally matching a pattern,
    then deletes them or reports them in dry-run mode.

    Args:
        directory (str): The path to the directory to scan.
        age_days (int): Files older than this many days will be considered.
        pattern (str, optional): Glob pattern to match files (e.g., '*.log').
        dry_run (bool): If True, only report files; do not delete.

    Returns:
        list: A list of files that were successfully processed (deleted or reported).
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return []

    cutoff_time = datetime.now() - timedelta(days=age_days)
    processed_files = []

    print(f"Scanning '{directory}' for files older than {age_days} days...")
    if pattern: 
        print(f"Filtering by pattern: '{pattern}'")
    print(f"Dry-run mode: {dry_run}")

    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)

            # Check pattern if provided
            if pattern and not fnmatch.fnmatch(filename, pattern):
                continue

            try:
                # Get modification time and convert to datetime object
                mod_timestamp = os.path.getmtime(full_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < cutoff_time:
                    if dry_run:
                        print(f"[DRY-RUN] Would delete: {full_path} (Last modified: {mod_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                        processed_files.append(full_path) # Add to processed in dry-run
                    else:
                        os.remove(full_path)
                        print(f"Deleted: {full_path} (Last modified: {mod_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                        processed_files.append(full_path) # Add to processed only if deletion succeeds

            except OSError as e:
                print(f"Warning: Could not access or delete '{full_path}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred with '{full_path}': {e}")

    if not processed_files:
        print("No cosmic dust found to collect.")
    elif dry_run:
        print(f"Dry-run complete. {len(processed_files)} files would have been deleted.")
    else:
        print(f"Collection complete. {len(processed_files)} files deleted.")

    return processed_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Clean up old files from directories."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be considered for deletion."
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=None,
        help="(Optional) Glob pattern to match files (e.g., '*.log', 'temp_*')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only report which files would be deleted, without actually deleting them."
    )

    args = parser.parse_args()

    collect_cosmic_dust(
        args.directory,
        args.age,
        args.pattern,
        args.dry_run
    )
