import os
import time
import fnmatch
import shutil
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except FileNotFoundError:
        return -1 # Indicate file not found, so it won't be processed

def sweep_directory(target_dirs, patterns, age_days, dry_run=True, verbose=False):
    """
    Scans specified directories for files matching patterns and older than age_days.
    Optionally deletes them.

    Args:
        target_dirs (list): List of directories to scan.
        patterns (list): List of glob-style patterns (e.g., ['*.tmp', '__pycache__']).
        age_days (int): Minimum age in days for a file to be considered for deletion.
        dry_run (bool): If True, only report files; do not delete.
        verbose (bool): If True, print detailed actions.

    Returns:
        dict: A dictionary containing 'deleted_files' (list of paths) and 'reported_files' (list of paths).
    """
    reported_files = []
    deleted_files = []

    for target_dir in target_dirs:
        if not os.path.isdir(target_dir):
            if verbose:
                print(f"Warning: Target directory '{target_dir}' does not exist or is not a directory. Skipping.")
            continue

        for root, dirnames, filenames in os.walk(target_dir):
            # Check directories first (e.g., __pycache__)
            # Iterate over a copy of dirnames to allow modification during iteration
            for dirname in list(dirnames):
                for pattern in patterns:
                    if fnmatch.fnmatch(dirname, pattern):
                        dir_path = os.path.join(root, dirname)
                        if get_file_age_days(dir_path) > age_days:
                            reported_files.append(dir_path)
                            if not dry_run:
                                try:
                                    shutil.rmtree(dir_path)
                                    deleted_files.append(dir_path)
                                    if verbose:
                                        print(f"DELETED (dir): {dir_path}")
                                    # Remove from dirnames so os.walk doesn't try to traverse it
                                    dirnames.remove(dirname)
                                except OSError as e:
                                    if verbose:
                                        print(f"Error deleting directory {dir_path}: {e}")
                            elif verbose:
                                print(f"REPORTED (dir): {dir_path}")
                        break # Matched a pattern, move to next dirname

            # Check files
            for filename in filenames:
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        filepath = os.path.join(root, filename)
                        if get_file_age_days(filepath) > age_days:
                            reported_files.append(filepath)
                            if not dry_run:
                                try:
                                    os.remove(filepath)
                                    deleted_files.append(filepath)
                                    if verbose:
                                        print(f"DELETED (file): {filepath}")
                                except OSError as e:
                                    if verbose:
                                        print(f"Error deleting file {filepath}: {e}")
                            elif verbose:
                                print(f"REPORTED (file): {filepath}")
                        break # Matched a pattern, move to next filename
    
    return {
        "reported_files": reported_files,
        "deleted_files": deleted_files
    }

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Cleans up old temporary files and directories."
    )
    parser.add_argument(
        "target_dirs",
        nargs=":", # Use ':' to allow 0 or more, but require at least one in practice for usefulness
        default=['.'], # Default to current directory if none provided
        help="One or more directories to scan for dust bunnies. Defaults to current directory if none specified."
    )
    parser.add_argument(
        "--patterns",
        nargs=":",
        default=["*.tmp", "*.log", "__pycache__", "*.bak", "*.swp", ".DS_Store", "Thumbs.db"],
        help="Glob-style patterns for files/directories to clean (e.g., '*.tmp', '__pycache__')."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=7,
        help="Minimum age in days for a file/directory to be considered for cleaning."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report files/directories that would be deleted, but do not actually delete them."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed actions during the sweep."
    )

    args = parser.parse_args()

    # Handle default for target_dirs if no explicit arguments were passed
    if not args.target_dirs:
        args.target_dirs = ['.']

    print(f"Starting sweep in {args.target_dirs} with patterns {args.patterns} for items older than {args.age} days.")
    if args.dry_run:
        print("--- DRY RUN ACTIVE --- No files will be deleted.")

    results = sweep_directory(
        args.target_dirs,
        args.patterns,
        args.age,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    print("\n--- Sweep Summary ---")
    print(f"Files/directories reported: {len(results['reported_files'])}")
    for f in results['reported_files']:
        print(f"  - {f}")

    if not args.dry_run:
        print(f"Files/directories deleted: {len(results['deleted_files'])}")
        for f in results['deleted_files']:
            print(f"  - {f}")
    else:
        print("No files were deleted (dry run).")

if __name__ == "__main__":
    main()
