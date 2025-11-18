import os
import sys
from datetime import datetime, timedelta

def find_empty_dirs(root_dir):
    """Finds all empty directories within the given root_dir."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # A directory is considered empty if it has no files and no subdirectories
        # at the time os.walk visits it. We collect all such paths.
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_small_files(root_dir, age_days, max_size_kb, patterns):
    """
    Finds files that are older than age_days, smaller than max_size_kb,
    and match one of the given patterns.
    """
    old_small_files = []
    cutoff_time = datetime.now() - timedelta(days=age_days)
    max_size_bytes = max_size_kb * 1024

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Check if file exists and is a regular file (not a symlink, etc.)
                if not os.path.isfile(file_path):
                    continue

                file_stat = os.stat(file_path)
                file_mtime = datetime.fromtimestamp(file_stat.st_mtime)
                file_size = file_stat.st_size

                # Check age, size, and pattern
                if file_mtime < cutoff_time and \
                   file_size < max_size_bytes and \
                   any(filename.endswith(f".{p}") for p in patterns):
                    old_small_files.append(file_path)
            except OSError as e:
                # Handle cases where file might be inaccessible or disappear during walk
                print(f"Warning: Could not access {file_path}: {e}", file=sys.stderr)
                continue
    return old_small_files

def run_duster(path, dry_run, age_days, max_size_kb, patterns):
    """Main function to run the dust bunny duster."""
    print(f"Scanning '{path}' for digital dust bunnies...")
    print(f"  - Dry Run: {dry_run}")
    print(f"  - Max File Age: {age_days} days")
    print(f"  - Max File Size: {max_size_kb} KB")
    print(f"  - File Patterns: {', '.join(patterns)}")
    print("-" * 30)

    empty_dirs = find_empty_dirs(path)
    old_small_files = find_old_small_files(path, age_days, max_size_kb, patterns)

    print(f"Found {len(empty_dirs)} empty directories.")
    for d in empty_dirs:
        print(f"  [DIR] {d}")

    print(f"Found {len(old_small_files)} old, small files matching patterns.")
    for f in old_small_files:
        print(f"  [FILE] {f}")

    if not empty_dirs and not old_small_files:
        print("No digital dust bunnies found. Your space is pristine!")
        return 2 # No-op exit code

    if not dry_run:
        print("\nProceeding with deletion...")
        deleted_count = 0

        # Delete files first
        for f in old_small_files:
            try:
                os.remove(f)
                print(f"  Deleted file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting file {f}: {e}", file=sys.stderr)

        # Delete empty directories, starting from deepest to avoid issues
        # with parent directories becoming empty after children are removed.
        # Sorting by length in reverse ensures deepest paths come first.
        empty_dirs.sort(key=len, reverse=True)
        for d in empty_dirs:
            try:
                # Re-check if directory is truly empty, as file deletions might have made parents empty
                # or other processes might have created files. os.listdir() raises OSError if not a directory.
                if not os.listdir(d):
                    os.rmdir(d)
                    print(f"  Deleted empty directory: {d}")
                    deleted_count += 1
                else:
                    print(f"  Skipped non-empty directory: {d}")
            except OSError as e:
                print(f"  Error deleting directory {d}: {e}", file=sys.stderr)

        print(f"\nDeletion complete. Total items deleted: {deleted_count}")
    else:
        print("\nDry run complete. No items were deleted.")

    return 0 # Success exit code

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Duster: Cleans up empty directories and old, small files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Root directory to scan for dust bunnies (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run: list items to be deleted without actually deleting them.",
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Minimum age in days for files to be considered (default: 30).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=1,
        help="Maximum size in KB for files to be considered (default: 1KB).",
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default="log,tmp,bak",
        help="Comma-separated file extensions to target (e.g., 'log,tmp,bak').",
    )

    args = parser.parse_args()
    patterns_list = [p.strip() for p in args.patterns.split(',') if p.strip()]

    exit_code = run_duster(args.path, args.dry_run, args.age, args.size, patterns_list)
    sys.exit(exit_code)
