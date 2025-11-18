import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days based on its modification time."""
    try:
        mod_timestamp = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        current_datetime = datetime.now()
        age = current_datetime - mod_datetime
        return age.days
    except OSError:
        return -1 # Indicate an error or unreadable file

def should_delete_file(filepath, age_threshold_days, include_patterns, exclude_patterns, verbose=False):
    """
    Determines if a file should be deleted based on age and patterns.
    """
    filename = os.path.basename(filepath)

    # Check age
    file_age = get_file_age_days(filepath)
    if file_age == -1:
        if verbose:
            print(f"Skipping unreadable file: {filepath}")
        return False
    if file_age < age_threshold_days:
        if verbose:
            print(f"Skipping {filepath}: too new ({file_age} days old, threshold {age_threshold_days})")
        return False

    # Check include patterns
    if include_patterns:
        matched_include = False
        for pattern in include_patterns:
            if fnmatch.fnmatch(filename, pattern):
                matched_include = True
                break
        if not matched_include:
            if verbose:
                print(f"Skipping {filepath}: no include pattern match")
            return False

    # Check exclude patterns
    if exclude_patterns:
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(filename, pattern):
                if verbose:
                    print(f"Skipping {filepath}: excluded by pattern '{pattern}'")
                return False

    return True

def sweep_directory(directory, age_threshold_days, include_patterns, exclude_patterns, dry_run, verbose):
    """
    Scans a directory for old files and optionally deletes them.
    Returns a tuple: (files_processed, files_deleted_or_marked)
    """
    files_processed = 0
    files_deleted_or_marked = 0
    if verbose:
        print(f"Scanning directory: {directory}")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            files_processed += 1

            if should_delete_file(filepath, age_threshold_days, include_patterns, exclude_patterns, verbose):
                files_deleted_or_marked += 1
                if dry_run:
                    print(f"[DRY RUN] Would delete: {filepath} (Age: {get_file_age_days(filepath)} days)")
                else:
                    try:
                        os.remove(filepath)
                        print(f"Deleted: {filepath} (Age: {get_file_age_days(filepath)} days)")
                    except OSError as e:
                        print(f"Error deleting {filepath}: {e}")
            elif verbose:
                print(f"Keeping: {filepath}")

    return files_processed, files_deleted_or_marked

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Cleans old files from directories."
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        required=True,
        help="One or more directories to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered for deletion. (Default: 30)"
    )
    parser.add_argument(
        "--include",
        nargs="*",
        default=[],
        help="Glob patterns for files to INCLUDE (e.g., '*.log', 'temp_*'). If not specified, all files are considered."
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Glob patterns for files to EXCLUDE, even if they match include patterns."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, printing files that *would* be deleted without actually deleting them."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed information during the scan."
    )

    args = parser.parse_args()

    total_processed = 0
    total_deleted_or_marked = 0

    print(f"--- Digital Dust Bunny Sweeper {'(DRY RUN)' if args.dry_run else ''} ---")
    print(f"Targeting files older than {args.age} days.")
    if args.include:
        print(f"Including patterns: {', '.join(args.include)}")
    if args.exclude:
        print(f"Excluding patterns: {', '.join(args.exclude)}")
    print("-" * 40)

    for directory in args.dirs:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not a directory: {directory}. Skipping.")
            continue
        processed, deleted = sweep_directory(
            directory,
            args.age,
            args.include,
            args.exclude,
            args.dry_run,
            args.verbose
        )
        total_processed += processed
        total_deleted_or_marked += deleted

    print("-" * 40)
    print(f"Scan complete. Total files processed: {total_processed}")
    print(f"Total files {'would be deleted' if args.dry_run else 'deleted'}: {total_deleted_or_marked}")
    print("------------------------------------------")

if __name__ == "__main__":
    main()
