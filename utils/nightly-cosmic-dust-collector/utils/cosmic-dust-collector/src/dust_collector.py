import os
import argparse
from datetime import datetime, timedelta
import fnmatch

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    mtime = os.path.getmtime(filepath)
    # Mock rationale: In tests, we'll mock datetime.now() to control the 'current' time
    # and thus deterministically calculate file ages relative to mocked creation times.
    return (datetime.now() - datetime.fromtimestamp(mtime)).days

def find_dust(path, age_days=0, patterns=None):
    """
    Finds 'cosmic dust' (files matching criteria) in the given path.
    Returns a list of file paths.
    """
    dust_files = []
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return []

    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            is_dust = False

            # Check age
            if age_days > 0 and get_file_age_days(filepath) >= age_days:
                is_dust = True

            # Check patterns (if age_days didn't already mark it as dust)
            if patterns and not is_dust:
                for pattern in patterns:
                    if fnmatch.fnmatch(file, pattern): # Match against filename only
                        is_dust = True
                        break

            if is_dust:
                dust_files.append(filepath)
    return dust_files

def clean_dust(files_to_clean, dry_run=True):
    """
    Cleans (deletes) the specified files.
    If dry_run is True, only prints what would be deleted.
    """
    if not files_to_clean:
        print("No cosmic dust found to clean.")
        return

    print(f"--- {'DRY RUN' if dry_run else 'CLEANING'} ---")
    for filepath in files_to_clean:
        if dry_run:
            print(f"Would delete: {filepath}")
        else:
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
    print("--- COMPLETE ---")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Cleans up digital detritus from your project directories."
    )
    parser.add_argument("path", help="The directory to scan for cosmic dust.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate cleaning without actually deleting files."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=0,
        help="Delete files older than this many days. (0 for no age limit)"
    )
    parser.add_argument(
        "--patterns",
        type=str,
        help="Comma-separated file patterns (e.g., '*.log,*.tmp,old_file.txt')."
    )

    args = parser.parse_args()

    patterns_list = [p.strip() for p in args.patterns.split(',')] if args.patterns else []

    print(f"Scanning '{args.path}' for cosmic dust...")
    dust_files = find_dust(args.path, args.age_days, patterns_list)

    if dust_files:
        print(f"Found {len(dust_files)} pieces of cosmic dust.")
        clean_dust(dust_files, args.dry_run)
    else:
        print("No cosmic dust found matching criteria.")

if __name__ == "__main__":
    main()
