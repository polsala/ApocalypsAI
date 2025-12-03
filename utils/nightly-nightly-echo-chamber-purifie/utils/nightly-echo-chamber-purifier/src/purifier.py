import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        # Handle cases like permission denied or file not found during hashing
        return None 

def find_duplicates(directory):
    """Finds duplicate files in the given directory based on content hash.

    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return {}

    files_by_size = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                try:
                    file_size = os.path.getsize(filepath)
                    if file_size > 0: # Skip empty files from hashing
                        files_by_size[file_size].append(filepath)
                except OSError: # Handle permission errors or broken symlinks for getsize
                    continue

    duplicates = defaultdict(list)
    for size, file_list in files_by_size.items():
        if len(file_list) > 1: # Only check for duplicates if there's more than one file of this size
            for filepath in file_list:
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    duplicates[file_hash].append(filepath)
    
    # Filter out groups that don't actually have duplicates (i.e., only one file per hash)
    return {h: paths for h, paths in duplicates.items() if len(paths) > 1}

def main():
    parser = argparse.ArgumentParser(
        description="Find and optionally remove duplicate files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, all but one instance of each duplicate file will be deleted. Use with caution!"
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicate_groups = find_duplicates(args.directory)

    if not duplicate_groups:
        print("No duplicate files found. Your digital echo chamber is pure!")
        return

    print("\n--- Duplicate Files Found ---")
    total_deleted_files = 0
    for file_hash, paths in duplicate_groups.items():
        print(f"\nHash: {file_hash}")
        print(f"  Original: {paths[0]}")
        for i, duplicate_path in enumerate(paths[1:]):
            print(f"  Duplicate {i+1}: {duplicate_path}")
            if args.delete:
                try:
                    os.remove(duplicate_path)
                    print(f"    -> Deleted: {duplicate_path}")
                    total_deleted_files += 1
                except OSError as e:
                    print(f"    -> Error deleting {duplicate_path}: {e}")
    
    if args.delete:
        print(f"\n--- Deletion Summary ---")
        print(f"Successfully deleted {total_deleted_files} duplicate files.")
    print("\n--- Scan Complete ---")

if __name__ == "__main__":
    main()
