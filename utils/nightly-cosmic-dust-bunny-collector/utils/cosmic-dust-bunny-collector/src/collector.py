import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from fnmatch import fnmatch

def find_dust_bunnies(
    directory: str,
    patterns: list[str],
    min_age_days: int = 0,
    verbose: bool = False
) -> list[str]:
    """
    Scans the specified directory for files matching patterns and age criteria.
    Returns a list of file paths that are considered 'dust bunnies'.
    """
    dust_bunnies = []
    now = time.time()
    min_timestamp = now - (min_age_days * 24 * 60 * 60)

    if verbose:
        print(f"Scanning directory: {directory}")
        print(f"Patterns: {patterns}")
        print(f"Minimum age: {min_age_days} days")

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Skip if it's a symlink to avoid infinite loops or external deletions
            if os.path.islink(file_path):
                if verbose: print(f"  Skipping symlink: {file_path}")
                continue

            # Check patterns
            is_match = False
            for pattern in patterns:
                if fnmatch(file_name, pattern):
                    is_match = True
                    break
            
            if not is_match:
                continue

            # Check age if min_age_days > 0
            if min_age_days > 0:
                try:
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime >= min_timestamp:
                        if verbose: print(f"  Skipping recent file: {file_path} (modified {datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
                        continue
                except OSError as e:
                    if verbose: print(f"  Warning: Could not get modification time for {file_path}: {e}")
                    continue # Skip files we can't stat

            dust_bunnies.append(file_path)
            if verbose: print(f"  Found dust bunny: {file_path}")

    return dust_bunnies

def clean_dust_bunnies(
    dust_bunnies: list[str],
    dry_run: bool = True,
    verbose: bool = False
) -> int:
    """
    Deletes the specified list of files if dry_run is False.
    Returns the count of files processed (either listed or deleted).
    """
    processed_count = 0
    action = "[DRY RUN] Would delete" if dry_run else "Deleting"

    if not dust_bunnies:
        if verbose: print("No cosmic dust bunnies found to process.")
        return 0

    if verbose and dry_run:
        print("\n--- Dry Run Mode: No files will be deleted ---")
    elif verbose and not dry_run:
        print("\n--- Deletion Mode: Files will be permanently removed ---")

    for file_path in dust_bunnies:
        try:
            if dry_run:
                print(f"  {action}: {file_path}")
            else:
                os.remove(file_path)
                print(f"  {action}: {file_path}")
            processed_count += 1
        except OSError as e:
            print(f"Error {action} {file_path}: {e}", file=sys.stderr)

    if verbose:
        print(f"\nProcessed {processed_count} cosmic dust bunnies.")
        if dry_run:
            print("To delete these files, run again with the --delete flag.")

    return processed_count

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Clean up temporary and old files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--patterns",
        nargs='+',
        default=['*.tmp', '*.log', '*~', '.#*', '#*#', '*.bak', '*.swp', '*.pyc'],
        help="Space-separated list of glob patterns to match (e.g., '*.tmp' '*.log')."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=0,
        help="Only consider files older than this many days. Defaults to 0 (all files matching patterns)."
    )
    parser.add_argument(
        "--delete",
        action='store_true',
        help="CAUTION: Enable this flag to actually delete the files. By default, it runs in dry-run mode."
    )
    parser.add_argument(
        "--verbose",
        action='store_true',
        help="Print more detailed information during the scan."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.", file=sys.stderr)
        sys.exit(1)

    dust_bunnies = find_dust_bunnies(
        args.directory,
        args.patterns,
        args.age,
        args.verbose
    )

    if dust_bunnies:
        print(f"Found {len(dust_bunnies)} cosmic dust bunnies.")
        clean_dust_bunnies(dust_bunnies, dry_run=not args.delete, verbose=args.verbose)
    else:
        print("No cosmic dust bunnies found matching the criteria.")

    sys.exit(0)

if __name__ == "__main__":
    main()
