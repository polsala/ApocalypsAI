import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Returns the age of a file in days."""
    mtime = os.path.getmtime(filepath)
    return (time.time() - mtime) / (24 * 3600)

def find_cosmic_dust(path, age_threshold_days=30, temp_extensions=None, exclude_patterns=None):
    """
    Scans a directory for 'cosmic dust':
    - Files matching temporary extensions and older than age_threshold_days.
    - Empty directories.
    """
    if temp_extensions is None:
        temp_extensions = ['.tmp', '.log', '.bak', '.swp', '.temp', '.old']
    if exclude_patterns is None:
        exclude_patterns = []

    dust_files = []
    empty_dirs = []

    for root, dirs, files in os.walk(path, topdown=False): # topdown=False for empty dir detection
        # Check for empty directories
        if not dirs and not files:
            is_excluded = False
            for pattern in exclude_patterns:
                if pattern in root:
                    is_excluded = True
                    break
            if not is_excluded:
                empty_dirs.append(root)

        # Check for temporary files
        for file in files:
            filepath = os.path.join(root, file)
            is_temp_file = any(file.endswith(ext) for ext in temp_extensions)
            is_old_file = False
            try:
                if os.path.isfile(filepath): # Ensure it's a file before checking age
                    is_old_file = get_file_age_in_days(filepath) > age_threshold_days
            except OSError:
                # Handle cases where file might be deleted between os.walk and os.path.isfile
                continue

            is_excluded = False
            for pattern in exclude_patterns:
                if pattern in filepath:
                    is_excluded = True
                    break

            if is_temp_file and is_old_file and not is_excluded:
                dust_files.append(filepath)
    
    return dust_files, empty_dirs

def clean_cosmic_dust(dust_files, empty_dirs, dry_run=True):
    """
    Removes identified cosmic dust.
    If dry_run is True, only prints what would be removed.
    """
    print(f"--- Cosmic Dust Collection Report ({'Dry Run' if dry_run else 'Cleaning'}) ---")
    
    if not dust_files and not empty_dirs:
        print("No cosmic dust detected. Your digital cosmos is pristine!")
        return

    if dust_files:
        print("\nFiles to be swept away:")
        for f in dust_files:
            print(f"  - {f}")
            if not dry_run:
                try:
                    os.remove(f)
                    print(f"    [REMOVED] {f}")
                except OSError as e:
                    print(f"    [ERROR] Could not remove {f}: {e}")
    else:
        print("\nNo old temporary files found.")

    if empty_dirs:
        print("\nEmpty directories to be collapsed:")
        # Sort from deepest to shallowest to ensure parent dirs are empty when removed
        empty_dirs.sort(key=lambda x: x.count(os.sep), reverse=True)
        for d in empty_dirs:
            print(f"  - {d}")
            if not dry_run:
                try:
                    os.rmdir(d)
                    print(f"    [REMOVED] {d}")
                except OSError as e:
                    print(f"    [ERROR] Could not remove {d}: {e}")
    else:
        print("\nNo empty directories found.")

    print("\n--- Collection Complete ---")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: A whimsical utility to clean up temporary files and empty directories."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The path to scan for cosmic dust (default: current directory)."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Minimum age in days for temporary files to be considered dust (default: 30)."
    )
    parser.add_argument(
        "--extensions",
        nargs=".",
        default=['.tmp', '.log', '.bak', '.swp', '.temp', '.old'],
        help="List of file extensions to consider as temporary (default: .tmp .log .bak .swp .temp .old)."
    )
    parser.add_argument(
        "--exclude",
        nargs=".",
        default=[],
        help="List of path patterns to exclude from scanning (e.g., 'node_modules', '.git')."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Perform actual cleanup (delete files/directories). By default, it's a dry run."
    )

    args = parser.parse_args()

    print(f"Scanning '{os.path.abspath(args.path)}' for cosmic dust...")
    dust_files, empty_dirs = find_cosmic_dust(
        args.path,
        age_threshold_days=args.age,
        temp_extensions=args.extensions,
        exclude_patterns=args.exclude
    )
    clean_cosmic_dust(dust_files, empty_dirs, dry_run=not args.clean)

if __name__ == "__main__":
    main()
