import os
import time
import argparse
from datetime import datetime, timedelta

def get_old_files(directory, days_old):
    """
    Scans a directory for files older than a specified number of days.
    Returns a list of (filepath, last_modified_timestamp) tuples.
    """
    cutoff_time = datetime.now() - timedelta(days=days_old)
    old_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Get last modification time
                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < cutoff_time:
                    old_files.append((filepath, mod_timestamp))
            except OSError as e:
                print(f"Warning: Could not access {filepath} - {e}")
                continue
    return old_files

def delete_files(files_to_delete, dry_run, force):
    """
    Deletes the specified files, with dry-run and confirmation options.
    """
    if not files_to_delete:
        print("No old files found to delete. Your digital bunker is pristine!")
        return

    print(f"Found {len(files_to_delete)} ancient files for potential purging:")
    for filepath, mod_timestamp in files_to_delete:
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        print(f"  - {filepath} (Last modified: {mod_datetime.strftime('%Y-%m-%d')})")

    if dry_run:
        print("\nDry run complete. No files were deleted.")
        return

    if not force:
        confirmation = input("\nProceed with deletion? (y/N): ").strip().lower()
        if confirmation != 'y':
            print("Deletion aborted. Your files live to see another day... for now.")
            return

    deleted_count = 0
    for filepath, _ in files_to_delete:
        try:
            os.remove(filepath)
            print(f"Purged: {filepath}")
            deleted_count += 1
        except OSError as e:
            print(f"Error purging {filepath}: {e}")

    print(f"\nCataclysmic cleanup complete! {deleted_count} files purged.")

def main():
    parser = argparse.ArgumentParser(
        description="Cataclysmic Cache Cleaner: Purge ancient files from your system."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan for old files. Can be specified multiple times."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Files older than this many days will be targeted. Default: 30."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a scan and report, but don't delete anything."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip interactive confirmation prompts and delete immediately."
    )

    args = parser.parse_args()

    all_old_files = []
    for path in args.path:
        if not os.path.isdir(path):
            print(f"Error: Path '{path}' is not a valid directory. Skipping.")
            continue
        print(f"Scanning '{path}' for files older than {args.days} days...")
        all_old_files.extend(get_old_files(path, args.days))

    delete_files(all_old_files, args.dry_run, args.force)

if __name__ == "__main__":
    main()
