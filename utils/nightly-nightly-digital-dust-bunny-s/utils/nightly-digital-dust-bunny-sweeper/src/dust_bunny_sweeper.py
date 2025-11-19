import os
import argparse
import shutil
import time
from datetime import datetime, timedelta
import fnmatch

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def find_dust_bunnies(root_path, patterns, max_age_days, verbose=False):
    """Finds files and directories matching patterns or older than max_age_days.

    Args:
        root_path (str): The directory to start scanning from.
        patterns (list): List of file/directory name patterns to match (e.g., '__pycache__', '.DS_Store', '*.log').
        max_age_days (int): Files older than this many days will be considered for deletion.
        verbose (bool): If True, print detailed information during scanning.

    Returns:
        list: A list of file/directory paths to be considered for deletion.
    """
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    dust_bunnies = []
    current_time = datetime.now()

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check directories
        for dname in list(dirnames): # Use list to allow modification of dirnames during iteration
            full_path = os.path.join(dirpath, dname)
            # Check for pattern match
            if any(fnmatch.fnmatch(dname, p) for p in patterns):
                dust_bunnies.append(full_path)
                if verbose: print(f"Found (pattern): {full_path}")
                dirnames.remove(dname) # Don't traverse into matched directories
            # Check for empty directories (only if not already matched by pattern)
            elif not os.listdir(full_path) and not os.path.islink(full_path):
                dust_bunnies.append(full_path)
                if verbose: print(f"Found (empty dir): {full_path}")
                dirnames.remove(dname) # Don't traverse into empty directories

        # Check files
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            # Check for pattern match
            if any(fnmatch.fnmatch(fname, p) for p in patterns):
                dust_bunnies.append(full_path)
                if verbose: print(f"Found (pattern): {full_path}")
            # Check for age
            elif max_age_days > 0:
                try:
                    mtime_timestamp = os.path.getmtime(full_path)
                    mtime_dt = datetime.fromtimestamp(mtime_timestamp)
                    if (current_time - mtime_dt).days > max_age_days:
                        dust_bunnies.append(full_path)
                        if verbose: print(f"Found (old file): {full_path} (age: {(current_time - mtime_dt).days} days)")
                except OSError:
                    if verbose: print(f"Warning: Could not get modification time for {full_path}")

    return sorted(list(set(dust_bunnies))) # Remove duplicates and sort for consistent output

def clean_dust_bunnies(dust_bunnies, dry_run, verbose=False):
    """Deletes or lists the identified dust bunnies."""
    if not dust_bunnies:
        print("No dust bunnies found to clean.")
        return

    action = "Deleting" if not dry_run else "Would delete (dry run)"
    print(f"\n{action} {len(dust_bunnies)} items:")

    for item_path in dust_bunnies:
        if dry_run:
            print(f"  [DRY RUN] {item_path}")
        else:
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    if verbose: print(f"  Deleted directory: {item_path}")
                else:
                    os.remove(item_path)
                    if verbose: print(f"  Deleted file: {item_path}")
            except OSError as e:
                print(f"  Error deleting {item_path}: {e}")

    if not dry_run:
        print("\nCleanup complete.")
    else:
        print("\nDry run complete. Use --delete to perform actual deletion.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Cleans up temporary files and old clutter."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Perform actual deletion. If omitted, runs in dry-run mode (list only)."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=['__pycache__', '.DS_Store'],
        help="Space-separated list of file/directory names to target (e.g., '__pycache__ .DS_Store')."
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=0,
        help="Delete files older than this many days. Applies to all files, not just pattern-matched ones. (e.g., 30 for files older than 30 days)."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about files found and actions taken."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for dust bunnies...")
    dust_bunnies = find_dust_bunnies(args.path, args.patterns, args.max_age_days, args.verbose)
    clean_dust_bunnies(dust_bunnies, not args.delete, args.verbose)

if __name__ == "__main__":
    main()
