import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def is_file_old(filepath, age_days):
    """Checks if a file is older than the specified number of days."""
    return get_file_age_days(filepath) > age_days

def find_old_files(path, age_days):
    """Generator that yields paths of files older than age_days."""
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) and is_file_old(filepath, age_days):
                yield filepath

def find_empty_dirs(path):
    """Generator that yields paths of empty directories, from deepest to shallowest."""
    # Walk from bottom-up to ensure subdirectories are checked first
    for root, dirs, files in os.walk(path, topdown=False):
        # A directory is considered empty if os.listdir returns an empty list.
        # This is more robust than relying solely on os.walk's 'dirs' and 'files' lists
        # which might not reflect real-time changes or hidden files.
        try:
            if not os.listdir(root):
                yield root
        except OSError: # e.g., permission denied, or directory removed by another process
            continue

def clean_up(path, age_days, dry_run, delete):
    """Orchestrates the cleanup process."""
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return

    print(f"Scanning '{path}' for temporal tears (old files and empty directories)...\n")

    # Determine actual dry_run status based on --delete flag
    # If --delete is present, it's a real run. Otherwise, it's a dry run.
    is_dry_run = not delete

    # Find and process old files
    old_files_found = list(find_old_files(path, age_days))
    if old_files_found:
        print(f"--- Old Files (older than {age_days} days) ---")
        for filepath in old_files_found:
            print(f"  - {filepath} (Age: {get_file_age_days(filepath):.1f} days)")
            if not is_dry_run:
                try:
                    os.remove(filepath)
                    print(f"    [DELETED] {filepath}")
                except OSError as e:
                    print(f"    [ERROR] Could not delete {filepath}: {e}")
        if is_dry_run:
            print(f"\n  (Run with --delete to remove these {len(old_files_found)} files.)")
    else:
        print(f"No old files found (older than {age_days} days).")

    print("\n")

    # Find and process empty directories
    empty_dirs_found = list(find_empty_dirs(path))
    if empty_dirs_found:
        print("--- Empty Directories ---")
        # Sort from deepest to shallowest to ensure subdirs are removed before parents
        empty_dirs_found.sort(key=lambda p: p.count(os.sep), reverse=True)
        for dirpath in empty_dirs_found:
            print(f"  - {dirpath}")
            if not is_dry_run:
                try:
                    os.rmdir(dirpath)
                    print(f"    [DELETED] {dirpath}")
                except OSError as e:
                    print(f"    [ERROR] Could not delete {dirpath}: {e}")
        if is_dry_run:
            print(f"\n  (Run with --delete to remove these {len(empty_dirs_found)} directories.)")
    else:
        print("No empty directories found.")

    print(f"\nCleanup complete. {'(Dry run)' if is_dry_run else ''}")

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally remove old files and empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for old files and empty directories."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered 'old'. Defaults to 30."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list files/dirs that would be deleted, do not delete anything. This is the default if --delete is not used."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Proceed with deleting identified old files and empty directories. Use with caution! This flag overrides --dry-run."
    )

    args = parser.parse_args()

    # The 'delete' flag determines if it's a real run. If --delete is present, it's not a dry run.
    # Otherwise, it's a dry run (either by default or if --dry-run was explicitly passed).
    # The 'dry_run' argument to clean_up is now redundant as 'delete' is the single source of truth.
    # We pass args.delete directly to clean_up, which then calculates its internal is_dry_run.
    clean_up(args.path, args.age, args.dry_run, args.delete)

if __name__ == "__main__":
    main()
