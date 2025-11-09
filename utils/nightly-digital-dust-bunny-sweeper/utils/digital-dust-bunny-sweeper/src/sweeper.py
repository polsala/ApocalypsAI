import os
import time
import argparse
from datetime import datetime, timedelta

def get_current_timestamp():
    """Helper to get current timestamp for mocking."""
    return time.time()

def find_empty_directories(root_dir, current_time):
    """Finds all empty directories within a given root directory."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the directory itself is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    # Sort by length descending to ensure child directories are processed first for deletion
    return sorted(empty_dirs, key=len, reverse=True)

def find_stale_files(root_dir, stale_days, current_time):
    """Finds files older than stale_days within a given root directory."""
    stale_files = []
    cutoff_timestamp = current_time - (stale_days * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Check if the file exists before getting mtime (might be a broken symlink etc.)
                if os.path.exists(filepath):
                    mtime = os.path.getmtime(filepath)
                    if mtime < cutoff_timestamp:
                        stale_files.append(filepath)
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital 'dust bunnies' (empty directories and stale files)."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Root directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered stale. Default is 30."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would be cleaned, do not make changes. (Default if --clean is not present)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Actually delete empty directories and stale files. Use with caution!"
    )

    args = parser.parse_args()

    if not args.clean and not args.dry_run:
        args.dry_run = True # Default to dry-run if neither --clean nor --dry-run is specified

    current_time = get_current_timestamp()

    print(f"\n--- Digital Dust Bunny Sweeper ({'DRY RUN' if args.dry_run else 'CLEANING'}) ---")
    print(f"Scanning for files older than {args.stale_days} days.")

    total_empty_dirs = []
    total_stale_files = []

    for path in args.path:
        if not os.path.isdir(path):
            print(f"Error: Path '{path}' is not a valid directory. Skipping.")
            continue

        print(f"\nScanning '{path}'...")
        empty_dirs = find_empty_directories(path, current_time)
        stale_files = find_stale_files(path, args.stale_days, current_time)

        total_empty_dirs.extend(empty_dirs)
        total_stale_files.extend(stale_files)

        if empty_dirs:
            print(f"  Found {len(empty_dirs)} empty directories:")
            for d in empty_dirs:
                print(f"    - {d}")
        else:
            print("  No empty directories found.")

        if stale_files:
            print(f"  Found {len(stale_files)} stale files:")
            for f in stale_files:
                print(f"    - {f}")
        else:
            print("  No stale files found.")

    if args.clean:
        print("\n--- Performing Cleanup ---")
        deleted_count = 0
        for f in total_stale_files:
            try:
                os.remove(f)
                print(f"  Deleted stale file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting file {f}: {e}")
        print(f"  Successfully deleted {deleted_count} stale files.")

        deleted_count = 0
        for d in total_empty_dirs:
            try:
                # Ensure it's still empty before attempting to remove
                if not os.listdir(d):
                    os.rmdir(d)
                    print(f"  Deleted empty directory: {d}")
                    deleted_count += 1
                else:
                    print(f"  Skipped non-empty directory (after scanning): {d}")
            except OSError as e:
                print(f"  Error deleting directory {d}: {e}")
        print(f"  Successfully deleted {deleted_count} empty directories.")
    elif args.dry_run:
        print("\n--- Dry Run Complete ---")
        print(f"Would delete {len(total_stale_files)} stale files and {len(total_empty_dirs)} empty directories.")

    print("\n--- Sweeper Finished ---")

if __name__ == "__main__":
    main()
