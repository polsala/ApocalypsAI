import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def find_dust_bunnies(path, old_days=30):
    """Scans the given path for empty directories, old log files, and temporary files.
    Returns a tuple: (empty_dirs, old_logs, temp_files)
    """
    empty_dirs = []
    old_logs = []
    temp_files = []

    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return [], [], []

    print(f"\nScanning '{path}' for digital dust bunnies (logs older than {old_days} days)...\n")

    # Walk directories from bottom-up to correctly identify empty directories
    for root, dirs, files in os.walk(path, topdown=False):
        # Check for empty directories
        # A directory is empty if it has no files and no subdirectories (that haven't been removed yet)
        if not dirs and not files:
            empty_dirs.append(root)

        for file in files:
            filepath = os.path.join(root, file)
            # Check for old log files
            if file.lower().endswith('.log'):
                if get_file_age_days(filepath) > old_days:
                    old_logs.append(filepath)
            # Check for temporary files
            elif file.lower().endswith('.tmp') or file.lower().startswith('tmp_'):
                temp_files.append(filepath)

    return empty_dirs, old_logs, temp_files

def delete_items(items, item_type):
    """Prompts user for confirmation and deletes a list of items."""
    if not items:
        return

    print(f"\n--- Identified {item_type} ---")
    for item in items:
        print(f"  - {item}")

    confirm = input(f"\nDo you want to delete these {item_type}? (y/N): ").lower()
    if confirm == 'y':
        for item in items:
            try:
                if os.path.isdir(item):
                    os.rmdir(item)
                    print(f"Deleted empty directory: {item}")
                else:
                    os.remove(item)
                    print(f"Deleted file: {item}")
            except OSError as e:
                print(f"Error deleting {item}: {e}")
    else:
        print(f"Skipping deletion of {item_type}.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep for digital dust bunnies (empty dirs, old logs, temp files)."
    )
    parser.add_argument("path", help="The root directory to scan.")
    parser.add_argument("--days", type=int, default=30,
                        help="Number of days after which log files are considered 'old'. Default is 30.")
    parser.add_argument("--delete", action="store_true",
                        help="If present, the utility will prompt for confirmation before deleting identified items.")

    args = parser.parse_args()

    empty_dirs, old_logs, temp_files = find_dust_bunnies(args.path, args.days)

    total_found = len(empty_dirs) + len(old_logs) + len(temp_files)

    if total_found == 0:
        print("\n✨ All clear! No digital dust bunnies found. Your system is sparkling! ✨")
        return

    print("\n--- Digital Dust Bunny Report ---")
    if empty_dirs:
        print(f"Found {len(empty_dirs)} empty directories.")
    if old_logs:
        print(f"Found {len(old_logs)} old log files.")
    if temp_files:
        print(f"Found {len(temp_files)} temporary files.")

    if args.delete:
        delete_items(empty_dirs, "empty directories")
        delete_items(old_logs, "old log files")
        delete_items(temp_files, "temporary files")
    else:
        print("\nRun with '--delete' to interactively clean up these items.")

    print("\nSweep complete. May your digital realm remain pristine!")

if __name__ == "__main__":
    main()
