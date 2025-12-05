import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def is_empty_dir(path):
    """Checks if a directory is empty (contains no files or subdirectories)."""
    return not os.listdir(path)

def find_dust_bunnies(root_path, age_threshold_days=None, patterns=None, empty_dirs_only=False):
    """
    Finds old files, files matching patterns, and empty directories.
    Returns a tuple: (files_to_clean, dirs_to_clean)
    """
    files_to_clean = []
    dirs_to_clean = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if not empty_dirs_only:
            # Check files
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                should_clean_file = False

                # Check by age
                if age_threshold_days is not None:
                    if get_file_age_in_days(filepath) > age_threshold_days:
                        should_clean_file = True

                # Check by pattern
                if patterns:
                    for pattern in patterns:
                        if fnmatch.fnmatch(filename, pattern):
                            should_clean_file = True
                            break # Found a match, no need to check other patterns

                if should_clean_file:
                    files_to_clean.append(filepath)

        # Check directories (only if they are currently empty)
        if not dirnames and not filenames: # Directory is empty
            dirs_to_clean.append(dirpath)

    return files_to_clean, dirs_to_clean

def clean_dust_bunnies(files_to_clean, dirs_to_clean, dry_run=True):
    """
    Performs the cleanup operation.
    """
    print(f"\n--- {'DRY RUN' if dry_run else 'CLEANUP'} RESULTS ---")
    print(f"Files to {'identify' if dry_run else 'delete'}: {len(files_to_clean)}")
    for f in files_to_clean:
        print(f"  File: {f}")
        if not dry_run:
            try:
                os.remove(f)
                print(f"    DELETED: {f}")
            except OSError as e:
                print(f"    ERROR deleting {f}: {e}")

    print(f"\nDirectories to {'identify' if dry_run else 'delete'}: {len(dirs_to_clean)}")
    # Sort directories by length in reverse to delete deepest first
    dirs_to_clean.sort(key=len, reverse=True)
    for d in dirs_to_clean:
        # Re-check if directory is truly empty before deleting, especially important for non-dry-runs
        if dry_run or is_empty_dir(d):
            print(f"  Directory: {d}")
            if not dry_run:
                try:
                    os.rmdir(d)
                    print(f"    DELETED: {d}")
                except OSError as e:
                    print(f"    ERROR deleting {d}: {e}")
        else:
            if not dry_run:
                print(f"  Skipping non-empty directory: {d}")


def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: old, unused, or empty files and directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=None,
        help="Files older than this many days will be considered for cleanup."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default=None,
        help="Comma-separated glob patterns (e.g., '*.log,*.tmp') for files to consider."
    )
    parser.add_argument(
        "--empty-dirs-only",
        action="store_true",
        help="Only scan for and clean up empty directories."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, listing what *would* be cleaned without making changes."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Execute the cleanup operation, deleting identified items. Use with caution!"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    if not args.dry_run and not args.clean:
        print("Error: You must specify either --dry-run or --clean.")
        exit(1)

    if args.clean and args.dry_run:
        print("Error: Cannot specify both --dry-run and --clean.")
        exit(1)

    patterns_list = [p.strip() for p in args.patterns.split(',')] if args.patterns else None

    print(f"Scanning '{args.path}' for digital dust bunnies...")

    files_to_clean, dirs_to_clean = find_dust_bunnies(
        root_path=args.path,
        age_threshold_days=args.age,
        patterns=patterns_list,
        empty_dirs_only=args.empty_dirs_only
    )

    clean_dust_bunnies(files_to_clean, dirs_to_clean, dry_run=args.dry_run)

    print("\nDigital dust bunny sweeping complete!")

if __name__ == "__main__":
    main()
