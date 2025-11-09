import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days based on its last modification time."""
    try:
        mod_timestamp = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        current_datetime = datetime.now()
        return (current_datetime - mod_datetime).days
    except OSError:
        return -1 # Indicate error or file not found

def is_excluded(path, exclude_patterns):
    """Checks if a path matches any of the exclusion patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(os.path.basename(path), pattern): # Match basename (e.g., '*.log')
            return True
        if fnmatch.fnmatch(path, pattern): # Match full path (e.g., 'node_modules')
            return True
    return False

def collect_dust_bunnies(paths, age_threshold_days, dry_run, exclude_patterns):
    """Scans specified paths for old files and optionally deletes them.

    Args:
        paths (list): List of directories to scan.
        age_threshold_days (int): Files older than this will be considered dust bunnies.
        dry_run (bool): If True, only list files; do not delete.
        exclude_patterns (list): List of glob patterns for files/dirs to exclude.
    """
    found_bunnies = []
    print(f"\n🌌 Initiating Cosmic Dust Bunny Collection... (Threshold: {age_threshold_days} days old)\n")

    for path_to_scan in paths:
        if not os.path.isdir(path_to_scan):
            print(f"⚠️ Warning: Path '{path_to_scan}' is not a valid directory. Skipping.")
            continue

        if is_excluded(path_to_scan, exclude_patterns):
            print(f"Skipping excluded directory: {path_to_scan}")
            continue

        print(f"Scanning: {path_to_scan}")
        for root, dirs, files in os.walk(path_to_scan, topdown=True):
            # Filter out excluded directories *before* recursing into them
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_patterns)]

            for file in files:
                filepath = os.path.join(root, file)
                if is_excluded(filepath, exclude_patterns):
                    # print(f"  Excluding file: {filepath}") # Too verbose for general use
                    continue

                age = get_file_age_in_days(filepath)
                if age >= age_threshold_days:
                    found_bunnies.append(filepath)
                    print(f"  Found dust bunny: {filepath} (Age: {age} days)")

    if not found_bunnies:
        print("✨ No cosmic dust bunnies found! Your digital space is pristine.")
        return

    print(f"\nFound {len(found_bunnies)} cosmic dust bunnies.\n")

    if dry_run:
        print("🔭 Dry run complete. No files were deleted. To remove them, run without --dry-run.")
    else:
        print("🧹 Sweeping away cosmic dust bunnies...")
        for bunny in found_bunnies:
            try:
                os.remove(bunny)
                print(f"  Removed: {bunny}")
            except OSError as e:
                print(f"  Failed to remove {bunny}: {e}")
        print("\n✅ Cosmic dust bunnies successfully swept! Your digital space feels lighter.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away old, forgotten files ('cosmic dust bunnies') from specified directories."
    )
    parser.add_argument(
        "--paths",
        nargs='*', # 0 or more arguments
        default=['.'], # Default to current directory
        help="Directories to scan for dust bunnies. Defaults to current directory."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered dust bunnies. Defaults to 30."
    )
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="Perform a dry run without actually deleting files."
    )
    parser.add_argument(
        "--exclude",
        nargs='*', # 0 or more arguments
        default=[],
        help="File/directory patterns to exclude (e.g., '*.log', 'node_modules/')."
    )

    args = parser.parse_args()

    collect_dust_bunnies(args.paths, args.age, args.dry_run, args.exclude)

if __name__ == "__main__":
    main()
