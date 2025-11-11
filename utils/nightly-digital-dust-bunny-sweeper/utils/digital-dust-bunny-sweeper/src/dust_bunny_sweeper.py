import os
import time
import argparse
from datetime import datetime, timedelta

def find_empty_dirs(path):
    """Finds all empty directories within the given path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(path, days_old):
    """Finds files older than a specified number of days within the given path."""
    old_files = []
    cutoff_timestamp = time.time() - (days_old * 24 * 60 * 60)

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(filepath):
                    mod_time = os.path.getmtime(filepath)
                    if mod_time < cutoff_timestamp:
                        old_files.append(filepath)
            except OSError: # Handle cases where file might be inaccessible (e.g., permission denied)
                pass
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: find empty directories and old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to scan (default: current directory)."
    )
    parser.add_argument(
        "--empty-dirs",
        action="store_true",
        help="Report empty directories."
    )
    parser.add_argument(
        "--old-files",
        type=int,
        metavar="DAYS",
        help="Report files older than this many days."
    )

    args = parser.parse_args()

    scan_path = os.path.abspath(args.path)

    print(f"\n--- Digital Dust Bunny Sweeper Report for '{scan_path}' ---")

    if args.empty_dirs:
        print("\n### Empty Directories (Digital Dust Bunnies): ###")
        empty_dirs = find_empty_dirs(scan_path)
        if empty_dirs:
            for d in empty_dirs:
                print(f"- {d}")
        else:
            print("  No empty directories found. Your digital corners are spotless!")

    if args.old_files is not None:
        print(f"\n### Ancient Files (Forgotten Scrolls, older than {args.old_files} days): ###")
        old_files = find_old_files(scan_path, args.old_files)
        if old_files:
            for f in old_files:
                print(f"- {f}")
        else:
            print("  No ancient files found. All your data is fresh and relevant!")

    if not args.empty_dirs and args.old_files is None:
        print("\nNo scan type specified. Use --empty-dirs or --old-files to begin sweeping.")
        parser.print_help()

    print("\n--- End of Report ---\n")

if __name__ == "__main__":
    main()
