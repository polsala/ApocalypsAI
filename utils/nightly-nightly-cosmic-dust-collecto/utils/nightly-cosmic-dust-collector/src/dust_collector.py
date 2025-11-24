import os
import re
import time
import argparse
from datetime import datetime, timedelta

def collect_dust(directories_patterns_ages, dry_run=False, verbose=False):
    """
    Scans specified directories for files matching patterns and age thresholds,
    then removes them.

    Args:
        directories_patterns_ages (list): A list of tuples, where each tuple is
                                          (directory, pattern_regex, age_days).
        dry_run (bool): If True, only report files to be removed, don't delete.
        verbose (bool): If True, print more detailed information.
    """
    print(f"Starting Cosmic Dust Collection (Dry Run: {dry_run})...")
    
    total_files_considered = 0
    total_files_removed = 0
    total_space_freed = 0

    for directory, pattern_regex, age_days in directories_patterns_ages:
        print(f"\nScanning '{directory}' for files matching '{pattern_regex}' older than {age_days} days...")
        
        compiled_pattern = re.compile(pattern_regex)
        
        now = datetime.now()
        threshold_date = now - timedelta(days=age_days)

        if not os.path.isdir(directory):
            print(f"Warning: Directory '{directory}' does not exist or is not a directory. Skipping.")
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                total_files_considered += 1
                filepath = os.path.join(root, filename)

                if verbose:
                    print(f"  Considering: {filepath}")

                # Check if file matches pattern
                if not compiled_pattern.match(filename):
                    if verbose:
                        print(f"    - Does not match pattern '{pattern_regex}'. Skipping.")
                    continue

                # Check file age
                try:
                    mtime_timestamp = os.path.getmtime(filepath)
                    mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                except OSError as e:
                    print(f"Warning: Could not get modification time for '{filepath}': {e}. Skipping.")
                    continue

                if mtime_datetime < threshold_date:
                    file_size = 0
                    try:
                        file_size = os.path.getsize(filepath)
                    except OSError as e:
                        print(f"Warning: Could not get size for '{filepath}': {e}. Proceeding with removal if not dry-run.")

                    print(f"  Found dust: '{filepath}' (Modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')}, Size: {file_size / (1024*1024):.2f} MB)")
                    
                    if not dry_run:
                        try:
                            os.remove(filepath)
                            total_files_removed += 1
                            total_space_freed += file_size
                            print(f"    - REMOVED.")
                        except OSError as e:
                            print(f"    - ERROR removing '{filepath}': {e}")
                    else:
                        total_files_removed += 1 # Count for dry run report
                        total_space_freed += file_size # Count for dry run report
                        print(f"    - (Dry Run) Would remove.")
                elif verbose:
                    print(f"    - Too new (Modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')}). Skipping.")

    print("\n--- Dust Collection Summary ---")
    print(f"Total files considered: {total_files_considered}")
    print(f"Total files {'would be removed' if dry_run else 'removed'}: {total_files_removed}")
    print(f"Total space {'would be freed' if dry_run else 'freed'}: {total_space_freed / (1024*1024):.2f} MB")
    print("Cosmic Dust Collection complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans old files based on patterns and age."
    )
    parser.add_argument(
        '--dir', action='append', dest='dirs',
        help='Directory to scan. Can be specified multiple times.'
    )
    parser.add_argument(
        '--pattern', action='append', dest='patterns',
        help='Regex pattern for files to match. Must be paired with --dir. Can be specified multiple times.'
    )
    parser.add_argument(
        '--age', action='append', dest='ages', type=int,
        help='Minimum age in days for files to be removed. Must be paired with --dir. Can be specified multiple times.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Only report what would be removed, do not delete files.'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Print more detailed output.'
    )

    args = parser.parse_args()

    if not args.dirs or not args.patterns or not args.ages:
        parser.error("At least one --dir, --pattern, and --age must be provided.")
    
    if not (len(args.dirs) == len(args.patterns) == len(args.ages)):
        parser.error("The number of --dir, --pattern, and --age arguments must match.")

    directories_patterns_ages = list(zip(args.dirs, args.patterns, args.ages))

    collect_dust(directories_patterns_ages, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
