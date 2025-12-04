import os
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo='md5', block_size=65536):
    """Calculates the hash of a file."""
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None

    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None

def find_duplicate_files(paths, hash_algo='md5'):
    """
    Finds duplicate files within the given list of paths.
    Returns a dictionary where keys are file hashes and values are lists of file paths.
    """
    files_by_size = defaultdict(list)
    for path in paths:
        if os.path.isfile(path):
            try:
                size = os.path.getsize(path)
                files_by_size[size].append(path)
            except OSError:
                # Ignore files we can't access
                continue
        elif os.path.isdir(path):
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    try:
                        size = os.path.getsize(filepath)
                        files_by_size[size].append(filepath)
                    except OSError:
                        # Ignore files we can't access
                        continue

    duplicate_hashes = defaultdict(list)
    for size, file_list in files_by_size.items():
        if size == 0: # Handle empty files separately, they all have the same hash
            if len(file_list) > 1:
                # All zero-byte files are duplicates of each other
                # The hash of an empty string is consistent across algorithms
                empty_hash = hashlib.new(hash_algo, b'').hexdigest()
                duplicate_hashes[empty_hash].extend(file_list)
            continue

        if len(file_list) > 1: # Only check for duplicates if there's more than one file of this size
            hashes = {}
            for filepath in file_list:
                file_hash = calculate_file_hash(filepath, hash_algo)
                if file_hash:
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(filepath)
            
            for file_hash, paths_with_same_hash in hashes.items():
                if len(paths_with_same_hash) > 1:
                    duplicate_hashes[file_hash].extend(paths_with_same_hash)
    
    # Filter out entries where there are no actual duplicates (e.g., if a hash was calculated but only one file had it)
    return {h: p for h, p in duplicate_hashes.items() if len(p) > 1}

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Nightly Data-Dust Sweeper: Identifies duplicate files in specified paths."
    )
    parser.add_argument(
        'paths',
        metavar='PATH',
        type=str,
        nargs='+',
        help='One or more file or directory paths to scan for duplicates.'
    )
    parser.add_argument(
        '--hash-algo',
        type=str,
        default='md5',
        choices=['md5', 'sha1', 'sha256'],
        help='Hashing algorithm to use (default: md5).'
    )

    args = parser.parse_args()

    print(f"Scanning for duplicate files in: {', '.join(args.paths)}")
    print(f"Using hashing algorithm: {args.hash_algo.upper()}")
    print("-" * 40)

    duplicates = find_duplicate_files(args.paths, args.hash_algo)

    if not duplicates:
        print("No data-dust found! All files are unique.")
        return

    print("\n--- Data-Dust Report (Duplicate Files) ---")
    duplicate_count = 0
    for file_hash, filepaths in duplicates.items():
        print(f"\nHash: {file_hash}")
        for filepath in filepaths:
            print(f"  - {filepath}")
            duplicate_count += 1
    
    print(f"\nTotal unique duplicate sets found: {len(duplicates)}")
    print(f"Total duplicate files identified: {duplicate_count}")
    print("-" * 40)

if __name__ == '__main__':
    main()
