import os
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    # For mocking purposes, if filepath is not a string, assume it's a mock object
    # with a .read_data attribute or a .read method that returns content.
    if not isinstance(filepath, str):
        # This branch is primarily for testing with mock_open's return_value
        # which might not have a 'name' attribute or be a real path.
        # We assume the mock object itself can provide the content.
        if hasattr(filepath, 'read_data'): # For mock_open(read_data=...).return_value
            sha256.update(filepath.read_data)
        elif hasattr(filepath, 'read'): # For generic mock file objects
            for block in iter(lambda: filepath.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def find_duplicate_files(directory):
    """
    Finds duplicate files in a given directory by comparing their SHA256 hashes.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = calculate_file_hash(filepath)
                hashes[file_hash].append(filepath)
            except IOError:
                # Handle cases where file might be inaccessible or not found
                pass
    
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def remove_duplicate_files(duplicates_map, dry_run=True):
    """
    Removes duplicate files, keeping the first encountered instance.
    Returns a list of files that would be/were removed.
    """
    removed_files = []
    for file_hash, filepaths in duplicates_map.items():
        # Keep the first file, remove the rest
        for filepath_to_remove in filepaths[1:]:
            if not dry_run:
                os.remove(filepath_to_remove)
            removed_files.append(filepath_to_remove)
    return removed_files

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Data Dustbin Duster: Find and remove duplicate files."
    )
    parser.add_argument("directory", help="The directory to scan for duplicate files.")
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete duplicate files, keeping only one instance. Use with caution!"
    )
    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicates = find_duplicate_files(args.directory)

    if not duplicates:
        print("No duplicate files found. Your data dustbin is sparkling clean!")
        return

    print("\n--- Duplicate Files Found ---")
    total_duplicates_to_remove = 0
    for file_hash, filepaths in duplicates.items():
        print(f"Hash: {file_hash}")
        print(f"  Keeping: {filepaths[0]}")
        for i, filepath in enumerate(filepaths[1:]):
            print(f"  Duplicate {i+1}: {filepath}")
            total_duplicates_to_remove += 1
        print("-" * 20)

    print(f"\nTotal unique files with duplicates: {len(duplicates)}")
    print(f"Total duplicate files that can be removed: {total_duplicates_to_remove}")

    if args.delete:
        print("\n--- Deleting Duplicate Files ---")
        removed = remove_duplicate_files(duplicates, dry_run=False)
        print(f"Successfully removed {len(removed)} duplicate files.")
        for f in removed:
            print(f"  Removed: {f}")
    else:
        print("\nTo remove these duplicates, run the command again with the '--delete' flag.")

if __name__ == "__main__":
    main()
