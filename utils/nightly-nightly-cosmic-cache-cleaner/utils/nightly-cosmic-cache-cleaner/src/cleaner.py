import os
import shutil
import argparse
from pathlib import Path
from typing import List

def get_directory_size(path: Path) -> int:
    """Calculates the total size of a directory."""
    total_size = 0
    for entry in path.rglob('*'):
        if entry.is_file():
            total_size += entry.stat().st_size
    return total_size

def format_bytes(size: int) -> str:
    """Formats a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def clean_caches(
    root_path: Path,
    patterns: List[str],
    dry_run: bool = True,
    verbose: bool = False
) -> int:
    """
    Finds and optionally deletes directories matching specified patterns.

    Args:
        root_path: The starting directory for the scan.
        patterns: A list of directory names to search for.
        dry_run: If True, only report what would be deleted. If False, actually delete.
        verbose: If True, print details for each found directory.

    Returns:
        The total size (in bytes) of directories processed.
    """
    if not root_path.is_dir():
        print(f"Error: Root path '{root_path}' is not a valid directory.")
        return 0

    print(f"Scanning '{root_path}' for cache directories matching patterns: {', '.join(patterns)}")
    print(f"Mode: {'Dry Run' if dry_run else 'Actual Deletion'}")

    total_cleaned_size = 0
    found_dirs = []

    for pattern in patterns:
        # Use rglob for recursive search for directories matching the pattern
        # Note: rglob matches files and directories. We need to filter for directories.
        for found_path in root_path.rglob(pattern):
            if found_path.is_dir() and found_path.name == pattern:
                found_dirs.append(found_path)

    if not found_dirs:
        print("No matching cache directories found.")
        return 0

    for dir_to_clean in found_dirs:
        try:
            size = get_directory_size(dir_to_clean)
            total_cleaned_size += size

            action_msg = "Would delete" if dry_run else "Deleting"
            if verbose:
                print(f"  - {action_msg}: {dir_to_clean} ({format_bytes(size)})")

            if not dry_run:
                shutil.rmtree(dir_to_clean)
        except OSError as e:
            print(f"Error processing {dir_to_clean}: {e}")
            continue

    action_summary = "would have been reclaimed" if dry_run else "reclaimed"
    print(f"\nSummary: {format_bytes(total_cleaned_size)} {action_summary}.")
    return total_cleaned_size

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Cache Cleaner: Reclaim disk space by removing common project cache directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to start scanning from. Defaults to current working directory."
    )
    parser.add_argument(
        "--patterns",
        nargs='+',
        default=["__pycache__", "node_modules", ".pytest_cache", ".mypy_cache"],
        help="A space-separated list of directory names to clean. E.g., '__pycache__ node_modules'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run. List what would be deleted without actually removing anything."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about each directory found."
    )

    args = parser.parse_args()

    root_path = Path(args.path).resolve() # Resolve to absolute path for clarity and robustness

    clean_caches(root_path, args.patterns, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
