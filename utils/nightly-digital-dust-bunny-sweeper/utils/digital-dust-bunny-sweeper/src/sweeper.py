import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        # Mock rationale: os.path.getmtime is a system call, needs to be mocked for deterministic tests.
        # We'll mock this to return specific timestamps for testing file age.
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or non-existent file

def is_empty_dir(path):
    """Checks if a directory is empty."""
    # Mock rationale: os.listdir is a system call, needs to be mocked for deterministic tests.
    # We'll mock this to return specific directory contents for testing empty directories.
    return not os.listdir(path)

def find_dust_bunnies(root_path, age_threshold_days, verbose=False):
    """
    Scans a directory for old files and empty directories.
    Returns lists of (filepath, age_days) for old files and (dirpath) for empty directories.
    """
    old_files = []
    empty_dirs = []
    
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return [], []

    if verbose:
        print(f"Scanning '{root_path}' for dust bunnies (files older than {age_threshold_days} days and empty directories)...")

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Check for old files
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            age = get_file_age_days(filepath)
            if age >= age_threshold_days:
                old_files.append((filepath, age))
                if verbose:
                    print(f"  Found old file: {filepath} ({age:.1f} days old)")
        
        # Check for empty directories (only if they are truly empty after processing files/subdirs)
        # We use topdown=False in os.walk to ensure subdirectories are processed first.
        # This way, when we check a directory, its contents (if any) would have already been processed.
        if is_empty_dir(dirpath) and dirpath != root_path: # Don't mark the root path itself as an empty dir to delete
            empty_dirs.append(dirpath)
            if verbose:
                print(f"  Found empty directory: {dirpath}")

    return old_files, empty_dirs

def delete_dust_bunnies(old_files, empty_dirs, verbose=False):
    """Deletes the identified old files and empty directories."""
    deleted_count = 0
    
    for filepath, _ in old_files:
        try:
            # Mock rationale: os.remove is a system call, needs to be mocked for deterministic tests.
            # We'll mock this to simulate file deletion without actual file system changes.
            os.remove(filepath)
            if verbose:
                print(f"  Deleted file: {filepath}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting file {filepath}: {e}")

    # Delete empty directories, starting from deepest
    # os.walk with topdown=False already gives us this order
    for dirpath in empty_dirs:
        try:
            # Mock rationale: os.rmdir is a system call, needs to be mocked for deterministic tests.
            # We'll mock this to simulate directory deletion without actual file system changes.
            os.rmdir(dirpath)
            if verbose:
                print(f"  Deleted empty directory: {dirpath}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting directory {dirpath}: {e}")
            
    return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Cleans up old files and empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="Files older than this many days will be considered dust bunnies. Default is 90 days."
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="If set, the utility will only report findings and not delete anything. This is the default behavior if --delete is not specified."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, the utility will prompt for confirmation before deleting identified dust bunnies. Use with caution!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed output during scanning and deletion."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The provided path '{args.path}' is not a valid directory.")
        exit(1)

    if args.delete and args.report_only:
        print("Error: Cannot use --delete and --report-only simultaneously. Choose one.")
        exit(1)

    old_files, empty_dirs = find_dust_bunnies(args.path, args.age, args.verbose)

    if not old_files and not empty_dirs:
        print("\n✨ All clear! No digital dust bunnies found. Your workspace is sparkling clean.")
        exit(0)

    print("\n--- Digital Dust Bunny Report ---")
    if old_files:
        print(f"\nFound {len(old_files)} old files (older than {args.age} days):")
        for filepath, age in old_files:
            print(f"  - {filepath} ({age:.1f} days old)")
    
    if empty_dirs:
        print(f"\nFound {len(empty_dirs)} empty directories:")
        for dirpath in empty_dirs:
            print(f"  - {dirpath}")

    if args.delete:
        print("\n⚠️  WARNING: You are about to delete the identified dust bunnies.")
        confirmation = input("Type 'YES' to proceed with deletion: ")
        if confirmation == "YES":
            deleted_count = delete_dust_bunnies(old_files, empty_dirs, args.verbose)
            print(f"\n🧹 Cleanup complete! {deleted_count} digital dust bunnies swept away.")
        else:
            print("\n🚫 Deletion cancelled. No changes made.")
            exit(2) # No-op exit code
    else:
        print("\nTo delete these dust bunnies, run again with the --delete flag.")
        print("Remember to use --report-only first to review what will be deleted.")
        exit(0) # Report-only is a successful operation

if __name__ == "__main__":
    main()
