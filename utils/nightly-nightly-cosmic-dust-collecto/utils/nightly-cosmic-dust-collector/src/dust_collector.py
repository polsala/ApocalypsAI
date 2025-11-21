import os
import time
import argparse
import fnmatch
import shutil
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def collect_dust(
    path: str,
    age_days: int = 30,
    patterns: list[str] = None,
    action: str = "list"
):
    """Collects 'dust' (old files) based on age and patterns, then performs an action.

    Args:
        path (str): The root directory to scan.
        age_days (int): Files older than this many days are considered dust.
        patterns (list[str]): Glob patterns to match file names.
        action (str): 'list', 'delete', or 'archive'.
    """
    if patterns is None:
        patterns = ['*.log', '*.tmp', '*.bak', '*.swp', '*~']

    if not os.path.isdir(path):
        print(f"Error: Directory not found: {path}")
        return

    dust_files = []
    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if any(fnmatch.fnmatch(filename, p) for p in patterns):
                file_age = get_file_age_days(filepath)
                if file_age > age_days:
                    dust_files.append(filepath)

    if not dust_files:
        print(f"No cosmic dust found in '{path}' older than {age_days} days matching patterns {patterns}.")
        return

    print(f"Found {len(dust_files)} cosmic dust files in '{path}' older than {age_days} days matching patterns {patterns}.")

    if action == "list":
        for f in dust_files:
            print(f"  - {f}")
    elif action == "delete":
        print("Initiating cosmic dust deletion...")
        for f in dust_files:
            try:
                os.remove(f)
                print(f"  Deleted: {f}")
            except OSError as e:
                print(f"  Error deleting {f}: {e}")
    elif action == "archive":
        print("Initiating cosmic dust archiving...")
        archive_dir = os.path.join(path, ".dust_archive")
        os.makedirs(archive_dir, exist_ok=True)
        for f in dust_files:
            try:
                # Ensure unique name in archive to prevent overwrites
                base_name = os.path.basename(f)
                dest_path = os.path.join(archive_dir, base_name)
                counter = 1
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(base_name)
                    dest_path = os.path.join(archive_dir, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.move(f, dest_path)
                print(f"  Archived: {f} -> {dest_path}")
            except OSError as e:
                print(f"  Error archiving {f}: {e}")
    else:
        print(f"Error: Unknown action '{action}'. Valid actions are 'list', 'delete', 'archive'.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans up old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered 'dust'. Default is 30."
    )
    parser.add_argument(
        "--patterns",
        nargs='+',
        default=['*.log', '*.tmp', '*.bak', '*.swp', '*~'],
        help="One or more glob patterns to match file names (e.g., '*.log', 'temp_*')."
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=['list', 'delete', 'archive'],
        default='list',
        help="The action to perform: 'list', 'delete', or 'archive'. Default is 'list'."
    )

    args = parser.parse_args()
    collect_dust(args.path, args.age_days, args.patterns, args.action)

if __name__ == "__main__":
    main()
