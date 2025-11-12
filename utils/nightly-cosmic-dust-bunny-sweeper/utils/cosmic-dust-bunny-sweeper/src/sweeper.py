import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    if not os.path.exists(filepath):
        return -1 # Indicate file not found
    mtime = os.path.getmtime(filepath)
    file_datetime = datetime.fromtimestamp(mtime)
    current_datetime = datetime.now()
    return (current_datetime - file_datetime).days

def is_empty_dir(path):
    """Checks if a directory is empty."""
    if not os.path.isdir(path):
        return False
    return not os.listdir(path)

def find_dust_bunnies(root_path, age_threshold_days):
    """Finds old files and empty directories within a root path."""
    old_files = []
    empty_dirs = []

    if not os.path.exists(root_path):
        print(f"Error: Path '{root_path}' does not exist.")
        return old_files, empty_dirs

    # Walk the directory tree from bottom-up (topdown=False) to ensure child directories are processed before parents.
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Check for old files
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                age = get_file_age_days(filepath)
                if age >= age_threshold_days:
                    old_files.append(filepath)
        
        # Check for empty directories. Only consider directories that are not the root_path itself.
        # This prevents the utility from deleting the target root if it becomes empty.
        if dirpath != root_path and is_empty_dir(dirpath):
            empty_dirs.append(dirpath)

    return old_files, empty_dirs

def sweep_bunnies(old_files, empty_dirs, dry_run):
    """Deletes the identified old files and empty directories."""
    if dry_run:
        print("\n--- DRY RUN MODE --- No changes will be made ---")

    print(f"\nFound {len(old_files)} old files to {'list' if dry_run else 'delete'}:")
    if old_files:
        for f in old_files:
            print(f"  - {f}")
            if not dry_run:
                try:
                    os.remove(f)
                except OSError as e:
                    print(f"    Error deleting file {f}: {e}")
    else:
        print("  No old files found.")

    print(f"\nFound {len(empty_dirs)} empty directories to {'list' if dry_run else 'delete'}:")
    if empty_dirs:
        # Sort in reverse order of path length to delete deepest directories first.
        # This prevents 'Directory not empty' errors if a parent directory is attempted before its children.
        empty_dirs.sort(key=len, reverse=True)
        for d in empty_dirs:
            print(f"  - {d}")
            if not dry_run:
                try:
                    # Re-check if directory is still empty before removing, as other processes might have added files.
                    if is_empty_dir(d):
                        os.rmdir(d)
                    else:
                        print(f"    Skipping {d}: no longer empty.")
                except OSError as e:
                    print(f"    Error deleting directory {d}: {e}")
    else:
        print("  No empty directories found.")

    if dry_run:
        print("\n--- DRY RUN COMPLETE --- No changes were made ---")
    else:
        print("\n--- SWEEP COMPLETE ---")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Sweeper: Cleans old files and empty directories."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to start sweeping from."
    )
    parser.add_argument(
        "--age", 
        type=int, 
        default=30, 
        help="Files older than this many days will be considered 'dust bunnies'. Default: 30."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="If present, only list what would be deleted, without making changes."
    )

    args = parser.parse_args()

    print(f"Starting Cosmic Dust Bunny Sweep in '{args.path}' (age threshold: {args.age} days)...\n")

    old_files, empty_dirs = find_dust_bunnies(args.path, args.age)
    sweep_bunnies(old_files, empty_dirs, args.dry_run)

if __name__ == "__main__":
    main()
