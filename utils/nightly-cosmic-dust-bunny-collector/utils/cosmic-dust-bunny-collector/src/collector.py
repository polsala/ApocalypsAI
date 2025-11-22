import os
import shutil
import argparse
import time
from datetime import datetime, timedelta

def find_empty_dirs(root_path):
    """Finds all empty directories within a given root path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the directory itself is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    # Sort by length descending to ensure inner empty dirs are processed first
    # This is crucial for deletion, as a parent directory cannot be deleted if its child
    # is still present. For listing, it provides a logical order.
    return sorted(empty_dirs, key=len, reverse=True)

def find_old_files(root_path, days_old):
    """Finds files older than a specified number of days within a given root path."""
    old_files = []
    if days_old <= 0:
        return old_files

    # Calculate the cutoff time based on current time minus days_old
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Use os.path.getmtime for last modification time, which is generally
                # more reliable and relevant for 'old' files than access time (atime).
                if os.path.getmtime(filepath) < cutoff_time:
                    old_files.append(filepath)
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")
    return old_files

def clean_up(items, dry_run, item_type="item"):
    """Deletes a list of files or directories, with a dry-run option."""
    if not items:
        print(f"No {item_type}s found to clean up.")
        return

    print(f"\n--- {item_type.capitalize()}s to be processed ({'Dry Run' if dry_run else 'Actual Deletion'}) ---")
    for item in items:
        if dry_run:
            print(f"[DRY RUN] Would remove: {item}")
        else:
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item) # Remove directory and its contents recursively
                    print(f"Removed directory: {item}")
                else:
                    os.remove(item) # Remove file
                    print(f"Removed file: {item}")
            except OSError as e:
                print(f"Error removing {item_type} {item}: {e}")
    if not dry_run:
        print(f"--- Finished {item_type} cleanup ---")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Sweeps away empty directories and old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory from which to start scanning."
    )
    parser.add_argument(
        "--days-old",
        type=int,
        default=0,
        help="Find files older than this many days (based on modification time). Set to 0 to disable."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only list items to be removed, do not actually delete them."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{args.path}' for dust bunnies...")

    # Find and process empty directories
    empty_dirs = find_empty_dirs(args.path)
    if empty_dirs:
        print(f"Found {len(empty_dirs)} empty director{'y' if len(empty_dirs) == 1 else 'ies'}.")
        clean_up(empty_dirs, args.dry_run, item_type="empty directory")
    else:
        print("No empty directories found.")

    # Find and process old files
    if args.days_old > 0:
        old_files = find_old_files(args.path, args.days_old)
        if old_files:
            print(f"Found {len(old_files)} file{'s' if len(old_files) != 1 else ''} older than {args.days_old} days.")
            clean_up(old_files, args.dry_run, item_type="old file")
        else:
            print(f"No files found older than {args.days_old} days.")
    else:
        print("Skipping old file scan (days-old not specified or 0).")

    print("\nCosmic Dust Bunny Collector finished its sweep!")

if __name__ == "__main__":
    main()
