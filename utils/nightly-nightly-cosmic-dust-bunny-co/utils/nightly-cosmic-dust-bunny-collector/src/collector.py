import os
import argparse
from pathlib import Path
from typing import List

def find_empty_directories(root_path: Path) -> List[Path]:
    """
    Recursively finds all empty directories within a given root path.
    A directory is considered empty if it contains no files or subdirectories.
    """
    empty_dirs = []
    if not root_path.is_dir():
        return []

    for dirpath, dirnames, filenames in os.walk(root_path):
        current_path = Path(dirpath)
        # Check if the current directory itself is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(current_path)
    return empty_dirs

def collect_dust_bunnies(root_path: Path, delete: bool = False) -> List[Path]:
    """
    Finds and optionally deletes empty directories.

    Args:
        root_path: The starting path to scan.
        delete: If True, empty directories will be deleted.

    Returns:
        A list of paths to the empty directories that were found/deleted.
    """
    if not root_path.is_dir():
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    print(f"Scanning '{root_path}' for cosmic dust bunnies...")
    empty_dirs = find_empty_directories(root_path)

    if not empty_dirs:
        print("No cosmic dust bunnies found! Your digital cosmos is pristine. ✨")
        return []

    print(f"\nFound {len(empty_dirs)} cosmic dust bunnies:")
    for d in sorted(empty_dirs):
        print(f"  - {d}")

    if delete:
        print("\nInitiating dust bunny collection protocol...")
        deleted_count = 0
        # Iterate in reverse order to delete deepest directories first
        for d in sorted(empty_dirs, reverse=True):
            try:
                # Re-check if it's still empty, as a parent might have been deleted
                # and made a previously non-empty child now empty, or vice-versa.
                # This is important for robustness.
                if d.is_dir() and not list(d.iterdir()): # Check if it's truly empty right before deleting
                    os.rmdir(d)
                    print(f"  🧹 Collected: {d}")
                    deleted_count += 1
                elif d.is_dir():
                    print(f"  ⚠️ Skipped (not empty anymore): {d}")
            except OSError as e:
                print(f"  ❌ Failed to collect {d}: {e}")
        print(f"\nSuccessfully collected {deleted_count} cosmic dust bunnies.")
    else:
        print("\nTo collect these dust bunnies, run with the --delete flag.")

    return empty_dirs

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Bunny Collector: Find and optionally remove empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root path to scan for empty directories."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, empty directories will be deleted. Otherwise, they are only listed."
    )

    args = parser.parse_args()
    root_path = Path(args.path).resolve() # Resolve to absolute path

    collect_dust_bunnies(root_path, args.delete)

if __name__ == "__main__":
    main()
