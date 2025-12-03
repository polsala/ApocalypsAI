import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def is_dust_file(filepath, min_age_days, max_size_kb, current_time):
    """
    Checks if a file qualifies as 'cosmic dust' based on age and size.
    """
    try:
        stat = os.stat(filepath)
        file_size_bytes = stat.st_size
        file_mtime_timestamp = stat.st_mtime

        # Check for empty file
        if file_size_bytes == 0:
            return True, "empty"

        # Check for small file
        if file_size_bytes < max_size_kb * 1024:
            return True, f"smaller than {max_size_kb}KB"

        # Check for old file
        file_age_seconds = current_time - file_mtime_timestamp
        if file_age_seconds > min_age_days * 24 * 3600:
            return True, f"older than {min_age_days} days"

        return False, ""
    except OSError:
        # File might have been deleted or permissions issue
        return False, ""

def find_dust_files(root_path, min_age_days, max_size_kb, exclude_patterns):
    """
    Walks through the root_path and identifies files that are considered 'cosmic dust'.
    Returns a list of (filepath, reason) tuples.
    """
    dust_files = []
    current_time = time.time()
    exclude_patterns = [p.strip() for p in exclude_patterns.split(',') if p.strip()]

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories
        # dirnames is a list of names of subdirectories in dirpath
        # Modifying dirnames in-place will affect which directories os.walk visits
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(os.path.join(dirpath, d), p) for p in exclude_patterns)]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Check if file itself is excluded
            if any(fnmatch.fnmatch(filepath, p) for p in exclude_patterns):
                continue

            is_dust, reason = is_dust_file(filepath, min_age_days, max_size_kb, current_time)
            if is_dust:
                dust_files.append((filepath, reason))
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Identify and manage small, old, or empty files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for cosmic dust."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=30,
        help="Files older than this many days (based on last modification time) will be considered dust. Default: 30."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=1,
        help="Files smaller than this many kilobytes will be considered dust. Default: 1 (1KB)."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, the identified dust files will be permanently deleted. Use with caution!"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="A comma-separated list of glob patterns to exclude files or directories. E.g., '*.log,temp_dir/*'."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{args.path}' for cosmic dust (min_age_days={args.min_age_days}, max_size_kb={args.max_size_kb}KB)...")
    dust_files = find_dust_files(args.path, args.min_age_days, args.max_size_kb, args.exclude)

    if not dust_files:
        print("No cosmic dust found. Your repository is sparkling clean!")
        exit(0)

    print(f"\nFound {len(dust_files)} cosmic dust files:")
    for filepath, reason in dust_files:
        print(f"  - {filepath} (Reason: {reason})")

    if args.delete:
        print("\nInitiating deletion of cosmic dust files...")
        deleted_count = 0
        for filepath, _ in dust_files:
            try:
                os.remove(filepath)
                print(f"  Deleted: {filepath}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting {filepath}: {e}")
        print(f"\nSuccessfully deleted {deleted_count} files.")
        exit(0)
    else:
        print("\nTo delete these files, run the command again with the '--delete' flag.")
        exit(0)

if __name__ == "__main__":
    main()
