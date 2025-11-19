import os
import argparse
from typing import List

def find_broken_symlinks(root_path: str) -> List[str]:
    """
    Finds all broken symbolic links within a given root path.
    A symlink is considered broken if its target does not exist.
    """
    broken_links = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check files
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            if os.path.islink(full_path) and not os.path.exists(os.path.realpath(full_path)):
                broken_links.append(full_path)
        # Check directories (which might be symlinks themselves)
        for name in dirnames:
            full_path = os.path.join(dirpath, name)
            if os.path.islink(full_path) and not os.path.exists(os.path.realpath(full_path)):
                broken_links.append(full_path)
    return broken_links

def find_empty_dirs(root_path: str) -> List[str]:
    """
    Finds all empty directories within a given root path.
    A directory is considered empty if it contains no files or subdirectories.
    """
    empty_dirs = []
    # os.walk traverses top-down by default. To correctly identify empty dirs
    # we need to check from bottom-up or after the walk.
    # The 'topdown=False' argument for os.walk is perfect for this.
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if not dirnames and not filenames:
            # Ensure it's not the root path itself if it's the only thing left
            if dirpath != root_path:
                empty_dirs.append(dirpath)
    return empty_dirs

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust-Buster: Cleans up broken symlinks and empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for broken symlinks and empty directories."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, identified broken symlinks and empty directories will be deleted. Use with caution!"
    )

    args = parser.parse_args()
    scan_path = os.path.abspath(args.path)

    if not os.path.isdir(scan_path):
        print(f"Error: The specified path '{scan_path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{scan_path}' for digital dust...")

    broken_links = find_broken_symlinks(scan_path)
    empty_directories = find_empty_dirs(scan_path)

    if not broken_links and not empty_directories:
        print("No digital dust found. Your system is sparkling clean!")
        exit(0)

    if broken_links:
        print("\n--- Broken Symbolic Links Found ---")
        for link in broken_links:
            print(f"  - {link}")
    else:
        print("\nNo broken symbolic links found.")

    if empty_directories:
        print("\n--- Empty Directories Found ---")
        for directory in empty_directories:
            print(f"  - {directory}")
    else:
        print("\nNo empty directories found.")

    if args.delete:
        print("\n--- Deleting Digital Dust ---")
        for link in broken_links:
            try:
                os.unlink(link)
                print(f"  Deleted broken symlink: {link}")
            except OSError as e:
                print(f"  Error deleting symlink {link}: {e}")
        
        # Sort empty directories by length (longest first) to ensure child directories are deleted before parents
        # This is important if an empty parent directory contains an empty child directory.
        # os.walk(topdown=False) already provides this order, but explicit sort is safer.
        empty_directories.sort(key=len, reverse=True) 
        for directory in empty_directories:
            try:
                os.rmdir(directory)
                print(f"  Deleted empty directory: {directory}")
            except OSError as e:
                print(f"  Error deleting directory {directory}: {e}")
        print("\nDigital dust cleanup complete!")
    else:
        print("\nRun with '--delete' to remove the identified items.")

if __name__ == "__main__":
    main()
