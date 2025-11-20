import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        file_datetime = datetime.fromtimestamp(mtime)
        return (datetime.now() - file_datetime).days
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible
    except Exception as e:
        print(f"Warning: Could not get modification time for {filepath}: {e}")
        return -1

def find_dust_bunnies(directories, age_threshold_days, patterns):
    """
    Finds files in specified directories that match age and pattern criteria.
    Returns a list of file paths.
    """
    dust_bunnies = []
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not accessible: {directory}. Skipping.")
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Check age
                file_age = get_file_age_days(filepath)
                if file_age == -1: # Skip if age could not be determined
                    continue

                if file_age > age_threshold_days:
                    # Check patterns
                    matched_pattern = False
                    for pattern in patterns:
                        if fnmatch.fnmatch(filename, pattern):
                            matched_pattern = True
                            break
                    
                    if matched_pattern:
                        dust_bunnies.append(filepath)
    return dust_bunnies

def sweep_dust_bunnies(file_paths, dry_run=True):
    """
    Deletes or lists files based on dry_run flag.
    """
    if not file_paths:
        print("No digital dust bunnies found to sweep!")
        return

    print(f"--- {'DRY RUN: Files that would be deleted' if dry_run else 'DELETING Files'} ---")
    for filepath in file_paths:
        if dry_run:
            print(f"  [DRY RUN] Would delete: {filepath} (Age: {get_file_age_days(filepath)} days)")
        else:
            try:
                os.remove(filepath)
                print(f"  Deleted: {filepath}")
            except OSError as e:
                print(f"  Error deleting {filepath}: {e}")
    print(f"--- {'DRY RUN Complete' if dry_run else 'Cleanup Complete'} ---")
    print(f"Total files {'identified' if dry_run else 'processed'}: {len(file_paths)}")


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Cleans up old, unused files."
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        required=True,
        help="One or more directories to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered dust bunnies. Default: 30."
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        default=["*"],
        help="One or more glob patterns (e.g., '*.log', 'temp_*') to match filenames. Default: '*' (all files)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only list files that would be deleted, do not actually delete them."
    )

    args = parser.parse_args()

    print(f"Scanning directories: {args.dirs}")
    print(f"Looking for files older than: {args.age} days")
    print(f"Matching patterns: {args.patterns}")
    print(f"Mode: {'Dry Run' if args.dry_run else 'Actual Deletion'}")

    dust_bunnies = find_dust_bunnies(args.dirs, args.age, args.patterns)
    sweep_dust_bunnies(dust_bunnies, args.dry_run)

if __name__ == "__main__":
    main()
