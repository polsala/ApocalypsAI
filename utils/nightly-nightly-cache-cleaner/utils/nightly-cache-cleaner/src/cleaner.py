import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def get_file_size_mb(filepath):
    """Returns the size of a file in megabytes."""
    try:
        return os.path.getsize(filepath) / (1024 * 1024)
    except OSError:
        return -1 # Indicate error or non-existent file

def matches_patterns(filepath, include_patterns, exclude_patterns):
    """Checks if a filepath matches include/exclude patterns."""
    filename = os.path.basename(filepath)
    
    # Check include patterns
    if include_patterns:
        if not any(fnmatch.fnmatch(filename, p) for p in include_patterns):
            return False
    
    # Check exclude patterns
    if exclude_patterns:
        if any(fnmatch.fnmatch(filename, p) for p in exclude_patterns):
            return False
            
    return True

def find_and_clean_files(
    paths,
    max_age_days=None,
    min_size_mb=None,
    include_patterns=None,
    exclude_patterns=None,
    dry_run=True
):
    """
    Scans specified paths for files matching criteria and optionally deletes them.
    """
    found_files = []
    
    print(f"Scanning directories: {', '.join(paths)}")
    print(f"Criteria: Max Age={max_age_days} days, Min Size={min_size_mb} MB")
    if include_patterns:
        print(f"Include Patterns: {', '.join(include_patterns)}")
    if exclude_patterns:
        print(f"Exclude Patterns: {', '.join(exclude_patterns)}")
    print("-" * 40)

    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a directory or does not exist. Skipping.")
            continue

        for root, _, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)

                # Check patterns first for efficiency
                if not matches_patterns(filepath, include_patterns, exclude_patterns):
                    continue

                file_age = get_file_age_days(filepath)
                file_size = get_file_size_mb(filepath)

                if file_age == -1 or file_size == -1:
                    print(f"Could not access file metadata for '{filepath}'. Skipping.")
                    continue

                # Apply age filter
                if max_age_days is not None and file_age < max_age_days:
                    continue

                # Apply size filter
                if min_size_mb is not None and file_size < min_size_mb:
                    continue
                
                found_files.append((filepath, file_age, file_size))

    if not found_files:
        print("No files found matching the criteria.")
        return 0

    print(f"\nFound {len(found_files)} files matching criteria:")
    for filepath, age, size in found_files:
        print(f"  - {filepath} (Age: {age:.1f} days, Size: {size:.2f} MB)")

    if dry_run:
        print("\nThis was a DRY RUN. No files were deleted.")
        print("To delete these files, run with the --delete flag.")
        return 0
    else:
        print("\nInitiating deletion...")
        deleted_count = 0
        total_reclaimed_size_mb = 0
        for filepath, _, size in found_files:
            try:
                os.remove(filepath)
                print(f"  Deleted: {filepath}")
                deleted_count += 1
                total_reclaimed_size_mb += size
            except OSError as e:
                print(f"  Error deleting '{filepath}': {e}")
        print(f"\nDeletion complete. Deleted {deleted_count} files.")
        print(f"Total disk space reclaimed: {total_reclaimed_size_mb:.2f} MB")
        return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Cleaner: Identifies and optionally removes old, large, or temporary files."
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="One or more directories to scan."
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        help="Files older than this many days will be considered."
    )
    parser.add_argument(
        "--min-size-mb",
        type=int,
        help="Files larger than this many megabytes will be considered."
    )
    parser.add_argument(
        "--include-patterns",
        nargs="+",
        help="Glob patterns for files to include (e.g., '*.tmp', 'cache/*')."
    )
    parser.add_argument(
        "--exclude-patterns",
        nargs="+",
        help="Glob patterns for files to exclude (e.g., '*.important', 'config/*')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True, # Default to dry run if --delete is not present
        help="Perform a dry run, listing files that *would* be deleted without actually deleting them."
    )
    parser.add_argument(
        "--delete",
        action="store_false", # If --delete is present, dry_run becomes False
        dest="dry_run",
        help="Actually delete the identified files. USE WITH CAUTION!"
    )

    args = parser.parse_args()

    # Ensure dry_run is correctly set based on presence of --delete
    # If --delete is present, args.dry_run will be False. If not, it will be True (default).

    find_and_clean_files(
        paths=args.paths,
        max_age_days=args.max_age_days,
        min_size_mb=args.min_size_mb,
        include_patterns=args.include_patterns,
        exclude_patterns=args.exclude_patterns,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
