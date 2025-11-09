import os
import time
import argparse
import sys
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def find_dust_bunnies(root_path, min_age_days):
    """Scans the given path for empty directories and old temporary files.

    Args:
        root_path (str): The directory to scan.
        min_age_days (int): Minimum age in days for files to be considered old.

    Returns:
        tuple: A tuple containing two lists: (empty_dirs, old_files).
    """
    empty_dirs = []
    old_files = []
    temp_extensions = ('.log', '.tmp', '.bak', '.old', '.swp', '.DS_Store')

    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.", file=sys.stderr)
        return [], []

    # os.walk with topdown=False ensures that subdirectories are visited before their parent directories.
    # This is crucial for correctly identifying truly empty directories, as files/subdirs within them
    # might be removed first.
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Check for old files
        for filename in filenames:
            if filename.lower().endswith(temp_extensions):
                filepath = os.path.join(dirpath, filename)
                age = get_file_age_in_days(filepath)
                if age >= min_age_days:
                    old_files.append(filepath)
        
        # Check for empty directories (after processing its contents)
        # A directory is considered empty if os.listdir returns an empty list.
        # We also ensure the root_path itself isn't marked as an empty directory.
        if not os.listdir(dirpath) and dirpath != root_path:
            empty_dirs.append(dirpath)

    return empty_dirs, old_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital 'dust bunnies' (empty directories and old temporary files)."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help='The root directory to scan. Defaults to current working directory.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        default=90, 
        help='Minimum age (in days) for temporary/log files to be considered old. Defaults to 90.'
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='Enable actual deletion of files and directories. Use with caution!'
    )

    args = parser.parse_args()

    print(f"\n🧹 Initiating Digital Dust Bunny Sweep in '{os.path.abspath(args.path)}'...")
    print(f"   (Looking for files older than {args.age} days and empty directories.)")

    empty_dirs, old_files = find_dust_bunnies(args.path, args.age)

    if not empty_dirs and not old_files:
        print("✨ Your digital space is sparkling clean! No dust bunnies found.")
        return

    print("\n--- Identified Digital Dust Bunnies ---")

    if empty_dirs:
        print("\n👻 Empty Directories:")
        for d in empty_dirs:
            print(f"  - {d}")
    else:
        print("\nNo empty directories found.")

    if old_files:
        print("\n⏳ Old Temporary/Log Files:")
        for f in old_files:
            print(f"  - {f}")
    else:
        print("\nNo old temporary/log files found.")

    print("\n---------------------------------------")

    if args.delete:
        print("\n🗑️ Deleting identified dust bunnies...")
        deleted_count = 0
        for f in old_files:
            try:
                os.remove(f)
                print(f"  ✅ Removed file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  ❌ Failed to remove file {f}: {e}", file=sys.stderr)
        
        # Remove empty directories, starting from deepest to shallowest
        # This prevents errors if a parent directory is attempted before its child.
        for d in sorted(empty_dirs, key=len, reverse=True):
            try:
                # Re-check if it's still empty, as files might have been removed from it
                # or new files might have appeared since the initial scan.
                if not os.listdir(d):
                    os.rmdir(d)
                    print(f"  ✅ Removed empty directory: {d}")
                    deleted_count += 1
                else:
                    print(f"  ⚠️ Directory {d} is no longer empty, skipping removal.")
            except OSError as e:
                print(f"  ❌ Failed to remove directory {d}: {e}", file=sys.stderr)
        
        print(f"\n🎉 Sweep complete! {deleted_count} dust bunnies banished.")
    else:
        print("\n(Dry run complete. To delete these items, run with the '--delete' flag.)")

if __name__ == '__main__':
    main()
