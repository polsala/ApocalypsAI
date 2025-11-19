import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.md5, block_size=65536):
    """
    Calculates the hash of a file's content.
    Uses MD5 by default for speed, but can be configured.
    """
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Warning: Could not read file {filepath} - {e}")
        return None

def find_duplicate_files(directory, verbose=False):
    """
    Scans the given directory for duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file associated (i.e., duplicates).
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Error: Directory not found: {directory}")

    file_hashes = defaultdict(list)
    total_files = 0
    scanned_files = 0

    if verbose:
        print(f"Scanning '{directory}' for data dust...")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            total_files += 1
            if verbose and total_files % 100 == 0:
                print(f"  Processed {total_files} files so far...", end='\r')

            file_hash = calculate_file_hash(filepath)
            if file_hash:
                file_hashes[file_hash].append(filepath)
                scanned_files += 1
    
    if verbose:
        print(f"  Processed {total_files} files. Hashed {scanned_files} files.")

    duplicate_groups = {
        file_hash: paths for file_hash, paths in file_hashes.items() if len(paths) > 1
    }
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Dust Defragmenter: Find duplicate files in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for duplicate files."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed information during the scan."
    )

    args = parser.parse_args()

    try:
        duplicate_groups = find_duplicate_files(args.path, args.verbose)

        if not duplicate_groups:
            print(f"No data dust (duplicate files) found in '{args.path}'. Your storage is pristine!")
            return

        print(f"\nFound {len(duplicate_groups)} groups of duplicate files (data dust):")
        for i, (file_hash, paths) in enumerate(duplicate_groups.items()):
            print(f"\n--- Group {i + 1} (Hash: {file_hash[:7]}...) ---")
            for path in paths:
                print(f"  - {path}")
        print("\nScan complete. May your storage be ever clean!")

    except ValueError as e:
        print(e)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
