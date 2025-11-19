import os
import time
import argparse
from datetime import datetime, timedelta

def get_current_time_timestamp():
    """Helper to get current time as a timestamp. Mockable for tests."""
    return time.time()

def get_file_modification_time(filepath):
    """Helper to get file modification time. Mockable for tests."""
    return os.path.getmtime(filepath)

def scan_directory(root_path):
    """Scans a directory for all files and returns their full paths."""
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    found_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            found_files.append(full_path)
    return found_files

def filter_by_age(files, days_old):
    """Filters a list of files, returning only those older than specified days."""
    current_timestamp = get_current_time_timestamp()
    cutoff_timestamp = current_timestamp - (days_old * 24 * 60 * 60)

    forgotten_files = []
    for filepath in files:
        try:
            mod_timestamp = get_file_modification_time(filepath)
            if mod_timestamp < cutoff_timestamp:
                forgotten_files.append(filepath)
        except OSError as e:
            print(f"Warning: Could not get modification time for '{filepath}': {e}")
    return forgotten_files

def delete_files(files, dry_run, confirm):
    """Deletes the specified files, with dry-run and confirmation options."""
    if not files:
        print("No forgotten files found to delete.")
        return

    print(f"\nFound {len(files)} forgotten files:")
    for f in files:
        print(f"  - {f} (Last modified: {datetime.fromtimestamp(get_file_modification_time(f)).strftime('%Y-%m-%d %H:%M:%S')})")

    if dry_run:
        print("\nDry run complete. No files were actually deleted.")
        return

    if not confirm:
        response = input("\nDo you want to proceed with deleting these files? (yes/no): ").lower()
        if response != 'yes':
            print("Deletion cancelled.")
            return

    print("\nProceeding with deletion...")
    deleted_count = 0
    for filepath in files:
        try:
            os.remove(filepath)
            print(f"  Deleted: {filepath}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting '{filepath}': {e}")
    print(f"\nDeletion complete. Successfully deleted {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility to forage for and remove old, forgotten files."
    )
    parser.add_argument("--path", required=True, help="The root directory to start foraging from.")
    parser.add_argument("--days", type=int, default=30, help="Files older than this many days will be considered 'forgotten'. Defaults to 30 days.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the deletion process without actually removing any files.")
    parser.add_argument("--confirm", action="store_true", help="Proceed with deletion without asking for confirmation (use with caution!).")

    args = parser.parse_args()

    print(f"Foraging for files older than {args.days} days in '{args.path}'...")

    all_files = scan_directory(args.path)
    if not all_files:
        print("No files found in the specified directory.")
        return

    forgotten_files = filter_by_age(all_files, args.days)

    delete_files(forgotten_files, args.dry_run, args.confirm)

if __name__ == "__main__":
    main()
