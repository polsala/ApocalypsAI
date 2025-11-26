import os
import argparse
import fnmatch
import time
from datetime import datetime, timedelta

def get_files_to_clean(root_path, patterns, min_age_days):
    """
    Identifies files within root_path that match patterns and are older than min_age_days.
    Returns a list of file paths.
    """
    files_to_delete = []
    now = datetime.now()
    age_threshold_timestamp = (now - timedelta(days=min_age_days)).timestamp()

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Check if file matches any pattern
            matches_pattern = False
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    matches_pattern = True
                    break
            
            if not matches_pattern:
                continue

            # Check file age
            try:
                mtime = os.path.getmtime(full_path)
                if mtime < age_threshold_timestamp:
                    files_to_delete.append(full_path)
            except OSError:
                # File might have been deleted between os.walk and os.path.getmtime
                continue
    return files_to_delete

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Cleaner of Forgotten Files: Cleans up old, temporary, or specified files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start cleaning from. The cleaner will recursively scan this directory."
    )
    parser.add_argument(
        "--patterns",
        required=True,
        help="A comma-separated list of glob patterns (e.g., '*.tmp,*.log'). Files matching any of these patterns will be considered for deletion."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be considered for deletion."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the utility will only list files that *would* be deleted, without actually removing them."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If present, skips the confirmation prompt before deleting files. Use with caution!"
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    patterns = [p.strip() for p in args.patterns.split(',')]
    min_age_days = args.age
    dry_run = args.dry_run
    force_delete = args.force

    if not os.path.isdir(root_path):
        print(f"Error: The specified path '{root_path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{root_path}' for files matching patterns {patterns} and older than {min_age_days} days...")
    files_to_delete = get_files_to_clean(root_path, patterns, min_age_days)

    if not files_to_delete:
        print("No forgotten files found matching the criteria. Your digital space is pristine!")
        exit(0)

    print(f"\nFound {len(files_to_delete)} forgotten files:")
    for f in files_to_delete:
        print(f"- {f}")

    if dry_run:
        print("\nThis was a DRY RUN. No files were deleted.")
        exit(0)

    if not force_delete:
        confirmation = input(f"\nDo you want to permanently delete these {len(files_to_delete)} files? (yes/no): ").lower()
        if confirmation != 'yes':
            print("Deletion cancelled.")
            exit(2) # No-op, nothing changed

    print("\nInitiating deletion...")
    deleted_count = 0
    for f in files_to_delete:
        try:
            os.remove(f)
            print(f"Deleted: {f}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting {f}: {e}")
    
    print(f"\nClean-up complete. Successfully deleted {deleted_count} files.")
    exit(0)

if __name__ == "__main__":
    main()
