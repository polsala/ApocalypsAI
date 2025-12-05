import os
import shutil
import argparse
import fnmatch
from datetime import datetime, timedelta

def is_older_than_threshold(filepath, threshold_datetime):
    """Checks if a file's modification time is older than the given threshold_datetime."""
    try:
        mtime_timestamp = os.path.getmtime(filepath)
        mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
        return mtime_datetime < threshold_datetime
    except OSError:
        # File might have been deleted between os.walk and os.path.getmtime
        return False

def matches_patterns(filepath, include_patterns, exclude_patterns):
    """Checks if a file matches any include patterns and no exclude patterns."""
    filename = os.path.basename(filepath)
    
    # If include patterns are specified, file must match at least one
    if include_patterns:
        if not any(fnmatch.fnmatch(filepath, p) or fnmatch.fnmatch(filename, p) for p in include_patterns):
            return False
    
    # If exclude patterns are specified, file must not match any
    if exclude_patterns:
        if any(fnmatch.fnmatch(filepath, p) or fnmatch.fnmatch(filename, p) for p in exclude_patterns):
            return False
            
    return True

def find_old_items(root_path, age_days, include_patterns, exclude_patterns):
    """Finds files and directories older than age_days, respecting patterns."""
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    threshold_datetime = datetime.now() - timedelta(days=age_days)
    items_to_clean = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False): # topdown=False for safe dir removal
        # Check files
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if is_older_than_threshold(filepath, threshold_datetime) and \
               matches_patterns(filepath, include_patterns, exclude_patterns):
                items_to_clean.append(filepath)
        
        # Check directories (only if empty or all its contents are also to be cleaned)
        # This is a simplification: we'll add directories if they are old and empty
        # or if all their contents have been marked for deletion. For simplicity, 
        # we'll just check if the directory itself is old and empty after files are processed.
        # A more robust solution would track if a directory becomes empty *because* its files were deleted.
        # For this utility, we'll check directories after their contents are processed.
        for dirname in dirnames:
            dirpath_full = os.path.join(dirpath, dirname)
            if is_older_than_threshold(dirpath_full, threshold_datetime) and \
               matches_patterns(dirpath_full, include_patterns, exclude_patterns):
                # Only add directory if it's empty or will become empty
                # This check is tricky with os.walk(topdown=False) and needs careful handling.
                # For now, we'll just add old, empty directories.
                if not os.listdir(dirpath_full): # Check if directory is empty
                    items_to_clean.append(dirpath_full)

    # Sort items to ensure files are deleted before their parent directories
    # and deeper paths are deleted before shallower ones.
    items_to_clean.sort(key=lambda x: (len(x.split(os.sep)), x), reverse=True)
    
    # Filter out items that are parents of already marked items
    final_items_to_clean = []
    seen_parents = set()
    for item in items_to_clean:
        is_child_of_marked_parent = False
        for parent in seen_parents:
            if item.startswith(parent + os.sep):
                is_child_of_marked_parent = True
                break
        if not is_child_of_marked_parent:
            final_items_to_clean.append(item)
            seen_parents.add(item)
            
    return final_items_to_clean

def clean_items(items_to_clean, dry_run):
    """Performs deletion or reports actions based on dry_run flag."""
    if not items_to_clean:
        print("No old items found to clean.")
        return

    action_word = "Would delete" if dry_run else "Deleting"
    print(f"\n--- {action_word} {len(items_to_clean)} items ---")

    for item_path in items_to_clean:
        try:
            if os.path.isfile(item_path):
                print(f"{action_word} file: {item_path}")
                if not dry_run:
                    os.remove(item_path)
            elif os.path.isdir(item_path):
                print(f"{action_word} directory: {item_path}")
                if not dry_run:
                    shutil.rmtree(item_path)
            else:
                print(f"Skipping unknown item type: {item_path}")
        except OSError as e:
            print(f"Error {action_word.lower()} {item_path}: {e}")

    print(f"--- Finished {action_word.lower()} ---")

def main():
    parser = argparse.ArgumentParser(
        description="Chronos Cache Cleaner: Identify and clean old files/directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        required=True,
        help="Files/directories older than this many days will be considered for cleaning."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True, # Default to dry-run for safety
        help="Perform a dry run (default). List items that would be deleted without actually deleting them."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified files and directories. Use with extreme caution."
    )
    parser.add_argument(
        "--include",
        type=str,
        action="append",
        default=[],
        help="Glob pattern to include files/directories. Can be specified multiple times."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        action="append",
        default=[],
        help="Glob pattern to exclude files/directories. Can be specified multiple times."
    )

    args = parser.parse_args()

    if args.delete and args.dry_run:
        print("Error: Cannot use --delete and --dry-run simultaneously. Choose one.")
        exit(1)
    
    # If --delete is specified, override default --dry-run behavior
    actual_dry_run = args.dry_run if not args.delete else False

    print(f"Scanning '{args.path}' for items older than {args.age_days} days...")
    if args.include: print(f"Including patterns: {args.include}")
    if args.exclude: print(f"Excluding patterns: {args.exclude}")
    print(f"Mode: {'Dry Run' if actual_dry_run else 'Deletion'}")

    items = find_old_items(args.path, args.age_days, args.include, args.exclude)
    clean_items(items, actual_dry_run)

if __name__ == "__main__":
    main()
