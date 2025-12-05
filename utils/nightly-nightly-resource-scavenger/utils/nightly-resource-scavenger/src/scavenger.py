import os
import time
import argparse
from datetime import datetime, timedelta

def find_old_files(directory, days_old, patterns=None):
    """
    Finds files in a directory (and its subdirectories) older than a specified number of days.
    Optionally filters by file name patterns.
    """
    cutoff_timestamp = (datetime.now() - timedelta(days=days_old)).timestamp()
    old_files = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Mock rationale: os.path.getmtime accesses the filesystem.
                # In tests, we will mock this to return controlled timestamps.
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_timestamp:
                    if patterns:
                        if any(pattern in file_name for pattern in patterns):
                            old_files.append(file_path)
                    else:
                        old_files.append(file_path)
            except OSError:
                # File might have been deleted between os.walk and os.path.getmtime
                continue
    return old_files

def delete_files(file_paths, dry_run=True):
    """
    Deletes a list of files. If dry_run is True, only prints what would be deleted.
    """
    if not file_paths:
        print("No files to process.")
        return 0

    print(f"{'DRY RUN: ' if dry_run else ''}Processing {len(file_paths)} files...")
    deleted_count = 0
    for file_path in file_paths:
        if dry_run:
            print(f"  Would delete: {file_path}")
        else:
            try:
                # Mock rationale: os.remove modifies the filesystem.
                # In tests, we will mock this to verify calls without actual deletion.
                os.remove(file_path)
                print(f"  Deleted: {file_path}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting {file_path}: {e}")
    print(f"Operation complete. {'Would have deleted' if dry_run else 'Deleted'} {deleted_count} files.")
    return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Scavenger: Cleans up old and temporary files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--days-old",
        type=int,
        default=30,
        help="Files older than this many days will be considered for cleanup. Default is 30."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        nargs='*',
        help="Optional: Space-separated list of patterns (substrings) to match in filenames. E.g., '.tmp' 'cache_'. If not provided, all old files are considered."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Perform actual deletion. By default, it's a dry run (only lists files)."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for files older than {args.days_old} days...")
    if args.patterns:
        print(f"  Filtering by patterns: {', '.join(args.patterns)}")

    found_files = find_old_files(args.directory, args.days_old, args.patterns)

    if found_files:
        print(f"\nFound {len(found_files)} files matching criteria:")
        delete_files(found_files, dry_run=not args.delete)
    else:
        print("No files found matching the criteria.")

if __name__ == "__main__":
    main()
