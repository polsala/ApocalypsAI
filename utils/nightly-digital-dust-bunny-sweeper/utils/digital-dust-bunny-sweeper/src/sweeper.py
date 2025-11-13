import os
import time
import argparse
from datetime import datetime, timedelta

def find_empty_directories(path):
    """Finds all empty directories within the given path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        # If no subdirectories and no files, it's empty
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(path, age_threshold_days):
    """Finds files older than the specified age threshold in days."""
    old_files = []
    current_time = time.time()
    threshold_timestamp = current_time - (age_threshold_days * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Check if it's a file (not a symlink to a dir, etc.)
                if os.path.isfile(filepath):
                    mod_time = os.path.getmtime(filepath)
                    if mod_time < threshold_timestamp:
                        old_files.append((filepath, datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')))
            except OSError as e:
                # Handle cases where file might be inaccessible or removed during scan
                print(f"Warning: Could not access {filepath} - {e}")
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: find empty directories and old files."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--age-threshold",
        type=int,
        default=90,
        help="Files older than this many days will be reported as ancient. Default is 90 days."
    )

    args = parser.parse_args()
    scan_path = args.path
    age_threshold = args.age_threshold

    if not os.path.isdir(scan_path):
        print(f"Error: The path '{scan_path}' does not exist or is not a directory.")
        exit(1)

    print(f"Scanning {scan_path} for digital dust bunnies...")

    empty_dirs = find_empty_directories(scan_path)
    old_files = find_old_files(scan_path, age_threshold)

    print("\n--- Empty Directories Found ---")
    if empty_dirs:
        for d in empty_dirs:
            print(f"🧹 {d}/")
    else:
        print("No empty directories found. Good job!")

    print(f"\n--- Ancient Files Found (older than {age_threshold} days) ---")
    if old_files:
        for f, mod_date in old_files:
            print(f"⏳ {f} (Last modified: {mod_date})")
    else:
        print("No ancient files found. Your files are spry!")

    print("\n--- Sweeping Complete! ---")
    if not empty_dirs and not old_files:
        print("Your workspace is sparkling clean! No digital dust bunnies found.")
    else:
        print("Time to consider some tidying up! (Remember, I only report, I don't delete!)")

if __name__ == "__main__":
    main()
