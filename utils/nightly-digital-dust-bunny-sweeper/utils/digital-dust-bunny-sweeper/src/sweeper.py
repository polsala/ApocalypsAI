import os
import time
import datetime
import fnmatch
import argparse

def find_empty_dirs(root_path):
    """Finds all empty directories within the given root_path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the current directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(root_path, age_days, patterns):
    """Finds files matching patterns that are older than age_days."""
    old_files = []
    now = time.time()
    threshold_timestamp = now - (age_days * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            
            # Skip if it's not a regular file (e.g., a symlink that points elsewhere)
            if not os.path.isfile(full_path):
                continue

            # Check if file matches any of the patterns
            is_match = False
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    is_match = True
                    break
            
            if is_match:
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime < threshold_timestamp:
                        old_files.append(full_path)
                except OSError: # Handle cases where file might be inaccessible
                    pass
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Identify and clean up digital dust bunnies (empty directories and old files)."
    )
    parser.add_argument(
        "path", 
        type=str, 
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Only print what would be cleaned, do not delete anything."
    )
    parser.add_argument(
        "--age", 
        type=int, 
        default=30, 
        help="Minimum age in days for a file to be considered 'old'. (Default: 30)"
    )
    parser.add_argument(
        "--patterns", 
        nargs='*', 
        default=['*.log', '*.tmp', '*.bak', '*.old', '*.swp'], 
        help="Glob patterns for files to consider as 'dust bunnies'. (Default: *.log *.tmp *.bak *.old *.swp)"
    )

    args = parser.parse_args()

    print(f"\nScanning '{args.path}' for digital dust bunnies...\n")

    empty_dirs = find_empty_dirs(args.path)
    old_files = find_old_files(args.path, args.age, args.patterns)

    if empty_dirs:
        print("--- Empty Directories Found ---")
        for d in empty_dirs:
            print(f"  [EMPTY] {d}")
    else:
        print("No empty directories found. Your digital space is surprisingly tidy!")

    if old_files:
        print(f"\n--- Old Files (older than {args.age} days, matching {args.patterns}) ---")
        for f in old_files:
            print(f"  [OLD] {f}")
    else:
        print(f"No old files matching patterns '{args.patterns}' found. Excellent hygiene!")

    total_clutter = len(empty_dirs) + len(old_files)

    if total_clutter > 0:
        print(f"\nTotal digital dust bunnies identified: {total_clutter}")
        if args.dry_run:
            print("\n(Dry run complete. No changes were made. Remove --dry-run to clean.)")
        else:
            print("\n(Cleaning functionality is not implemented in this version. Please review findings manually.)")
            # Future enhancement: Implement actual deletion here
            # for d in empty_dirs: os.rmdir(d)
            # for f in old_files: os.remove(f)
    else:
        print("\nYour repository is sparkling clean! No dust bunnies detected.")


if __name__ == "__main__":
    main()
