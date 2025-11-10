import os
import argparse
import datetime
import time

def find_empty_dirs(root_path):
    """Finds all empty directories within a given root path."""
    empty_dirs = []
    # os.walk traverses top-down. We need to process subdirectories first for deletion.
    # So, we collect all empty dirs and then sort them by length in reverse.
    for dirpath, dirnames, filenames in os.walk(root_path):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    # Sort in reverse order of path length to ensure deeper directories are listed first.
    # This is crucial for os.rmdir, which can only remove truly empty directories.
    return sorted(empty_dirs, key=len, reverse=True)

def find_old_logs(root_path, days_old, log_extensions):
    """Finds log files older than 'days_old' within a given root path."""
    old_logs = []
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            # Check if the file has one of the specified log extensions
            if any(filename.lower().endswith(ext.lower()) for ext in log_extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    # Check if the file's modification time is older than the cutoff
                    if os.path.getmtime(file_path) < cutoff_time:
                        old_logs.append(file_path)
                except OSError: # Handle cases where file might be deleted or inaccessible during walk
                    continue
    return old_logs

def perform_cleanup(
    root_path,
    dry_run,
    delete_empty_dirs_flag,
    delete_old_logs_days,
    log_extensions
):
    """Performs the cleanup operations based on flags."""
    print(f"\nScanning '{root_path}' for digital dust bunnies...")
    if dry_run:
        print("*** DRY RUN MODE: No files or directories will be deleted. ***")

    if delete_empty_dirs_flag:
        print("\n--- Empty Directories ---")
        empty_dirs = find_empty_dirs(root_path)
        if empty_dirs:
            for d in empty_dirs:
                print(f"{'[DRY RUN] ' if dry_run else ''}Found empty directory: {d}")
                if not dry_run:
                    try:
                        os.rmdir(d)
                        print(f"  Deleted: {d}")
                    except OSError as e:
                        print(f"  Error deleting {d}: {e}")
        else:
            print("No empty directories found. Your digital space is tidy!")

    if delete_old_logs_days is not None:
        print(f"\n--- Old Log Files (older than {delete_old_logs_days} days) ---")
        old_logs = find_old_logs(root_path, delete_old_logs_days, log_extensions)
        if old_logs:
            for f in old_logs:
                print(f"{'[DRY RUN] ' if dry_run else ''}Found old log file: {f}")
                if not dry_run:
                    try:
                        os.remove(f)
                        print(f"  Deleted: {f}")
                    except OSError as e:
                        print(f"  Error deleting {f}: {e}")
        else:
            print("No old log files found. Your logs are fresh!")

    print("\nDigital Dust Bunny Sweeper finished its rounds!")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies (empty directories and old log files)."
    )
    parser.add_argument(
        "path_to_scan",
        type=str,
        help="The root directory from which to start scanning."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run; report actions without deleting anything."
    )
    parser.add_argument(
        "--delete-empty-dirs",
        action="store_true",
        help="Enable deletion of empty directories."
    )
    parser.add_argument(
        "--delete-old-logs",
        type=int,
        metavar="DAYS",
        help="Enable deletion of log files older than specified DAYS."
    )
    parser.add_argument(
        "--log-extensions",
        nargs='+',
        default=['.log', '.txt'],
        help="Specify custom log file extensions (e.g., .log .out)."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_scan):
        print(f"Error: '{args.path_to_scan}' is not a valid directory.")
        exit(1)

    perform_cleanup(
        args.path_to_scan,
        args.dry_run,
        args.delete_empty_dirs,
        args.delete_old_logs,
        args.log_extensions
    )

if __name__ == "__main__":
    main()
