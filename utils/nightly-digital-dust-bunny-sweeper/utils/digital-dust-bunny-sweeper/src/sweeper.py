import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mtime)
        now = datetime.now()
        return (now - mod_datetime).days
    except (FileNotFoundError, OSError):
        return -1 # Indicate error or non-existent file

def find_dust_bunnies(root_path, age_threshold_days=365):
    """
    Scans a directory for empty files, empty directories, and old files.

    Args:
        root_path (str): The path to the directory to scan.
        age_threshold_days (int): Files older than this many days are considered "old".

    Returns:
        dict: A dictionary containing lists of 'old_files', 'empty_files', 'empty_dirs'.
    """
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return None

    old_files = []
    empty_files = []
    empty_dirs = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check for empty files and old files
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(filepath): # Ensure it's a file, not a broken symlink or something else
                    if os.path.getsize(filepath) == 0:
                        empty_files.append(filepath)
                    else:
                        age = get_file_age_in_days(filepath)
                        if age >= age_threshold_days:
                            old_files.append((filepath, datetime.fromtimestamp(os.path.getmtime(filepath))))
            except (FileNotFoundError, OSError):
                # File might have been deleted during walk, or permissions issue
                continue

        # Check for empty directories
        # A directory is considered empty if it contains no files and no subdirectories.
        # We use os.listdir to be robust, as os.walk's dirnames/filenames reflect what it *found*,
        # not necessarily the current state if other processes modify the directory.
        # Also, exclude the root_path itself from being flagged as an empty directory.
        if dirpath != root_path:
            try:
                if not os.listdir(dirpath):
                    empty_dirs.append(dirpath)
            except (FileNotFoundError, OSError):
                continue


    # Sort old files by modification date for better readability
    old_files.sort(key=lambda x: x[1])
    old_files_paths_with_dates = [(f[0], f[1].strftime("%Y-%m-%d %H:%M:%S")) for f in old_files]

    return {
        "old_files": old_files_paths_with_dates,
        "empty_files": empty_files,
        "empty_dirs": empty_dirs,
    }

def print_report(results, root_path, age_threshold_days):
    """Prints a formatted report of the dust bunnies found."""
    if results is None:
        return

    print("\n🧹 Digital Dust Bunny Sweeper Report 🧹")
    print(f"\nScanning: {root_path}")
    print(f"Files older than {age_threshold_days} days:")
    if results["old_files"]:
        for filepath, mod_date_str in results["old_files"]:
            print(f"  - {filepath} (Modified: {mod_date_str})")
    else:
        print("  None found. Your files are spry!")

    print("\nEmpty Files:")
    if results["empty_files"]:
        for filepath in results["empty_files"]:
            print(f"  - {filepath}")
    else:
        print("  None found. No phantom files here!")

    print("\nEmpty Directories:")
    if results["empty_dirs"]:
        for dirpath in results["empty_dirs"]:
            print(f"  - {dirpath}/")
    else:
        print("  None found. Your directories are bustling!")

    print("\nSummary:")
    print(f"  - Total old files found: {len(results['old_files'])}")
    print(f"  - Total empty files found: {len(results['empty_files'])}")
    print(f"  - Total empty directories found: {len(results['empty_dirs'])}")
    print("\nConsider sweeping these digital dust bunnies away!")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Find old, empty files and directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=365,
        help="Files older than this many days will be flagged as 'ancient'. Default is 365."
    )

    args = parser.parse_args()

    results = find_dust_bunnies(args.path, args.age_days)
    print_report(results, args.path, args.age_days)

if __name__ == "__main__":
    main()
