import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(
    root_path: str,
    age_days: int,
    min_size: int,
    max_size: int,
    include_patterns: list[str],
    exclude_patterns: list[str]
) -> list[str]:
    """
    Scans a directory for files matching 'dust bunny' criteria.

    Args:
        root_path: The root directory to scan.
        age_days: Files older than this many days are considered.
        min_size: Files smaller than this many bytes are considered.
        max_size: Files larger than this many bytes are considered.
        include_patterns: List of glob patterns for files to include.
        exclude_patterns: List of glob patterns for files to exclude.

    Returns:
        A list of file paths identified as dust bunnies.
    """
    dust_bunnies = []
    now = time.time()
    age_threshold_timestamp = now - (age_days * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            try:
                # Check if it's a file and not a broken symlink
                if not os.path.isfile(file_path):
                    continue

                # Check include/exclude patterns
                if include_patterns:
                    if not any(fnmatch.fnmatch(filename, p) for p in include_patterns):
                        continue # Not matching any include pattern
                if exclude_patterns:
                    if any(fnmatch.fnmatch(filename, p) for p in exclude_patterns):
                        continue # Matching an exclude pattern

                file_mtime = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)

                # Check age
                is_old_enough = file_mtime < age_threshold_timestamp

                # Check size
                is_correct_size = min_size <= file_size <= max_size

                if is_old_enough and is_correct_size:
                    dust_bunnies.append(file_path)

            except OSError as e:
                print(f"Warning: Could not access {file_path} - {e}")
                continue

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility to sweep away old, unused, or temporary 'digital dust bunny' files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered dust bunnies. (default: 30)"
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=0,
        help="Files smaller than this many bytes will be considered dust bunnies. (default: 0)"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=2**63 - 1, # Max signed 64-bit integer, effectively no upper limit
        help="Files larger than this many bytes will be considered dust bunnies. (default: 9223372036854775807)"
    )
    parser.add_argument(
        "--include-pattern",
        action='append',
        default=[],
        help="Glob pattern(s) for files to include (e.g., '*.log', 'temp_*'). Can be specified multiple times."
    )
    parser.add_argument(
        "--exclude-pattern",
        action='append',
        default=[],
        help="Glob pattern(s) for files to exclude (e.g., '*.tmp', 'important_*'). Can be specified multiple times."
    )
    parser.add_argument(
        "--delete",
        action='store_true',
        help="Actually delete the identified dust bunnies. (DANGER ZONE!)"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"\n--- Sweeping for Digital Dust Bunnies in '{args.path}' ---")
    print(f"  Criteria: Older than {args.age_days} days, size between {args.min_size} and {args.max_size} bytes.")
    if args.include_pattern: print(f"  Including patterns: {', '.join(args.include_pattern)}")
    if args.exclude_pattern: print(f"  Excluding patterns: {', '.join(args.exclude_pattern)}")
    print("--------------------------------------------------\n")

    dust_bunnies = find_dust_bunnies(
        args.path,
        args.age_days,
        args.min_size,
        args.max_size,
        args.include_pattern,
        args.exclude_pattern
    )

    if not dust_bunnies:
        print("No digital dust bunnies found. Your digital space is sparkling clean! ✨")
        return

    print(f"Found {len(dust_bunnies)} digital dust bunnies:\n")
    for bunny in dust_bunnies:
        print(f"  - {bunny}")

    if args.delete:
        print("\n--- Initiating Dust Bunny Extermination! --- ")
        for bunny in dust_bunnies:
            try:
                os.remove(bunny)
                print(f"  Deleted: {bunny}")
            except OSError as e:
                print(f"  Error deleting {bunny}: {e}")
        print("\n--- Extermination Complete! --- ")
    else:
        print("\n(Dry run: Use --delete to actually remove these files.)")

if __name__ == "__main__":
    main()
