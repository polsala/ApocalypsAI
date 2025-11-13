import os
import time
import argparse
from datetime import datetime, timedelta

def find_old_files(directory: str, age_days: int) -> list[str]:
    """
    Recursively finds files in a directory that are older than a specified age.

    Args:
        directory: The root directory to scan.
        age_days: The minimum age in days for a file to be considered old.

    Returns:
        A list of absolute paths to old files.
    """
    old_files = []
    cutoff_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()

    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Use getmtime (last modification time) as a proxy for "last used" or "relevant"
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_timestamp:
                    old_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access file {file_path}: {e}")
                continue
    return old_files

def delete_files(file_paths: list[str]) -> None:
    """
    Deletes a list of files.

    Args:
        file_paths: A list of absolute paths to files to delete.
    """
    if not file_paths:
        print("No files to delete.")
        return

    print(f"Attempting to delete {len(file_paths)} files...")
    deleted_count = 0
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
    print(f"Successfully deleted {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Find and delete old, unused files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="The minimum age in days for a file to be considered 'old' (default: 90)."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Enable actual file deletion. If omitted, only a dry run is performed."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for files older than {args.age} days...")
    old_files = find_old_files(args.path, args.age)

    if not old_files:
        print("No digital dust bunnies found! Your specified directory is sparkling clean.")
        return

    print(f"\nFound {len(old_files)} old files (digital dust bunnies):")
    for file_path in old_files:
        print(f"  - {file_path}")

    if args.delete:
        print("\n--- DELETION MODE ACTIVATED ---")
        delete_files(old_files)
    else:
        print("\nThis was a DRY RUN. No files were deleted.")
        print("To delete these files, run the command again with the --delete flag.")

if __name__ == "__main__":
    main()
