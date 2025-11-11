import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(directory, age_days=30, patterns=None):
    """
    Scans the specified directory for files that match the criteria (age and/or patterns).
    Returns a list of file paths.
    """
    dust_bunnies = []
    now = time.time() # Mock rationale: time.time() is mocked in tests for deterministic age calculation.
    age_threshold_timestamp = now - (age_days * 24 * 60 * 60)

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_mtime = os.path.getmtime(filepath) # Mock rationale: os.path.getmtime is mocked for deterministic file modification times.

                # Check age criterion
                is_old_enough = file_mtime < age_threshold_timestamp

                # Check pattern criterion
                is_pattern_match = False
                if patterns:
                    for pattern in patterns:
                        if fnmatch.fnmatch(filename, pattern):
                            is_pattern_match = True
                            break
                else:
                    # If no patterns are specified, all files are considered for pattern matching
                    is_pattern_match = True
                
                # A file is a dust bunny if it's old enough AND (matches a pattern OR no patterns were specified)
                # If only age is specified, it just needs to be old enough (is_pattern_match will be True).
                # If only patterns are specified, it just needs to match a pattern (is_old_enough will be True if age_days is 0 or very large).
                # The default age_days=30 means files must be old AND match pattern (if patterns provided).
                
                # Refined logic: If patterns are provided, both age and pattern must match. 
                # If no patterns are provided, only age must match.
                if patterns:
                    if is_old_enough and is_pattern_match:
                        dust_bunnies.append(filepath)
                else:
                    if is_old_enough:
                        dust_bunnies.append(filepath)

            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")
                continue
    return dust_bunnies

def delete_files(file_paths, dry_run=True):
    """
    Deletes the specified files or prints them if in dry-run mode.
    """
    if not file_paths:
        print("No digital dust bunnies found to sweep.")
        return

    if dry_run:
        print("\n--- Dry Run: Files that would be swept away ---")
        for f in file_paths:
            print(f"[DRY RUN] Would delete: {f}")
        print("---------------------------------------------")
        print(f"Found {len(file_paths)} digital dust bunnies. Run with --delete to actually sweep them.")
    else:
        print("\n--- Sweeping away digital dust bunnies ---")
        deleted_count = 0
        for f in file_paths:
            try:
                os.remove(f) # Mock rationale: os.remove is mocked to prevent actual file deletion during tests.
                print(f"Deleted: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting {f}: {e}")
        print("----------------------------------------")
        print(f"Successfully swept away {deleted_count} digital dust bunnies.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies (old/redundant files)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start sweeping for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Only consider files older than this many days. Default is 30."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        help="One or more glob patterns (e.g., '*.log', '*.tmp', '~*') to match files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, listing files that *would* be deleted. This is the default if --delete is not used."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="CAUTION! Actually delete the identified files. Use with care."
    )

    args = parser.parse_args()

    if args.delete and args.dry_run:
        print("Error: Cannot use --delete and --dry-run simultaneously. Choose one.")
        exit(1)

    # If neither --delete nor --dry-run is specified, default to dry-run
    is_dry_run = not args.delete or args.dry_run

    print(f"Scanning '{args.path}' for digital dust bunnies...")
    bunnies = find_dust_bunnies(args.path, args.age, args.patterns)
    delete_files(bunnies, dry_run=is_dry_run)

if __name__ == "__main__":
    main()
