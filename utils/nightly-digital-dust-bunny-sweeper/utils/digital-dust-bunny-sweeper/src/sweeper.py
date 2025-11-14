import os
import time
import argparse
import sys

def find_empty_dirs(path):
    """Finds all empty directories within a given path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        # If no subdirectories and no files, it's empty
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(path, age_threshold_days, file_extensions):
    """Finds files older than age_threshold_days with specified extensions."""
    old_files = []
    now = time.time()
    age_threshold_seconds = age_threshold_days * 24 * 60 * 60

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_extensions):
                filepath = os.path.join(dirpath, filename)
                try:
                    # getmtime returns the time of last modification
                    mod_time = os.path.getmtime(filepath)
                    if (now - mod_time) > age_threshold_seconds:
                        old_files.append(filepath)
                except OSError as e:
                    print(f"Warning: Could not access file {filepath}: {e}", file=sys.stderr)
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Clean up digital detritus."
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=[os.getcwd()],
        help="One or more paths to scan (default: current directory).",
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered old (default: 30).",
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=[".log", ".tmp", ".bak"],
        help="File extensions to consider for 'old file' cleanup (e.g., .log .tmp .bak). Default: .log .tmp .bak",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete identified empty directories and old files. Use with caution!",
    )

    args = parser.parse_args()

    all_empty_dirs = []
    all_old_files = []

    print(f"\n--- Scanning for Digital Dust Bunnies in: {', '.join(args.paths)} ---")

    for path in args.paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.", file=sys.stderr)
            continue

        print(f"Scanning '{path}'...")
        empty_dirs = find_empty_dirs(path)
        old_files = find_old_files(path, args.age, args.extensions)

        all_empty_dirs.extend(empty_dirs)
        all_old_files.extend(old_files)

    if all_empty_dirs:
        print("\nFound Empty Directories (potential dust bunnies):")
        for d in all_empty_dirs:
            print(f"  - {d}")
    else:
        print("\nNo empty directories found. Your digital space is surprisingly tidy!")

    if all_old_files:
        print(f"\nFound Old Files (stale digital detritus older than {args.age} days):")
        for f in all_old_files:
            print(f"  - {f}")
    else:
        print("\nNo old files found matching criteria. Excellent archival discipline!")

    if args.delete:
        print("\n--- Initiating Digital Detritus Purge (Deletion Mode Active!) ---")
        deleted_count = 0
        for f in all_old_files:
            try:
                os.remove(f)
                print(f"  Deleted old file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting file {f}: {e}", file=sys.stderr)
        for d in all_empty_dirs:
            try:
                os.rmdir(d)
                print(f"  Deleted empty directory: {d}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting directory {d}: {e}", file=sys.stderr)
        print(f"\n--- Purge Complete! Total items removed: {deleted_count} ---")
    else:
        print("\n--- Dry Run Complete. Use --delete to perform actual cleanup. ---")


if __name__ == "__main__":
    main()
