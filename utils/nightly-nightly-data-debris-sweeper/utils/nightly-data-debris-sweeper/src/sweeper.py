import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_modification_time(path):
    """Wrapper for os.path.getmtime to allow mocking."""
    return os.path.getmtime(path)

def remove_file(path):
    """Wrapper for os.remove to allow mocking."""
    os.remove(path)

def remove_dir(path):
    """Wrapper for os.rmdir to allow mocking."""
    os.rmdir(path)

def list_dir(path):
    """Wrapper for os.listdir to allow mocking."""
    return os.listdir(path)

def is_dir(path):
    """Wrapper for os.path.isdir to allow mocking."""
    return os.path.isdir(path)

def clean_directory(root_path: str, age_days: int, patterns: list[str], dry_run: bool):
    """
    Sweeps a directory for old files and empty directories matching patterns.

    Args:
        root_path (str): The root directory to clean.
        age_days (int): Files/dirs older than this many days will be removed.
        patterns (list[str]): List of fnmatch patterns for files to target.
                              If empty, all files older than age_days are targeted.
        dry_run (bool): If True, only report actions, don't perform them.
    """
    if not os.path.isdir(root_path):
        print(f"Error: Root path '{root_path}' is not a valid directory.")
        return

    print(f"\n--- Nightly Data Debris Sweeper Report ---")
    print(f"Targeting: {root_path}")
    print(f"Age threshold: {age_days} days")
    print(f"File patterns: {patterns if patterns else 'All files'}")
    print(f"Mode: {'Dry Run' if dry_run else 'Execute'}\n")

    cutoff_timestamp = time.time() - (age_days * 24 * 60 * 60)
    deleted_files_count = 0
    deleted_dirs_count = 0
    potential_files_to_delete = []
    potential_dirs_to_delete = []

    # First pass: identify files for deletion
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                mod_time = get_modification_time(full_path)
                if mod_time < cutoff_timestamp:
                    if not patterns or any(fnmatch.fnmatch(filename, p) for p in patterns):
                        potential_files_to_delete.append(full_path)
            except OSError as e:
                print(f"Warning: Could not access file '{full_path}': {e}")

    # Perform file deletions
    for file_path in potential_files_to_delete:
        if dry_run:
            print(f"[DRY RUN] Would delete file: {file_path}")
        else:
            try:
                remove_file(file_path)
                print(f"Deleted file: {file_path}")
                deleted_files_count += 1
            except OSError as e:
                print(f"Error deleting file '{file_path}': {e}")

    # Second pass: identify and delete empty directories (bottom-up)
    # We need to walk again, or iterate in reverse, to catch newly emptied dirs
    # os.walk yields directories from top-down, so we need to process them in reverse order
    # to ensure child directories are empty before parent directories are checked.
    all_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        all_dirs.append(dirpath)

    for dir_to_check in reversed(all_dirs):
        if dir_to_check == root_path: # Don't delete the root path itself
            continue
        try:
            # Check if directory is empty *after* potential file deletions
            if not list_dir(dir_to_check) and is_dir(dir_to_check):
                mod_time = get_modification_time(dir_to_check)
                if mod_time < cutoff_timestamp:
                    potential_dirs_to_delete.append(dir_to_check)
        except OSError as e:
            print(f"Warning: Could not access directory '{dir_to_check}': {e}")

    # Perform directory deletions
    for dir_path in potential_dirs_to_delete:
        if dry_run:
            print(f"[DRY RUN] Would delete empty directory: {dir_path}")
        else:
            try:
                remove_dir(dir_path)
                print(f"Deleted empty directory: {dir_path}")
                deleted_dirs_count += 1
            except OSError as e:
                print(f"Error deleting directory '{dir_path}': {e}")

    print(f"\n--- Summary ---")
    print(f"Files {'would be' if dry_run else ''} deleted: {deleted_files_count}")
    print(f"Empty directories {'would be' if dry_run else ''} deleted: {deleted_dirs_count}")
    print(f"Cleanup {'simulated' if dry_run else 'completed'}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Nightly Data Debris Sweeper: Clean old files and empty directories."
    )
    parser.add_argument(
        '--path', type=str, required=True,
        help='The root directory to start sweeping from.'
    )
    parser.add_argument(
        '--age', type=int, required=True,
        help='Files and empty directories older than this many days will be considered for removal.'
    )
    parser.add_argument(
        '--patterns', nargs='*', default=[],
        help='One or more file patterns (e.g., *.log, *.tmp, __pycache__). Only files matching these patterns will be considered. If no patterns are provided, all files older than --age will be considered.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='If present, the utility will only report what *would* be deleted, without making any changes.'
    )

    args = parser.parse_args()

    clean_directory(args.path, args.age, args.patterns, args.dry_run)
