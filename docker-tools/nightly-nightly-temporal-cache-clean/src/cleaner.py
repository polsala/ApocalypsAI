import os
import time
import argparse
from datetime import datetime, timedelta

def find_old_files(base_path, age_days, current_time=None):
    """
    Finds files in base_path (and its subdirectories) that are older than age_days.
    Returns a list of paths to old files.
    """
    if current_time is None:
        current_time = datetime.now()

    cutoff_time = current_time - timedelta(days=age_days)
    old_files = []

    if not os.path.isdir(base_path):
        print(f"Error: Path '{base_path}' is not a valid directory.")
        return []

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Get modification time (mtime) as a timestamp
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < cutoff_time:
                    old_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access file '{file_path}': {e}")
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally remove old files from a directory."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The absolute path to the directory to scan."
    )
    parser.add_argument(
        "--age", 
        type=int, 
        required=True, 
        help="Files older than this many days will be targeted."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Only list files that would be deleted, do not delete them. (Default if --delete is not used)"
    )
    parser.add_argument(
        "--delete", 
        action="store_true", 
        help="Actually delete the identified old files. Use with caution!"
    )

    args = parser.parse_args()

    if not args.dry_run and not args.delete:
        print("No action specified. Running in --dry-run mode by default.")
        args.dry_run = True

    print(f"Scanning '{args.path}' for files older than {args.age} days...")
    old_files = find_old_files(args.path, args.age)

    if not old_files:
        print("No old files found. Your temporal cache is pristine!")
        return

    print(f"Found {len(old_files)} old files:")
    for f in old_files:
        print(f"  - {f}")

    if args.dry_run:
        print("\nThis was a DRY RUN. No files were deleted.")
        print("To delete these files, run again with the --delete flag.")
    elif args.delete:
        print("\nInitiating temporal stabilization (deletion)...")
        deleted_count = 0
        for f in old_files:
            try:
                os.remove(f)
                print(f"  Deleted: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting '{f}': {e}")
        print(f"\nTemporal stabilization complete. {deleted_count} files removed.")

if __name__ == "__main__":
    main()
