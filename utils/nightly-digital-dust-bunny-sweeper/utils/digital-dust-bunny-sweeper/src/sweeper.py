import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(paths, age_days, patterns=None):
    """
    Scans specified paths for files older than age_days, optionally matching patterns.
    Returns a list of file paths.
    """
    dust_bunnies = []
    # Mock rationale: time.time is mocked in tests to fix the 'current time' for age calculations.
    cutoff_timestamp = (datetime.fromtimestamp(time.time()) - timedelta(days=age_days)).timestamp()

    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a directory or does not exist. Skipping.")
            continue

        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Mock rationale: os.path.getmtime is mocked in tests to control file ages.
                    mod_time = os.path.getmtime(file_path)
                    if mod_time < cutoff_timestamp:
                        if patterns:
                            # Check if file matches any of the provided patterns
                            if any(fnmatch.fnmatch(file, p) for p in patterns):
                                dust_bunnies.append(file_path)
                        else:
                            # No patterns specified, consider all old files
                            dust_bunnies.append(file_path)
                except OSError as e:
                    print(f"Warning: Could not access '{file_path}': {e}")
    return dust_bunnies

def sweep_dust_bunnies(file_list, dry_run=True):
    """
    Deletes files in the given list if not in dry_run mode.
    """
    if not file_list:
        print("No digital dust bunnies found to sweep.")
        return

    if dry_run:
        print("\n--- Digital Dust Bunnies (Dry Run) ---")
        for f in file_list:
            print(f"[DRY RUN] Would delete: {f}")
        print("--------------------------------------")
        print(f"Found {len(file_list)} dust bunnies. Use --delete to remove them.")
    else:
        print("\n--- Sweeping Digital Dust Bunnies ---")
        deleted_count = 0
        for f in file_list:
            try:
                # Mock rationale: os.remove is mocked in tests to prevent actual file deletion.
                os.remove(f)
                print(f"Deleted: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting '{f}': {e}")
        print("-------------------------------------")
        print(f"Successfully swept away {deleted_count} dust bunnies.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away old, unused, or temporary files (digital dust bunnies)."
    )
    parser.add_argument(
        "--paths",
        nargs='+',
        required=True,
        help="One or more directories to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be considered dust bunnies."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=[],
        help="Optional: Only consider files matching these glob patterns (e.g., '*.log', '*.tmp')."
    )
    parser.add_argument(
        "--list",
        action='store_true',
        help="List the identified dust bunnies without deleting them (default if --delete is not used)."
    )
    parser.add_argument(
        "--delete",
        action='store_true',
        help="Delete the identified dust bunnies. Use with caution!"
    )
    parser.add_argument(
        "--force",
        action='store_true',
        help="Skip the confirmation prompt when using --delete."
    )

    args = parser.parse_args()

    if not args.delete and not args.list:
        args.list = True # Default to listing if neither --delete nor --list is specified

    print(f"Scanning paths: {args.paths} for files older than {args.age} days...")
    if args.patterns:
        print(f"Filtering by patterns: {args.patterns}")

    dust_bunnies = find_dust_bunnies(args.paths, args.age, args.patterns)

    if args.list:
        sweep_dust_bunnies(dust_bunnies, dry_run=True)
    elif args.delete:
        if not dust_bunnies:
            print("No digital dust bunnies found to sweep.")
            return

        if not args.force:
            confirm = input(f"Found {len(dust_bunnies)} dust bunnies. Are you sure you want to delete them? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
        sweep_dust_bunnies(dust_bunnies, dry_run=False)

if __name__ == "__main__":
    main()
