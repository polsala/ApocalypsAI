import os
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo='md5', block_size=65536):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None # Or raise an error, depending on desired behavior
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def find_duplicate_files(directory, hash_algo='md5'):
    """
    Finds duplicate files in the given directory and its subdirectories.
    Returns a dictionary where keys are file hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated.
    """
    files_by_hash = defaultdict(list)
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath, hash_algo)
            if file_hash:
                files_by_hash[file_hash].append(filepath)

    duplicates = {
        h: paths for h, paths in files_by_hash.items() if len(paths) > 1
    }
    return duplicates

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Resonator: Finds duplicate files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
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
    duplicates = find_duplicate_files(args.directory, args.hash_algo)

    if not duplicates:
        print("\nNo echoes detected! All files are unique in the specified chamber.")
    else:
        print("\nEchoes detected! The following files are duplicates:")
        for file_hash, filepaths in duplicates.items():
            print(f"\nHash: {file_hash}")
            for filepath in filepaths:
                print(f"  - {filepath}")
        print(f"\nTotal unique duplicate sets found: {len(duplicates)}")

if __name__ == "__main__":
    main()
