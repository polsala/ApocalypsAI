import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """
    Calculates the age of a file in days.
    """
    try:
        mtime = os.path.getmtime(filepath)
        file_datetime = datetime.fromtimestamp(mtime)
        now = datetime.now()
        age = now - file_datetime
        return age.days
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible
    except Exception as e:
        print(f"Error getting age for {filepath}: {e}")
        return -1

def find_old_files(paths, older_than_days):
    """
    Scans specified paths for files older than a given number of days.
    Returns a list of file paths.
    """
    old_files = []
    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        print(f"Scanning '{path}' for files older than {older_than_days} days...")
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                age_in_days = get_file_age_in_days(filepath)
                if age_in_days >= older_than_days:
                    old_files.append(filepath)
    return old_files

def delete_files(file_list, dry_run, confirm_delete):
    """
    Deletes files from the given list, with dry-run and confirmation options.
    """
    if not file_list:
        print("No old files found to delete. Your digital space is pristine!")
        return

    print(f"\nFound {len(file_list)} potential digital dust bunnies:")
    for i, filepath in enumerate(file_list):
        print(f"  {i+1}. {filepath} (Age: {get_file_age_in_days(filepath)} days)")

    if dry_run:
        print("\n--- Dry Run Complete ---")
        print("No files were deleted. Run without --dry-run to perform actual deletion.")
        return

    if not confirm_delete:
        response = input("\nDo you want to delete these files? (y/N): ").lower()
        if response != 'y':
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
    print(f"\n--- Deletion Complete ---")
    print(f"Successfully deleted {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Find and delete old, unused files."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--older-than",
        type=int,
        default=90,
        help="Only consider files older than this many days (default: 90)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a scan and list files, but do not delete anything."
    )
    parser.add_argument(
        "--confirm-delete",
        action="store_true",
        help="Automatically confirm deletion of all found files without prompting. Use with caution!"
    )

    args = parser.parse_args()

    if args.confirm_delete and args.dry_run:
        print("Error: Cannot use --confirm-delete with --dry-run simultaneously.")
        return

    old_files = find_old_files(args.path, args.older_than)
    delete_files(old_files, args.dry_run, args.confirm_delete)

if __name__ == "__main__":
    main()
