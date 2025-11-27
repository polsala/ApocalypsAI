import os
import time
import argparse
from datetime import datetime, timedelta

def get_old_files(directory: str, days_threshold: int, verbose: bool = False) -> list[str]:
    """
    Scans a directory for files older than a specified number of days.

    Args:
        directory: The root directory to scan.
        days_threshold: Files modified more than this many days ago are considered old.
        verbose: If True, print more details during scanning.

    Returns:
        A list of absolute paths to old files.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return []

    old_files = []
    current_time = time.time()
    threshold_timestamp = current_time - (days_threshold * 24 * 60 * 60)

    if verbose:
        print(f"Scanning '{directory}' for files older than {days_threshold} days...")

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Use modification time (mtime) as it's generally more reliable for "last changed"
                # than access time (atime) which can be updated by simple reads.
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < threshold_timestamp:
                    old_files.append(file_path)
                    if verbose:
                        mod_date = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        print(f"  Found old file: {file_path} (Modified: {mod_date})")
            except OSError as e:
                print(f"Warning: Could not access file '{file_path}': {e}")
                continue
    return old_files

def delete_files(file_paths: list[str], verbose: bool = False) -> None:
    """
    Deletes a list of files.

    Args:
        file_paths: A list of absolute paths to files to delete.
        verbose: If True, print details about each deletion.
    """
    if not file_paths:
        print("No files to delete.")
        return

    print(f"\nAttempting to delete {len(file_paths)} files...")
    deleted_count = 0
    for file_path in file_paths:
        try:
            os.remove(file_path)
            deleted_count += 1
            if verbose:
                print(f"  Deleted: {file_path}")
        except OSError as e:
            print(f"Error: Could not delete '{file_path}': {e}")
    print(f"Successfully deleted {deleted_count} out of {len(file_paths)} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Debris Duster: Identify and optionally delete old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="The age threshold in days. Files modified more than this many days ago will be considered 'debris'."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, the utility will prompt for confirmation before deleting the identified files. Use with caution!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed output during scanning and deletion."
    )

    args = parser.parse_args()

    old_files = get_old_files(args.path, args.days, args.verbose)

    if not old_files:
        print(f"No files older than {args.days} days found in '{args.path}'. Your data is pristine!")
        return

    print(f"\nFound {len(old_files)} files older than {args.days} days:")
    for f in old_files:
        print(f"- {f}")

    if args.delete:
        confirmation = input("\nAre you sure you want to delete these files? Type 'yes' to confirm: ")
        if confirmation.lower() == 'yes':
            delete_files(old_files, args.verbose)
        else:
            print("Deletion cancelled.")
    else:
        print("\nRun with --delete to remove these files.")

if __name__ == "__main__":
    main()
