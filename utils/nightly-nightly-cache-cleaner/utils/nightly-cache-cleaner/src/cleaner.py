import os
import time
import argparse
from datetime import datetime, timedelta

def find_old_files(directory: str, days_old: int) -> list[str]:
    """
    Scans the given directory for files older than 'days_old'.
    Returns a list of paths to old files.
    """
    old_files = []
    cutoff_timestamp = (datetime.now() - timedelta(days=days_old)).timestamp()

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Get last modification time
                mod_time = os.path.getmtime(file_path)
                if mod_time < cutoff_timestamp:
                    old_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access {file_path} - {e}")
    return old_files

def delete_files(files: list[str]):
    """
    Deletes the given list of files.
    """
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path} - {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Cleaner: Scans directories for old files and optionally deletes them."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="The age threshold in days. Files older than this will be flagged."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, the utility will actually delete the identified files. Without this flag, it performs a dry run."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' does not exist or is not a directory.")
        exit(1)

    print(f"Scanning '{args.path}' for files older than {args.days} days...")
    old_files = find_old_files(args.path, args.days)

    if not old_files:
        print("No old files found. Your digital landscape is pristine!")
        exit(0)

    print(f"Found {len(old_files)} old files:")
    for f in old_files:
        print(f"  - {f}")

    if args.delete:
        print("\nProceeding with deletion...")
        delete_files(old_files)
        print("Deletion complete. Disk space reclaimed!")
    else:
        print("\nThis was a dry run. No files were deleted. Use --delete to remove them.")

if __name__ == "__main__":
    main()
