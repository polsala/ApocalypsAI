import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(paths, patterns, age_days):
    """
    Scans specified paths for files matching patterns and older than age_days.

    Args:
        paths (list): List of directories to scan.
        patterns (list): List of glob-style patterns (e.g., '*.log', '*.tmp').
        age_days (int): Files older than this many days will be considered.

    Returns:
        list: A list of file paths identified as dust bunnies.
    """
    dust_bunnies = []
    now = time.time()
    age_threshold_timestamp = now - (age_days * 24 * 60 * 60)

    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        for root, _, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Check if file matches any pattern
                matches_pattern = False
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        matches_pattern = True
                        break
                
                if not matches_pattern:
                    continue

                # Check file age
                try:
                    file_mtime = os.path.getmtime(filepath)
                    if file_mtime < age_threshold_timestamp:
                        dust_bunnies.append(filepath)
                except OSError as e:
                    print(f"Warning: Could not get modification time for '{filepath}': {e}")
                    continue
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Bunny Collector: Scans and cleans old, temporary files."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--patterns",
        nargs=":",
        default=["*.log", "*.tmp", "*.bak", "~*", ".#*"],
        help="Glob-style file patterns to match (e.g., '*.log', '*.tmp'). Default: *.log *.tmp *.bak ~* .#*"
    )
    parser.add_argument(
        "--age",
        type=int,
        default=7,
        help="Files older than this many days will be considered dust bunnies. Default: 7"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be deleted without actually deleting them."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified dust bunnies. Use with caution!"
    )

    args = parser.parse_args()

    if args.delete and args.dry_run:
        parser.error("Cannot use --delete and --dry-run together. Choose one.")

    print(f"Scanning paths: {', '.join(args.path)}")
    print(f"Looking for patterns: {', '.join(args.patterns)}")
    print(f"Files older than: {args.age} days")

    dust_bunnies = find_dust_bunnies(args.path, args.patterns, args.age)

    if not dust_bunnies:
        print("\nNo cosmic dust bunnies found. Your system is sparkling clean! ✨")
        return

    print(f"\nFound {len(dust_bunnies)} cosmic dust bunnies:")
    for bunny in dust_bunnies:
        print(f"  - {bunny}")

    if args.dry_run:
        print("\n(Dry run complete. No files were deleted.)")
    elif args.delete:
        print("\nInitiating cosmic dust bunny purge...")
        deleted_count = 0
        for bunny in dust_bunnies:
            try:
                os.remove(bunny)
                print(f"  Deleted: {bunny}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting '{bunny}': {e}")
        print(f"\nPurge complete. {deleted_count} cosmic dust bunnies removed. 🚀")
    else:
        print("\nTo delete these files, run again with the --delete flag.")
        print("To perform a dry run, run again with the --dry-run flag.")

if __name__ == "__main__":
    main()
