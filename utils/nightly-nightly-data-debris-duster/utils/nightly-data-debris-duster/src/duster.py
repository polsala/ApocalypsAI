import argparse
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

def get_file_age_in_days(filepath: Path) -> float:
    """Returns the age of a file in days based on its last modification time."""
    try:
        mod_timestamp = filepath.stat().st_mtime
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        return (datetime.now() - mod_datetime).total_seconds() / (60 * 60 * 24)
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible

def find_old_files(directory: Path, age_threshold_days: int, recursive: bool = False) -> list[Path]:
    """
    Finds files in a directory (and optionally subdirectories) older than a given threshold.
    """
    old_files = []
    if not directory.is_dir():
        print(f"Error: Directory not found or is not a directory: {directory}")
        return old_files

    for root, _, files in os.walk(directory):
        current_dir = Path(root)
        for file_name in files:
            file_path = current_dir / file_name
            if file_path.is_file():
                age_days = get_file_age_in_days(file_path)
                if age_days >= age_threshold_days:
                    old_files.append(file_path)
        if not recursive:
            break # Only process the top directory if not recursive
    return old_files

def clean_debris(directory: Path, age_threshold_days: int, dry_run: bool = True, recursive: bool = False) -> list[Path]:
    """
    Identifies and optionally deletes old files.
    Returns a list of files that were processed (listed or deleted).
    """
    print(f"Scanning '{directory}' for files older than {age_threshold_days} days...")
    old_files = find_old_files(directory, age_threshold_days, recursive)

    if not old_files:
        print("No data debris found. Your digital wasteland is surprisingly clean!")
        return []

    print(f"Found {len(old_files)} potential pieces of data debris:")
    processed_files = []
    for file_path in old_files:
        print(f"  - {file_path} (Age: {get_file_age_in_days(file_path):.1f} days)")
        if not dry_run:
            try:
                os.remove(file_path)
                print(f"    [DELETED]")
                processed_files.append(file_path)
            except OSError as e:
                print(f"    [ERROR] Could not delete {file_path}: {e}")
        else:
            processed_files.append(file_path) # In dry-run, we still "process" by listing
    
    if dry_run:
        print("\nThis was a DRY RUN. No files were actually deleted.")
        print("To delete files, run with the --delete flag.")
    else:
        print(f"\nSuccessfully cleared {len(processed_files)} pieces of data debris.")
    
    return processed_files

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Data Debris Duster: Identify and clean up old, unused files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="Minimum age in days for a file to be considered 'debris'. Default is 90 days."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified files. By default, it performs a dry run (lists files)."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively. By default, only the top directory is scanned."
    )

    args = parser.parse_args()
    
    target_directory = Path(args.directory).resolve()
    
    clean_debris(target_directory, args.age, dry_run=not args.delete, recursive=args.recursive)

if __name__ == "__main__":
    main()
