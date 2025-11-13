import os
import time
import argparse
from datetime import datetime, timedelta

def find_dust_bunnies(root_dir, max_log_age_days=90):
    """
    Scans a directory for 'dust bunnies': empty directories, old log files,
    and temporary files.

    Args:
        root_dir (str): The root directory to scan.
        max_log_age_days (int): Log files older than this many days are considered aged.

    Returns:
        dict: A dictionary containing lists of 'empty_dirs', 'aged_log_files',
              and 'temp_files'.
    """
    dust_bunnies = {
        'empty_dirs': [],
        'aged_log_files': [],
        'temp_files': []
    }

    if not os.path.isdir(root_dir):
        # print(f"Error: Directory not found: {root_dir}") # Suppress print in function for cleaner testing
        return dust_bunnies

    now = time.time()
    age_threshold_seconds = max_log_age_days * 24 * 60 * 60

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check for empty directories
        # Only consider subdirectories, not the root_dir itself if it's technically empty of files
        # but contains subdirs.
        if not dirnames and not filenames and dirpath != root_dir:
            dust_bunnies['empty_dirs'].append(dirpath)

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Check for aged log files
            if filename.lower().endswith('.log'):
                try:
                    mtime = os.path.getmtime(full_path)
                    if (now - mtime) > age_threshold_seconds:
                        dust_bunnies['aged_log_files'].append((full_path, datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')))
                except OSError:
                    # Handle cases where file might be inaccessible (e.g., permissions)
                    pass

            # Check for temporary files
            if filename.lower().endswith(('.tmp', '.bak')) or filename.startswith('~'):
                dust_bunnies['temp_files'].append(full_path)

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify and report on digital 'dust bunnies' in a directory."
    )
    parser.add_argument(
        "path_to_scan",
        type=str,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--max-log-age-days",
        type=int,
        default=90,
        help="Log files older than this many days are considered aged. Default is 90."
    )

    args = parser.parse_args()

    print("--- Cosmic Dust Bunny Report ---")

    bunnies = find_dust_bunnies(args.path_to_scan, args.max_log_age_days)

    if not os.path.isdir(args.path_to_scan):
        print(f"\nError: Directory not found: {args.path_to_scan}")
        return

    if bunnies['empty_dirs']:
        print("\nEmpty Directories:")
        for d in bunnies['empty_dirs']:
            print(f"  - {d}")
    else:
        print("\nNo empty directories found.")

    if bunnies['aged_log_files']:
        print(f"\nAged Log Files (older than {args.max_log_age_days} days):")
        for f, mtime_str in bunnies['aged_log_files']:
            print(f"  - {f} (Last Modified: {mtime_str})")
    else:
        print(f"\nNo aged log files found (older than {args.max_log_age_days} days).")

    if bunnies['temp_files']:
        print("\nTemporary Files:")
        for f in bunnies['temp_files']:
            print(f"  - {f}")
    else:
        print("\nNo temporary files found.")

    print("\n--- End Report ---")

if __name__ == "__main__":
    main()
