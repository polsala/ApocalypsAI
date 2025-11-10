import os
import time
import argparse
import datetime

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (24 * 3600)
    except OSError:
        return float('inf') # File not found or inaccessible

def is_directory_empty(path):
    """Checks if a directory is empty (contains no files or subdirectories)."""
    try:
        return not any(os.listdir(path))
    except OSError:
        return False # Directory not found or inaccessible

def sweep_dust_bunnies(target_path, age_days, dry_run=True, verbose=False):
    """Scans a directory for old files and empty directories, optionally removing them.

    Args:
        target_path (str): The root directory to scan.
        age_days (int): Files older than this many days are considered for removal.
        dry_run (bool): If True, only report actions, don't perform them.
        verbose (bool): If True, print detailed information during scanning.

    Returns:
        dict: A report containing 'found_files', 'removed_files', 'found_empty_dirs', 'removed_empty_dirs'.
    """
    if not os.path.isdir(target_path):
        print(f"Error: Target path '{target_path}' is not a valid directory.")
        return {
            'found_files': 0, 'removed_files': 0,
            'found_empty_dirs': 0, 'removed_empty_dirs': 0
        }

    found_files = []
    removed_files = []
    found_empty_dirs = []
    removed_empty_dirs = []

    # First pass: find old files and mark directories that become empty
    for root, dirs, files in os.walk(target_path, topdown=False):
        for file in files:
            filepath = os.path.join(root, file)
            age = get_file_age_days(filepath)
            if age > age_days:
                found_files.append(filepath)
                if verbose:
                    print(f"Found old file: {filepath} (age: {age:.1f} days)")
                if not dry_run:
                    try:
                        os.remove(filepath)
                        removed_files.append(filepath)
                        if verbose:
                            print(f"  Removed: {filepath}")
                    except OSError as e:
                        print(f"  Error removing {filepath}: {e}")

    # Second pass: find empty directories (after potential file removals)
    # We walk topdown=False again to ensure we catch directories that became empty
    # due to file removals in the first pass, and to remove deepest first.
    for root, dirs, files in os.walk(target_path, topdown=False):
        # Check if the current directory is empty *after* processing its contents
        # This is crucial for `topdown=False` to work correctly for empty dirs.
        if is_directory_empty(root) and root != target_path: # Don't remove the target_path itself
            found_empty_dirs.append(root)
            if verbose:
                print(f"Found empty directory: {root}")
            if not dry_run:
                try:
                    os.rmdir(root)
                    removed_empty_dirs.append(root)
                    if verbose:
                        print(f"  Removed empty directory: {root}")
                except OSError as e:
                    print(f"  Error removing empty directory {root}: {e}")

    report = {
        'found_files': len(found_files),
        'removed_files': len(removed_files),
        'found_empty_dirs': len(found_empty_dirs),
        'removed_empty_dirs': len(removed_empty_dirs)
    }

    action_word = "would be" if dry_run else "were"
    print(f"\n--- Cosmic Dust Bunny Sweeper Report ({'Dry Run' if dry_run else 'Actual Run'}) ---")
    print(f"Scanned: {target_path}")
    print(f"Age threshold: {age_days} days")
    print(f"Found {report['found_files']} old files, {action_word} {report['removed_files']} removed.")
    print(f"Found {report['found_empty_dirs']} empty directories, {action_word} {report['removed_empty_dirs']} removed.")
    print("--------------------------------------------------")

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sweep away cosmic dust bunnies (old files and empty directories)."
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
        default=30,
        help="Files older than this many days will be considered for removal."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only report what would be removed, without deleting anything."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about each file/directory found."
    )

    args = parser.parse_args()

    sweep_dust_bunnies(args.path, args.age_days, args.dry_run, args.verbose)
