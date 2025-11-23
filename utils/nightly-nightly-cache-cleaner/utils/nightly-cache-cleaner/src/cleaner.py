import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_files_to_clean(
    paths: list[str],
    age_days: int,
    patterns: list[str]
) -> list[str]:
    """
    Finds files in specified paths that are older than age_days and match any of the patterns.
    """
    files_to_clean = []
    cutoff_time = datetime.now() - timedelta(days=age_days)

    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        for root, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    # Get last modification time
                    mod_timestamp = os.path.getmtime(filepath)
                    mod_datetime = datetime.fromtimestamp(mod_timestamp)

                    # Check age
                    if mod_datetime < cutoff_time:
                        # Check patterns if provided, otherwise consider all old files
                        if not patterns or any(fnmatch.fnmatch(filename, p) for p in patterns):
                            files_to_clean.append(filepath)
                except OSError as e:
                    print(f"Error accessing file '{filepath}': {e}")
                    continue
    return files_to_clean

def clean_files(files: list[str], dry_run: bool, force: bool):
    """
    Deletes files or prints them if in dry-run mode.
    """
    if not files:
        print("No files found to clean.")
        return

    print(f"Found {len(files)} files to {'delete' if not dry_run else 'consider for deletion'}:")
    for f in files:
        print(f"  - {f}")

    if dry_run:
        print("\nThis was a dry run. No files were deleted.")
        return

    if not force:
        confirmation = input("\nAre you sure you want to delete these files? (y/N): ").lower()
        if confirmation != 'y':
            print("Aborted. No files were deleted.")
            return

    deleted_count = 0
    for f in files:
        try:
            os.remove(f)
            print(f"Deleted: {f}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting file '{f}': {e}")
    print(f"\nSuccessfully deleted {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(description="Clean old or temporary files from specified directories.")
    parser.add_argument(
        "--paths",
        nargs='+',
        required=True,
        help="One or more directories to scan for old files."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Delete files older than this many days. (default: 30)"
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=[],
        help="Glob-style patterns for files to consider (e.g., '*.log', '__pycache__'). If not specified, all files older than --age-days are considered."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, only printing files that would be deleted without actually deleting them."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass confirmation prompt and delete files immediately (use with caution)."
    )

    args = parser.parse_args()

    files_to_clean = find_files_to_clean(args.paths, args.age_days, args.patterns)
    clean_files(files_to_clean, args.dry_run, args.force)

if __name__ == "__main__":
    main()
