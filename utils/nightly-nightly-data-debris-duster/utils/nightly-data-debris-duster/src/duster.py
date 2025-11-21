import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days based on its last modification time."""
    mod_timestamp = os.path.getmtime(filepath)
    mod_datetime = datetime.fromtimestamp(mod_timestamp)
    current_datetime = datetime.now()
    age = current_datetime - mod_datetime
    return age.days

def find_old_files(directory, days_old, recursive=False):
    """
    Finds files in a directory (and optionally subdirectories) that are older than `days_old`.
    Returns a list of file paths.
    """
    old_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.exists(filepath) and os.path.isfile(filepath):
                if get_file_age_in_days(filepath) >= days_old:
                    old_files.append(filepath)
        if not recursive:
            break # Only process the top-level directory if not recursive
    return old_files

def delete_files(file_list, force=False):
    """
    Deletes files from the given list. Prompts for confirmation unless `force` is True.
    """
    if not file_list:
        print("No files to delete.")
        return

    print(f"\nIdentified {len(file_list)} files for deletion:")
    for f in file_list:
        print(f"- {f}")

    if not force:
        confirmation = input("\nAre you sure you want to delete these files? (yes/no): ").lower()
        if confirmation != 'yes':
            print("Deletion cancelled.")
            return

    deleted_count = 0
    for filepath in file_list:
        try:
            os.remove(filepath)
            print(f"Deleted: {filepath}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting {filepath}: {e}")
    print(f"\nSuccessfully deleted {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Debris Duster: Identify and optionally remove old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for old files."
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="The minimum age in days for a file to be considered 'debris'."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If present, identified files will be deleted. Use with caution!"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="If present, the duster will scan subdirectories as well."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If present with --delete, files will be deleted without a confirmation prompt."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.")
        exit(1)

    print(f"Scanning '{args.path}' for files older than {args.days} days...")
    old_files = find_old_files(args.path, args.days, args.recursive)

    if not old_files:
        print("No old files found matching the criteria. Your digital wasteland is surprisingly clean!")
        exit(0)

    if args.delete:
        delete_files(old_files, args.force)
    else:
        print(f"\nFound {len(old_files)} files older than {args.days} days (use --delete to remove them):")
        for f in old_files:
            print(f"- {f}")
        print("\nNo files were deleted. To delete, run again with the --delete flag.")

if __name__ == "__main__":
    main()
