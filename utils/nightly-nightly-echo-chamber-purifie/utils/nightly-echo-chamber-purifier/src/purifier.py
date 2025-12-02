import os
import hashlib
import argparse
from collections import defaultdict
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files

def find_duplicate_files(directory):
    """Finds duplicate files in a directory based on content hash.

    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath) and not os.path.islink(filepath):
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hashes[file_hash].append(filepath)
    return hashes

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for duplicate files based on content hash and optionally delete them."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to start scanning for duplicate files."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, all but one instance of each set of duplicate files will be deleted. Use with caution!"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If provided, only report what would be deleted without making any changes. Default if --delete is not specified."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        sys.exit(1)

    print(f"Scanning '{args.directory}' for duplicate files...")
    all_hashes = find_duplicate_files(args.directory)

    duplicates_found = False
    for file_hash, filepaths in all_hashes.items():
        if len(filepaths) > 1:
            duplicates_found = True
            print(f"\n--- Duplicates for hash {file_hash} ---")
            # Keep the first file as the 'original'
            print(f"  Original: {filepaths[0]}")
            for i, duplicate_path in enumerate(filepaths[1:]):
                print(f"  Duplicate {i+1}: {duplicate_path}")
                if args.delete and not args.dry_run:
                    try:
                        os.remove(duplicate_path)
                        print(f"    -> Deleted: {duplicate_path}")
                    except OSError as e:
                        print(f"    -> Error deleting {duplicate_path}: {e}")
                else:
                    # This branch covers: --dry-run is true, or --delete is false
                    print(f"    -> (Dry Run) Would delete: {duplicate_path}")

    if not duplicates_found:
        print("\nNo duplicate files found.")
    elif not args.delete or args.dry_run:
        print("\nOperation completed in dry-run mode. No files were deleted.")
    else:
        print("\nDuplicate files deleted successfully.")

if __name__ == "__main__":
    main()
