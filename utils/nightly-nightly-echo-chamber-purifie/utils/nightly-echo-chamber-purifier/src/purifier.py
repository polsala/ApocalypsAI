import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo='md5', block_size=65536):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algo)
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_duplicates(directory, hash_algo='md5'):
    """
    Finds duplicate files in a given directory based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = calculate_file_hash(filepath, hash_algo)
                hashes[file_hash].append(filepath)
            except IOError as e:
                print(f"Warning: Could not read file {filepath}: {e}")
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")
    
    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Finds duplicate files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for duplicate files."
    )
    parser.add_argument(
        "--hash-algo",
        type=str,
        default="md5",
        choices=["md5", "sha1", "sha256"],
        help="Hashing algorithm to use (default: md5)."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        exit(1)

    print(f"Scanning '{args.directory}' for duplicate files using {args.hash_algo.upper()} hashing...")
    duplicate_groups = find_duplicates(args.directory, args.hash_algo)

    if not duplicate_groups:
        print("\nNo duplicate files found. Your digital echo chamber is pristine!")
        exit(0)

    print(f"\nFound {len(duplicate_groups)} groups of duplicate files:")
    for i, (file_hash, paths) in enumerate(duplicate_groups.items()):
        print(f"\n--- Duplicate Group {i+1} (Hash: {file_hash}) ---")
        for path in sorted(paths): # Sort for deterministic output
            print(f"  - {path}")
    
    print("\nPurification complete. Consider removing redundant echoes.")
    exit(0)

if __name__ == "__main__":
    main()
