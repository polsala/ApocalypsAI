import os
import shutil
import argparse
import fnmatch
from typing import List, Set

DEFAULT_PATTERNS = [
    '__pycache__',
    '.DS_Store',
    '*.tmp',
    '*.log',
    '*.bak',
    'Thumbs.db',
    '*.swp',
    '*.swo',
    '*.pyc'
]

def is_empty_dir(path: str) -> bool:
    """Checks if a directory is empty."""
    return os.path.isdir(path) and not os.listdir(path)

def find_and_clean(
    target_directory: str,
    patterns: List[str],
    dry_run: bool = True
) -> Set[str]:
    """
    Finds and optionally cleans files and directories matching patterns or empty.

    Args:
        target_directory: The root directory to start sweeping from.
        patterns: A list of glob-style patterns to match against file/directory names.
        dry_run: If True, only print what would be deleted. If False, perform deletions.

    Returns:
        A set of paths that were identified for deletion.
    """
    if not os.path.isdir(target_directory):
        print(f"Error: Target directory '{target_directory}' does not exist or is not a directory.")
        return set()

    print(f"Sweeping '{target_directory}' for cosmic dust bunnies... (Dry Run: {dry_run})")
    deleted_paths: Set[str] = set()
    potential_deletions: Set[str] = set()

    # First pass: identify files and non-empty directories to delete
    for root, dirnames, filenames in os.walk(target_directory, topdown=False):
        for name in filenames:
            full_path = os.path.join(root, name)
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    potential_deletions.add(full_path)
                    break

        for name in dirnames:
            full_path = os.path.join(root, name)
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    # If a directory matches a pattern, mark it for deletion
                    # We'll delete it with shutil.rmtree later if it's not empty
                    potential_deletions.add(full_path)
                    break

    # Second pass: process deletions and empty directories
    # Iterate topdown=False to ensure empty subdirectories are processed before their parents
    for root, dirnames, filenames in os.walk(target_directory, topdown=False):
        # Delete files
        for name in filenames:
            full_path = os.path.join(root, name)
            if full_path in potential_deletions:
                if dry_run:
                    print(f"[DRY RUN] Would delete file: {full_path}")
                else:
                    try:
                        os.remove(full_path)
                        print(f"Deleted file: {full_path}")
                        deleted_paths.add(full_path)
                    except OSError as e:
                        print(f"Error deleting file {full_path}: {e}")

        # Delete directories (matching patterns or empty)
        for name in dirnames:
            full_path = os.path.join(root, name)
            if full_path in potential_deletions:
                # This directory matched a pattern, delete it recursively
                if dry_run:
                    print(f"[DRY RUN] Would delete directory (recursive): {full_path}")
                else:
                    try:
                        shutil.rmtree(full_path)
                        print(f"Deleted directory (recursive): {full_path}")
                        deleted_paths.add(full_path)
                    except OSError as e:
                        print(f"Error deleting directory {full_path}: {e}")
            elif is_empty_dir(full_path):
                # This directory is empty, delete it
                if dry_run:
                    print(f"[DRY RUN] Would delete empty directory: {full_path}")
                else:
                    try:
                        os.rmdir(full_path)
                        print(f"Deleted empty directory: {full_path}")
                        deleted_paths.add(full_path)
                    except OSError as e:
                        print(f"Error deleting empty directory {full_path}: {e}")

    if not potential_deletions and not deleted_paths:
        print("No cosmic dust bunnies found. Your space is pristine!")
    elif dry_run:
        print("\nDry run complete. Use --no-dry-run to perform actual deletions.")
    else:
        print("\nSweeping complete!")

    return deleted_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sweep away digital 'dust bunnies' from your project directory."
    )
    parser.add_argument(
        "target_directory",
        type=str,
        help="The root directory to start sweeping from."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=DEFAULT_PATTERNS,
        help="Glob-style patterns for files/directories to delete (e.g., '*.tmp', '__pycache__')."
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_true",
        help="Perform actual deletions instead of just a dry run."
    )

    args = parser.parse_args()

    find_and_clean(args.target_directory, args.patterns, not args.no_dry_run)
