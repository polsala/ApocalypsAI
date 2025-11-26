import os
import time
import shutil
import argparse
import fnmatch

def get_current_time():
    """Helper to get current time, useful for mocking in tests."""
    return time.time()

def is_older_than(filepath, age_days, current_time):
    """Checks if a file/directory is older than a specified number of days."""
    try:
        mtime = os.path.getmtime(filepath)
        # Convert age_days to seconds and compare
        return (current_time - mtime) > (age_days * 24 * 60 * 60)
    except OSError:
        # If file/dir cannot be accessed (e.g., permission error, or it disappeared),
        # assume it's not older for safety or handle gracefully.
        return False

def matches_patterns(name, patterns):
    """Checks if a name matches any of the given glob patterns."""
    if not patterns:
        return True # No patterns means match all
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def collect_dust(path, age_days, patterns, dry_run=True, verbose=False):
    """Collects 'cosmic dust' (old files/directories) based on criteria.

    Args:
        path (str): The root directory to scan.
        age_days (int): Files/directories older than this many days will be considered.
        patterns (list): List of glob patterns to match against names. Empty list matches all.
        dry_run (bool): If True, only report what would be deleted, don't delete.
        verbose (bool): If True, print detailed output.

    Returns:
        list: A list of paths that were (or would be) deleted.
    """
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return []

    if verbose:
        print(f"Scanning '{path}' for cosmic dust older than {age_days} days...")
        if patterns:
            print(f"Matching patterns: {', '.join(patterns)}")
        else:
            print("No specific patterns provided, matching all files/directories.")

    deleted_items = []
    current_time = get_current_time()

    # Iterate topdown=False to ensure child directories are processed before parents,
    # allowing safe removal of empty directories.
    for root, dirs, files in os.walk(path, topdown=False):
        # Check files
        for name in files:
            filepath = os.path.join(root, name)
            if is_older_than(filepath, age_days, current_time) and matches_patterns(name, patterns):
                if verbose:
                    print(f"  [FILE] Found potential dust: {filepath}")
                if not dry_run:
                    try:
                        os.remove(filepath)
                        deleted_items.append(filepath)
                        if verbose:
                            print(f"    Deleted: {filepath}")
                    except OSError as e:
                        print(f"    Error deleting file {filepath}: {e}")
                else:
                    deleted_items.append(filepath)

        # Check directories
        for name in dirs:
            dirpath = os.path.join(root, name)
            # Only consider deleting directories if they match patterns AND are old.
            # os.walk(topdown=False) ensures that if a directory becomes empty due to
            # its contents being deleted, it can then be removed itself.
            if is_older_than(dirpath, age_days, current_time) and matches_patterns(name, patterns):
                if verbose:
                    print(f"  [DIR] Found potential dust: {dirpath}")
                if not dry_run:
                    try:
                        shutil.rmtree(dirpath)
                        deleted_items.append(dirpath)
                        if verbose:
                            print(f"    Deleted: {dirpath}")
                    except OSError as e:
                        print(f"    Error deleting directory {dirpath}: {e}")
                else:
                    deleted_items.append(dirpath)

    if dry_run:
        print(f"Dry run complete. Would delete {len(deleted_items)} items.")
        if verbose and deleted_items:
            print("Items to be deleted:")
            for item in deleted_items:
                print(f"  - {item}")
    else:
        print(f"Cleanup complete. Deleted {len(deleted_items)} items.")

    return deleted_items


def main():
    parser = argparse.ArgumentParser(description="Nightly Cosmic Dust Collector: Cleans old files and directories.")
    parser.add_argument('--path', type=str, required=True, help='The root directory to scan for cosmic dust.')
    parser.add_argument('--age', type=int, default=30, help='Files/directories older than this many days will be considered for deletion. (Default: 30)')
    parser.add_argument('--patterns', nargs='*', default=[], help='One or more glob patterns to match against file/directory names. If not provided, all files/directories older than --age are considered.')
    parser.add_argument('--dry-run', action='store_true', help='If set, only report what would be deleted, without performing any actual deletions.')
    parser.add_argument('--verbose', action='store_true', help='If set, provides more detailed output about the scanning and deletion process.')

    args = parser.parse_args()

    collect_dust(args.path, args.age, args.patterns, args.dry_run, args.verbose)


if __name__ == '__main__':
    main()
