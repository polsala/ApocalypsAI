import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def find_old_files(root_dir, age_days):
    """Finds files older than age_days in root_dir."""
    old_files = []
    cutoff_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.getmtime(filepath) < cutoff_timestamp:
                    old_files.append(filepath)
            except OSError:
                # File might have been deleted between walk and getmtime
                continue
    return old_files

def find_empty_dirs(root_dir):
    """Finds empty directories in root_dir, bottom-up."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # If a directory contains no files and all its subdirectories (that were
        # just processed) are also empty and were removed, then it's empty.
        # os.walk(topdown=False) ensures subdirs are processed first.
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def delete_files(file_list, dry_run=True):
    """Deletes files from the list."""
    deleted_count = 0
    for filepath in file_list:
        if dry_run:
            print(f"[DRY RUN] Would delete: {filepath}")
        else:
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
    return deleted_count

def delete_empty_directories(dir_list, dry_run=True):
    """Deletes empty directories from the list."""
    deleted_count = 0
    # Sort in reverse order to delete deepest first
    dir_list.sort(key=len, reverse=True)
    for dirpath in dir_list:
        if dry_run:
            print(f"[DRY RUN] Would delete empty directory: {dirpath}")
        else:
            try:
                # Check if it's still empty before removing
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    print(f"Deleted empty directory: {dirpath}")
                    deleted_count += 1
                else:
                    print(f"Skipped non-empty directory: {dirpath}")
            except OSError as e:
                print(f"Error deleting empty directory {dirpath}: {e}")
    return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies (old files and empty directories)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered for cleanup."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["list", "delete", "list-empty-dirs", "delete-empty-dirs"],
        default="list",
        help="Operation mode: list/delete old files, or list/delete empty directories."
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required for 'delete' and 'delete-empty-dirs' modes to prevent accidental data loss."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    dry_run = not args.confirm

    if args.mode in ["list", "delete"]:
        if args.mode == "delete" and not args.confirm:
            print("Error: '--confirm' is required for 'delete' mode.")
            exit(1)

        print(f"Scanning '{args.path}' for files older than {args.age} days...")
        old_files = find_old_files(args.path, args.age)

        if old_files:
            print(f"Found {len(old_files)} old files:")
            for f in old_files:
                print(f"- {f}")
            if args.mode == "delete":
                print("\nInitiating deletion...")
                deleted_count = delete_files(old_files, dry_run=dry_run)
                print(f"\nOperation complete. {deleted_count} files {'would be' if dry_run else 'were'} deleted.")
        else:
            print("No old files found.")

    elif args.mode in ["list-empty-dirs", "delete-empty-dirs"]:
        if args.mode == "delete-empty-dirs" and not args.confirm:
            print("Error: '--confirm' is required for 'delete-empty-dirs' mode.")
            exit(1)

        print(f"Scanning '{args.path}' for empty directories...")
        empty_dirs = find_empty_dirs(args.path)

        if empty_dirs:
            print(f"Found {len(empty_dirs)} empty directories:")
            for d in empty_dirs:
                print(f"- {d}")
            if args.mode == "delete-empty-dirs":
                print("\nInitiating deletion of empty directories...")
                deleted_count = delete_empty_directories(empty_dirs, dry_run=dry_run)
                print(f"\nOperation complete. {deleted_count} empty directories {'would be' if dry_run else 'were'} deleted.")
        else:
            print("No empty directories found.")

if __name__ == "__main__":
    main()
