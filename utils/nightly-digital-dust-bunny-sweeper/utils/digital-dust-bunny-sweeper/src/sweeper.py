import os
import time
import datetime
import argparse
import fnmatch
import sys

def find_empty_dirs(root_path):
    """Finds all empty directories within a given root path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the current directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    # Sort by length descending to ensure child directories are deleted before parents
    return sorted(empty_dirs, key=len, reverse=True)

def find_stale_files(root_path, age_days, patterns):
    """Finds files matching patterns and older than age_days within a root path."""
    stale_files = []
    cutoff_time = time.time() - (age_days * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Check if file matches any pattern
                if any(fnmatch.fnmatch(filename, p) for p in patterns):
                    # Check if file is older than cutoff_time
                    if os.path.getmtime(file_path) < cutoff_time:
                        stale_files.append(file_path)
            except OSError: # Handle cases where file might be inaccessible
                pass
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep for digital dust bunnies (empty dirs, stale files)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, identified dust bunnies will be deleted after confirmation."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered stale. Default: 30."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default=".tmp,.log",
        help="Comma-separated file patterns (e.g., .tmp,.log,cache_*.txt). Default: .tmp,.log"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    patterns = [p.strip() for p in args.patterns.split(',') if p.strip()]

    print(f"\nScanning '{args.path}' for digital dust bunnies...\n")

    empty_dirs = find_empty_dirs(args.path)
    stale_files = find_stale_files(args.path, args.age_days, patterns)

    total_found = len(empty_dirs) + len(stale_files)

    if total_found == 0:
        print("✨ All clear! No digital dust bunnies found. Your system is sparkling! ✨")
        sys.exit(0)

    print(f"Found {total_found} digital dust bunnies:\n")

    if empty_dirs:
        print("--- Empty Directories ---")
        for d in empty_dirs:
            print(f"  [DIR] {d}")

    if stale_files:
        print(f"\n--- Stale Files (older than {args.age_days} days, matching {', '.join(patterns)}) ---")
        for f in stale_files:
            print(f"  [FILE] {f}")

    if args.delete:
        print("\n--- Deletion Mode Activated ---")
        confirmation = input("Are you sure you want to sweep these dust bunnies away? (y/N): ").lower()
        if confirmation == 'y':
            print("\nSweeping away...\n")
            deleted_count = 0
            for f in stale_files:
                try:
                    os.remove(f)
                    print(f"  Deleted file: {f}")
                    deleted_count += 1
                except OSError as e:
                    print(f"  Error deleting file {f}: {e}", file=sys.stderr)
            for d in empty_dirs:
                try:
                    os.rmdir(d)
                    print(f"  Deleted empty directory: {d}")
                    deleted_count += 1
                except OSError as e:
                    print(f"  Error deleting directory {d}: {e}", file=sys.stderr)
            print(f"\n🧹 Swept away {deleted_count} digital dust bunnies! Your system thanks you. 🧹")
        else:
            print("\nDeletion cancelled. Dust bunnies live to see another day. 😔")
    else:
        print("\nTo delete these items, run with the '--delete' flag. (e.g., python3 src/sweeper.py <path> --delete)")

    sys.exit(0)

if __name__ == "__main__":
    main()
