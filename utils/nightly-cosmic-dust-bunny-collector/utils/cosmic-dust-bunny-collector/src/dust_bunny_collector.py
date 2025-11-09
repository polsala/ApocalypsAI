import os
import argparse
import datetime
import sys

def scan_directory(path):
    """Recursively scans a directory and yields (filepath, last_modified_timestamp)."""
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.", file=sys.stderr)
        return

    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(filepath)
                yield filepath, mtime
            except OSError as e:
                print(f"Warning: Could not access '{filepath}': {e}", file=sys.stderr)

def filter_old_files(files_data, days_old):
    """Filters a list of (filepath, timestamp) tuples, returning files older than days_old."""
    current_time = datetime.datetime.now().timestamp()
    threshold_timestamp = current_time - (days_old * 24 * 60 * 60)
    
    old_files = []
    for filepath, mtime in files_data:
        if mtime < threshold_timestamp:
            old_files.append(filepath)
    return old_files

def report_files(files):
    """Prints a list of files to be acted upon."""
    if not files:
        print("No cosmic dust bunnies found! Your space is sparkling clean.")
        return

    print(f"Found {len(files)} cosmic dust bunnies (files older than specified days):")
    for file in files:
        print(f"  - {file}")

def delete_files(files):
    """Deletes a list of files."""
    if not files:
        return

    print("Initiating cosmic dust bunny removal...")
    deleted_count = 0
    for file in files:
        try:
            os.remove(file)
            print(f"  Deleted: {file}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting '{file}': {e}", file=sys.stderr)
    print(f"Successfully removed {deleted_count} cosmic dust bunnies.")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Find and remove old, unused files."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--days-old", 
        type=int, 
        default=30, 
        help="Files not modified within this many days will be considered 'dust bunnies'."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Only report files that would be deleted, do not actually delete them."
    )
    parser.add_argument(
        "--delete", 
        action="store_true", 
        help="Actually delete the identified old files. Use with extreme caution!"
    )

    args = parser.parse_args()

    if args.days_old < 0:
        print("Error: --days-old cannot be negative.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{args.path}' for files older than {args.days_old} days...")
    
    all_files_data = list(scan_directory(args.path))
    if not all_files_data and os.path.isdir(args.path):
        print("No files found in the specified directory.")
        sys.exit(0)
    elif not os.path.isdir(args.path):
        sys.exit(1) # Error message already printed by scan_directory

    old_files = filter_old_files(all_files_data, args.days_old)

    if args.dry_run:
        print("\n--- DRY RUN MODE ---")
        report_files(old_files)
        print("--- END DRY RUN ---\n")
        print("No files were deleted. To delete, run again without --dry-run and with --delete.")
    elif args.delete:
        report_files(old_files)
        if old_files:
            confirm = input("Are you sure you want to delete these files? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_files(old_files)
            else:
                print("Deletion cancelled.")
        else:
            print("No files to delete.")
    else:
        # Default behavior: just report
        report_files(old_files)
        if old_files:
            print("\nTo delete these files, run again with the --delete flag.")

if __name__ == "__main__":
    main()
