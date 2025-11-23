import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def should_delete_file(file_path, age_days, include_patterns, exclude_patterns, current_time):
    """Determines if a file should be deleted based on age and patterns."""
    try:
        mod_time_timestamp = os.path.getmtime(file_path)
        mod_datetime = datetime.fromtimestamp(mod_time_timestamp)
    except OSError:
        # File might have been deleted between os.walk and getmtime, or permissions issue
        return False

    # Check age
    if (current_time - mod_datetime).days < age_days:
        return False

    file_name = os.path.basename(file_path)

    # Check exclude patterns first (they take precedence)
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_name, pattern):
            return False

    # Check include patterns (if any are specified)
    if include_patterns:
        for pattern in include_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True # Matched an include pattern, and not excluded
        return False # No include patterns matched, so don't delete

    # If no include patterns, and not excluded, then it's eligible by default
    return True

def clean_directory(path, age_days, dry_run, include_patterns, exclude_patterns):
    """Scans a directory and deletes old files based on criteria."""
    if not os.path.isdir(path):
        print(f"Error: Directory not found or not accessible: {path}")
        return

    print(f"{'[DRY RUN] ' if dry_run else ''}Scanning '{path}' for files older than {age_days} days...")
    deleted_count = 0
    current_time = datetime.now()

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if should_delete_file(file_path, age_days, include_patterns, exclude_patterns, current_time):
                if dry_run:
                    print(f"[DRY RUN] Would delete: {file_path}")
                else:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                        deleted_count += 1
                    except OSError as e:
                        print(f"Error deleting {file_path}: {e}")
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Finished. {'Would delete' if dry_run else 'Deleted'} {deleted_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Cleaner of Forgotten Files - Purge old files based on age and patterns."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The root directory to start scanning for old files."
    )
    parser.add_argument(
        "--age-days", 
        type=int, 
        required=True, 
        help="Files older than this many days will be considered for deletion."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="If present, only print what would be deleted, without actual deletion."
    )
    parser.add_argument(
        "--include-patterns", 
        nargs='*', 
        default=[], 
        help="One or more glob patterns (e.g., '*.tmp', 'cache/*') to ONLY consider files matching these patterns."
    )
    parser.add_argument(
        "--exclude-patterns", 
        nargs='*', 
        default=[], 
        help="One or more glob patterns to IGNORE files matching these patterns. Takes precedence over --include-patterns."
    )

    args = parser.parse_args()

    clean_directory(
        args.path,
        args.age_days,
        args.dry_run,
        args.include_patterns,
        args.exclude_patterns
    )

if __name__ == "__main__":
    main()
