import os
import argparse
import datetime
import sys

def get_file_age_in_days(filepath):
    """Returns the age of a file in days based on its modification time."""
    try:
        mtime = os.path.getmtime(filepath)
        return (datetime.datetime.now() - datetime.datetime.fromtimestamp(mtime)).days
    except OSError:
        return -1 # Indicate error or file not found

def is_directory_empty(path):
    """Checks if a directory is truly empty (contains no files or subdirectories)."""
    try:
        return not bool(os.listdir(path))
    except OSError:
        return False # Directory might not exist or permissions issue

def find_dust_bunnies(root_path, age_days, extensions, delete_empty_dirs, dry_run, verbose):
    """Scans the file system for digital dust bunnies (empty dirs, old files)."""
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.", file=sys.stderr)
        return

    print(f"Scanning '{root_path}' for digital dust bunnies... (Dry Run: {dry_run})\n")

    empty_dirs_found = []
    old_files_found = []

    # Convert extensions to a set for faster lookup
    target_extensions = {ext.lower() for ext in extensions}

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Find old files
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1].lower()

            if target_extensions and file_ext not in target_extensions:
                continue # Skip if extensions are specified and don't match

            age = get_file_age_in_days(filepath)
            if age >= age_days:
                old_files_found.append((filepath, age))

        # Find empty directories (only if not already marked for deletion by parent walk)
        # topdown=False ensures we process children before parents
        if delete_empty_dirs and is_directory_empty(dirpath):
            # Ensure it's not the root path itself unless it's truly empty and not the starting point
            if dirpath != root_path or is_directory_empty(dirpath):
                empty_dirs_found.append(dirpath)

    # Report and optionally delete old files
    if old_files_found:
        print(f"--- Old Files (older than {age_days} days) ---")
        for filepath, age in old_files_found:
            print(f"  [FILE] {filepath} (Age: {age} days)")
            if not dry_run:
                try:
                    os.remove(filepath)
                    if verbose: print(f"    Deleted: {filepath}")
                except OSError as e:
                    print(f"    Error deleting {filepath}: {e}", file=sys.stderr)
    else:
        print(f"No old files found older than {age_days} days.")

    print("\n")

    # Report and optionally delete empty directories
    if empty_dirs_found:
        print("--- Empty Directories ---")
        # Sort from deepest to shallowest to avoid issues with parent deletion
        empty_dirs_found.sort(key=lambda p: p.count(os.sep), reverse=True)
        for dirpath in empty_dirs_found:
            print(f"  [DIR] {dirpath}")
            if not dry_run:
                try:
                    os.rmdir(dirpath)
                    if verbose: print(f"    Deleted: {dirpath}")
                except OSError as e:
                    print(f"    Error deleting {dirpath}: {e}", file=sys.stderr)
    else:
        print("No empty directories found.")

    print("\nScan complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Clean up empty directories and old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered for deletion. (Default: 30)"
    )
    parser.add_argument(
        "--extensions",
        nargs='*', # 0 or more arguments
        default=[],
        help="Space-separated list of file extensions to target (e.g., .log .tmp). If not provided, all files older than age-days will be considered."
    )
    parser.add_argument(
        "--delete-empty-dirs",
        action='store_true',
        help="If present, empty directories found will be deleted. (Use with --dry-run first!)"
    )
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="If present, the script will only list what *would* be deleted, without making any changes."
    )
    parser.add_argument(
        "--verbose",
        action='store_true',
        help="Print more detailed information during the scan."
    )

    args = parser.parse_args()

    find_dust_bunnies(
        args.path,
        args.age_days,
        args.extensions,
        args.delete_empty_dirs,
        args.dry_run,
        args.verbose
    )

if __name__ == "__main__":
    main()
