import os
import shutil
import argparse
from datetime import datetime, timedelta

# Define common "dust bunny" patterns
# Directories to remove entirely
DIR_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "target",  # Common for Java/Rust builds
    "dist",
    "build",
    ".venv",  # Be careful with this one, only if not active
    ".mypy_cache",
    ".gradle",
    "tmp",
    "temp",
]

# Files to remove based on name or extension
FILE_PATTERNS = [
    ".DS_Store",
    "Thumbs.db",
    "*.tmp",
    "*.log",
    "*.bak",
    "*.swp",
]

def is_old_enough(filepath, age_days):
    """Checks if a file is older than a specified number of days."""
    if age_days <= 0:
        return True # No age limit
    try:
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        return (datetime.now() - mod_time) > timedelta(days=age_days)
    except OSError:
        return False # File might not exist or permissions issue

def find_dust_bunnies(root_path, age_days=7):
    """
    Scans the root_path for common temporary and cache files/directories.
    Returns a list of paths to be considered for deletion.
    """
    dust_bunnies = []
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    print(f"Scanning '{root_path}' for digital dust bunnies...")

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check for directories to remove
        for dname in list(dirnames): # Iterate over a copy to allow modification
            if dname in DIR_PATTERNS:
                full_path = os.path.join(dirpath, dname)
                dust_bunnies.append(full_path)
                dirnames.remove(dname) # Don't recurse into this directory
                print(f"  Found directory: {full_path}")

        # Check for files to remove
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            for pattern in FILE_PATTERNS:
                if pattern.startswith('*') and fname.endswith(pattern[1:]):
                    if pattern.endswith('.log') or pattern.endswith('.tmp'):
                        if is_old_enough(full_path, age_days):
                            dust_bunnies.append(full_path)
                            print(f"  Found old file: {full_path}")
                    else:
                        dust_bunnies.append(full_path)
                        print(f"  Found file: {full_path}")
                    break # Found a match, move to next file
                elif fname == pattern:
                    dust_bunnies.append(full_path)
                    print(f"  Found file: {full_path}")
                    break # Found a match, move to next file

    return dust_bunnies

def delete_dust_bunnies(paths):
    """
    Deletes the files and directories specified in the paths list.
    """
    if not paths:
        print("No dust bunnies to delete. Your digital space is sparkling!")
        return

    print("\nInitiating dust bunny purge...")
    deleted_count = 0
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"  Deleted directory: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                print(f"  Deleted file: {path}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting '{path}': {e}")
    print(f"\nPurge complete! {deleted_count} digital dust bunnies removed.")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Duster: Purge temporary and cache files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, actually delete the found dust bunnies. Use with caution!"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would be deleted, without making changes. (Default if --delete is not present)."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=7,
        help="For files like *.log or *.tmp, only consider them dust bunnies if they are older than this many days. Defaults to 7 days."
    )

    args = parser.parse_args()

    if not args.delete and not args.dry_run:
        args.dry_run = True # Default to dry-run if neither delete nor dry-run is specified

    print(f"Digital Dust Bunny Duster is running in {'DRY RUN' if args.dry_run else 'DELETE'} mode.")
    print(f"Scanning path: {args.path}")
    print(f"Age threshold for logs/tmp files: {args.age_days} days")

    dust_bunnies_found = find_dust_bunnies(args.path, args.age_days)

    if dust_bunnies_found:
        print("\n--- Summary of Digital Dust Bunnies Found ---")
        for bunny in dust_bunnies_found:
            print(f"- {bunny}")
        print(f"\nTotal: {len(dust_bunnies_found)} items.")

        if not args.dry_run:
            confirm = input("Are you sure you want to delete these items? (yes/no): ").lower()
            if confirm == 'yes':
                delete_dust_bunnies(dust_bunnies_found)
            else:
                print("Deletion cancelled by user.")
        else:
            print("\n(This was a dry run. No files were deleted.)")
    else:
        print("\nNo digital dust bunnies found. Your digital space is pristine!")

if __name__ == "__main__":
    main()
