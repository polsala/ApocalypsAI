import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible

def get_file_size_kb(filepath):
    """Calculates the size of a file in kilobytes."""
    try:
        return os.path.getsize(filepath) / 1024
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible

def scan_directory(directory_path, max_age_days, min_size_kb):
    """
    Scans a directory for files matching age and size criteria.
    Returns a list of (filepath, age_days, size_kb) tuples.
    """
    files_to_consider = []
    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            age_days = get_file_age_days(filepath)
            size_kb = get_file_size_kb(filepath)

            if age_days >= max_age_days and size_kb >= min_size_kb:
                files_to_consider.append((filepath, age_days, size_kb))
    return files_to_consider

def report_files(files_data, dry_run=True):
    """Prints a formatted report of files to be deleted."""
    if not files_data:
        print("No files found matching the criteria.")
        return 0

    action = "would be deleted" if dry_run else "will be deleted"
    print(f"\n--- Files that {action} ---")
    total_size_kb = 0
    for filepath, age_days, size_kb in files_data:
        print(f"- {filepath} (Age: {age_days:.1f} days, Size: {size_kb:.2f} KB)")
        total_size_kb += size_kb
    print(f"--------------------------------------------------")
    print(f"Total files: {len(files_data)}")
    print(f"Total size: {total_size_kb:.2f} KB ({total_size_kb / 1024:.2f} MB)")
    print(f"--------------------------------------------------\n")
    return len(files_data)

def delete_files(files_data, dry_run, confirm):
    """Deletes the specified files."""
    if not files_data:
        return

    if dry_run:
        print("Dry run complete. No files were deleted.")
        return

    if confirm:
        response = input(f"Proceed with deleting {len(files_data)} files? (y/N): ").lower()
        if response != 'y':
            print("Deletion cancelled.")
            return

    deleted_count = 0
    for filepath, _, _ in files_data:
        try:
            os.remove(filepath)
            print(f"Deleted: {filepath}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting {filepath}: {e}")
    print(f"\nSuccessfully deleted {deleted_count} out of {len(files_data)} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Rift Repair Kit: Clean up old/large temporary files."
    )
    parser.add_argument(
        "--path",
        nargs=":",
        required=True,
        help="One or more paths to directories to scan."
    )
    parser.add_argument(
        "--max-age",
        type=int,
        default=30,
        help="Files older than this many days will be considered for deletion. Default: 30."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=0, # KB
        help="Files larger than this many kilobytes will be considered for deletion. Default: 0."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only report files that would be deleted, without actually deleting them."
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="If set, prompt for confirmation before deleting files. Ignored if --dry-run is set."
    )

    args = parser.parse_args()

    all_files_to_delete = []
    for path in args.path:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue
        print(f"Scanning '{path}' for files older than {args.max_age} days and larger than {args.min_size} KB...")
        files_in_path = scan_directory(path, args.max_age, args.min_size)
        all_files_to_delete.extend(files_in_path)

    num_reported = report_files(all_files_to_delete, args.dry_run)

    if num_reported > 0:
        delete_files(all_files_to_delete, args.dry_run, args.confirm)
    else:
        print("No files to delete based on the specified criteria.")

if __name__ == "__main__":
    main()
